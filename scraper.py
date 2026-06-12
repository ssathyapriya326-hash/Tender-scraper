from playwright.sync_api import sync_playwright
import csv

def scrape_tenders():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        url = "https://eprocure.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct&sp=SPv9ocG08bS43U4itO7HIntS0Fec7wUuNy1YFXyqSerE%3D"
        page.goto(url, wait_until="networkidle")
        page.wait_for_selector(".list_table")
        
        rows = page.query_selector_all(".list_table tr")
        tenders = []
        
        for row in rows:
            cols = row.query_selector_all("td")
            if len(cols) >= 3:
                # Get the full text from the cell containing the info
                full_text = cols[2].inner_text().strip()
                
                # Split based on closing bracket ']'
                # This breaks "[Title][ID][Value]" into parts
                parts = full_text.split(']')
                
                # Clean up the parts by removing opening brackets
                title = parts[0].replace('[', '') if len(parts) > 0 else "N/A"
                val = parts[1].replace('[', '') if len(parts) > 1 else "N/A"
                tid = parts[2].replace('[', '') if len(parts) > 2 else "N/A"
                
                # Only add if we actually found data
                if title != "N/A":
                    tenders.append([title, val, tid])
        
        browser.close()
        
    with open('tenders.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Tender Title', 'Tender Value', 'Tender ID'])
        writer.writerows(tenders)
        print(f"Successfully scraped {len(tenders)} tenders.")

if __name__ == "__main__":
    scrape_tenders()
