import requests
from bs4 import BeautifulSoup
import json
import os  # Add this import at the top with other imports

def scrape_job_listing(url):
    try:
        # Send a request to the website
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            return None
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.select_one('h1.heading_2_4.heading_title').text.strip() if soup.select_one('h1.heading_2_4.heading_title') else None
        job_title = soup.select_one('div.heading_4_5.profile').text.strip() if soup.select_one('div.heading_4_5.profile') else None
        company_name = soup.select_one('div.heading_6.company_name a').text.strip() if soup.select_one('div.heading_6.company_name a') else None
        location = soup.select_one('#location_names span a').text.strip() if soup.select_one('#location_names span a') else None
        salary = soup.select_one('div.item_body.salary span.desktop').text.strip() if soup.select_one('div.item_body.salary span.desktop') else None
        experience = soup.select_one('div.item_body.desktop-text').text.strip() if soup.select_one('div.item_body.desktop-text') else None
        skills = ", ".join([span.text.strip() for span in soup.select('span.round_tabs')]) if soup.select('span.round_tabs') else None
        other_requirements = ", ".join([p.text.strip() for p in soup.select('div.text-container.additional_detail p')]) if soup.select('div.text-container.additional_detail p') else None
        responsibilities = (soup.select_one('div.text-container').get_text()).strip() if soup.select_one('div.text-container') else None


        start_date = soup.select_one('div.item_body#start-date-first').text.strip() if soup.select_one('div.item_body#start-date-first') else None


        rows = soup.find_all('div', class_='other_detail_item_row')

        start_date = None
        for row in rows:
            heading = row.find('span')
            if heading and 'Start date' in heading.text:
                date_div = row.find('div', class_='item_body', id='start-date-first')
                if date_div:
                    start_date = date_div.text.strip()
                    break

        end_date = None
        for row in rows:
            heading = row.find('span')
            if heading and 'Apply By' in heading.text:
                date_div = row.find('div', class_='item_body')
                if date_div:
                    end_date = date_div.text.strip()
                    break

        heading = soup.find('h3', string="Number of openings")
        num_openings = None
        if heading:
            openings_div = heading.find_next_sibling('div', class_='text-container')
            if openings_div:
                num_openings = openings_div.text.strip()

        opportunities_divs = soup.find_all('div', class_='text body-main')
        opportunities_posted = None
        for div in opportunities_divs:
            text = div.text.strip()
            if "opportunities posted" in text.lower():
                opportunities_posted = text
                break

        candidates_hired = None
        for div in opportunities_divs:
            text = div.text.strip()
            if "candidates hired" in text.lower():
                candidates_hired = text
                break

        perks_heading = soup.find('h3', class_='section_heading heading_5_5 perks_heading')
        if perks_heading:
            perks_container = perks_heading.find_next('div', class_='round_tabs_container')
            perks = ', '.join(span.text.strip() for span in perks_container.find_all('span', class_='round_tabs'))
        else: 
            perks= None

        posted_time = soup.select_one('div.status.status-small.status-success').text.strip() if soup.select_one('div.status.status-small.status-success') else None
        salary_details = ", ".join([p.text.strip() for p in soup.select('div.salary_container p')]) if soup.select_one('div.salary_container p') else None
        # perks = ", ".join([span.text.strip() for span in soup.select('span.round_tabs')]) if soup.select_one('span.round_tabs') else None
        about_company = ", ".join([p.text.strip() for p in soup.select('div.about_company_text_container')]) if soup.select_one('div.about_company_text_container') else None
        who_can_apply  = ", ".join([p.text.strip() for p in soup.select('div.who_can_apply.text-container p')]) if soup.select_one('div.who_can_apply.text-container p') else None
        # who_can_apply = soup.select_one('div.who_can_apply.text-container span.desktop').text.strip() if soup.select_one('div.who_can_apply.text-container span.desktop') else None

        
        hiring_since = soup.select_one('div.text.body-main').text.strip() if soup.select_one('div.text.body-main') else None
        # opportunities_posted = soup.select_one('div.text.body-main:nth-of-type(2)').text.strip() if soup.select_one('div.text.body-main:nth-of-type(2)') else None
        # candidates_hired = soup.select_one('div.text.body-main:nth-of-type(3)').text.strip() if soup.select_one('div.text.body-main:nth-of-type(3)') else None
        
        # Create a dictionary with job details
        job_details = {
            'Title': title,
            'Job Title': job_title,
            'Company Name': company_name,
            'Location': location,
            'Salary': salary,
            'Experience': experience,
            'Skills': skills,
            'Other Requirements': other_requirements,
            'Responsibilities': responsibilities,
            'Start Date': start_date,
            'End Date': end_date,
            'Who can apply': who_can_apply,
            'Posted Time': posted_time,
            'Salary Details': salary_details,
            'Perks': perks,
            'Number of Openings': num_openings,
            'About Company': about_company,
            'Hiring Since': hiring_since,
            'Opportunities Posted': opportunities_posted,
            'Candidates Hired': candidates_hired
        }
        
        return job_details
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_to_json(job_details, filename='job_listing.json'):
    if job_details:
        # Create a 'data' directory if it doesn't exist
        data_dir = os.path.dirname(__file__)
        os.makedirs(data_dir, exist_ok=True)
        
        # Create full file path
        file_path = os.path.join(data_dir, filename)
        
        # Write job details to a JSON file
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(job_details, jsonfile, ensure_ascii=False, indent=4)
        print(f"Job details saved to {file_path}")

def main():
    url = input("Enter the URL of the job listing: \n")
    # url = 'https://internshala.com/job/detail/business-development-executive-job-in-mumbai-at-renovate-india1742884144'
    job_details = scrape_job_listing(url)
    
    if job_details:
        save_to_json(job_details)
    else:
        print("Could not retrieve job details.")

if __name__ == '__main__':
    main()