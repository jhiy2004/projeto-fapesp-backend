from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.data.loader import DOWNLOADS_PATH
from app.models.predict_models import PredictRequest, PredictResponseLink
from app.services.predict_service import predict_alunos, gerar_xlsx
from typing import List

router = APIRouter(prefix="/predict")

@router.post("/", response_model=PredictResponseLink)
def answer_question(request: List[PredictRequest], num_features: int = 10):
    predicts = predict_alunos(request, num_features)
    link = gerar_xlsx(predicts)

    return PredictResponseLink(
        resultados=predicts,
        download=link
    )

@router.get("/downloads/{filename}")
def download_arquivo(filename: str):
    print("HIT")
    path = DOWNLOADS_PATH / filename

    if not path.exists():
        return {
            "erro": "Arquivo não encontrado"
        }

    return FileResponse(
        path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )