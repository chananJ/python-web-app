import datetime
import os
from pymongo import MongoClient
from flask import Flask ,render_template,request
from dotenv import load_dotenv

load_dotenv() 

def create_app():
    app = Flask(__name__)
    client=MongoClient(os.getenv("MONGODB_URI"))
    app.db=client.microblog



    @app.route("/",methods =["GET","POST"])
    def index():
        if request.method== "POST":
            entry_content=request.form.get("content")
            date_now=datetime.datetime.now()
            formatted_date = date_now.strftime('%Y-%m-%d %H:%M')
            app.db.entries.insert_one({"content": entry_content, "date":formatted_date })
        entries_with_date=[(
                entry.get("content","[no content]"),
                entry.get("date","[no date]")
            )
        for entry in app.db.entries.find({})
                            ]
        return render_template('index.html',entries=entries_with_date)



    app.db.entries.delete_many({
        "$or": [
            {"content": {"$exists": False}},
            {"date": {"$exists": False}}
        ]
    })
    return app