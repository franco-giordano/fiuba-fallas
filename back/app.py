from experto import CoviDetector, SintomasPaciente, EstadoClinico, ParametrosPaciente, Hisopado
from flask import Flask, jsonify, request
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/")
def home():
    return 'intenta POST /analisis'


@app.route("/analisis", methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def analizar():
    """
    {
        estadoClinico: 'ESTABLE'
        sintomasPaciente: 2
        hisopado: 'NO_DISPONIBLE'
    }
    """
    content = request.json

    print(f"""
    Params
        {content}
    """)

    experto = CoviDetector()
    experto.reset()

    try:
        param = ParametrosPaciente(
            estado_clinico=EstadoClinico.from_name(content['estadoClinico']),
            sintomas=content['sintomasPaciente'],
            resultado_hisopado=Hisopado.from_name(content['hisopado'])
        )
    except (ValueError, KeyError) as e:
        return jsonify({'err': f'body invalido, {e}'})

    print("Parametros iniciales", param)
    experto.declare(param)
    experto.run()
    print("Sugerencias resultantes para cada uno:",
          experto.sugerencias_paciente,
          experto.sugerencias_contactos_estrechos)

    para_paciente = [x.value for x in experto.sugerencias_paciente]
    para_contactos = [x.value for x in experto.sugerencias_contactos_estrechos]

    return jsonify({
        'sugerencias_paciente': para_paciente,
        'sugerencias_contactos_estrechos': para_contactos
    })


if __name__ == "__main__":
    app.run()
