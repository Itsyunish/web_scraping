import os
import aiofiles
from src.scrape.web_scrape import main
from fastapi import HTTPException, APIRouter

router = APIRouter()

folder_name = 'scraped_file'
@router.post("/save_scrape_data")
async def save_scrape_data():
    
    if os.path.exists(folder_name):
        return {"message": f"Folder folder_name' already exists."}

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
