from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Company(db.Model):
    """companies & accompanying data taken in from glassdoor db"""

    __tablename__ = "companies"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    logo = db.Column(db.String(300), nullable=True)
    industry = db.Column(db.String(100), nullable=True)


    def __repr__(self):
        """prettify output"""

        return "<Item item_id=%s name=%s>" % (self.item_id, self.name)


def connect_to_db(app, db_uri="postgresql:///companydata"):
    """Connect the database to app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    db.app = app
    db.init_app(app)



if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB, Yayyy!"
