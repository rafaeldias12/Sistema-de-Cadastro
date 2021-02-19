from PyQt5 import  uic,QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox,QLineEdit
import sqlite3 
from sqlite3 import Error
from passlib.hash import pbkdf2_sha256
from datetime import date, datetime
import smtplib
from email.mime.text import MIMEText
#####################################################################################################

def cadastrarUsuario():
    email = cadastroUsuario.lineEdit.text().lower()
    login = cadastroUsuario.lineEdit_2.text().lower()
    senha = cadastroUsuario.lineEdit_3.text()
    c_senha = cadastroUsuario.lineEdit_4.text()
    hashed = pbkdf2_sha256.hash(senha)

    if (email.count ("@")):
        if (senha == c_senha):
            try:
                banco = sqlite3.connect ('_db/cadastro.db')
                cursor = banco.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (Email text, Login Text UNIQUE, Senha text)")
                cursor.execute("INSERT INTO cadastro VALUES ('"+email+"', '"+login+"', '"+hashed+"')")
                banco.commit()
                banco.close()

                cadastroUsuario.label_7.setText("Cadastro Realizado")
                cadastroUsuario.lineEdit.setText("")
                cadastroUsuario.lineEdit_2.setText("")
                cadastroUsuario.lineEdit_3.setText("")
                cadastroUsuario.lineEdit_4.setText("")

            except sqlite3.IntegrityError:
                cadastroUsuario.label_7.setText("Login já cadastrado, por favor, tente outro.")
        else:
            cadastroUsuario.label_7.setText("As senhas digitadas estão diferentes")
    else:
        cadastroUsuario.label_7.setText("Digitar um e-mail valido.")

def login():
    nome_usuario = telaLogin.lineEdit.text() 
    senha_usuario = telaLogin.lineEdit_2.text()
    banco = sqlite3.connect ('_db/cadastro.db')
    cursor = banco.cursor()

    try:
        cursor.execute(f"SELECT senha FROM cadastro WHERE login = '{nome_usuario}'")
        senha_db = cursor.fetchall()
        hashed_verificacao = pbkdf2_sha256.verify(senha_usuario, senha_db[0][0])
        banco.close()
    except:
        telaLogin.label_4.setText("Erro ao validar o login!")
    try:
        if hashed_verificacao == True:
            telaLogin.close() 
            telaPrincipal.show()
            tabela()
            telaPrincipal.label_3.setText(f"Usuario Logado: {nome_usuario}")
            diasAtualizadosSeguro()
            diasAtualizadosCnh()
            envioEmail()
        else:
            telaLogin.label_4.setText("Sua senha está incorreta!")
            telaLogin.frame_5.show()     
    except:
        telaLogin.label_4.setText("Usuario não existe!")
        telaLogin.frame_5.show()

def diasAtualizadosSeguro():
    banco = sqlite3.connect ('_db/cadastro.db')
    cursor = banco.cursor() 
    query = "SELECT cadastro_motorista.cpf, cadastro_motorista.vencimento_seguro FROM cadastro_motorista "
    result = cursor.execute(query)
    dadosbanco = cursor.fetchall()

    dataHoje = datetime.today().strftime("%d/%m/%Y")
    hojeConvertido = datetime.strptime(dataHoje, "%d/%m/%Y")
    for l in dadosbanco:
        cpf = l[0]
        data = datetime.strptime(str(l[1]), "%d/%m/%Y")
        diasAtualizadosSeguro = ((data - hojeConvertido).days)
        
        cursor .execute (f"update cadastro_motorista set seguro_dias_vencido='{diasAtualizadosSeguro}'where cpf= '{cpf}'")

        banco.commit()
    banco.close()

def diasAtualizadosCnh():
    banco = sqlite3.connect ('_db/cadastro.db')
    cursor = banco.cursor() 
    query = "SELECT cadastro_motorista.cpf, cadastro_motorista.vencimento_cnh FROM cadastro_motorista "
    result = cursor.execute(query)
    dadosbanco = cursor.fetchall()

    dataHoje = datetime.today().strftime("%d/%m/%Y")
    hojeConvertido = datetime.strptime(dataHoje, "%d/%m/%Y")
    for l in dadosbanco:
        cpf = l[0]
        data = datetime.strptime(str(l[1]), "%d/%m/%Y")
        diasAtualizadosCnh = ((data - hojeConvertido).days)
        
        cursor .execute (f"update cadastro_motorista set dias_vencida='{diasAtualizadosCnh}'where cpf= '{cpf}'")

        banco.commit()
    banco.close()

