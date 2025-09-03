import aiohttp
import requests
import asyncio
from bs4 import BeautifulSoup
import time


async def fetch_and_parse(session, url, course_name):
    """Fetch a URL, parse it with Beautiful Soup, and insert the course name"""
    try:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            data = {}
            accordion_items = soup.find_all('div', class_="accordion-item")

            for item in accordion_items:
                heading_tag = item.find('h2', class_="panel-heading")
                heading = heading_tag.get_text(strip=True) if heading_tag else "No Heading"

                content_tag = item.find('div', class_="accordion-content")
                if content_tag:
                    for br in content_tag.find_all("br"):
                        br.replace_with("\n")
                    content = content_tag.get_text(" ", strip=True)
                else:
                    content = "No Content"

                data[heading] = content

            data['course_name'] = course_name

            return {'url': url, 'data': data}

    except Exception as e:
        return {'url': url, 'error': str(e)}


def extract_links(html: str):
    """Extract all graduate program links"""
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', class_="uk-width-medium-1-1")
    base_url = "https://msutexas.edu/academics/graduate-school/"

    links = []
    for div in divs:
        for tag in div.find_all('a', href=True):
            href = base_url + tag['href']
            links.append(href)

    print("Number of links:", len(links))
    return links


def extract_courses(html: str):
    """Extract course names as file-system-friendly strings"""
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', class_="uk-width-medium-1-1")

    courses = []
    for div in divs:
        for li in div.find_all('li'):
            a_tag = li.find('a', href=True)
            if a_tag:
                course_name = a_tag.get_text(strip=True)
                course_name = course_name.replace(',', '')   
                course_name = course_name.replace('.', '')   
                course_name = course_name.lower()        
                course_name = course_name.replace(' ', '_')    
                courses.append(course_name)

    print("Number of courses:", len(courses))
    return courses


async def main():
    url = "https://msutexas.edu/academics/graduate-school/graduate-degrees.php"
    webpage = requests.get(url)
    
    link_result = extract_links(webpage.text)
    course_names = extract_courses(webpage.text)

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_and_parse(session, url, course_names[i] if i < len(course_names) else None)
            for i, url in enumerate(link_result)
        ]
        results = await asyncio.gather(*tasks)

        # for res in results:
        #     print(res['url'], res['data'].get('course_name'))
            
        return results


# if __name__ == "__main__":
#     start = time.time()
#     asyncio.run(main())
#     end = time.time()
#     print("Execution time:", end - start, "seconds")
