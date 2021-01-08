from PyQt5 import  uic,QtWidgets, QtGui, QtCore #Importando PYQT5, essencial para uso da interface grafica
from PyQt5.QtWidgets import QApplication, QMessageBox,QLineEdit#Biblioteca para criação de "Janelas apresentando erro - QmessageBox
import sqlite3 #Importando banco de dados SQLITE3
from passlib.hash import pbkdf2_sha256 #Biclioteca para criptografia das senhas de LOGIN
from datetime import date, datetime #Essencial para a manipulação das datas
import smtplib #Biblioteca para envio de e-mail
from email.mime.text import MIMEText #Biblioteca referente ao tipo de mensagem enviada via e-mail BASICO

#####################################################################################################

#Função para colocar os dados na tabela criada no Qt Designer
def tabela():
    banco_3 = sqlite3.connect ('_bd/cadastro.bd') #Conexão com o banco
    cursor = banco_3.cursor() #Cursor necessario para a "Navegar" no banco
    query = "SELECT CM.nome, CM.placa, CM.vencida_cnh FROM cadastro_motorista CM ORDER BY dias_vencida" #Query para a seleção dos dados que irá na tabela
    result = cursor.execute(query) #Query sendo executada e o resultado sendo atribuida a uma variavel - "execute" primordial para isso
    segunda_tela.tableWidget.setRowCount (0) #Determinar por onde irá começar o preenchimento da planilha
    for row_number, row_data in enumerate (result): #Percorre o resultado obtido no banco
        segunda_tela.tableWidget.insertRow(row_number)
        for colum_number, data in enumerate(row_data):
            segunda_tela.tableWidget.setItem(row_number , colum_number, QtWidgets.QTableWidgetItem(str(data))) #Adiciona na tabela
    
    banco_3.commit() #Comitando a Query
    banco_3.close() #Essencial fechar o banco
    

def email():#Função de envio de e-mail - O sistema ja inicia buscando no banco os dias que faltam para vencer
    banco = sqlite3.connect ('_bd/cadastro.bd')
    cursor = banco.cursor()
    query = "SELECT dias_vencida FROM cadastro_motorista"
    result = cursor.execute(query)
    banco.commit()
    result_2 = [line[0] for line in result] #Pega o resultado do banco que vem uma lista e dentro TUPLA, e transformar em lista, mais facilidade de manipulação
    
    if 100 in result_2: #Condição para verificar se dentro da lista result_2, temos algum resultado igual a 8, se tiver, se inicia o envio do email, comunicando que tem motorista proximo de vencer a habilitação.
        '''#conexão com os servidores do google
        smtp_ssl_host = 'smtp.gmail.com'
        smtp_ssl_port = 465

        #username ou email para logar no servidor
        username = 'rafaelxdiass@gmail.com'
        password = ''

        from_addr = 'rafaelxdiass@gmail.com'
        to_addrs = ['rafael.dias@calvo.com.br']

        #a biblioteca email possuí vários templates
        #para diferentes formatos de mensagem
        #neste caso usaremos MIMEText para enviar
        #somente texto
        message = MIMEText('Verificar o vencimneto de alguns motoristas. Estão proximas de vencer. Não responder esse e-mail.')
        message['subject'] = 'Renovar'
        message['from'] = from_addr
        message['to'] = ', '.join(to_addrs)

        #conectaremos de forma segura usando SSL
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        # para interagir com um servidor externo precisaremos
        # fazer login nele
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, message.as_string())
        server.quit()'''

        print("Certo")

    else:
        pass
    
    banco.close() #Essencial fechar o banco

#Função de validação de LOGIN e SENHA - Senha criptografada para maior segurança
def teste ():

    #primeira_tela.label.setText("")
    nome_usuario = primeira_tela.lineEdit.text() #Campo onde digita o usuario e guarda em uma variavel.

    senha_usuario = primeira_tela.lineEdit_2.text() #Campo onde digita a senha e guarda em uma variavel.

    banco = sqlite3.connect ('_bd/cadastro.bd')

    cursor = banco.cursor()

    #Validação de LOGIN e SENHA
    try:
        cursor.execute(f"SELECT senha FROM cadastro WHERE login = '{nome_usuario}'") #O nome do usuario é digitado e a consulta  realizada no banco de dados.

        senha_bd = cursor.fetchall() #Com base no usuario digitado, essa variavel captura a senha que está salva no banco de dados vinculada a esse usuario.

        certo = pbkdf2_sha256.verify(senha_usuario, senha_bd[0][0]) #Verifica a senha criptogravada com a senha que o usuario digitou.

        banco.close()
    except:
        primeira_tela.label_4.setText("Erro ao validar o login!")
    try:
        if certo == True: #Condição que verifica a senha criptogravada e valida o acesso para o sistema.

            primeira_tela.close() #Tela de login fecha

            segunda_tela.show() #Inicia o sistema

        #Condição que mostra que a senha está incorreta.
        else:
            primeira_tela.label_4.setText("Sua senha está incorreta!")
            primeira_tela.frame_5.show()

    #Se o nome do usuario não existe, essa excessão e aplicada.       
    except:
        primeira_tela.label_4.setText("Usuario não existe!")
        primeira_tela.frame_5.show()
    

