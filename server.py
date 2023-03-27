# pylint: disable-all

from flask import Flask
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

app.route("/players", methods=["GET"])(get_all_players)


app.route("/players/<name>", methods=["POST"])(create_player)
app.route("/matches/<winner>/<loser>/<sets>/<score>", methods=["POST"])(add_match)
app.route("/matches/<path:filepath>", methods=["POST"])(add_match_from_csv)


app.route("/players/<id>", methods=["PATCH"])(update_match)

app.route("/players/<id>", methods=["DELETE"])(delete_user)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
