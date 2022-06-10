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

    url_string = f"https://6228-103-213-210-210.in.ngrok.io/checktool?claim1={incoming_msg}"
    print(url_string.replace(' ','%20'))
    response = None
    response = requests.get(url=url_string.replace(' ','%20'))

    result = response.json()

    print(incoming_msg)
    print(result['truth'])
    
    # responded = False
    # # if 'quote' in incoming_msg:
    # #     # return a quote
    # #     r = requests.get('https://api.quotable.io/random')
    # #     if r.status_code == 200:
    # #         data = r.json()
    # #         quote = f'{data["content"]} ({data["author"]})'
    # #     else:
    # #         quote = 'I could not retrieve a quote at this time, sorry.'
    # #     msg.body(quote)
    # #     responded = True
    # # if 'cat' in incoming_msg:
    # #     # return a cat pic
    # #     msg.media('https://cataas.com/cat')
    # #     responded = True
    
    # msg.body('This claim appears to be '+str(result['truth'].lower()+'!'))
    try:
        msg.body('This claim appears to be '+str(result['truth'].lower()+'!\n*More info:'+str(result['url'].lower())))
    except:
        msg.body('This claim appears to be '+str(result['truth'].lower()+'!')) 


    
    # pwt.sendwhatmsg("+917676265272","welcome to pywhatkit",20,21)
    return str(resp)


if __name__ == '__main__':
    app.run(host="localhost", port=5002,debug=True)