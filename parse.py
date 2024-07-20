import requests
from bs4 import BeautifulSoup
import json

def parse_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing the company information
        table = soup.find('table', {'class': 'ts1'})
        company_data = []

        # Iterate through each row in the table, except the header row
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            if len(columns) > 1:  # Ensure it's not an empty row
                company_name = columns[0].get_text(strip=True)
                company_link = columns[0].find('a')['href']
                company_data.append({
                    'name': company_name,
                    'link': company_link
                })

        return company_data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

def scrape_all_pages():
    base_url = "https://www.listafirme.ro/hunedoara/petrosani/"
    all_company_details = []
    for page_number in range(1, 2):  # Adjust range as needed
        page_url = f"{base_url}o{page_number}.htm"
        print(f"Scraping page: {page_url}")
        company_details = parse_page(page_url)
        all_company_details.extend(company_details)
    return all_company_details

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    all_company_details = scrape_all_pages()
    save_to_json(all_company_details, 'company_data.json')
    print(f"Data saved to company_data.json")
