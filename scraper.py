import requests
from bs4 import BeautifulSoup
import csv

def scrape_tenders():
    # Use a Session to persist headers and cookies
    session = requests.Session()
    url = "https://eprocure.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct&sp=SPv9ocG08bS43U4itO7HIntS0Fec7wUuNy1YFXyqSerE%3D"
    
    # Crucial: Headers that make it look like a real browser
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://eprocure.gov.in/eprocure/app"
    })
    
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Based on your inspector, the table uses the class 'list_table'
    table = soup.find('table', {'class': 'list_table'})
    
    tenders = []
    if table:
        # Find all rows in the table body
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            # Check for columns - usually ID, Title, Value are prominent
            if len(cols) >= 4:
                # Adjust index if necessary based on the specific CPPP view
                tender_id = cols[0].text.strip()
                tender_title = cols[1].text.strip()
                tender_value = cols[3].text.strip()
                tenders.append([tender_id, tender_title, tender_value])
    
    print(f"DEBUG: Found {len(tenders)} rows in the table.")
    
    with open('tenders.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Tender ID', 'Tender Title', 'Tender Value'])
        writer.writerows(tenders)

if __name__ == "__main__":
    scrape_tenders()