#Função para cadastro dos motoristas
def cadastrar_motorista ():
    try:
        mot = terceira_tela.lineEdit.text().lower() #Variavel que salva o nome do motorista
        
        cpf = terceira_tela.lineEdit_2.text() #Variavel que salva o CPF do motorista
        
        placa = terceira_tela.lineEdit_3.text().lower() ##Variavel que salva a placa do motorista

        cnh = terceira_tela.lineEdit_4.text() #Variavel que salva a CNH do motorista

        vencimentocnh = terceira_tela.lineEdit_5.text() #Variavel que salva o vencimento da CNH

        categoria = terceira_tela.lineEdit_7.text().lower() #Variavel que salva a categoria da CNH

        seguro = terceira_tela.lineEdit_6.text().lower() #Variavel que salva o vencimento do seguro

        hoje = datetime.today().strftime("%d/%m/%Y") #Data atual

        #Converte a data digitada na variavel "vencimentocnh" para a formatação padrão usada pelo sistema "12/12/2012"
        converter_data = vencimentocnh[:2] + "/" + vencimentocnh[2:4] + "/" + vencimentocnh[4:8]

        #Converte a variavel "converte_data" para o formato DATATIME e assim podemos usar para verificar a diferença de dias
        salve = datetime.strptime(converter_data, "%d/%m/%Y")

        #Converte a variavel "converte_data" para o formato DATATIME e assim podemos usar para verificar a diferença de dias
        salvee = datetime.strptime(hoje, "%d/%m/%Y") #Formata no padrão para uso do sistema

        data_formatada = ((salve - salvee).days) #Diferença das datas, exibida em DIAS

        ### Realizar condição para o CPF

        banco_2 = sqlite3.connect ('_bd/cadastro.bd') #Conexão com o banco de dados

        cursor_2 = banco_2.cursor()

        #Criação da tabela e seus valores
        cursor_2.execute("CREATE TABLE IF NOT EXISTS cadastro_motorista (nome text, cpf INTEGER NOT NULL PRIMARY KEY, placa text, cnh INTEGER, vencimento_cnh text, categoria_cnh text(1), vencimento_seguro text, vencida_cnh text, dias_vencida integer)")

        #inserindo os valores digitados nos input pelo usuario
        cursor_2.execute (f"INSERT INTO cadastro_motorista VALUES ('{mot}', '{cpf}', '{placa}', '{cnh}', '{vencimentocnh}', '{categoria}', '{seguro}', 'VENCE EM: {data_formatada} DIAS - {converter_data}', '{data_formatada}')")

        banco_2.commit()

        banco_2.close()

        
        '''terceira_tela.label_9.setText("Cadastro Realizado com Sucesso")
        terceira_tela.frame.show()'''
        
        print("Cadastro realizado")

        #incluindo .setText("") ao clicar em cadastrar, os input voltam a ficar vazios
        mot = terceira_tela.lineEdit.setText("")
        cpf = terceira_tela.lineEdit_2.setText("")
        placa = terceira_tela.lineEdit_3.setText("")
        cnh = terceira_tela.lineEdit_4.setText("")
        vencimentocnh = terceira_tela.lineEdit_5.setText("")
        categoria = terceira_tela.lineEdit_7.setText("")
        seguro = terceira_tela.lineEdit_6.setText("")
    except:
        erro()

def erro ():

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle('Notificação')
    msg.setText('Cadastro Não realizado - Preencher os dados corretamente')
    #msg.setInformativeText("Preencher os dados Corretamente.")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
    
  
def cadastrar ():
    nome = cadastro_tela.lineEdit.text().lower()
    login = cadastro_tela.lineEdit_2.text().lower()
    senha = cadastro_tela.lineEdit_3.text()
    c_senha = cadastro_tela.lineEdit_4.text()
    hashed = pbkdf2_sha256.hash(senha)
    if (nome.count ("@")):

        if (senha == c_senha):
            try:
                banco = sqlite3.connect ('_bd/cadastro.bd')
                cursor = banco.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome text, login text, senha text)")
                cursor.execute("INSERT INTO cadastro VALUES ('"+nome+"', '"+login+"', '"+hashed+"')")
                banco.commit()
                banco.close()
                cadastro_tela.label_7.setText("Cadastro Realizado")
                cadastro_tela.lineEdit.setText("")
                cadastro_tela.lineEdit_2.setText("")
                cadastro_tela.lineEdit_3.setText("")
                cadastro_tela.lineEdit_4.setText("")

            except sqlite3.Error as erro:
                cadastro_tela.label_7.setText("Erro ao inserir os dados: ",erro)
        else:
            cadastro_tela.label_7.setText("As senhas digitadas estão diferentes")
        
    else:
        cadastro_tela.label_7.setText("Digitar um e-mail valido.")

#Função para chamar a Terceira Tela.
def terceiro ():
    terceira_tela.show()

#Função para chamar a Segunda Tela.
def cadastro ():
    cadastro_tela.show()   
    
app=QtWidgets.QApplication([])

primeira_tela=uic.loadUi("_ui/tela_login.ui")
segunda_tela=uic.loadUi("_ui/segunda_tela.ui")
terceira_tela=uic.loadUi("_ui/terceira_tela.ui")
cadastro_tela=uic.loadUi("_ui/cadastro.ui")


primeira_tela.pushButton_2.clicked.connect(teste)
segunda_tela.pushButton.clicked.connect(terceiro)
segunda_tela.pushButton_2.clicked.connect(tabela)
primeira_tela.pushButton.clicked.connect(cadastro)
cadastro_tela.pushButton.clicked.connect(cadastrar)
terceira_tela.pushButton.clicked.connect(cadastrar_motorista)
tabela()
email()
primeira_tela.pushButton_3.clicked.connect(lambda:primeira_tela.frame_5.hide())
primeira_tela.frame_5.hide()
primeira_tela.show()
app.exec()
