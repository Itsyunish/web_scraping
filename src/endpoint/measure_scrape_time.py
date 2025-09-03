from fastapi.responses import JSONResponse
from src.model.university import ModelName
from src.scrape.web_scrape import main
from src.scrape.web_scrape import main
from fastapi import HTTPException, APIRouter

router = APIRouter()

@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.midwestern:
        try:
          await main()
          return JSONResponse(content={"university_name": model_name, "status": "Data Web scraped successfully"})
        except Exception as e:
          raise HTTPException(status_code=500, details=f"Error: {e}")  