from flask import Flask, jsonify, send_from_directory, render_template
import pandas as pd
import os

app = Flask(__name__, static_folder='boletins', template_folder='templates')

# Carrega a planilha com os dados
df = pd.read_excel("planilha_base.xlsx", dtype={'CPF': str})
df = df[['CPF', 'Cursista']]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/buscar/<cpf>")
def buscar_boletim(cpf):
    resultado = df[df["CPF"] == cpf]
    if resultado.empty:
        return jsonify({"erro": "CPF não encontrado"}), 404
    nome = resultado.iloc[0]["Cursista"]
    link = f"/boletins/{cpf}.pdf"
    return jsonify({"cpf": cpf, "nome": nome, "link": link})

@app.route("/boletins/<path:filename>")
def boletins(filename):
    return send_from_directory("boletins", filename)

# Serve arquivos estáticos da pasta 'templates' (onde está o index.html e logo.png)
@app.route('/templates/<path:filename>')
def templates_static(filename):
    return send_from_directory('templates', filename)

# ✅ Este bloco abaixo é ESSENCIAL para rodar no Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
