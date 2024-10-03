import yaml
from bs4 import BeautifulSoup #Add pip install beautifulsoup4 to the pipeline

file_path = "e2e.log" #plugins/systemd-logs/e2e.log
file_path_yaml = "sonobuoy_results.yaml" #plugins/systemd-logs/sonobuoy_results.yaml

# Function to parse .txt and .report files
def parse_txt_report(file_path):
    failed = False
    with open(file_path, 'r') as file:
        for line in file:
            if "FAIL" in line or "Test Suite Failed" in line:
                print("Sonobuoy End to End Test suite Failed")
                failed = True
                break
    if not failed:
        print("Tests passed")
    return failed


def parse_yaml(file_path):  
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        if data['status'] == 'passed':
            print("Sonobuoy systemd Tests Passed")
            return True
        else:
            print("Sonobuoy systemd Tests Failed")
            return False

# Call the function
parse_txt_report(file_path)
parse_yaml(file_path_yaml)