# pylint: disable-all

from flask import Flask
from flask_cors import CORS
from routes import *

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.Tennis_DB
    mongo.server_info()
except:
    print("Error -- can't connect")


app = Flask(__name__)
CORS(app)

app.route("/", methods=["GET"])(original)

app.route("/players", methods=["GET"])(get_all_players)
app.route("/players/matches/<name>", methods=["GET"])(get_all_player_matches)


app.route("/players/create_player/<name>", methods=["POST"])(create_player)
app.route("/matches/add_match/<winner>/<loser>/<sets>/<score>", methods=["POST"])(add_match)
app.route("/matches/add_csv/<path:filepath>", methods=["POST"])(add_match_from_csv)


app.route("/players/update/name/<id>", methods=["PATCH"])(update_name)
app.route("/players/update/score/<id>", methods=["PATCH"])(update_score)

app.route("/players/delete/id/<id>", methods=["DELETE"])(delete_player_id)
app.route("/players/delete/name/<name>", methods=["DELETE"])(delete_player_name)
app.route("/matches/delete/<id>", methods=["DELETE"])(delete_match)
app.route("/matches/deleteall", methods=["DELETE"])(delete_matches)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
