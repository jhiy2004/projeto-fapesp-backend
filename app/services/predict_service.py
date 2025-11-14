from app.data.loader import df, encoders_dict, model, explainer, nomes_colunas_categoricas, DOWNLOADS_PATH
from app.models.predict_models import PredictRequest, PredictResponse
import pandas as pd
import numpy as np
from typing import List
from datetime import datetime

def decodificar_fatores_lime(fatores_lime, encoders_dict, nomes_colunas_categoricas):
    """
    Recebe a lista de fatores do LIME e a traduz usando os encoders.
    
    fatores_lime: A lista de tuplas (fator_string, peso) vinda do exp.as_list()
    encoders_dict: O dicionário {nome_coluna: objeto_label_encoder}
    nomes_colunas_categoricas: A lista de nomes das colunas categóricas
    """
    
    fatores_decodificados = []
    
    for fator_string, peso in fatores_lime:
        
        fator_decodificado = fator_string
        foi_decodificado = False

        for nome_col in nomes_colunas_categoricas:
            
            if fator_string.startswith(nome_col + " = "):
                try:
                    valor_str = fator_string.split(' = ')[1]
                    
                    valor_int = int(float(valor_str))
                    
                    encoder = encoders_dict[nome_col]
                    
                    valor_texto = encoder.inverse_transform([valor_int])[0]
                    
                    fator_decodificado = f"{nome_col} = {valor_texto}"
                    foi_decodificado = True
                    break
                
                except Exception as e:
                    print(f"Aviso: Não foi possível decodificar '{fator_string}'. Erro: {e}")
                    fator_decodificado = fator_string
        
        fatores_decodificados.append((fator_decodificado, peso))
        
    return fatores_decodificados

def gerar_nome_arquivo():
    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"explicacoes_alunos_{agora}.xlsx"

def gerar_xlsx(dados: List[PredictResponse]) -> str:
    nome_arquivo = gerar_nome_arquivo()
    with pd.ExcelWriter(DOWNLOADS_PATH / nome_arquivo) as writer:
        for idx, dado in enumerate(dados):
            dados_para_df = []
            dados_para_df.append({'Item': 'Probabilidade de Risco (Evasão)', 'Valor/Peso': dado.probalidade_evasao})
            dados_para_df.append({'Item': 'Valor Base (Intercepto)', 'Valor/Peso': dado.intercepto})
            dados_para_df.append({'Item': '---', 'Valor/Peso': '---'})
            dados_para_df.append({'Item': 'Fatores de Contribuição (para Classe 0)', 'Valor/Peso': '(Peso)'})
            
            for fator, peso in dado.fatores_lime:
                dados_para_df.append({'Item': fator, 'Valor/Peso': peso})

            df_explicacao_aluno = pd.DataFrame(dados_para_df)

            nome_aba = f'Aluno_Indice_{idx}'
            df_explicacao_aluno.to_excel(writer, sheet_name=nome_aba, index=False)
    
    return nome_arquivo

def predict_alunos(dados: PredictRequest, num_features: int) -> List[PredictResponse]:
    X = pd.DataFrame([{
        "ANO_MATRICULA": dado.ano_matricula,
        "ANO_NASCIMENTO": dado.ano_nascimento,
        "AVG_FREQUENCIA": dado.avg_frequencia,
        "AVG_NOTA": dado.avg_nota,
        "COTAS": encoders_dict["COTAS"].transform([dado.cotas])[0],
        "ENSINO_MEDIO": encoders_dict["ENSINO_MEDIO"].transform([dado.ensino_medio])[0],
        "IDADE_MATRICULA": dado.idade_matricula,
        "MAX_FREQUENCIA": dado.max_frequencia,
        "MAX_NOTA": dado.max_nota,
        "MEDIAN_FREQUENCIA": dado.median_frequencia,
        "MEDIAN_NOTA": dado.median_nota,
        "MES_NASCIMENTO": dado.mes_nascimento,
        "MIN_FREQUENCIA": dado.min_frequencia,
        "MIN_NOTA": dado.min_nota,
        "NOME_CURSO": encoders_dict["NOME_CURSO"].transform([dado.nome_curso])[0],
        "PERC_EXAMES": dado.perc_exames,
        "PERC_REPROVACAO": dado.perc_reprovacao,
        "PERIODO": encoders_dict["PERIODO"].transform([dado.periodo])[0],
        "QTD_DISCIPLINAS": dado.qtd_disciplinas,
        "RACA_COR": encoders_dict["RACA_COR"].transform([dado.raca_cor])[0],
        "SEXO": encoders_dict["SEXO"].transform([dado.sexo])[0],
        "TIPO_INGRESSO": encoders_dict["TIPO_INGRESSO"].transform([dado.tipo_ingresso])[0],
    } for dado in dados])

    X_np = np.array(X)
    y_pred = model.predict(X)

    res = []
    for idx in range(X_np.shape[0]):
        exp = explainer.explain_instance(
            data_row=X_np[idx],
            predict_fn=model.predict_proba,
            num_features=num_features,
            labels=(0,1)
        )

        prob_evasao = exp.predict_proba[0]
        intercepto = exp.intercept[0]

        fatores_lime_codificados = exp.as_list(label=0)

        fatores_lime_decodificados = decodificar_fatores_lime(
            fatores_lime_codificados, 
            encoders_dict, 
            nomes_colunas_categoricas
        )

        fatores_lime = [(fator, peso) for fator, peso in fatores_lime_decodificados]

        res.append(PredictResponse(
            probalidade_evasao=prob_evasao,
            intercepto=intercepto,
            resposta=y_pred[idx],
            fatores_lime=fatores_lime
        ))

    
    return res