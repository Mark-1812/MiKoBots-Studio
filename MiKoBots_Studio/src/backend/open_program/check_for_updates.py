import requests
from bs4 import BeautifulSoup
from backend.core.event_manager import event_manager
import backend.core.variables as var
import re
import time

class CheckUpdate():
    def __init__(self):
        # URL of the webpage to check
        self.url = "https://mikobots.com/mikobots-studio/downloads-mikobots-studio/"  # Replace with the target webpage URL
        self.search_phrase = "Version"  # The phrase you want to search for
        self.current_version = None
        
        self.update_version = 0
        self.update_description = "none"
        

    def fetch_and_parse(self, url):
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return BeautifulSoup(response.text, 'html.parser')

    def check_for_phrase_in_specific_section(self, soup, tag='article'):
        content = soup.find(tag)  # Replace 'body' with the specific tag or class you want to search in
        version_match = re.search(r'Mikobots Stuido version</strong> V(\d+\.\d+)', str(content))
        
        self.update_version  = version_match.group(1) if version_match else None
        
        description_match = re.search(r'<strong>Description:\s*</strong>\s*([^<]+)', str(content), re.DOTALL)
        self.update_description = description_match.group(1).strip() if description_match else None
        
        description_tag = soup.find(string="Description: ")  # Find the string "Description:"
        if description_tag:
            # Get the next sibling, which should be the text after 'Description'
            description = description_tag.find_next().get_text(strip=True)
            self.update_description = description   
        
        self.update_version = float(self.update_version)
        


    def CheckUpdateSoftware(self):
        # Fetch and parse the current content of the website 
        try:
            soup = self.fetch_and_parse(self.url)
            self.check_for_phrase_in_specific_section(soup)
            
            # print(self.update_version)
            # print(self.update_description)
            
            return self.update_version, self.update_description
            

        except:
            return self.update_version, self.update_description
            

