from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from src.model.university import ModelName
from src.scrape.web_scrape import main
from src.endpoint.scrapedata_save import save_scraped_data
from src.endpoint.measure_time import add_process_time_header

app = FastAPI()

# Register middleware
app.middleware("http")(add_process_time_header)

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.midwestern:
        try:
            await main()
            return JSONResponse(
                content={"university_name": str(model_name), "status": "Data Web scraped successfully"}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {e}")

@app.post("/save_scrape_data")
async def save_scrape_data():
    try:
        message = await save_scraped_data()
        return {"message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing files: {e}")
