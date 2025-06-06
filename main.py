from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    estimate_price = None
    a_value = None

    if request.method == 'POST':
        if 'recalculate' in request.form:
            estimate_price = session.get('estimate_price')
            a_value = session.get('a_value')
        else:
            estimate_price = float(request.form['estimate_price'])
            a_value = float(request.form['a_value'])
            session['estimate_price'] = estimate_price
            session['a_value'] = a_value

        plus_randoms = [estimate_price + (estimate_price * random.uniform(0, 0.02)) for _ in range(8)]
        minus_randoms = [estimate_price + (estimate_price * random.uniform(-0.02, 0)) for _ in range(7)]
        all_randoms = plus_randoms + minus_randoms
        selected = random.sample(all_randoms, 4)
        planned_price = sum(selected) / 4
        final_price = ((planned_price - a_value) * 0.87745) + a_value
        result = round(final_price, 2)

    return render_template('index.html', result=result, estimate_price=session.get('estimate_price'), a_value=session.get('a_value'))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
