import os
import requests
from bs4 import BeautifulSoup

class EdgarScraper:
    def __init__(self, cik, doc_type, user_email, file_type='txt', count=100):
        self.edgar_base_url = 'https://www.sec.gov/cgi-bin/browse-edgar'
        self.cik = cik
        self.doc_type = doc_type
        self.user_email = user_email
        self.file_type = file_type
        self.count = count

    def get_document_links(self):
        params = {
            'action': 'getcompany',
            'CIK': self.cik,
            'type': self.doc_type,
            'dateb': '',
            'owner': 'exclude',
            'start': '',
            'output': '',
            'count': str(self.count)
        }

        headers = {"User-Agent": self.user_email}

        response = requests.get(self.edgar_base_url, params=params, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        document_links = []
        for table_row in soup.find_all('tr'):
            if self.doc_type in table_row.text:
                for link in table_row.find_all('a'):
                    if 'Documents' in link.text:
                        document_links.append(link['href'])

        return document_links

    def download_documents(self, document_links):
        headers = {"User-Agent": self.user_email}

        for document_link in document_links:
            document_url = 'https://www.sec.gov' + document_link
            document_response = requests.get(document_url, headers=headers)
            document_soup = BeautifulSoup(document_response.content, 'html.parser')

            for table_row in document_soup.find_all('tr'):
                for link in table_row.find_all('a'):
                    if self.file_type in link['href']:
                        file_link = 'https://www.sec.gov' + link['href']
                        file_response = requests.get(file_link, headers=headers)
                        with open(os.path.join('.', os.path.basename(link['href'])), 'wb') as f:
                            f.write(file_response.content)



# Create an instance of the class for each bank
# lehman_scraper = EdgarScraper('0000806085', '10-K', 'jorgev@illinois.edu', 'htm')
wamu_scraper = EdgarScraper('0000933136', '10-K', 'jorgev@illinois.edu', 'htm')

# Get the document links
# lehman_links = lehman_scraper.get_document_links()
wamu_links = wamu_scraper.get_document_links()

# Download the documents
# lehman_scraper.download_documents(lehman_links)
wamu_scraper.download_documents(wamu_links)