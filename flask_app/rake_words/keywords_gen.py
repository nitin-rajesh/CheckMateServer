from rake_nltk import Rake
from news_rp import check_mate
import requests


class keyword_extractor:
    def __init__(self) -> None:
        self.r = Rake()
        pass

    def get_keywords(self, str):
        self.r.extract_keywords_from_text(str)
        keywords = self.r.get_ranked_phrases()
        return keywords

    def get_keyphrase(self,str):
        return " ".join(self.get_keywords(str))