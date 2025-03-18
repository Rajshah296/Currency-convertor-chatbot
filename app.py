from flask import Flask,request,jsonify
import currencyapicom


app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name'][0]


    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source,target):

    """_summary_
        This functions returns the latest exhange rate for the source currency in target currency.
    Returns:
        Returns floating-point value.
    """
    client = currencyapicom.Client('cur_live_n0VkK3qX1ft6LiITu09ItilBS8rj9PZiMfMgX8D5')
    exch_rate = client.latest(source,currencies=[target])
    return exch_rate['data'][f'{target}']['value']

if __name__ == "__main__":
    app.run(debug=True)