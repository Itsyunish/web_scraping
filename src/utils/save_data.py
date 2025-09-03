import aiofiles
import os
from src.scrape.web_scrape import main  # your scraping function

folder_name = 'scraped_file'

async def write_to_file_async():
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    try:
        results = await main()  

        for result in results:
            course_name = result['data'].get('course_name', 'unknown_course')
            safe_filename = f"{course_name}.txt"
            file_path = os.path.join(folder_name, safe_filename)

            text_content = f"Course Name: {course_name}\n\n"
            for heading, content in result['data'].items():
                if heading != 'course_name':  
                    text_content += f"{heading}:\n{content}\n\n"

            async with aiofiles.open(file_path, mode="w", encoding="utf-8") as f:
                await f.write(text_content)

        print("All files written successfully.")

    except Exception as e:
        print(f"Error writing files: {e}")
