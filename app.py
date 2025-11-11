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
    return resultado.zfill(2) 

def Bin_Dec(bits):
    value = 0
    potencia = len(bits) - 1
    for bit in bits:
        value += bit * (2 ** potencia)
        potencia -= 1
    return value

def Binario_HexaHoras(bits_str):
    bits = [int(b) for b in bits_str] 
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
            Hexa[i] = chr(55 + HexaPre[i]) 
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

def _convertir_tiempo(horas, minutos, segundos):
    try:
        bin_horas = ConversorBinarioHoras(horas)
        bin_minutos = ConversorBinarioMinutosSegundos(minutos)
        bin_segundos = ConversorBinarioMinutosSegundos(segundos)
        hexa_horas = conversorHexa2(horas)
        hexa_minutos = conversorHexa2(minutos)
        hexa_segundos = conversorHexa2(segundos)
        octa_horas = conversorOctal(horas)
        octa_minutos = conversorOctal(minutos)
        octa_segundos = conversorOctal(segundos)
        
        return {
            "binario": f"{bin_horas} : {bin_minutos} : {bin_segundos}",
            "octal": f"{octa_horas} : {octa_minutos} : {octa_segundos}",
            "hexadecimal": f"{hexa_horas} : {hexa_minutos} : {hexa_segundos}",
        }
    except Exception as e:
        return {"error": f"Error de conversión: {str(e)}"}

# PARTE 2 ___________________________________________________________________-
BIT_WIDTH = 16

def decimal_a_binario(n, bits=BIT_WIDTH):
    bin_list = [0] * bits
    i = bits - 1
    while n > 0 and i >= 0:
        resto = n % 2
        bin_list[i] = resto
        n = n // 2
        i -= 1
    return bin_list

def complemento_a_uno(bin_list):
    c_uno = [0] * len(bin_list)
    for i in range(len(bin_list)):
        if bin_list[i] == 0:
            c_uno[i] = 1
        else:
            c_uno[i] = 0
    return c_uno

def suma_binaria(bin_a, bin_b):
    longitud = len(bin_a)
    resultado = [0] * longitud
    acarreo = 0
    i = longitud - 1
    while i >= 0:
        suma_bits = bin_a[i] + bin_b[i] + acarreo
        if suma_bits == 0:
            resultado[i] = 0
            acarreo = 0
        elif suma_bits == 1:
            resultado[i] = 1
            acarreo = 0
        elif suma_bits == 2:
            resultado[i] = 0
            acarreo = 1
        elif suma_bits == 3:
            resultado[i] = 1
            acarreo = 1
        i -= 1
    return resultado

def complemento_a_dos(bin_list):
    c_uno = complemento_a_uno(bin_list)
    uno_binario = [0] * len(bin_list)
    uno_binario[len(bin_list) - 1] = 1
    c_dos = suma_binaria(c_uno, uno_binario)
    return c_dos

def decimal_a_binario_ca2(n, bits=BIT_WIDTH):
    if n >= 0:
        return decimal_a_binario(n, bits)
    else:
        bin_abs = decimal_a_binario(abs(n), bits)
        return complemento_a_dos(bin_abs)

def binario_a_decimal_ca2(bin_list):
    bits = len(bin_list)
    if bin_list[0] == 1:
        bin_positivo = complemento_a_dos(bin_list)
        valor = 0
        potencia = 0
        i = bits - 1
        while i >= 0:
            valor += bin_positivo[i] * (2 ** potencia)
            potencia += 1
            i -= 1
        return -valor
    else:
        valor = 0
        potencia = 0
        i = bits - 1
        while i >= 0:
            valor += bin_list[i] * (2 ** potencia)
            potencia += 1
            i -= 1
        return valor
    





@app.route("/")
def home():
    return render_template("reloj.html")

@app.route("/operaciones")
def operaciones():
    return render_template("operaciones.html")

@app.route("/convertir", methods=["POST"])
def convertir():
    data = request.get_json()
    hora_str = data.get("hora") 
    if not hora_str:
        return jsonify({"error": "No se recibió la hora"}), 400
    try:
        partes = hora_str.split(":")
        horas = int(partes[0])
        minutos = int(partes[1])
        segundos = int(partes[2])
    except Exception:
        return jsonify({"error": "Formato de hora inválido"}), 400
    conversiones = _convertir_tiempo(horas, minutos, segundos)
    if "error" in conversiones:
         return jsonify(conversiones), 500
    conversiones["hora"] = hora_str
    return jsonify(conversiones)



# --- RUTA /CALCULAR (Lógica C a 2) ---
@app.route("/calcular", methods=["POST"])
def calcular():
    try:
        h_op_str = request.form.get('horas_op', '0')
        m_op_str = request.form.get('minutos_op', '0')
        hora_actual_str = request.form.get('hora_actual')
        operacion = request.form.get('operacion') 

        h_op = int(h_op_str) if h_op_str.strip().lstrip('-').isdigit() else 0
        m_op = int(m_op_str) if m_op_str.strip().lstrip('-').isdigit() else 0
        partes_actual = hora_actual_str.split(":")
        h_actual = int(partes_actual[0])
        m_actual = int(partes_actual[1])
        s_actual = int(partes_actual[2])
        minutos_actual_dec = (h_actual * 60) + m_actual
        minutos_op_dec = (h_op * 60) + m_op
        
        
        if operacion == 'restar':
            minutos_op_dec = -minutos_op_dec
        minutos_actual_bin = decimal_a_binario_ca2(minutos_actual_dec, BIT_WIDTH)
        minutos_op_bin = decimal_a_binario_ca2(minutos_op_dec, BIT_WIDTH)
        resultado_minutos_bin = suma_binaria(minutos_actual_bin, minutos_op_bin)
        resultado_minutos_dec = binario_a_decimal_ca2(resultado_minutos_bin)
       
       
        minutos_normalizados_dec = resultado_minutos_dec % 1440
        nuevas_horas_dec = minutos_normalizados_dec // 60
        nuevos_minutos_dec = minutos_normalizados_dec % 60
        nuevos_segundos_dec = s_actual

        nueva_hora_str = f"{nuevas_horas_dec:02}:{nuevos_minutos_dec:02}:{nuevos_segundos_dec:02}"
        

        conversiones = _convertir_tiempo(nuevas_horas_dec, nuevos_minutos_dec, nuevos_segundos_dec)
        if "error" in conversiones:
            return jsonify(conversiones), 500
        
        # Respuesta JSON 
        respuesta = {
            "hora_original": hora_actual_str,
            "hora_calculada": nueva_hora_str, 
            **conversiones 
        }
        return jsonify(respuesta)

    except Exception as e:
        print(f"Error en /calcular: {e}") 
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)





