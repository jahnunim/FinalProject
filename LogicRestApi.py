from flask import Flask, jsonify
from flask import request
from flask import abort

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/tests/', methods=['GET'])
def run_test():
    if request.args.get('test') == 'SPF':
        test_output = [
            {
                'test':'PSF',
                'score':'10'
            }
        ]
    elif request.args.get('test') == 'VRFY':
        test_output = [
            {
                'test':'VRFY',
                'score':'5'
            }
        ]
    if len(test_output) == 0:
        abort(404)
    return jsonify({'tests': test_output})


if __name__ == '__main__':
    app.run(debug=True)