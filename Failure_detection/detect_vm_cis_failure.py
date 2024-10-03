from bs4 import BeautifulSoup #Add pip install beautifulsoup4 to the pipeline

file_path = "usg-report-20240521.0326.html" #kube-bench-results-/0/usg-report-20240521.0326.html
# Function to parse .html files for compliance score
def parse_html(file_path):
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        score_cell = soup.find('td', class_='text-center')
        if score_cell:
            compliance_score = float(score_cell.text.strip())
            print(f"Compliance score: {compliance_score}")
            return compliance_score == 100.0
        return False

    
parse_html(file_path)

