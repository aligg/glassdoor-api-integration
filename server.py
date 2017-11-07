import json
import requests
from flask import (Flask, jsonify, render_template, session, redirect, request, flash)
from model import (connect_to_db, db, Company)
from sqlalchemy import desc



app = Flask(__name__)
app.secret_key = "miau"


def grab_gd_data():
    """queries glassdoor api, returns company information in json format"""

    #to do: store keys in session or secret.py
    query = "http://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=206388&t.k=gwse8iYzpD1&action=employers&q=%s" % ('computer')
    headers = {'user-agent': 'Mozilla/5.0'}
    data = requests.get(query, headers=headers)
    data = data.text

    return json.loads(data)


def add_to_db():
    """add select data from api to internal db"""

    existing_data = [company.name for company in Company.query.all()]
    
    result = grab_gd_data()["response"]["employers"]
    for employer in result:
        if employer["name"] not in existing_data:
            employer = Company(name = employer["name"],
                                rating = float(employer["overallRating"]),
                                logo = employer["squareLogo"],
                                industry = employer["industry"])
            ##to do: add if employer logo is None 
            db.session.add(employer)
    db.session.commit()


@app.route("/")
def render_home():
    """Display company rating information"""

    companies = [company for company in Company.query.order_by(desc('rating')).all()]
    session["companies"] = [(company.name, company.rating) for company in companies]

    return render_template("home.html", 
                            companies = companies)


@app.route("/rate")
def render_ratings_updater():
    """Render page for user to update rating"""

    return render_template("rate.html")



@app.route("/rated", methods=["POST"])
def handle_new_rating_input():
    """Handles rating form inputs updating db if valid, redirects home"""

    session.pop("companies", None)

    name = request.form.get("company")
    newrating = request.form.get("newrating")
  
    company = Company.query.filter_by(name=name).first()
    company.rating = float(newrating)
    db.session.commit()

    messagetoflash = "Rating for %s updated to %s" % (name, newrating)
    flash(messagetoflash)

    return redirect("/")


@app.route("/api/ratings")
def render_api_endpoint():
    """Renders an API endpoint with data from db"""

    companydict = {}
    companies = Company.query.all()

    for company in companies:
        companydict[company.item_id] = [company.name, company.rating, company.logo, company.industry]

    return jsonify(companydict)

  

if __name__ == "__main__":
    app.debug = True
    connect_to_db(app, "postgresql:///companydata")
    app.run(port=5000)
    add_to_db()
