from playwright.sync_api import sync_playwright
import csv

def scrape_tenders():
    with sync_playwright() as p:
        # Launch headless browser
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Navigate to the URL
        url = "https://eprocure.gov.in/eprocure/app?component=%24DirectLink&page=FrontEndTendersByOrganisation&service=direct&sp=SPv9ocG08bS43U4itO7HIntS0Fec7wUuNy1YFXyqSerE%3D"
        page.goto(url, wait_until="networkidle")
        
        # Wait specifically for the table to appear
        page.wait_for_selector(".list_table")
        
        # Extract rows
        rows = page.query_selector_all(".list_table tr")
        tenders = []
        
        for row in rows:
            cols = row.query_selector_all("td")
            if len(cols) >= 4:
                # Based on standard CPPP table structure
                tender_id = cols[1].inner_text().strip()
                tender_title = cols[2].inner_text().strip()
                tender_val = cols[4].inner_text().strip()
                tenders.append([tender_id, tender_title, tender_val])
        
        browser.close()
        
    # Save to CSV
    with open('tenders.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Tender ID', 'Tender Title', 'Tender Value'])
        writer.writerows(tenders)
        print(f"Successfully scraped {len(tenders)} tenders.")

if __name__ == "__main__":
    scrape_tenders()
