import os
import csv
import re
from bs4 import BeautifulSoup

class DocumentParser:
    def __init__(self, document_dir, csv_path):
        self.document_dir = document_dir
        self.csv_path = csv_path

    def parse_documents(self):
        headers = ['company_name', 'filing_date', 'revenues', 'expenses', 'net_income', 'file_name', 'content']
        with open(self.csv_path, "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

            for document_file in os.listdir(self.document_dir):
                try:
                    with open(os.path.join(self.document_dir, document_file), 'r') as doc_file:
                        content = doc_file.read()
                        data = self.parse_content(content)

                        if data:
                            data["file_name"] = document_file
                            writer.writerow(data)
                            print(f'Processed {document_file}')  
                        else:
                            print(f'Failed to process {document_file}')  
                except Exception as e:
                    print(f'Error processing {document_file}: {e}')  

    def parse_content(self, content):
        company_name = self.extract_company_name(content)
        filing_date = self.extract_filing_date(content)
        revenues = self.extract_financial_data(content, 'Total revenue')
        expenses = self.extract_financial_data(content, 'Total expense')
        net_income = self.extract_financial_data(content, 'Net income')
        text_content = self.extract_html_content(content)

        if company_name and filing_date and revenues and expenses and net_income and text_content:
            return {
                "company_name": company_name,
                "filing_date": filing_date,
                "revenues": revenues,
                "expenses": expenses,
                "net_income": net_income,
                "content": text_content,
            }

    def extract_company_name(self, content):
        match = re.search(r'COMPANY CONFORMED NAME:\s+([^\n]+)', content)
        if match:
            return match.group(1).strip()
        return None

    def extract_filing_date(self, content):
        match = re.search(r'CONFORMED PERIOD OF REPORT:\s+([^\n]+)', content)
        if match:
            return match.group(1).strip()
        return None

    def extract_financial_data(self, content, data_name):
        pattern = re.compile(r'{}[\s\S]*?(\b[\d,]+\b)'.format(data_name), re.IGNORECASE)
        match = pattern.search(content)
        if match:
            return int(match.group(1).replace(',', ''))
        return None

    def extract_html_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')

        # Extract all the text inside <p> tags
        paragraphs = soup.find_all('p')
        return ' '.join([p.get_text() for p in paragraphs])
    
    
# Define the directory where the file is located
file_path = '/Users/jorgevelez/Desktop/GitHub/reinforcement-learning-finance-research/finance_research/data/Washington-Mutual-data/a07-3851_110k.htm'

# Define the directory where the file is located
document_dir = os.path.dirname(file_path)

# Define the output file path
output_file_path = '/Users/jorgevelez/Desktop/GitHub/reinforcement-learning-finance-research/finance_research/data/wm_data.csv'

# Create an instance of the DocumentParser class
parser = DocumentParser(document_dir, output_file_path)

# Parse all the documents in the directory
parser.parse_documents()

