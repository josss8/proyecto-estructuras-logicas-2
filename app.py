from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def ConversorBinarioHoras(decimal):
    bits = [0,0,0,0,0]  
    value = 2**4
    for i in range(len(bits)):
        if decimal >= value:
            bits[i] = 1
            decimal -= value
        value //= 2
    return ''.join(str(bit) for bit in bits)


def ConversorBinarioMinutosSegundos(decimal):
    bits = [0,0,0,0,0,0]  
    value = 2**5
    for i in range(len(bits)):
        if decimal >= value:
            bits[i] = 1
            decimal -= value
        value //= 2
    return ''.join(str(bit) for bit in bits)

def conversorHexa2(numero):
    hex_map = "0123456789ABCDEF"
    if numero == 0:
        return "00"
    resultado = ""
    while numero > 0:
        resto = numero % 16
        numero //= 16
        resultado = hex_map[resto] + resultado
    return resultado.zfill(2)  # siempre dos dígitos
def Bin_Dec(bits):
    value = 0
    potencia = len(bits) - 1
    for bit in bits:
        value += bit * (2 ** potencia)
        potencia -= 1
    return value


# --- Conversión binario a hexadecimal manual ---
def Binario_HexaHoras(bits_str):
    bits = [int(b) for b in bits_str]  # ejemplo: "10101" → [1,0,1,0,1]
    
    HexaPre = [0, 0]
    Hexa = ["0", "0"]
    
    cant1 = [0, 0, 0, bits[0]]
    cant2 = [bits[1], bits[2], bits[3], bits[4]]

    HexaPre[0] = Bin_Dec(cant1)
    HexaPre[1] = Bin_Dec(cant2)

    for i in range(2):
        if HexaPre[i] < 10:
            Hexa[i] = str(HexaPre[i])
        else:
            Hexa[i] = chr(55 + HexaPre[i])  # 10=A, 11=B

    return ''.join(Hexa)

def conversorOctal(numero):
    if numero == 0:
        return "00"
    resultado = ""
    while numero > 0:
        resto = numero % 8
        numero //= 8
        resultado = str(resto) + resultado
    return resultado.zfill(2)  
    


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convertir", methods=["POST"])
def convertir():
    data = request.get_json()
    hora_str = data.get("hora")  # formato "HH:MM:SS" viene en string
    if not hora_str:
        return jsonify({"error": "No se recibió la hora"}), 400

    try:
        partes = hora_str.split(":")
        horas = int(partes[0])
        minutos = int(partes[1])
        segundos = int(partes[2])
    except (ValueError, IndexError):
        return jsonify({"error": "Formato de hora inválido"}), 400

    # llamar funciones binario
    bin_horas = ConversorBinarioHoras(horas)
    bin_minutos = ConversorBinarioMinutosSegundos(minutos)
    bin_segundos = ConversorBinarioMinutosSegundos(segundos)


    #llamar funciones hexa
    hexa_horas = Binario_HexaHoras(bin_horas)
    hexa_minutos = Binario_HexaHoras(bin_minutos[:5])  # recorta a 5 bits
    hexa_segundos = Binario_HexaHoras(bin_segundos[:5])

    #llamar funciones octal
    octa_horas = conversorOctal(horas)
    octa_minutos = conversorOctal(minutos)
    octa_segundos = conversorOctal(segundos)


    

    return jsonify({
        "hora": hora_str,
        "binario": f"{bin_horas} : {bin_minutos} : {bin_segundos}",
        "octal": f"{octa_horas} : {octa_minutos} : {octa_segundos}",
        "hexadecimal": f"{hexa_horas} : {hexa_minutos} : {hexa_segundos}",
    })


if __name__ == "__main__":
    app.run(debug=True)
