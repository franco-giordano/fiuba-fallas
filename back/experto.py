from random import choice
from experta import *
from enum import Enum
from typing import List


class EstadoClinico(Enum):
    ESTABLE = 0
    DE_GRAVEDAD = 1


class SintomasPaciente(Enum):
    TOS = 0
    FIEBRE = 1
    MOCOS = 2
    DIFICULTAD_RESPIRATORIA = 3
    DOLOR_MUSCULAR = 4
    DECAIMIENTO = 5
    DIARREA = 6
    VOMITOS = 7


class Hisopado(Enum):
    NO_DISPONIBLE = 0
    POSITIVO = 1
    NEGATIVO = 2


class TratamientosSugeridos(Enum):
    HISOPAR = "Hisopar al paciente"
    INDICAR_AISLAMIENTO = "Indicar aislamiento"
    TRATAR_CON_ANTITERMICO = "Tratar con antitermico"  # (???) muy random
    LLAMAR_PERIODICAMENTE = "Llamar periodicamente, cada 10 dias"
    LIBERAR_AISLAMIENTO = "Liberar del aislamiento"
    INTERNAR = "Internar"
    MONITOREAR_EVOLUCION = "Monitorear evolucion"
    REALIZAR_ESTUDIOS = "Realizar estudios"


class ParametrosPaciente(Fact):
    sintomas = Field([SintomasPaciente], default=[])
    estado_clinico = Field(
        EstadoClinico, default=EstadoClinico.ESTABLE, mandatory=True)
    resultado_hisopado = Field(Hisopado, default=Hisopado.NO_DISPONIBLE)


def tiene_demasiados_sintomas(lista_sintomas: List[SintomasPaciente]) -> bool:
    return len(lista_sintomas) >= 2


class CoviDetector(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.sugerencias_paciente: List[TratamientosSugeridos] = []
        self.sugerencias_contactos_estrechos: List[TratamientosSugeridos] = []

    @Rule(
        ParametrosPaciente(sintomas=P(tiene_demasiados_sintomas),
                           resultado_hisopado=Hisopado.NO_DISPONIBLE)
    )
    def enfermo_sin_hisopado(self):
        self.sugerencias_paciente += [TratamientosSugeridos.HISOPAR]

    # === ENFERMO ESTABLE
    @Rule(
        ParametrosPaciente(sintomas=P(tiene_demasiados_sintomas),
                           estado_clinico=EstadoClinico.ESTABLE,
                           #    resultado_hisopado=OR(Hisopado.POSITIVO, Hisopado.NO_DISPONIBLE)       # descomentando esto evita el INDICA+LIBERAR aislamiento para un caso
                           )
    )
    def enfermo_estable(self):
        self.sugerencias_paciente += [
            TratamientosSugeridos.INDICAR_AISLAMIENTO]
        self.sugerencias_contactos_estrechos += [
            TratamientosSugeridos.INDICAR_AISLAMIENTO]

    @Rule(
        ParametrosPaciente(estado_clinico=EstadoClinico.ESTABLE,
                           resultado_hisopado=Hisopado.POSITIVO)
    )
    def enfermo_estable_positivo(self):
        self.sugerencias_paciente += [TratamientosSugeridos.TRATAR_CON_ANTITERMICO,
                                      TratamientosSugeridos.LLAMAR_PERIODICAMENTE]

    @Rule(
        ParametrosPaciente(estado_clinico=EstadoClinico.ESTABLE,
                           resultado_hisopado=Hisopado.NEGATIVO)
    )
    def enfermo_estable_negativo(self):
        self.sugerencias_paciente += [
            TratamientosSugeridos.LIBERAR_AISLAMIENTO]
        self.sugerencias_contactos_estrechos += [
            TratamientosSugeridos.LIBERAR_AISLAMIENTO]

    # === ENFERMO DE DE_GRAVEDAD
    @Rule(
        ParametrosPaciente(estado_clinico=EstadoClinico.DE_GRAVEDAD)
    )
    def enfermo_gravedad(self):
        self.sugerencias_paciente += [TratamientosSugeridos.INTERNAR]
        self.sugerencias_contactos_estrechos += [
            TratamientosSugeridos.INDICAR_AISLAMIENTO]

    @Rule(
        ParametrosPaciente(estado_clinico=EstadoClinico.DE_GRAVEDAD,
                           resultado_hisopado=Hisopado.POSITIVO)
    )
    def enfermo_gravedad_positivo(self):
        self.sugerencias_paciente += [
            TratamientosSugeridos.MONITOREAR_EVOLUCION]

    @Rule(
        ParametrosPaciente(estado_clinico=EstadoClinico.DE_GRAVEDAD,
                           resultado_hisopado=Hisopado.NEGATIVO)
    )
    def enfermo_gravedad_negativo(self):
        self.sugerencias_paciente += [TratamientosSugeridos.REALIZAR_ESTUDIOS]
        self.sugerencias_contactos_estrechos += [
            TratamientosSugeridos.LIBERAR_AISLAMIENTO]
