from flask import Flask, request
from news_rp import check_mate
import json
import time
from similarity_check.sentence_mech import sentence_mech

app = Flask(__name__)

@app.route('/checktool',methods=['GET'])
def checktool():

    startTime = int(round(time.time()*1000))

    data = {}

    claim1 = request.args.get('claim1')
    claim2 = request.args.get('claim2')

    print('Claim recieved: ' + claim1)

    claimResponse = cm.query(claim1)
    data['statement'] = []
    data['comparison'] = []

    isJustSense = True
    trueTag = False

    print('Checking justSense')
    with open('lookup/grammar.txt') as f:
        print(claimResponse['justification'])
        for word in f.read().split():
            if word in str(claimResponse['justification']):
                isJustSense = False
                print('justSense false')
                break

    if bool(claimResponse['justification']) and isJustSense:
        #Reading justification

        for val in claimResponse['justification']:
            data['rating'] = val['truth_rating']
            if data['rating'] != 'Indeterminable':
                data['truth'] = data['rating']
                trueTag = True            
            data['statement'].append(val['justification'])
            
        if not trueTag:    
            #No truth tag
            data['truth'] = 'False'
            for word in claim1.lower().split(' '):
                if word in data['statement'][0].lower():
                    data['truth'] = 'True'
                    break
                
        else:
            if(data['truth'] == True):
                data['truth'] = 'True'
            else:
                data['truth'] = 'False'
    else:
        #Fact check
        data = {}

        simVal = -0.1

        claimList=cm.scrape(claim1)

        for oneClaim in claimList['justification']:
            try:
                #print(oneClaim)
                if 'says' in oneClaim['claim']:
                    continue
                tempData = {}
                tempData['claim'] = oneClaim['claim']
                tempData['comparison'] = sm.compare(oneClaim['claim'],claim1)
                tempData['truth'] = oneClaim['truth_rating']
                tempData['url'] = oneClaim['url']
                print(tempData)
                if(float(tempData['comparison']) > simVal):
                    data = tempData
                    simVal = float(tempData['comparison'])
            finally:
                continue

    endTime = int(round(time.time()*1000))

    print('Execution time: ' + str(endTime - startTime))

    return data



if __name__ == '__main__':
    cm = check_mate()
    sm = sentence_mech()
    app.run()

