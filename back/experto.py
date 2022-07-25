from random import choice
from experta import *
from enum import Enum
from typing import List


class BuildableEnum(Enum):
    @classmethod
    def from_name(cls, string: str):
        for p in cls:
            if p.name == string:
                return p
        raise ValueError(string)


class EstadoClinico(BuildableEnum):
    ESTABLE = 0
    DE_GRAVEDAD = 1

# obsoleto


class SintomasPaciente(BuildableEnum):
    TOS = 0
    FIEBRE = 1
    MOCOS = 2
    DIFICULTAD_RESPIRATORIA = 3
    DOLOR_MUSCULAR = 4
    DECAIMIENTO = 5
    DIARREA = 6
    VOMITOS = 7


class Hisopado(BuildableEnum):
    NO_DISPONIBLE = 0
    POSITIVO = 1
    NEGATIVO = 2


class TratamientosSugeridos(BuildableEnum):
    HISOPAR = "Hisopar al paciente"
    INDICAR_AISLAMIENTO = "Indicar aislamiento"
    TRATAR_CON_MEDICAMENTOS = "Tratar con medicamentos"
    LLAMAR_PERIODICAMENTE = "Llamar periodicamente, cada 10 dias"
    LIBERAR_AISLAMIENTO = "No debe cumplir aislamiento"
    INTERNAR = "Internar"
    MONITOREAR_EVOLUCION = "Monitorear evolucion"
    REALIZAR_ESTUDIOS = "Realizar estudios"
    ANALIZAR = "Analizar paciente"


class ParametrosPaciente(Fact):
    sintomas = Field(int, default=0)
    estado_clinico = Field(
        EstadoClinico, default=EstadoClinico.ESTABLE, mandatory=True)
    resultado_hisopado = Field(Hisopado, default=Hisopado.NO_DISPONIBLE)


def tiene_demasiados_sintomas(cant_sintomas: int) -> bool:
    return cant_sintomas >= 2


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
                           resultado_hisopado=Hisopado.NO_DISPONIBLE
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
        self.sugerencias_paciente += [TratamientosSugeridos.TRATAR_CON_MEDICAMENTOS,
                                      TratamientosSugeridos.LLAMAR_PERIODICAMENTE]

    @Rule(
        ParametrosPaciente(sintomas=P(lambda x: x > 0),
                           estado_clinico=EstadoClinico.ESTABLE,
                           resultado_hisopado=Hisopado.NEGATIVO)
    )
    def enfermo_estable_negativo(self):
        self.sugerencias_paciente += [
            TratamientosSugeridos.LIBERAR_AISLAMIENTO]
        self.sugerencias_contactos_estrechos += [
            TratamientosSugeridos.LIBERAR_AISLAMIENTO]

    @Rule(
        ParametrosPaciente(sintomas=P(lambda x: x > 0))
    )
    def enfermo_sano_estable(self):
        self.sugerencias_paciente += [
            TratamientosSugeridos.ANALIZAR]
        self.sugerencias_contactos_estrechos += []

    # === ENFERMO DE DE_GRAVEDAD
    @Rule(
        ParametrosPaciente(estado_clinico=EstadoClinico.DE_GRAVEDAD)
    )
    def enfermo_gravedad(self):
        self.sugerencias_paciente += [TratamientosSugeridos.INTERNAR]

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

    @Rule(
        ParametrosPaciente(resultado_hisopado=Hisopado.POSITIVO)
    )
    def positivo(self):
        self.sugerencias_paciente += [
            TratamientosSugeridos.INDICAR_AISLAMIENTO]
        self.sugerencias_contactos_estrechos += [
            TratamientosSugeridos.INDICAR_AISLAMIENTO]
