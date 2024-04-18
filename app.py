from flask import Flask, render_template, request, session, redirect, jsonify
from usuario import Usuario
from chat import Chat
from contatos import Contatos


app = Flask(__name__)
app.secret_key = "ben10"
usuario = Usuario()


@app.route("/", methods=["GET", "POST"])
def pag_cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        senha = request.form["senha"]
        
        usuario.cadastrar(nome, telefone, senha)
        return render_template("login.html")

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def pag_login():
    if request.method == "POST":
        telefone = request.form["telefone"]
        senha = request.form["senha"]

        usuario.logar(telefone, senha)
        
        if usuario.logado:
            session['usuario_logado'] = {"nome": usuario.nome, "telefone": usuario.telefone}
            return redirect("/chat")
        else:
            session.clear()
            return "Erro ao logar"
    else:
        return render_template("login.html")

@app.route("/chat")
def pag_chat():
    if "usuario_logado" in session:
        return render_template("chat.html")
    else:
        return redirect("/login") 

@app.route("/mostrar_usuarios")
def mostrar_user():
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)

    contatos = chat.retornar_contatos()

    return jsonify(contatos), 200

@app.route("/get/mensagens/<tel_destinatario>")
def get_mensagem(tel_destinatario):

    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario, telefone_usuario)
    destinatario = Contatos("", tel_destinatario)
    mensagens = chat.verificar_mensagem(0, destinatario)

    return jsonify(mensagens),200 

@app.route("/enviar_mensagem", methods = ["POST"])
def enviar_mensagem() :
    dados= request.get_json()
    
    mensagem = dados["mensagem"]
    destinatario = dados["destinatario"]

    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]

    enviar = Chat(nome_usuario, telefone_usuario)


    enviar.enviar_mensagem(mensagem, destinatario)

    if enviar.enviar_mensagem() == True:
        return jsonify ({'mensagem':'Cadastro OK'}),200
    else:
        return jsonify ({'mensagem':'ERRO'}),500
    

app.run(debug=True)
