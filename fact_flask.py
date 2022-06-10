from flask import Flask, request
from fct import check_mate
import json

from nltk_trial import extract_keywords

app = Flask(__name__)

@app.route('/checktool',methods=['GET'])
def checktool():
    claim1 = request.args.get('claim1')

    keywords = extract_keywords(claim1)
    
    return {"Claim":claim1,"Keys":keywords}


if __name__ == '__main__':
    cm = check_mate()
    app.run()

