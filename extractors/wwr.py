from requests import get
from bs4 import BeautifulSoup


def extract_wwr_jobs(keyword):
    # Initialize search related value
    wwr_url = "https://weworkremotely.com/remote-jobs/search?term="
    search_term = keyword

    # Get html
    response = get(f"{wwr_url}{search_term}")

    # Check response Status
    if response.status_code != 200:
        # Error
        print("Can't request website")
    else:
        # No error
        # Get Company information
        # print(response.text)

        results = []
        # Get html
        soup = BeautifulSoup(response.text, "html.parser")

        # print(soup.prettify())

        jobs = soup.find_all('section', class_="jobs")

        for job_section in jobs:
            job_posts = job_section.find_all('li')

            # Remove last LI which is class="view-all"
            job_posts.pop(-1)

            for post in job_posts:
                anchors = post.find_all('a')

                # Remove first div whic is class="tooltop"
                anchor = anchors[1]

                # Get link
                link = anchor['href']

                # Get company, kink, region
                company, kind, region = anchor.find_all('span',
                                                        class_="company")

                # Get title
                title = anchor.find('span', class_="title")

                # Save web scrapping data in dictionary
                job_data = {
                    'link': f"https://weworkremotely.com{link}",
                    'company': company.string.replace(",", " "),
                    'location': region.string.replace(",", " "),
                    'position': title.string.replace(",", " "),
                }

                results.append(job_data)

        return results
