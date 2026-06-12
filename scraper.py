import requests
from bs4 import BeautifulSoup
import csv

def scrape_tenders():
    # Use the exact URL where you see the table
    url = "https://eprocure.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct&sp=SPv9ocG08bS43U4itO7HIntS0Fec7wUuNy1YFXyqSerE%3D"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # We find the table by looking for the list_table class
    table = soup.find('table', {'class': 'list_table'})
    
    tenders = []
    if table:
        # Each row in the table
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 4:  # Ensure there are enough columns
                # Adjust these indices (0, 1, 2, etc.) to match your table columns
                tender_id = cols[0].text.strip()
                tender_title = cols[1].text.strip()
                tender_value = cols[3].text.strip() # Usually the 4th column
                tenders.append([tender_id, tender_title, tender_value])
                
    # Save to CSV
    with open('tenders.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Tender ID', 'Tender Title', 'Tender Value'])
        writer.writerows(tenders)
        
    print(f"Successfully scraped {len(tenders)} tenders.")

if __name__ == "__main__":
    scrape_tenders()
