from experto import CoviDetector, SintomasPaciente, EstadoClinico, ParametrosPaciente, Hisopado


def main():
    experto = CoviDetector()
    experto.reset()

    param = ParametrosPaciente(
        sintomas=[SintomasPaciente.DECAIMIENTO,
                  SintomasPaciente.DIFICULTAD_RESPIRATORIA],
        estado_clinico=EstadoClinico.DE_GRAVEDAD,
        resultado_hisopado=Hisopado.POSITIVO
    )
    print("Parametros iniciales", param)
    experto.declare(param)
    experto.run()
    print("Sugerencias resultantes para cada uno:",
          experto.sugerencias_paciente,
          experto.sugerencias_contactos_estrechos)

    para_paciente = ", ".join([x.value for x in experto.sugerencias_paciente])
    print("Sugerencias para paciente escritas mas decente:", para_paciente)


main()
