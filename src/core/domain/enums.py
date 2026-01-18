from enum import Enum

class TeamSide(str, Enum):
    A = "A"
    B = "B"

class DefenseType(str, Enum):
    SIX_ZERO = "6:0"
    FIVE_ONE = "5:1"
    THREE_TWO_ONE = "3:2:1"
    FOUR_TWO = "4:2"
    MIXED = "Mixta"
    PRESSURE = "Presión"
    OTHER = "Otro"

class ActionType(str, Enum):
    GOL = "GOL"
    GOL_7M = "GOL 7M"
    GOL_CAMPO_A_CAMPO = "GOL CAMPO A CAMPO"
    FALLO_7M = "FALLO 7M"
    PARADA = "PARADA"
    FUERA = "FUERA"
    POSTE = "POSTE"
    BLOCADO = "BLOCADO"
    PERDIDA = "PÉRDIDA"
    RECUPERACION = "RECUPERACIÓN"
    ASISTENCIA = "ASISTENCIA"

class CourtZone(str, Enum):
    EXTREMO_IZQ = "Extremo Izq"
    LATERAL_IZQ = "Lateral Izq"
    CENTRAL = "Central"
    LATERAL_DER = "Lateral Der"
    EXTREMO_DER = "Extremo Der"
    PIVOTE = "Pivote"
    NUEVE_M = "9m"

class MatchStatus(str, Enum):
    SETUP = "SETUP"
    IN_PROGRESS = "IN_PROGRESS"
    PAUSED = "PAUSED"
    FINISHED = "FINISHED"

class Position(str, Enum):
    PORTERO = "Portero"
    EXTREMO_IZQ = "Extremo Izq"
    EXTREMO_DER = "Extremo Der"
    LATERAL_IZQ = "Lateral Izq"
    LATERAL_DER = "Lateral Der"
    CENTRAL = "Central"
    PIVOTE = "Pivote"

class Hand(str, Enum):
    DIESTRO = "Diestro"
    ZURDO = "Zurdo"
