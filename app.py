from fixedfloat import FixedFloatAPI
from flask import Flask, request, send_file, render_template, Response, jsonify
import json
import traceback
import re
import random
import string

# Update your API key and secret here! You can get this from fixedfloat.com/apikey

ff = FixedFloatAPI(
    key="YOUR KEY HERE",
    secret="YOUR SECRET HERE"
)

app = Flask(__name__)

@app.route('/')
def home():
  return send_file('index.html')

@app.route('/exchange')
def exchange():
    return send_file('index.html')

@app.route('/status')
def status_form():
    return send_file('status.html')

@app.route('/contact')
def contact():
    return send_file('contact.html')

@app.route('/getorderstatus', methods=['POST'])
def getorderstatus():
    json_str = json.dumps(request.json)
    resp = json.loads(json_str)

    # Get the order ID from the request
    order_id = resp['order_id']

    # Open the order status file that has the order_id variable as the file name in the folder orders
    with open('orders/' + order_id + '.json') as f:
        order_post = json.load(f)

        #get the order id and token from the file and set it to variables
        order_id = order_post['ff_order_id']
        order_token = order_post['ff_order_token']

        # Get the order status from the API
        order_status = ff.getOrder({'id': order_id, 'token': order_token})

        if order_status['status'] == "0":
            return render_template('order_status/pending.html', order_status=order_status, order_id=order_id, amountToSend=order_status['from']['qty'], fr=order_status['from']['currency'], recQty=order_status['to']['qty'], recCoin=order_status['to']['currency'], address=order_status['from']['address'])
        elif order_status['status'] == "1":
            order_post['status'] = 'confirming'
            return render_template('order_status/confirming.html', order_status=order_status)
        elif order_status['status'] == "2":
            order_post['status'] = 'exchanging'
            return render_template('order_status/exchanging.html', order_status=order_status)
        elif order_status['status'] == "3":
            order_post['status'] = 'sending'
            return render_template('order_status/sending.html', order_status=order_status)
        elif order_status['status'] == "4":
            order_post['status'] = 'complete'
            return render_template('order_status/complete.html', order_status=order_status)
        elif order_status['status'] == "5":
            order_post['status'] = 'expired'
            return render_template('order_status/expired.html', order_status=order_status)
        elif order_status['status'] == "6":
            order_post['status'] = 'failed'
            return render_template('order_status/fail.html', order_status=order_status)
        elif order_status['status'] == "7":
            order_post['status'] = 'failed'
            return render_template('order_status/fail.html', order_status=order_status)

    # Save the updated JSON data
    with open('orders/' + order_id + '.json', 'w') as f:
        json.dump(order_post, f)

@app.route('/getprice', methods=['POST'])
def getprice():
    try:
        form_data_price = request.form
        json_form = jsonify(form_data_price)
        json_price_form_data = json_form.get_json()

        # Get the amount and currency from the request
        amount = json_price_form_data['amount_sent']
        currencyToSend = json_price_form_data['send']
        currencyToRecieve = json_price_form_data['receive']

        #If amount has a decimal point and nothing after it, remove the decimal point
        if amount[-1] == ".":
            amount = amount[:-1]

        # If the amount is 0, return 0
        if amount == "0":
            return "0"
        
        print(amount)

        # Get the price from the API
        price = ff.getPrice({'fromCurrency': currencyToSend, 'toCurrency': currencyToRecieve, 'fromQty': amount, 'type': 'fixed'})

        youGet = price['to']['amount']

        #convert Decimal to string
        youGet = str(youGet)

        # Return the price
        return youGet
    except Exception as e:
        # Get the exception traceback as a string
        tb = traceback.format_exc()
        # Use a regular expression to extract the relevant parts of the traceback
        exception_pattern = r'Exception: \(.+\)'
        matches = re.findall(exception_pattern, tb)

        # If matches contains the text "Internal error", then load the error page
        if 'Internal error' in str(matches):
            print("[!] Internal Error 300 | Possible Crypto Amount Issue | Exchanging: " + amount + " ")
            return render_template('error300.html')
        else:
            print("[!] Unknown Error | Error Text:")
            print(matches)
            print("")
            return 'An error occurred: {}'.format(matches)

