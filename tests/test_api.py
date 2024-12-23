import json


def test_process_receipt(client):
    # using the data from the samples 
    data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "total": "1.25",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
        ]
    }
    
    # sending the POST Requests
    response = client.post(
        '/receipts/process', 
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # assertions to check for response
    assert response.status_code == 200
    assert 'id' in response.json


def test_get_points(client):
    # other data
    data = {
        "retailer": "Target",
        "purchaseDate": "2022-01-02",
        "purchaseTime": "13:13",
        "total": "1.25",
        "items": [
            {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
        ]
    }
    
    # POST request
    process_response = client.post(
        '/receipts/process',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    # get the ID from the response
    receipt_id = process_response.json['id']
    
    # GET request
    response = client.get(f'/receipts/{receipt_id}/points')
    
    # assertion to get response
    assert response.status_code == 200
    assert response.json['points'] == 31


def test_invalid_receipt_id(client):
    # sending a GET request with an invalid receipt ID
    response = client.get('/receipts/invalid-id/points')
    
    # checking for 404 code error
    assert response.status_code == 404


def test_list_receipts(client):
    # sending a GET request to list all receipts
    response = client.get('/receipts')
    
    # checking for 200 code error
    assert response.status_code == 200
