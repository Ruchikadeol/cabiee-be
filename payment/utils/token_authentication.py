
import requests
from goSwift import settings
from rest_framework.response import Response

def get_cashfree_token():

    url = "https://payout-gamma.cashfree.com/payout/v1/authorize"
    headers = {
        "X-Client-Id": settings.CASHFREE_CLIENT_ID,
        "X-Client-Secret": settings.CASHFREE_CLIENT_SECRET
    }
    response = requests.post(url, headers=headers)

    try:
        response.raise_for_status()
        data = response.json()
        token = data.get("data", {}).get("token")

        if not token:
            raise ValueError(f"No token received: {data}")
        return token
    except Exception as e:
        print("error===========>",str(e))
        return None

def transfer_to_user(transfer_data):
    token = get_cashfree_token()

    url = "https://sandbox.cashfree.com/payout/transfers"
    
    
    headers = {
    "Content-Type": "application/json",
    "x-client-id": settings.CASHFREE_CLIENT_ID,
    "x-client-secret": settings.CASHFREE_CLIENT_SECRET,
    "x-api-version": "2024-01-01"
    }

    response = requests.post(url, headers=headers, json=transfer_data)
    return response.json()

def add_beneficiary(receiver):
    token = get_cashfree_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    id=f"user{str(receiver.user.id)}"
    id=id.replace('-','')
    receiver.beneficiary_id=id
    receiver.save()

    data = {
        "beneId":id,
        "name": receiver.name,
        "email": receiver.user.email or "dummy@example.com",
        "phone": receiver.phone_number or "9999999999",
        "bankAccount": receiver.bank_account,
        "ifsc": receiver.ifsc,
        "address1": "N/A",
        "city": "City",
        "state": "State",
        "pincode": "000000"
    }

    url = "https://payout-gamma.cashfree.com/payout/v1/addBeneficiary"
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def transfer_status(transfer_id):
    token = get_cashfree_token()

    url = f"https://sandbox.cashfree.com/payout/transfers?transfer_id={transfer_id}"
    
    
    headers = {
    "x-client-id": settings.CASHFREE_CLIENT_ID,
    "x-client-secret": settings.CASHFREE_CLIENT_SECRET,
    "x-api-version": "2024-01-01"
    }

    response = requests.get(url, headers=headers)
    return response.json()