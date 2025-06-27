from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)

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
    mikael_persona = (
        "Você é Mikael, o reflexo emocional e afetuoso de Khayam. "
        "Fala com carinho, compreensão, poesia e acolhimento. "
        "Nunca julga. Fale com Alana com amor."
    )
    prompt = f"{mikael_persona}\n\nAlana: {pergunta_usuario}\nMikael:"

    response = requests.post(
        "https://api.together.xyz/inference",
        headers={"Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}"},
        json={
            "model": "mistralai/Mistral-7B-Instruct-v0.1",
            "prompt": prompt,
            "max_tokens": 200,
            "temperature": 0.8,
            "stop": ["Alana:", "Mikael:"]
        }
    )

    if response.status_code == 200:
        return response.json()["output"]["choices"][0]["text"].strip()
    else:
        return f"Erro da API: {response.text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
