
import random

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

for i in range(1,100):
    a=i



@app.route("/convertir", methods=["POST"])
def convertir():
    data = request.get_json()
    hora = data.get("hora")  # La hora actual enviada desde JS
    # Aquí es donde tú harás la lógica de conversión en diferentes bases
    return jsonify({
        "hora": hora,
        "binario": a,
        "octal": None,
        "hexadecimal": None
    })

if __name__ == "__main__":
    app.run(debug=True)
