import os
import requests
from bs4 import BeautifulSoup

# Define the base URL of the EDGAR website and the CIK for Washington Mutual
edgar_base_url = 'https://www.sec.gov/cgi-bin/browse-edgar'

# Lehman Brothers
cik = '0000854886'

#  Washington Mutual
# cik = '0000933136'

# Define the parameters for the search
params = {
    'action': 'getcompany',
    'CIK': cik,
    'type': '10-K',
    'dateb': '',
    'owner': 'exclude',
    'start': '',
    'output': '',
    'count': '100'
}

headers = {
    "User-Agent": "Jorge Velez(jorgev@illinois.edu)"
}

# Make the request to the EDGAR website
response = requests.get(edgar_base_url, params=params, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the document links on the search results page
document_links = []
for table_row in soup.find_all('tr'):
    if '10-K' in table_row.text:
        for link in table_row.find_all('a'):
            if 'Documents' in link.text:
                document_links.append(link['href'])

# Download the documents
for document_link in document_links:
    document_url = 'https://www.sec.gov' + document_link
    document_response = requests.get(document_url, headers=headers)
    document_soup = BeautifulSoup(document_response.content, 'html.parser')
    
    for table_row in document_soup.find_all('tr'):
        for link in table_row.find_all('a'):
            if '.txt' in link['href']:
                txt_link = 'https://www.sec.gov' + link['href']
                txt_response = requests.get(txt_link, headers=headers)
                with open(os.path.join('.', os.path.basename(link['href'])), 'wb') as f:
                    f.write(txt_response.content)
