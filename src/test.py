import requests
from bs4 import BeautifulSoup

def extract_courses(html: str):
    """Extract course names as file-system-friendly strings"""
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', class_="uk-width-medium-1-1")

    courses = []
    for div in divs:
        for li in div.find_all('li'):
            a_tag = li.find('a', href=True)
            if a_tag:
                # Clean the course name
                course_name = a_tag.get_text(strip=True)
                course_name = course_name.replace(',', '')      # remove commas
                course_name = course_name.replace('.', '')      # remove dots
                course_name = course_name.lower()               # lowercase
                course_name = course_name.replace(' ', '_')     # replace spaces with underscores
                courses.append(course_name)

    print("Number of courses:", len(courses))
    return courses

# Fetch webpage content
url = "https://msutexas.edu/academics/graduate-school/graduate-degrees.php"
response = requests.get(url)
html = response.text

course_names = extract_courses(html)
for course in course_names:
    print(course)
