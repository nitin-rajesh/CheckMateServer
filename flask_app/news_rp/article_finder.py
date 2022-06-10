import requests
import os


class check_mate:
    def __init__(self) -> None:
        with open(os.path.expanduser('~/TextRef/api_key.txt')) as f:
            self.api_key = f.read().split()[0]
            self.request_headers = {"x-api-key": self.api_key}
        pass

    def query(self,str):
        api_endpoint = f"https://idir.uta.edu/claimbuster/api/v2/query/knowledge_bases/{str}"
        api_response = requests.get(url=api_endpoint, headers=self.request_headers)
        return api_response.json()

    def scrape(self,str):
        api_endpoint = f"https://idir.uta.edu/claimbuster/api/v2/query/fact_matcher/{str}"
        api_response = requests.get(url=api_endpoint, headers=self.request_headers)
        return api_response.json()
