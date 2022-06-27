from rake_nltk import Rake
from news_rp import check_mate
import requests


cm = check_mate()
r = Rake()

query = "Climate change causes hurricanes"

r.extract_keywords_from_text(query)

keywords = r.get_ranked_phrases()

string = " ".join(keywords)

print(string)

print(cm.scrape(string))



