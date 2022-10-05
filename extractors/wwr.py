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
                count_company = len(anchor.find_all('span', class_="company"))

                if count_company == 2:
                    company, region = anchor.find_all('span', class_="company")

                elif count_company == 3:
                    company, kind, region = anchor.find_all('span',
                                                            class_="company")
                company = str(company.string).replace(",", " ")
                region = str(region.string).replace(",", " ")

                # Get title
                title = str(anchor.find('span',
                                        class_="title").string).replace(
                                            ",", " ")

                # Save web scrapping data in dictionary
                job_data = {
                    'link': link,
                    'company': company,
                    'location': region,
                    'position': title,
                }


                results.append(job_data)

        return results
