import requests
from bs4 import BeautifulSoup
import csv

def save_tenders():
    url = "https://eprocure.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct&sp=SPv9ocG08bS43U4itO7HIntS0Fec7wUuNy1YFXyqSerE%3D"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # We will save to a CSV file
    with open('tenders.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Tender Title', 'Closing Date']) # Headers
        
        # This part will be updated once we identify the specific table classes
        # For now, it creates the file structure
        print("Tender check completed.")

if __name__ == "__main__":
    save_tenders()
