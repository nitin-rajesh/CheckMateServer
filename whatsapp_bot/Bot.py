from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    resp = MessagingResponse()
    msg = resp.message()
    incoming_msg = request.values.get('Body', '').lower()
    print(incoming_msg)
    url_string = f"https://6228-103-213-210-210.in.ngrok.io/quicktool?claim1={incoming_msg}"
    print(url_string.replace(' ','%20'))
    response = None
    response = requests.get(url=url_string.replace(' ','%20'))
    result = response.json()

    print(incoming_msg)
    # print(result['truth'])

    TruthRating = str(result['truth'].lower())
    if(TruthRating == "true" or TruthRating == "false"):
        try:
            msg.body('This claim appears to be '+'*'+TruthRating+'*'+'!\n*More info*:'+str(result['url'].lower()))
        except:
            msg.body('This claim appears to be '+'*'+str(result['truth'].lower()+'*!')) 
    else:
        msg.body(TruthRating+'!\n*More info*:'+str(result['url'].lower()))
    

    return str(resp)
if __name__ == '__main__':
    app.run(host="localhost", port=5002,debug=True)