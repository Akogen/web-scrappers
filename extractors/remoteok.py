from bs4 import BeautifulSoup
import requests


def extract_remoteok_jobs(term):
    # Initialize search related value
    url = f"https://remoteok.com/remote-{term}-jobs"

    # Get html
    request = requests.get(url, headers={"User-Agent": "Kimchi"})

    # Check response Status
    if request.status_code != 200:
        # Error
        print("Can't request website")
    else:
        # No error
        # Get Company information
        # print(response.text)

        soup = BeautifulSoup(request.text, "html.parser")
        # write your ✨magical✨ code here

        results = []
        # Get html

        #print(soup.prettify())

        jobs = soup.find_all('tr', class_="job")

        # print(soup.prettify())

        for job_section in jobs:
            #print(job_section)

            job_posts = job_section.find_all('td', class_="company")

            for post in job_posts:
                #print(post)

                anchor = post.find('a')
                #print(anchor)

                # Get link
                link = anchor['href']
                #print(link)

                # Get title
                title = anchor.find('h2')
                #print(title.string.replace(",", " "))

                # Get company
                company = post.find('h3')
                #print(company.string.replace(",", " ").strip())

                # Get kink
                kind = "kind"

                # Get region
                regions = post.find_all('div', class_="location")
                #print(regions)
                region = regions[0]
                salary = regions[1]

                # Save web scrapping data in dictionary
                job_data = {
                    'link': f"https://remoteok.com{link}",
                    'company': company.string.replace(",", " ").strip(),
                    'location': region.string.replace(",", " ").strip(),
                    'position': title.string.replace(",", " ").strip(), 
                }

                results.append(job_data)
                
        return results
