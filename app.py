from flask import Flask,render_template,request
import pymongo
import certifi

from data import typeImages
from scrape_data import Scrapper

app = Flask(__name__)

connection = "mongodb+srv://user1:PassWord@cluster0.wpysgqb.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection,tlsCAFile=certifi.where())
db =client['poke']
coll = db['pokemon_db']
pokemon_list = sorted(set([ x['name'] for x in coll.find()]))

scrapper = Scrapper()

currentForm = 0
poke = None
currentPoke = None


@app.route("/")
def hello_world():
    return render_template("index.html",pokes=pokemon_list,typeImages=typeImages,poke_data=None,form=0)

@app.route("/search",methods=["POST"])
def search():
    global currentForm,currentPoke,poke
    searchName = request.form["select-poke"]
    
    if searchName!=currentPoke:
        currentPoke = searchName
        currentForm = 0

    poke = coll.find({"name":searchName})[0]['data']
    return render_template("index.html",pokes=pokemon_list,typeImages=typeImages,poke_data = poke,form=currentForm)


@app.route("/formchange",methods=["POST"])
def formchange():
    global currentForm
    typ = request.form['action']

    if(typ=="next"):
        currentForm+=1
    else:
        currentForm-=1
    
    
    return render_template("index.html",pokes=pokemon_list,typeImages=typeImages,poke_data = poke,form=currentForm)
    
    

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5001,debug=True)