def tabela():
    diasAtualizadosSeguro()
    diasAtualizadosCnh()
    banco = sqlite3.connect ('_db/cadastro.db')
    cursor = banco.cursor() 
    query = "SELECT cadastro_motorista.nome, cadastro_motorista.placa, cadastro_motorista.dias_vencida, cadastro_motorista.vencimento_cnh, cadastro_motorista.seguro_dias_vencido, cadastro_motorista.vencimento_seguro FROM cadastro_motorista  ORDER BY cadastro_motorista.seguro_dias_vencido" 
    result = cursor.execute(query) 
    telaPrincipal.tableWidget.setRowCount (0) 
    
    for row_number, row_data in enumerate (result): 
        telaPrincipal.tableWidget.insertRow(row_number)
        for colum_number, data in enumerate(row_data):
            telaPrincipal.tableWidget.setItem(row_number , colum_number, QtWidgets.QTableWidgetItem(str(data)))

    banco.commit()
    banco.close()

def cadastrarMotorista():
    try:
        nomeMotorista = cadastroMotorista.lineEdit.text().upper()
        cpfMotorista = cadastroMotorista.lineEdit_2.text()
        placaMotorista = cadastroMotorista.lineEdit_3.text().upper()
        cnhMotorista = cadastroMotorista.lineEdit_4.text()
        vencimentoCnh = cadastroMotorista.lineEdit_5.text()
        categoriaCnh = cadastroMotorista.lineEdit_7.text().upper()
        vencimentoSeguro = cadastroMotorista.lineEdit_6.text()
        ############################ - CONVERTER TEXTO PARA DATA - ##################################
        dataHoje = datetime.today().strftime("%d/%m/%Y")
        converterData = vencimentoCnh[:2] + "/" + vencimentoCnh[2:4] + "/" + vencimentoCnh[4:8]
        converterSeguro = vencimentoSeguro[:2] + "/" + vencimentoSeguro[2:4] + "/" + vencimentoSeguro[4:8]
        dataConvertida = datetime.strptime(converterData, "%d/%m/%Y")
        seguroConvertido = datetime.strptime(converterSeguro, "%d/%m/%Y")
        hojeConvertido = datetime.strptime(dataHoje, "%d/%m/%Y")
        dataFormatada = ((dataConvertida - hojeConvertido).days)
        seguroFormatado = ((seguroConvertido - hojeConvertido).days)
        #############################################################################################
        banco = sqlite3.connect ('_db/cadastro.db')
        cursor = banco.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS cadastro_motorista (nome text, cpf INTEGER NOT NULL PRIMARY KEY, placa text, cnh INTEGER, vencimento_cnh text, categoria_cnh text(2), vencimento_seguro text, dias_vencida integer, seguro_dias_vencido integer)")
        cursor.execute (f"INSERT INTO cadastro_motorista VALUES ('{nomeMotorista}', '{cpfMotorista}', '{placaMotorista}', '{cnhMotorista}', '{converterData}', '{categoriaCnh}', '{converterSeguro}', '{dataFormatada}', '{seguroFormatado}')")

        banco.commit()
        banco.close()
    
        cadastroMotorista.lineEdit.setText("")
        cadastroMotorista.lineEdit_2.setText("")
        cadastroMotorista.lineEdit_3.setText("")
        cadastroMotorista.lineEdit_4.setText("")
        cadastroMotorista.lineEdit_5.setText("")
        cadastroMotorista.lineEdit_7.setText("")
        cadastroMotorista.lineEdit_6.setText("")

    except sqlite3.IntegrityError:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Notificação')
        msg.setText('CPF já cadastrado')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Notificação')
        msg.setText('Cadastro Não realizado - Preencher os dados corretamente')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

