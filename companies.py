import requests
from bs4 import BeautifulSoup
import json
import time

base_url = "https://www.listafirme.ro/hunedoara/petrosani/"
page_pattern = "o{}.htm"

def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    company_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if "detalii" in href:  # Adjust this condition based on the actual link pattern
            company_links.append(href)
    
    return company_links

def scrape_company_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    name = soup.find('h1').text.strip()
    cui = None
    for td in soup.find_all('td'):
        if "CUI:" in td.text:
            cui = td.findNext('td').text.strip()
            break
    
    return {
        "name": name,
        "cui": cui,
    }

def scrape_all_pages():
    all_company_details = []
    for page_num in range(1, 30):
        page_url = base_url + page_pattern.format(page_num)
        print(f"Scraping page: {page_url}")
        company_links = parse_page(page_url)
        
        for company_link in company_links:
            print(f"Scraping company: {company_link}")
            details = scrape_company_details(company_link)
            all_company_details.append(details)
            time.sleep(1)  # Respectful scraping, avoid getting blocked
        
    return all_company_details

if __name__ == "__main__":
    all_company_details = scrape_all_pages()
    with open('company_details.json', 'w', encoding='utf-8') as f:
        json.dump(all_company_details, f, ensure_ascii=False, indent=4)
    print("Scraping completed and saved to company_details.json")
