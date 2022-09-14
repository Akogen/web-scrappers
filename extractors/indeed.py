from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
# Only for replit
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def get_page_count(keyword):
    # Initialize search related value
    indeed_url = "https://www.indeed.com/jobs?q="
    search_term = keyword

    # Get html
    browser = webdriver.Chrome(options=options)
    browser.get(f"{indeed_url}{search_term}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find('ul', class_="pagination-list")
    pages = pagination.find_all("li", recursive=False)

    page_count = len(pages)

    if page_count >= 5:
        return 5
    else:
        return page_count


def extract_indeed_jobs(keyword):
    browser = webdriver.Chrome(options=options)
    results = []
    search_term = keyword

    # Page count
    pages = get_page_count(search_term)

    # print(f"total Pages{pages}")

    for page in range(pages):

        # Initialize search related value
        indeed_url = "https://www.indeed.com/jobs"

        # Get html
        final_url = f"{indeed_url}?q={search_term}&start={page*10}"
        print("Requesting", final_url)

        browser = webdriver.Chrome(options=options)
        browser.get(final_url)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find('ul', class_="jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)

        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                # print("job list")\

                # h2 = job.find('h2', class_="jobTitle")
                # anchor = h2.find('a').href

                anchor = job.select_one("h2 a")
                link = anchor['href']
                aria_label = anchor['aria-label']
                title = anchor.find('span')['title']

                company = job.find('span', class_="companyName")
                location = job.find('div', class_="companyLocation")

                # Save web scrapping data in dictionary
                job_data = {
                    'link': f"https://www.indeed.com{link}",
                    'company': company.string.replace(",", " "),
                    'location': location.string.replace(",", " "),
                    'position': aria_label.replace(",", " "),
                }

                results.append(job_data)

    return results