@app.route('/formstatus', methods=['POST'])
def status():
    form_data = request.form
    json_form = jsonify(form_data)
    json_data = json_form.get_json()

    order_id = json_data['order_id']
    #order_token = request.form['order_token']

    # Get the order id and token from the corresponding file
    with open('orders/' + order_id + '.json') as f:
        order_json = json.load(f)

        #get the order id and token from the file and set it to variables
        order_id = order_json['ff_order_id']
        order_token = order_json['ff_order_token']

        order_status = ff.getOrder({'id': order_id, 'token': order_token})

        if order_status['status'] == "0":
            return render_template('order_status/pending.html', order_status=order_status, order_id=order_id, amountToSend=order_status['from']['qty'], fr=order_status['from']['currency'], recQty=order_status['to']['qty'], recCoin=order_status['to']['currency'], address=order_status['from']['address'])     
        elif order_status['status'] == "1":
            order_json['status'] = "confirming"  # Update the status field in the JSON data
            return render_template('order_status/confirming.html', order_status=order_status)
        elif order_status['status'] == "2":
            order_json['status'] = "exchanging"  # Update the status field in the JSON data
            return render_template('order_status/exchanging.html', order_status=order_status)
        elif order_status['status'] == "3":
            order_json['status'] = "sending"  # Update the status field in the JSON data
            return render_template('order_status/sending.html', order_status=order_status)
        elif order_status['status'] == "4":
            order_json['status'] = "complete"  # Update the status field in the JSON data
            return render_template('order_status/complete.html', order_status=order_status)
        elif order_status['status'] == "5":
            order_json['status'] = "expired"  # Update the status field in the JSON data
            return render_template('order_status/expired.html', order_status=order_status)
        elif order_status['status'] == "6":
            order_json['status'] = "failed"  # Update the status field in the JSON data
            return render_template('order_status/fail.html', order_status=order_status)
        elif order_status['status'] == "7":
            order_json['status'] = "failed"  # Update the status field in the JSON data
            return render_template('order_status/fail.html', order_status=order_status)
    # Save the updated JSON data
    with open('orders/' + order_id + '.json', 'w') as f:
        json.dump(order_json, f)

@app.route('/exchange', methods=['POST'])
def process_exchange():
    try:
        send = request.form.get('send')
        receive = request.form.get('receive')
        amount = request.form['amount1']
        address = request.form['address']

        # Get price
        # price = ff.getPrice({'fromCurrency': fr, 'toCurrency': to, 'fromQty': amount, 'type': 'fixed'})

        # Create order
        order = ff.createOrder({
            'fromCurrency': send,
            'toCurrency': receive,
            'fromQty': amount,
            'toAddress': address,
            'type': 'fixed'
        })
    except Exception as e:
        # Get the exception traceback as a string
        tb = traceback.format_exc()
        # Use a regular expression to extract the relevant parts of the traceback
        exception_pattern = r'Exception: \(.+\)'
        matches = re.findall(exception_pattern, tb)

        # If matches contains the text "Internal error", then load the error page
        if 'Internal error' in str(matches):
            print("[!] Internal Error 300 | Possible Crypto Amount Issue | Exchanging: " + amount + " " + send)
            return render_template('error300.html')
        if 'Invalid address' in str(matches):
            print("[!] Invalid Address | Address: " + address)
            return render_template('invalidaddress.html')
        else:
            print("[!] Unknown Error | Error Text:")
            print(matches)
            print("")
            return 'An error occurred: {}'.format(matches)
    else:
        print(order)

        #if the order json is not empty, then the order was created successfully
        if order:
            #generate a random 10 digit order id
            order_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

            #make a new array to store the order data
            orderDetails = {}
            orderDetails['id'] = order_id
            orderDetails['ff_order_id'] = order['id']
            orderDetails['ff_order_token'] = order['token']
            orderDetails['status'] = 'pending'
            orderDetails['fromQty'] = order['from']['qty']
            orderDetails['fromCoin'] = order['from']['symbol']
            orderDetails['toQty'] = order['to']['qty']
            orderDetails['toCoin'] = order['to']['symbol']

            recQty = order['to']['qty']
            recQty = '{:g}'.format(float(recQty))

            json_data = json.dumps(orderDetails)

            # Write the JSON object to a file with the order id as the file name
            with open('orders/' + order_id + '.json', 'w') as f:
                f.write(json_data)

            resp = Response(render_template('confirmation.html', order_id=order_id, amountToSend=amount, fr=send, recQty=recQty, recCoin=order['to']['symbol'], address=order['from']['address']))
            resp.set_cookie('order_id', order_id)
            return resp
        else:
            return "Order creation failed!"

if __name__ == '__main__':
  app.run(host='208.167.253.83')