def listaComboBox():
    atualizacaoMotorista.show()
    banco = sqlite3.connect ('_db/cadastro.db')
    cursor = banco.cursor()
    cursor.execute ("SELECT nome FROM cadastro_motorista ORDER BY nome")
    data = cursor.fetchall()
    atualizacaoMotorista.comboBox.clear()

    for category in data:
        atualizacaoMotorista.comboBox.addItem(category[0].upper())

    banco.commit()
    banco.close()
    
def listarDadosMotorista():
    try:
        banco = sqlite3.connect ('_db/cadastro.db')
        cursor = banco.cursor()
        nome = atualizacaoMotorista.comboBox.currentText().upper()
        cursor.execute(f"select nome, cpf, placa, cnh, vencimento_cnh, categoria_cnh, vencimento_seguro from cadastro_motorista WHERE nome = '{nome}'")
        resultado = cursor.fetchall()
        banco.commit()
        atualizacaoMotorista.lineEdit.setText(str(resultado[0][0].upper()))
        atualizacaoMotorista.lineEdit_2.setText(str(resultado[0][1]))
        atualizacaoMotorista.lineEdit_3.setText(str(resultado[0][2].upper()))
        atualizacaoMotorista.lineEdit_4.setText(str(resultado[0][3]))
        atualizacaoMotorista.lineEdit_5.setText(str(resultado[0][4]))
        atualizacaoMotorista.lineEdit_7.setText(str(resultado[0][5].upper()))
        atualizacaoMotorista.lineEdit_6.setText(str(resultado[0][6]))

        banco.commit()
        banco.close()

    except IndexError:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Aviso')
        msg.setText('Motorista não consta no banco de dados!')
        msg.setInformativeText('Motorista excluido recentemente.')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

