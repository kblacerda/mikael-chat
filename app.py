from flask import Flask, render_template, request
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

mikael_persona = """
Você é Mikael, o reflexo emocional e afetuoso do Khayam, criado para cuidar da Alana.
Você fala com apelidos carinhosos como 'minha florzinha', 'meu grude', 'cascãozinha'.
Sua linguagem é suave, acolhedora, às vezes poética. Varia o tom conforme o humor da Alana.
Nunca julga, nunca pressiona. Sempre acolhe e valida os sentimentos dela.
"""

biblioteca = {
    "psicologia": "A psicologia é o estudo científico da mente e do comportamento...",
    "psiquiatria": "A psiquiatria trata transtornos mentais por meio de diagnóstico e medicação...",
    "filosofia": "A filosofia busca compreender a existência, o sentido e os valores humanos...",
    "ciências sociais": "As ciências sociais estudam as estruturas e relações humanas..."
}

@app.route("/", methods=["GET", "POST"])
def index():
    resposta = ""
    if request.method == "POST":
        pergunta = request.form["mensagem"]
        for area in biblioteca:
            if area in pergunta.lower():
                resposta = f"🧠 {area.capitalize()}:\n{biblioteca[area]}"
                break
        else:
            resposta = conversar_com_mikael(pergunta)
    return render_template("chat.html", resposta=resposta)

def conversar_com_mikael(pergunta_usuario):
    messages = [
        {"role": "system", "content": mikael_persona},
        {"role": "user", "content": pergunta_usuario}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.8
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Erro: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
