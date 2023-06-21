from flask import Flask,render_template,request
import pymongo
import certifi

app = Flask(__name__)

connection = "mongodb+srv://user1:PassWord@cluster0.wpysgqb.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection,tlsCAFile=certifi.where())
db =client['poke']
coll = db['pokemon_list']
pokemon_list = sorted(set([ x['name'] for x in coll.find()]))



@app.route("/")
def hello_world():
    return render_template("index.html",pokes=pokemon_list)

@app.route("/search",methods=["POST"])
def search():
    searchName = request.form["select-poke"]
    return f"<h1>{searchName}</h1>"

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)