def atualizarCadastroMotorista():
    try:
        dataHoje = datetime.today().strftime("%d/%m/%Y")
        banco = sqlite3.connect ('_db/cadastro.db')
        cursor = banco.cursor()
        
        nomeMotorista = atualizacaoMotorista.lineEdit.text().upper()
        cpfMotorista = atualizacaoMotorista.lineEdit_2.text()
        placaMotorista = atualizacaoMotorista.lineEdit_3.text().upper()
        cnhMotorista = atualizacaoMotorista.lineEdit_4.text()
        vencimentoCnh = atualizacaoMotorista.lineEdit_5.text()
        categoriaCnh = atualizacaoMotorista.lineEdit_7.text().upper()
        vencimentoSeguro = atualizacaoMotorista.lineEdit_6.text()

        if  (vencimentoCnh.count  ("/")) and (vencimentoSeguro.count ('/')):
            dataConvertida = datetime.strptime(vencimentoCnh, "%d/%m/%Y")
            hojeConvertido = datetime.strptime(dataHoje, "%d/%m/%Y")
            dataFormatada = ((dataConvertida - hojeConvertido).days) 
            seguroConvertido = datetime.strptime(vencimentoSeguro, "%d/%m/%Y")
            seguroFormatado = ((seguroConvertido - hojeConvertido).days)
            
            cursor .execute (f"update cadastro_motorista set nome='{nomeMotorista}', placa='{placaMotorista}', cnh='{cnhMotorista}', vencimento_cnh='{vencimentoCnh}', categoria_cnh='{categoriaCnh}', vencimento_seguro='{vencimentoSeguro}', dias_vencida='{dataFormatada}', seguro_dias_vencido='{seguroFormatado}'  where cpf= '{cpfMotorista}'")
            

        elif vencimentoSeguro not in ("/") and (vencimentoCnh.count ("/")):

            converterSeguro = vencimentoSeguro[:2] + "/" + vencimentoSeguro[2:4] + "/" + vencimentoSeguro[4:8]
            seguroConvertido = datetime.strptime(converterSeguro, "%d/%m/%Y")
            hojeConvertido = datetime.strptime(dataHoje, "%d/%m/%Y")
            seguroFormatado = ((seguroConvertido - hojeConvertido).days)

            cursor .execute (f"update cadastro_motorista set nome='{nomeMotorista}', placa='{placaMotorista}', cnh='{cnhMotorista}', categoria_cnh='{categoriaCnh}', vencimento_seguro='{converterSeguro}', seguro_dias_vencido='{seguroFormatado}'  where cpf= '{cpfMotorista}'")
            
        

        elif vencimentoCnh not in ("/") and (vencimentoSeguro.count ("/")):
            converterData = vencimentoCnh[:2] + "/" + vencimentoCnh[2:4] + "/" + vencimentoCnh[4:8]
            dataConvertida = datetime.strptime(converterData, "%d/%m/%Y")
            hojeConvertido = datetime.strptime(dataHoje, "%d/%m/%Y")
            dataFormatada = ((dataConvertida - hojeConvertido).days)

            cursor .execute (f"update cadastro_motorista set nome='{nomeMotorista}', placa='{placaMotorista}', cnh='{cnhMotorista}', vencimento_cnh='{converterData}', categoria_cnh='{categoriaCnh}', dias_vencida='{dataFormatada}' where cpf= '{cpfMotorista}'")
            

        else:
            ############################ - CONVERTER TEXTO PARA DATA - ################################# 
            converterData = vencimentoCnh[:2] + "/" + vencimentoCnh[2:4] + "/" + vencimentoCnh[4:8]
            converterSeguro = vencimentoSeguro[:2] + "/" + vencimentoSeguro[2:4] + "/" + vencimentoSeguro[4:8]
            dataConvertida = datetime.strptime(converterData, "%d/%m/%Y")
            seguroConvertido = datetime.strptime(converterSeguro, "%d/%m/%Y")
            hojeConvertido = datetime.strptime(dataHoje, "%d/%m/%Y")
            dataFormatada = ((dataConvertida - hojeConvertido).days) 
            seguroFormatado = ((seguroConvertido - hojeConvertido).days)
            #############################################################################################

            cursor .execute (f"update cadastro_motorista set nome='{nomeMotorista}', placa='{placaMotorista}', cnh='{cnhMotorista}', vencimento_cnh='{converterData}', categoria_cnh='{categoriaCnh}', vencimento_seguro='{converterSeguro}', dias_vencida='{dataFormatada}', seguro_dias_vencido='{seguroFormatado}'  where cpf= '{cpfMotorista}'")

        banco.commit()
        banco.close()

    except:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle('Erro')
        msg.setText('Atualização não realizada')
        msg.setInformativeText('Preencher os dados com o formato correto!')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    atualizacaoMotorista.lineEdit.setText("")
    atualizacaoMotorista.lineEdit_2.setText("")
    atualizacaoMotorista.lineEdit_3.setText("")
    atualizacaoMotorista.lineEdit_4.setText("")
    atualizacaoMotorista.lineEdit_5.setText("")
    atualizacaoMotorista.lineEdit_7.setText("")
    atualizacaoMotorista.lineEdit_6.setText("")

def excluirMotorista():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle('Excluir Definitivamente')
    msg.setText('Deseja REALMENTE excluir os dados desse Motorista?')
    msg.setInformativeText('Após confirmar, não será possivel recuperar os dados!')
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    qmessageBoxBotao = msg.exec_()

    if qmessageBoxBotao == QMessageBox.Ok:
        banco = sqlite3.connect ('_db/cadastro.db')
        cursor = banco.cursor()
        nome = atualizacaoMotorista.comboBox.currentText().upper()
        cursor.execute(f"DELETE FROM cadastro_motorista WHERE nome = '{nome}'")
        banco.commit()
        banco.close()
        
    elif qmessageBoxBotao == QMessageBox.Cancel:
        pass

