from flask import Flask, request, Response
import requests
from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv
import config
import time
app = Flask(__name__)
load_dotenv()


@app.route('/webhook', methods=['POST', 'GET'])  # Paypal IPN Listener
def IPNListener():
    data = request.form
    print(data)


    if data["txn_type"] == "send_money":
        collection = db["deposits"]

        grossAmount = float(data['mc_gross'])
        try:
            feeAmount = float(data["payment_fee"])
        except:
            feeAmount = float(data["mc_fee"])

        sandbox_endpoint = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'

        headers = {"User-Agent": "DiscordBot-IPN"}
        payload = {"cmd": '_notify-validate'}
        payload.update(request.form)
        response = requests.post(sandbox_endpoint, data=payload, headers=headers)


        if response.text == "VERIFIED":
            fData = {
                "_id": data["txn_id"],
                "userID": "",
                "unixTime": str(time.time()),
                "senderEmail": data["payer_email"],
                "grossAmount": grossAmount,
                "feeAmount": feeAmount,
                "feePercentage": float(f"{feeAmount / grossAmount:.3f}") * 100,
                "actualAmount": float(f"{grossAmount - feeAmount:.2f}"),
                "currency": data["mc_currency"]
            }
            collection.insert_one(fData)

        else:
            print(response.text)
            print("IPN is not verified!")

    elif data["txn_type"] == "masspay":
        collection = db["payouts"]

        grossAmount = float(data['mc_gross_1'])
        try:
            feeAmount = float(data["payment_fee_1"])
        except:
            feeAmount = float(data["mc_fee_1"])

        sandbox_endpoint = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'

        headers = {"User-Agent": "DiscordBot-IPN"}
        payload = {"cmd": '_notify-validate'}
        payload.update(request.form)
        response = requests.post(sandbox_endpoint, data=payload, headers=headers)

        if response.text == "VERIFIED":
            fData = {
                "_id": data["masspay_txn_id_1"],
                "userID": "",
                "unixTime": str(time.time()),
                "receiverEmail": data["receiver_email_1"],
                "grossAmount": grossAmount,
                "feeAmount": feeAmount,
                "feePercentage": float(f"{feeAmount / grossAmount:.3f}") * 100,
                "actualAmount": float(f"{grossAmount - feeAmount:.2f}"),
                "currency": data["mc_currency_1"]
            }
            collection.insert_one(fData)

        else:
            print(response.text)
            print("IPN is not verified!")

    else:
        print("Invalid transaction type")



    return Response(status=200)


if __name__ == "__main__":
    db = MongoClient(getenv("MONGODB"))[config.database_name]
    app.run()
