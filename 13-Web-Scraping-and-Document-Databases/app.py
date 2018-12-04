# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo


# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
#mongo = PyMongo(app)

#Other import method
conn = "mongodb://localhost:27017"
client =pymongo.MongoClient(conn)
db = client.mars_db
collection = db.mars_data
db.mars_data.drop()


@app.route("/")
def home():

    #Find data
    data = list(db.mars_data.find())
    print(data)
    #return template and data
    return render_template("index.html", data=data)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    mars_dict = scrape_mars.scrape()

    # Insert mars_dict into database
    db.mars_data.insert_one(mars_dict)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
