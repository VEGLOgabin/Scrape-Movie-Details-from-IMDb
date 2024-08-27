import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import csv
import time
async def scrape_movies_from_imdb():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=True if you do not need to see the browser
        page = await browser.new_page()

        # Go to the Bing News search page
        await page.goto('https://www.imdb.com/find/?q=all&ref_=nv_sr_sm')
        
        data = []
        base_url = "https://www.imdb.com"
        
        for item in range(10):
            time.sleep(10)
            await page.locator("span.ipc-see-more__text").first.click()
        up = True
        while up:
            await page.wait_for_timeout(2000)  # Here is a timeout  for the new content to load
            
            # Extract content
            content = await page.content()
            soup = BeautifulSoup(content, 'lxml')
            movies = soup.find_all('li', class_='ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click find-result-item find-title-result')

            # Prepare data for CSV

            for item in movies:
                Movie_Title = item.find('a', class_='ipc-metadata-list-summary-item__t').text.strip()
                Movie_URL = base_url + item.find('a', class_='ipc-metadata-list-summary-item__t').get("href")
                list_data = item.find_all("span", class_ = "ipc-metadata-list-summary-item__li")
                Movie_Cover = item.find('img')
                if Movie_Cover is not None:
                    Movie_Cover = Movie_Cover.get("src")
                else:
                    Movie_Cover = None
                if len(list_data) >0:
                    if len(list_data) >=2:
                        Release_Date = list_data[0].text.strip()
                        # Genre = list_data[1].text.strip()
                        Genre = None
                        Movie_Directors = list_data[1].text.strip()
                    if len(list_data)>=3:
                        Genre = list_data[1].text.strip()
                        
                if not Release_Date:
                    Release_Date =None   
                    
                if not Genre:
                    Genre =None   
                    
                if not Movie_Directors:
                    Movie_Directors = None 
                
                
            
                data.append({
                    'Movie_Title': Movie_Title,
                    'Movie_URL': Movie_URL,
                    'Movie_Cover': Movie_Cover,
                    'Release_Date': Release_Date,
                    'Genre': Genre,
                    "Movie_Directors": Movie_Directors
                })
                
            # Now we can update up value in order to stop the while loop
            up = False

        # Save data to CSV
        
        if len(data) > 0:
            with open('movies_from_imdb.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Movie_Title',"Movie_URL","Movie_Cover","Release_Date","Genre", "Movie_Directors"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)

            print(f'Scraped {len(data)} movies. Data saved to movies_from_imdb.csv.')
            
        else:
            print(f'Scraped {len(data)} movies.')

        # Close the browser
        await browser.close()

# Run the scrape function
asyncio.run(scrape_movies_from_imdb())