from flask import Flask
from creditcarddefault.logger import logging
from creditcarddefault.exception import CreditCardDefaultException
import sys

app=Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        logging.info("testing logging module")
        return "Starting Ineuron's Intership Project"
    except Exception as e:
        raise CreditCardDefaultException(e, sys) from e
        
  
if __name__ == '__main__':
    app.run(debug=True)
