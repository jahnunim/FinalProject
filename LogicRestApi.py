from flask import Flask, jsonify
from flask import request
from flask import abort
import SPFoop

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/tests/', methods=['GET'])
def run_test():
    test_domain = request.args.get('domain')
    if request.args.get('test') == 'SPF':
        test_object = SPFoop.SPF(test_domain)
        test_score = test_object.SPFcheck(test_domain)
        test_output = [
            {
                'test':'PSF',
                'score percent': test_score
            }
        ]
    else:
        test_output = [
            {
                'test':'FAIL',
                'score percent': 'FAIL'
            }
        ]
    #elif request.args.get('test') == 'VRFY':
     #   test_output = [
        #    {
      #          'test':'VRFY',
       #         'score':'5'
        #    }
        #]
    if len(test_output) == 0:
        abort(404)
    return jsonify({'tests': test_output})

if __name__ == '__main__':
    app.run(debug=True)