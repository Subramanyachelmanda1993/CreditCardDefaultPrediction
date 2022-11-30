from flask import Flask

app=Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return "Starting Ineuron's Intership Project"
  
if __name__ == '__main__':
    app.run(debug=True)
    

