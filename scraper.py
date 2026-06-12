import requests
from bs4 import BeautifulSoup
import csv

def scrape_tenders():
    url = "https://eprocure.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct&sp=SPv9ocG08bS43U4itO7HIntS0Fec7wUuNy1YFXyqSerE%3D"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # We look for the main tender table
    # Note: eProcure tables are often inside specific IDs or classes
    table = soup.find('table', {'class': 'list_table'})
    
    tenders = []
    if table:
        rows = table.find_all('tr')[1:] # Skip header row
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 2:
                title = cols[1].text.strip()
                closing_date = cols[5].text.strip() # Adjust index based on table
                tenders.append([title, closing_date])
    
    # Save to CSV
    with open('tenders.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Tender Title', 'Closing Date'])
        writer.writerows(tenders)
        
    print(f"Scraped {len(tenders)} tenders.")

if __name__ == "__main__":
    scrape_tenders()
