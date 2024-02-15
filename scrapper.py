from bs4 import BeautifulSoup
import requests
import csv

def exportCsv(URL):
    try:
        # Send HTTP request
        URL_RESP = requests.get(URL)
        # Check if the request was successful
        if URL_RESP.status_code == 200:
            # Access the content of the response
            htmlContent = URL_RESP.content
            soup = BeautifulSoup(htmlContent, 'html.parser')

            # Finding tables with specific requirements
            tables = soup.find_all('table')
            print(len(tables))

            # Attempting to export to csv
            with open('crimeData.csv', 'w', newline='') as file:
                writer = csv.writer(file)

                # Loop to write the scraped data into the csv file
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows:
                        columns = row.find_all('td')
                        rowData = [column.text.strip() for column in columns]
                        writer.writerow(rowData)
                
                print("Data was successfully exported")

    except Exception as e:
        print("An error occurred:", e)

exportCsv("https://www.purdue.edu/ehps/police/statistics-policies/daily-crime-log-archives/020524-daily-crime-log.php")
