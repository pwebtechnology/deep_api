from flask import Flask, jsonify, Response, request
from variables import *
from functions import *
from api import *
from operations import *

app = Flask(__name__)

@app.route('/total_data_no_params')
async def total_data_no_params():
    data = await get_total_affiliates_data()
    response = Response(data, content_type='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/total_data_prev_day')
async def total_data_prev_day():
    data = await get_total_affiliates_data_prev_day()
    response = Response(data, content_type='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/total_data_compare',methods=['GET'])
async def total_data_compare():
    props = {
        'startDate': request.args.get('startDate'),
        'endDate': request.args.get('endDate'),
        'affiliates': request.args.getlist('affiliates[]'),
        'divider': request.args.get('divider')
    }
    print(props)
    print(request.args)
    data = await getTotalAffilatesDataCompare(props)
    response = Response(data, content_type='application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# loop = asyncio.get_event_loop()
# loop.run_until_complete(app.run(host='127.0.0.1', port=5000))

# strart = time.time()
asyncio.run(app.run(host='172.23.2.15', port=5000))
# end = time.time()
# print("time exec", end - strart)