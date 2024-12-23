from flask import Flask, request, jsonify
import re
import uuid
from datetime import datetime
import math

# flash app initialization
app = Flask(__name__)

# map to store reciepts and the data
receipts = {}

def calculate_points(receipt):
    points = 0

    #  storing the values from the receipt map
    retailer = receipt.get('retailer', '')
    total = receipt.get('total', '0.00') 
    purchase_date = receipt.get('purchaseDate', '')
    purchase_time = receipt.get('purchaseTime', '')
    items = receipt.get('items', [])

    # 1. Points for retailer name
    retailer_points = sum(c.isalnum() for c in retailer)
    points += retailer_points

    # 2. points for the cost
    if re.match(r'^\d+\.00$', total):
        points += 50

    # 3. points for the total is a multiple of 0.25
    total_float = float(total)
    if abs(total_float % 0.25) < 1e-9:
        points += 25

    # 4. points for pairs of items 
    points += (len(items) // 2) * 5

    # 5. points for item descriptiom
    #    If the length of the cleaned description is a multiple of 3, calculate 20% of the price.
    for item in items:
        description = item.get('shortDescription', '').strip()
        # parsing the data for alphanumeric values
        cleaned_description = ''.join(c for c in description if c.isalnum() or c.isspace())
        cleaned_description = ' '.join(cleaned_description.split())  # Normalize spaces
        
        price = float(item.get('price', '0.00'))
        description_length = len(cleaned_description)
        
        # points for description length
        if description_length % 3 == 0:
            points += math.ceil(price * 0.2)

    # 6. points for an odd day of the month
    day = int(purchase_date.split('-')[2])  
    if day % 2 == 1:
        points += 6

    # 7. points for purchase time
    time = datetime.strptime(purchase_time, '%H:%M').time()
    if datetime.strptime('14:00', '%H:%M').time() <= time <= datetime.strptime('16:00', '%H:%M').time():
        points += 10

    return points

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.get_json()  # get the receipt data from the request
    receipt_id = str(uuid.uuid4())  # this is making the unique ID
    points = calculate_points(data)  # this is doing the math for the points

    
    receipts[receipt_id] = points

    # Debug print statements for tracking
    print(f"ID: {receipt_id} with points: {points}")
    print(f"current receipts: {receipts}")

    # ID is returned as a response
    return jsonify({"id": receipt_id}), 200

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_receipt_points(receipt_id):
    points = receipts.get(receipt_id)  # retrieve points from memory using the receipt ID

    # if the receipt ID is not found, return a 404 error
    if points is None:
        print(f"ID {receipt_id} not found")  # Debug statement
        return jsonify({"error": "receipt not found"}), 404

    # debug
    print(f"points for every ID {receipt_id}: {points}")
    
    # returing the points as a response
    return jsonify({"points": points}), 200

@app.route('/receipts', methods=['GET'])# end point
def list_receipts():
    print(f"all reciepts- {receipts}")  # Debug statement
    return jsonify(receipts), 200

@app.route('/')
def home():

    return "flask is working"

if __name__ == '__main__':
    # confirming that flask is working
    print("flask server on port 5000")

    # running server on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
