import time
import aiofiles
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os
from src.model.university import ModelName
from src.scrape.web_scrape import main

folder_name = "scraped_file"

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.midwestern:
        try:
          await main()
          return JSONResponse(content={"university_name": model_name, "status": "Data Web scraped successfully"})
        except Exception as e:
          raise HTTPException(status_code=500, details=f"Error: {e}")   


folder_name = 'scraped_file'
@app.post("/save_scrape_data")
async def save_scrape_data():
    
    if os.path.exists(folder_name):
        return {"message": f"Folder folder_name}' already exists."}

    try:
        os.makedirs(folder_name, exist_ok=True)

        results = await main()  

        for result in results:
            course_name = result['data'].get('course_name', 'unknown_course')
            
            safe_course_name = course_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
            
            file_path = os.path.join(folder_name, f"{safe_course_name}.txt")

            text_content = f"Course Name: {course_name}\n\n"
            for heading, content in result['data'].items():
                if heading != 'course_name':  
                    text_content += f"{heading}:\n{content}\n\n"

            async with aiofiles.open(file_path, mode="w", encoding="utf-8") as f:
                await f.write(text_content)

        return {"message": "All files written successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing files: {e}")
