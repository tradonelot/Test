from flask import Flask, render_template, request
from replit import web
from flask_cors import CORS
from flask_api import FlaskAPI
import requests
import datetime
import json
import time



__request_headers = {
        'Host':'groww.in', 
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
        'Accept-Language':'en-US,en;q=0.5', 
        'DNT':'1', 
        'Connection':'keep-alive', 
        'Upgrade-Insecure-Requests':'1',
        'Pragma':'no-cache',
        'Cache-Control':'no-cache',    
    }

s =requests.Session()
#s.proxies.update(proxies)
output = s.get("https://groww.in",headers=__request_headers)
print(output)

expdt = "22MAY" #22113

# Call Range
strike = 17350
ST1 = strike + 50
ST2 = strike + 100
ST3 = strike + 150
ST4 = strike + 200
ST_1 = strike - 50
ST_2 = strike - 100
ST_3 = strike - 150
ST_4 = strike - 200

def nsefetch(payload):
    import requests
    __request_headers = {
        'Host':'groww.in', 
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 
        'Accept-Language':'en-US,en;q=0.5', 
        'DNT':'1', 
        'Connection':'keep-alive', 
        'Upgrade-Insecure-Requests':'1',
        'Pragma':'no-cache',
        'Cache-Control':'no-cache',    
    }
    s =requests.Session()
    output = s.get(payload, headers=__request_headers)
    if output.status_code == 200:
        return output.json()
    else:
        output = s.get("https://groww.in",headers=__request_headers)
        if output.status_code == 200:
            output = s.get(payload, headers=__request_headers)
            if output.status_code == 200:
                return output.json()
            else: print("Error Fetching Payload")

#https://groww.in/v1/api/stocks_fo_data/v1/charting_service/chart/exchange/NSE/segment/FNO/NIFTY2210617350CE/daily?intervalInMinutes=1
#https://groww.in/v1/api/stocks_fo_data/v1/charting_service/chart/exchange/NSE/segment/FNO/NIFTY2210617350PE/daily?intervalInMinutes=1


#STRIKE
_strikeCE = nsefetch("https://groww.in/v1/api/stocks_fo_data/v1/charting_service/chart/exchange/NSE/segment/FNO/NIFTY"+expdt+str(strike)+"CE/daily?intervalInMinutes=1")
_strikeCE = [[(item[0]*1000),item[1]] for item in _strikeCE['candles']]
with open('CE'+str(strike)+'.json', 'w') as outfile:
    json.dump(_strikeCE, outfile)

_strikePE = nsefetch("https://groww.in/v1/api/stocks_fo_data/v1/charting_service/chart/exchange/NSE/segment/FNO/NIFTY"+expdt+str(strike)+"PE/daily?intervalInMinutes=1")
_strikePE = [[(item[0]*1000),item[1]] for item in _strikePE['candles']]
with open('PE'+str(strike)+'.json', 'w') as outfile:
    json.dump(_strikePE, outfile)




app = Flask('app')
CORS(app)
@app.route('/')
def home():
  return render_template('index.html');
  return render_template('CE17350.json');
  return render_template('PE17350.json');

@app.route('/<filename>', methods=['GET'])
def get_json_response(filename):
    labels_dict = {}
    response_dict = {}
    try:
        with open(filename, 'r') as labels:
            labels_dict = json.load(labels)
        response_dict[STATUS] = "true"
        response_dict["labels_mapping"] = labels_dict
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump,status=200,
                        mimetype='application/json')
    except FileNotFoundError as err:
        response_dict = {'error': 'file not found in server'}
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump,status=500,
                        mimetype='application/json')
    except RuntimeError as err:
        response_dict = {'error': 'error occured on Server side.Please try again'}
        js_dump = json.dumps(response_dict)
        resp = Response(js_dump, status=500,
                        mimetype='application/json')
    return resp

app.run(host='0.0.0.0')