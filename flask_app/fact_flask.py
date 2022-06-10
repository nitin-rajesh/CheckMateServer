from flask import Flask, request
from news_rp import check_mate
import json
import time
from time import sleep
from similarity_check.sentence_mech import sentence_mech
import threading
import sqlite3

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



@app.route('/quicktool',methods=['GET'])
def quick_page():

    startTime = int(round(time.time()*1000))

    claim1 = request.args.get('claim1')
    claim2 = request.args.get('claim2')

    print('Claim recieved: ' + claim1)

    data = []


    #create two threads; one for query() and one for scrape()

    ### justSense Section

    justSenseThread = threading.Thread(target=justSense,args=(claim1,data,))

    justSenseThread.start()

    ### factScrape section

    factScrapeThread = threading.Thread(target=factScrape,args=(claim1,data,))

    factScrapeThread.start()

    while(justSenseThread.is_alive() or factScrapeThread.is_alive()):
        sleep(0.05)

    jsonData = {}

    finalData = {}

    for val in data:
        jsonData[val['type']] = val

    if jsonData['justSense']['truth'] == 'Void':
        finalData = jsonData['factScrape']

    else:
        finalData = jsonData['justSense']

    endTime = int(round(time.time()*1000))

    print('Execution time: ' + str(endTime - startTime))

    return finalData


def justSense(claim1, dataArr):

    startTime = int(round(time.time()*1000))
    
    isJustSense = True
    claimResponse = cm.query(claim1)
    data = {}
    data['statement'] = []
    data['comparison'] = []

    print('Checking justSense')

    if not bool(claimResponse['justification']):
        isJustSense = False

    else:
        with open('lookup/grammar.txt') as f:
            print(claimResponse['justification'])
            for word in f.read().split():
                if word in str(claimResponse['justification']):
                    isJustSense = False
                    print('justSense false')
                    break
    
    if isJustSense:
        #Reading justification
        isJustSense = True
        trueTag = False

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

    if not isJustSense:
        data['truth'] = 'Void'

    print('Data in justSense thread: ')
    print(data)

    data['type'] = 'justSense'

    dataArr.append(data)


def factScrape(claim1,dataArr):

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

    print('Data in factScrape Thread: ')
    print(data)

    data['type'] = 'factScrape'

    dataArr.append(data)



if __name__ == '__main__':
    cm = check_mate()
    sm = sentence_mech()

    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    
    #conn.execute("INSERT INTO User (name,username,password) VALUES (\'dank\',\'bot\',\'pwd\')")

    #print("Tuple created successfully")

    conn.row_factory = sqlite3.Row


    cur = conn.cursor()
    cur.execute("select * from User")
   
    rows = cur.fetchall(); 

    print(len(rows))
    for row in rows:
        print(row['name'])

    conn.commit()
    conn.close()


    app.run()

