import requests
import csv
from flask import Flask, render_template, request

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()\

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        currency_code = request.form['currency']
        amount = float(request.form['amount'])

        for rate in data['rates']:
            if rate['code'] == currency_code:
                bid_rate = float(rate['bid'])
                break
        else:
            return "Invalid currency code"
        
        cost_in_pln = amount * bid_rate
        
        return render_template('index.html', cost=cost_in_pln, currency=currency_code, amount=amount)
    else:
        response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
        global data
        data = response.json()

        with open('exchange_rates.csv', mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['currency', 'code', 'bid', 'ask']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for rate in data['rates']:
                writer.writerow({'currency': rate['currency'], 
                                 'code': rate['code'], 
                                 'bid': rate['bid'], 
                                 'ask': rate['ask']})

    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if __name__ == '__main__':
        app.run(debug=True)