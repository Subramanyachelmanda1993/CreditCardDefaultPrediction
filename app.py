from flask import Flask
from creditcarddefault.logger import logging
from creditcarddefault.exception import CreditCradDefaultException
import sys

app=Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        raise Exception("testing custom exception")
    except Exception as e:
        default=CreditCardDefaultException(e,sys)
        logging.info(CreditCardDefaultException.error_message)
        logging.info("testing logging module")
        return "Starting Ineuron's Intership Project"
  
if __name__ == '__main__':
    app.run(debug=True)
    

