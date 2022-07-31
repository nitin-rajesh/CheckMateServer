import secrets
from flask import Flask, request, session, jsonify
from news_rp import check_mate
import json
import time
from time import sleep
from similarity_check.sentence_mech import sentence_mech
from flask_cors import CORS, cross_origin
from rake_words import keyword_extractor
import threading
import sqlite3
from lookup import rating

COUNT = 5

app = Flask(__name__)
app.secret_key = "AbhayArvindhKritikaNitin"
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/checktool',methods=['GET'])
@cross_origin()
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
                tempData['comparison'] = str(sm.compareStr((oneClaim['claim'],claim1, 0)))
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

    return prepareJson(data)



    
@app.route('/quicktool',methods=['GET'])
@cross_origin()
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

    finalData['question'] = jsonData['justSense']['question']

    endTime = int(round(time.time()*1000))

    print('Execution time: ' + str(endTime - startTime))

    return prepareJson(finalData)


@app.route('/checkmate',methods=['GET'])
def checkMate():
    startTime = int(round(time.time()*1000))
    conn = connect_to_db()
    cur = conn.cursor()


    claim1 = request.args.get('claim1')
    claim2 = request.args.get('claim2')
    api_key = request.args.get('key')

    if(api_key == None):
        return prepareJson({"message": "Failed"})
    try:
        key = cur.execute("select * from Keys where key='" + api_key + "'").fetchall()
    except:
        return prepareJson({"message": "Failed"})
    if(len(key) == 0):
        return prepareJson({"message": "Failed"})
    

    count = key[0][2]
    activated = key[0][3]
    if(activated == 0):
        return prepareJson({"message": "Pay Money"})
    

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

    if((count+1)%COUNT == 0):
        cur.execute("Update Keys set count="+str(count+1)+", activated="+str(0)+" where key='"+ api_key +"'")
        pass
    else:
        cur.execute("Update Keys set count="+str(count+1)+" where key='"+ api_key +"'")
    conn.commit()

    endTime = int(round(time.time()*1000))

    print('Execution time: ' + str(endTime - startTime))

    conn.close()
    return prepareJson(finalData)


def justSense(claim1, dataArr):

    startTime = int(round(time.time()*1000))
    
    isJustSense = True
    claimResponse = cm.query(claim1)
    data = {}
    question = ''
    data['statement'] = []
    data['comparison'] = []

    print('Checking justSense')

    if not bool(claimResponse['justification']):
        isJustSense = False

    else:
        question = claimResponse['justification'][0]['question']
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
            if 'what' not in val['question'].lower():
                question = val['question']
            
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
    data['question'] = question

    dataArr.append(data)


def factScrape(claim1,dataArr):

    data = {}

    simVal = -0.1

    claimList=cm.scrape(claim1)

    #print(claimList['justification'])

    for oneClaim in claimList['justification']:
        print(oneClaim)
        if 'says' in oneClaim['claim']:
            continue
        tempData = {}
        tempData['claim'] = oneClaim['claim']
        tempData['comparison'] = str(sm.compareStr(oneClaim['claim'],claim1, 0))
        print(tempData['comparison'])
        tempData['truth'] = oneClaim['truth_rating']
        tempData['url'] = oneClaim['url']
        print(tempData)
        if(float(tempData['comparison']) > simVal):
            data = tempData
            simVal = float(tempData['comparison'])


    print('Data in factScrape Thread: ')
    print(data)

    if not data:
        data['truth'] = rt.procure(simVal)

    data['type'] = 'factScrape'

    dataArr.append(data)



def connect_to_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    # conn.execute("INSERT INTO User (name,username,password) VALUES (\'dank\',\'bot\',\'pwd\')")
    # print("Tuple created successfully")

    return conn

@app.route('/login', methods=["POST"])
@cross_origin()
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    try:    
        conn = connect_to_db()
        user = conn.execute("select * from User where username='"+username+"'").fetchone()

        if(user[2] == password):
            session['user'] = username
            return prepareJson({"message": "Logged In"})
        else:
            return prepareJson({"message": "Failed","desc":"out of bounds"})
    except:
        return prepareJson({"message": "Failed","desc":"db session fail"})

@app.route('/logout', methods=["GET"])
@cross_origin()
def logout():
    try:
        session.pop('user', default=None)
        return prepareJson({"message":"Logout success"})
    except:
        return prepareJson({"message": "Failed"})

@app.route('/add-api-key', methods=["GET"])
@cross_origin()
def addKey():
    try:
        username = session['user']
    except:    
        return prepareJson({"message": "Failed 1"})
    conn = connect_to_db()
    cur = conn.cursor()
    api_key = secrets.token_hex(16)
    cur.execute("insert into Keys (username,key,count,activated) values (\'"+ username +"\',\'"+ api_key +"\',0,1)")
    conn.commit()
    conn.close()
    #return {"message": "Failed 2"}
    return prepareJson({"message": "Key Added"})


@app.route('/keys', methods=["GET"])
@cross_origin()
def all():
    try:
        username = session['user']
    except:    
        return prepareJson({"message": "Failed"})
    conn = connect_to_db()
    cur = conn.cursor()
    users = cur.execute("select * from Keys where username='" + username + "'").fetchall()
    conn.close()

    return prepareJson({"users":users})

@app.route("/renew", methods=["GET"])
@cross_origin()
def activate():
    api_key = request.args.get("key")
    try:
        username = session['user']
    except:    
        return prepareJson({"message": "Failed","desc":"user not logged in"})
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        #users = cur.execute("select * from Keys where username='" + username + "', key='"+ api_key +"'").fetchall()
        cur.execute("Update Keys set activated="+str(1)+" where key='"+ api_key +"'")
        conn.commit()
    except:
        return prepareJson({"message": "Failed","desc":"db entry fail"})
    return prepareJson({"message": "Renewed"})

@app.route("/trial",methods=["GET"])
@cross_origin()
def trial():
    response = jsonify({"message":"Checkmate"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return prepareJson(response)

def prepareJson(dict):
    response = jsonify(dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    cm = check_mate()
    sm = sentence_mech('/Users/nitinrajesh/Code/FantomCode/FC11-404/flask_app/bert_model/custom-bert')
    rt = rating()
    app.run(port=5001, debug=False)
