from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
#that will query your Mongo database and pass the mars data into an HTML template to display the data.

def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
# define multiple functions that will scrape each webpage for information
def scrape():
    mars = mongo.db.mars
    data = mission_to_mars.scrape_all()
    mars.update({}, data, upsert=True)
    return redirect("/", code=302)



if __name__ == "__main__":
	app.run(debug=True)


