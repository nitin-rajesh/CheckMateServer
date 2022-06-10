from flask import Flask, request
from news_rp import check_mate
import json

from nltk_trial import extract_keywords

app = Flask(__name__)

@app.route('/checktool',methods=['GET'])
def checktool():
    claim1 = request.args.get('claim1')

    return json.dumps(cm.scrape(claim1))


if __name__ == '__main__':
    cm = check_mate()
    app.run()

