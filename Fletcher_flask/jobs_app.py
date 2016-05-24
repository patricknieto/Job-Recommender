import flask
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd

#---------- DATAFRAME IN MEMORY ----------------#

#df = pd.read_csv('/static/city.csv')




#---------- URLS AND WEB PAGES -------------#

# Initialize the app
app = flask.Flask(__name__, static_url_path='')

# Homepage
@app.route("/")
def viz_page():
    """
    Homepage: serve our visualization page, awesome.html
    """
    with open("jobs.html", 'r') as viz_file:
        return viz_file.read()

# Get an example and return it's score from the predictor model
@app.route("/score", methods=["POST"])
def score():
    """
    When A POST request with json data is made to this url,
    return the correct barplot
    """
    # Get decision score for our example that came with the request
    data = flask.request.json
    x = data["example"]
    x[0] = 1
    # Put the result in a nice dict so we can send it as json
    results = {"score": x}
    return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#

if __name__ == '__main__':
    app.run()