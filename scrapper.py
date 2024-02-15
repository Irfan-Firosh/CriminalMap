from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import csv

def exportCsv(URL, mode):

    # Only creating a new file
    if (URL == "create"):
        with open('crimeData.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            colNames = ["Nature", "Case Number", "Date/Time Occured", "Date/Time Reported", "Location", "Disposition"]
            writer.writerow(colNames)
        return

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

            # Attempting to export to csv
            with open('crimeData.csv', mode, newline='') as file:
                writer = csv.writer(file)

                # Loop to write the scraped data into the csv file
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows:
                        columns = row.find_all('td')
                        rowData = [column.text.strip() for column in columns]
                        writer.writerow(rowData)
                return 1

    except Exception as e:
        print("An error occurred in:", URL)
        return 0

def caller():
    current = datetime.now()
    recentMonday = current- timedelta(current.weekday())

    base1 = "https://www.purdue.edu/ehps/police/statistics-policies/daily-crime-log-archives/"
    base2 = "-daily-crime-log.php"

    status = 0

    exportCsv("create", 'a')

    for i in range(1,12):
        mondays = recentMonday - timedelta(weeks=i)
        formattedMonday = mondays.strftime("%m%d%y")
        url = base1 + formattedMonday + base2
        exportCsv(url, 'a')
        if exportCsv == 0:
            print("Error in: " + url)
            status += 1
    
    if status == 0:
        print("Success!")


caller()


