import requests
from bs4 import BeautifulSoup
from backend.core.event_manager import event_manager
import backend.core.variables as var
import re
import time

class CheckUpdate():
    def __init__(self):
        # URL of the webpage to check
        self.url = "https://mikobots.com/downloads-mikobots-studio/"  # Replace with the target webpage URL
        self.search_phrase = "Version"  # The phrase you want to search for

    def fetch_and_parse(self, url):
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return BeautifulSoup(response.text, 'html.parser')

    def check_for_phrase_in_specific_section(self, soup, tag='article'):
        content = soup.find(tag)  # Replace 'body' with the specific tag or class you want to search in
        
        version_match = re.search(r'MiKoBots Studio version V(\d+\.\d+)', str(content))
        
        var.UPDATE_VERSION  = version_match.group(1) if version_match else None
        
        description_match = re.search(r'Description:\s*(.*?)(</p>|$)', str(content))
        var.UPDATE_DESCRIPTION = description_match.group(1).strip() if description_match else None
        
        print(f"var.UPDATE_DESCRIPTION {var.UPDATE_DESCRIPTION}")
        
        if float(var.UPDATE_VERSION ) > var.CURRENT_VERSION:
            return True
        else:
            return False

    def CheckUpdateSoftware(self):
        # Fetch and parse the current content of the website 
        try:
            soup = self.fetch_and_parse(self.url)
            # Check if the specific phrase exists in the specified section
            if self.check_for_phrase_in_specific_section(soup):
                var.UPDATE = True
            else:
                var.UPDATE = False
                
        except:
            var.UPDATE = False
            

