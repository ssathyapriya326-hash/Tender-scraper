import requests
from bs4 import BeautifulSoup
import csv

def scrape_tenders():
    url = "https://eprocure.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct&sp=SPv9ocG08bS43U4itO7HIntS0Fec7wUuNy1YFXyqSerE%3D"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    table = soup.find('table', {'class': 'list_table'})
    
    tenders = []
    if table:
        # We skip the first 2 rows because they are headers/labels
        rows = table.find_all('tr')[2:] 
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 6:  # Ensure the row has enough columns
                # Based on standard CPPP tables:
                # Column 1: Tender ID
                # Column 2: Tender Title
                # Column 4: Tender Value
                tender_id = cols[1].text.strip()
                tender_title = cols[2].text.strip()
                tender_value = cols[4].text.strip()
                
                tenders.append([tender_id, tender_title, tender_value])
    
    with open('tenders.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Tender ID', 'Tender Title', 'Tender Value'])
        writer.writerows(tenders)
        print(f"Scraped {len(tenders)} rows.")

if __name__ == "__main__":
    scrape_tenders()
