from flask import Flask, redirect, render_template, request, jsonify, url_for

app = Flask(__name__)

# Dummy model function (replace with your model logic)
def predict(data):
    return {'result': f'You submitted: {data}'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/submit', methods=['POST'])
def api_submit():
    data = request.json.get('complaint')
    result = predict(data)
    return jsonify(result)

# @app.route('/')
# def signup():
#     return render_template('signup.html')

# @app.route('/resident-dashboard')
# def dashboard():
#     return render_template('resident-dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
