from pydantic import BaseModel
from typing import List, Tuple

class PredictRequest(BaseModel):
    nome_curso: str
    periodo: str
    raca_cor: str
    sexo: str
    ensino_medio: str
    cotas: str
    tipo_ingresso: str
    situacao: str
    ano_matricula: int

    avg_nota: float
    max_nota: float
    min_nota: float
    median_nota: float

    avg_frequencia: float
    max_frequencia: float
    min_frequencia: float
    median_frequencia: float

    perc_reprovacao: float
    perc_exames: float
    qtd_disciplinas: int
    ano_nascimento: int
    mes_nascimento: int
    idade_matricula: int

class PredictResponse(BaseModel):
    probalidade_evasao: float
    intercepto: float
    resposta: int
    fatores_lime: List[Tuple[str, float]]

class PredictResponseLink(BaseModel):
    resultados: List[PredictResponse]
    download: str