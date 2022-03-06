# Imports
from flask import Flask, Response
from flask_cors import CORS
from flask import request
from flask import jsonify
from flask_session import Session
from flask import Flask, render_template, request, session
import time
import os

# Defining the Flask APP and Setting up the
# Cross-Origin Resource Policy for the web-based front_end
app = Flask(__name__, static_folder="static")
CORS(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

MAX_LOG_RESULTS = 20

class Calculator:
    def __init__(self):
        self.last_valid_request_timestamp = 0
        self._MAX_CONSECUTIVE_ATTEMPTS = 5
        self._TIMEOUT_INTERVAL_SECONDS = 15
        self.consecutive_attempts = 0
        self.notes = []
        self.block_requests = False
        self.log = ""
    
    def local_log_message(self):
        # Create log file
        logging_fname = f"logs/calculator_log_{time.time()}.txt"
        f = open(logging_fname, "x")
        f.close()

        # Save log file
        f = open(logging_fname, "a")
        f.write(self.log)
        f.close()

    def is_timeout_completed(self):
        return int(time.time() - self.last_valid_request_timestamp) > self._TIMEOUT_INTERVAL_SECONDS

    def calculate_output(self):
        ans = ans_expr = ""

        print(f"max consec attempts: {self.consecutive_attempts}")

        # If the maximum number of consecutive requests was reached but the timeout interval has passed, reset the requests count
        if self.consecutive_attempts >= self._MAX_CONSECUTIVE_ATTEMPTS and self.is_timeout_completed():
            #self.notes.clear()
            self.block_requests = False
            self.consecutive_attempts = 0
        
        # If the maximum number of consecutive requests haven't been made, fulfill the request
        if self.consecutive_attempts < self._MAX_CONSECUTIVE_ATTEMPTS:
            self.consecutive_attempts += 1
            expr = request.form['expression']

            # Best-effort to evaluate the input expression
            try:
                ans = str(eval(expr))
                ans_expr = f"{expr.lstrip()} = {ans}"
            except:
                ans_expr = ans = "Invalid syntax!"
            
            print(f"{expr} = {ans}")
            self.log += ans_expr + "\n"
            
            # Add message to log list for client
            self.notes.append(ans_expr)

            # Start a timer by recording the timestamp of the last valid consecutive request
            if self.consecutive_attempts == self._MAX_CONSECUTIVE_ATTEMPTS - 1:
                self.last_valid_request_timestamp = time.time()
        elif not self.block_requests:
            self.block_requests = True
            self.notes.append("You have reached your maximum limit, please wait for 15 seconds")
        
        return ans

calculator = None

def get_client_ip_addr(request):
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy

@app.route('/', methods=['GET', 'POST'])
def home():
    global calculator
    # If the webpage is being requested for the first time
    if request.method == 'GET':
        calculator = Calculator()
        return render_template('index.html')

    ans = calculator.calculate_output()
    return render_template('index.html', entry=ans, logs = calculator.notes[-MAX_LOG_RESULTS:], L=min(len(calculator.notes), MAX_LOG_RESULTS), ip = get_client_ip_addr(request), message="you have reached maximum limit, please try again after 10 seconds")

@app.route('/test', methods=['GET', 'POST'])
def test():
    return "Hello, world"

@app.route('/exportLog', methods=['POST'])
def export_log():
    log_msg = calculator.log
    calculator.local_log_message()
    return Response(log_msg, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))