def envioEmail():
    email_usuario = telaPrincipal.label_3.text()
    banco = sqlite3.connect ('_db/cadastro.db')
    cursor = banco.cursor()
    query_cnh_vencida = "SELECT dias_vencida FROM cadastro_motorista"
    query_seguro_vencido = "SELECT seguro_dias_vencido FROM cadastro_motorista"
    query_email = (f"SELECT Email FROM cadastro WHERE login = '{email_usuario[16:]}'")

    result = cursor.execute(query_cnh_vencida)
    cnh_vencida = cursor.fetchall()

    result2 = cursor.execute(query_seguro_vencido)
    seguro_vencido = cursor.fetchall()

    result3 = cursor.execute(query_email)
    email_cadastro = cursor.fetchall()

    banco.commit()

    lista_cnh_vencida = [line[0] for line in cnh_vencida]
    lista_seguro_vencido = [line2[0] for line2 in seguro_vencido]
    
    
    if 10 in lista_cnh_vencida or 20 in lista_cnh_vencida or 30 in lista_cnh_vencida:
        
        #conexão com os servidores do google
        smtp_ssl_host = 'smtp.gmail.com'
        smtp_ssl_port = 465

        #username ou email para logar no servidor
        username = ''
        password = ''

        from_addr = 'entregas.portaporta@gmail.com'
        to_addrs = [email_cadastro[0][0]]

        #a biblioteca email possuí vários templates
        #para diferentes formatos de mensagem
        #neste caso usaremos MIMEText para enviar
        #somente texto
        message = MIMEText('Consta CNH proxima de sua data de validade. Por gentileza, verificar qual motorista e realizar a atualização no sistema. \n \n \n \n ### - E-mail automático, não responder esse e-mail! - ###')
        message['subject'] = 'Verificar'
        message['from'] = from_addr
        message['to'] = ', '.join(to_addrs)

        #conectaremos de forma segura usando SSL
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        # para interagir com um servidor externo precisaremos
        # fazer login nele
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, message.as_string())
        server.quit()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Aviso')
        msg.setText('Email Enviado com Sucesso')
        msg.setInformativeText(f'Verificar a caixa de entrada/Spam - {email_cadastro[0][0]}')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    else:
        pass

    if 10 in lista_seguro_vencido or 20 in lista_seguro_vencido or 30 in lista_seguro_vencido: 
        #conexão com os servidores do google
        smtp_ssl_host = 'smtp.gmail.com'
        smtp_ssl_port = 465

        #username ou email para logar no servidor
        username = ''
        password = ''

        from_addr = 'entregas.portaporta@gmail.com'
        to_addrs = [email_cadastro[0][0]]

        #a biblioteca email possuí vários templates
        #para diferentes formatos de mensagem
        #neste caso usaremos MIMEText para enviar
        #somente texto
        message = MIMEText('Consta SEGURO proximo de sua data de validade. Por gentileza, verificar qual motorista e realizar a atualização no sistema. \n \n \n ### - E-mail automático, não responder esse e-mail! - ###')
        message['subject'] = 'Verificar'
        message['from'] = from_addr
        message['to'] = ', '.join(to_addrs)

        #conectaremos de forma segura usando SSL
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        # para interagir com um servidor externo precisaremos
        # fazer login nele
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, message.as_string())
        server.quit()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Aviso')
        msg.setText('Email Enviado com Sucesso')
        msg.setInformativeText(f'Verificar a caixa de entrada/Spam - {email_cadastro[0][0]}')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    else:
        pass
    banco.close()

app=QtWidgets.QApplication([])

telaLogin=uic.loadUi("_ui/telaLogin.ui")
telaPrincipal=uic.loadUi("_ui/telaPrincipal.ui")
cadastroMotorista=uic.loadUi("_ui/cadastroMotorista.ui")
cadastroUsuario=uic.loadUi("_ui/cadastroUsuario.ui")
atualizacaoMotorista=uic.loadUi("_ui/atualizacaoMotorista.ui")

telaLogin.pushButton_2.clicked.connect(login)
telaPrincipal.pushButton.clicked.connect(cadastroMotorista.show)
telaPrincipal.pushButton_2.clicked.connect(tabela)
telaLogin.pushButton.clicked.connect(cadastroUsuario.show)
cadastroUsuario.pushButton.clicked.connect(cadastrarUsuario)
cadastroMotorista.pushButton.clicked.connect(cadastrarMotorista)
telaPrincipal.pushButton_3.clicked.connect(listaComboBox)
atualizacaoMotorista.pushButton_3.clicked.connect(listarDadosMotorista)
atualizacaoMotorista.pushButton.clicked.connect(atualizarCadastroMotorista)
atualizacaoMotorista.pushButton_2.clicked.connect(excluirMotorista)



telaLogin.pushButton_3.clicked.connect(lambda:telaLogin.frame_5.hide())



telaLogin.frame_5.hide()

telaLogin.show()
app.exec()