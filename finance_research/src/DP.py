from bs4 import BeautifulSoup
import csv
import os

class DocumentParser:
    def __init__(self, document_dir, csv_path):
        self.document_dir = document_dir
        self.csv_path = csv_path

    def parse_documents(self):
        headers = ['file_name', 'content']
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
        soup = BeautifulSoup(content, 'html.parser')

        # Extract all the text inside <p> tags
        paragraphs = soup.find_all('p')
        text_content = ' '.join([p.get_text() for p in paragraphs])

        if text_content:
            return {
                "content": text_content,
            }

# Define the directory where the file is located
file_path = '/Users/jorgevelez/Desktop/GitHub/reinforcement-learning-finance-research/finance_research/data/Lehman-Brothers-data/a07-4192_110k.htm'

# Define the directory where the file is located
document_dir = os.path.dirname(file_path)

# Define the output file path
output_file_path = '/Users/jorgevelez/Desktop/GitHub/reinforcement-learning-finance-research/finance_research/data/sample.csv'

# Create an instance of the DocumentParser class
parser = DocumentParser(document_dir, output_file_path)

# Parse all the documents in the directory
parser.parse_documents()
