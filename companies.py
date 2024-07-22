import requests
from bs4 import BeautifulSoup
import json

# Step 1: Fetch the web page
url = "https://www.listafirme.ro/hunedoara/petrosani/o1.htm"
response = requests.get(url)
response.raise_for_status()

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Step 3: Locate the relevant section
tbody = soup.find('tbody')

# Step 4: Extract the data-href values
data = []
for row in tbody.find_all('tr'):
    td = row.find('td', class_='clickable-row')
    if td and 'data-href' in td.attrs:
        data_href = td['data-href']
        # Split into name and number
        parts = data_href.rsplit('-', 1)
        name = parts[0]
        number = parts[1] if len(parts) > 1 else ''
        data.append({"name": name, "number": number})

# Step 5: Save the data to a JSON file
with open('extracted_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=2)

print("Data extracted and saved to extracted_data.json")
