import json
import requests
from flask import (Flask, jsonify, render_template)
from model import (connect_to_db, db, Company)



app = Flask(__name__)
app.secret_key = "miau"


def grab_gd_data():
    """queries glassdoor api, returns company information in json format"""

    query = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=206388&t.k=gwse8iYzpD1&action=employers"
    headers = {'user-agent': 'Mozilla/5.0'}
    data = requests.get(query, headers=headers)
    data = data.text

    return json.loads(data)


@app.route("/")
def add_to_db():
    """add select data from api to internal db"""

    result = grab_gd_data()["response"]["employers"]
    for employer in result:
        print employer["name"], employer["overallRating"], employer["squareLogo"], employer["industry"]


    return jsonify(result)

# glassdoor api
# find companies and their ratings
# store into db
# create webapp to display companies & their ratings 
# allow user to update the ratings 

#mine
#http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=217197&t.k=dR0RbavMJUI&action=employers&q=pharmaceuticals&userip=192.168.43.42&useragent=Mozilla/%2F4.0

#david's
#http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=206388&t.k=gwse8iYzpD1&action=employers&q=pharmaceuticals&userip=192.168.43.42&useragent=Mozilla/%2F4.0

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app, "postgresql:///companydata")
    app.run(port=5000)
    grab_gd_data()
