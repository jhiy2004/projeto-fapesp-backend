from app.data.loader import df, encoders_dict
import pandas as pd

def value_counts_decoded(column_name: str):
    encoder = encoders_dict[column_name]
    decoded = encoder.inverse_transform(df[column_name])
    return pd.Series(decoded).value_counts().to_dict()

def q1():
    return value_counts_decoded("SEXO")

def q2():
    return value_counts_decoded("RACA_COR")

def q3():
    return df["SEXO"].value_counts().to_dict()

def q4():
    return value_counts_decoded("NOME_CURSO")

def q5():
    return value_counts_decoded("IDADE_MATRICULA")

def q6():
    return df["SEXO"].value_counts().to_dict()

def q7():
    return df["SEXO"].value_counts().to_dict()

def q8():
    return df["SEXO"].value_counts().to_dict()

questions = {
    1: { "text": "Qual é a distribuição de gênero dos alunos?", "func": q1 },
    2: { "text": "Qual é a distribuição racial dos alunos?", "func": q2 },
    3: { "text": "Qual é a distribuição de alunos por campus?", "func": q3 },
    4: { "text": "Qual é a distribuição de alunos por curso?", "func": q4 },
    5: { "text": "Qual é a média de idade dos alunos no momento da matrícula?", "func": q5 },
    6: { "text": "Como a distribuição de idade varia entre alunos de diferentes cursos?", "func": q6 },
    7: { "text": "Qual é a proporção de alunos que se autodeclaram de raça/cor específica?", "func": q7 },
    8: { "text": "Qual é a distribuição geográfica dos alunos?", "func": q8 },
}
