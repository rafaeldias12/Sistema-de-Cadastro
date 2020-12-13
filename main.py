from PyQt5 import  uic,QtWidgets
import sqlite3

def teste ():
    primeira_tela.label.setText("")
    nome_usuario = primeira_tela.lineEdit.text()
    senha_usuario = primeira_tela.lineEdit_2.text()
    banco = sqlite3.connect ('_bd/cadastro.bd')
    cursor = banco.cursor()
    try:
        cursor.execute(f"SELECT senha FROM cadastro WHERE login = '{nome_usuario}'")
        senha_bd = cursor.fetchall()
        banco.close()
    except:
        primeira_tela.label_4.setText("Erro ao validar o login!")
    try:
        if senha_usuario == senha_bd[0][0]:
            primeira_tela.close()
            segunda_tela.show()
        else:
            primeira_tela.label_4.setText("Sua senha está incorreta!")
            primeira_tela.frame_5.show()
    except:
        primeira_tela.label_4.setText("Usuario não existe!")
        primeira_tela.frame_5.show()

def terceiro ():
    terceira_tela.show()

def cadastro ():
    cadastro_tela.show()

def cadastrar ():
    nome = cadastro_tela.lineEdit.text()
    login = cadastro_tela.lineEdit_2.text()
    senha = cadastro_tela.lineEdit_3.text()
    c_senha = cadastro_tela.lineEdit_4.text()

    if (senha == c_senha):
        try:
            banco = sqlite3.connect ('_bd/cadastro.bd')
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome text, login text, senha text)")
            cursor.execute("INSERT INTO cadastro VALUES ('"+nome+"', '"+login+"', '"+senha+"')")
            banco.commit()
            banco.close()
            cadastro_tela.label_7.setText("Cadastro Realizado")

        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ",erro)
    else:
        cadastro_tela.label_7.setText("As senhas digitadas estão diferentes")

app=QtWidgets.QApplication([])

primeira_tela=uic.loadUi("_ui/tela_login.ui")
segunda_tela=uic.loadUi("_ui/segunda_tela.ui")
terceira_tela=uic.loadUi("_ui/terceira_tela.ui")
cadastro_tela=uic.loadUi("_ui/cadastro.ui")

primeira_tela.pushButton_2.clicked.connect(teste)
segunda_tela.pushButton.clicked.connect(terceiro)
primeira_tela.pushButton.clicked.connect(cadastro)
cadastro_tela.pushButton.clicked.connect(cadastrar)

primeira_tela.pushButton_3.clicked.connect(lambda:primeira_tela.frame_5.hide())
primeira_tela.frame_5.hide()

primeira_tela.show()
app.exec()