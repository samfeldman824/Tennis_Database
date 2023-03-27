# pylint: disable-all

import re
import os
from flask import Response, request
import json
from bson.objectid import ObjectId
import pymongo
import csv

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

# function to list all players
def get_all_players():
    try:
        data = list(db.player_stats.find()) # list of all players in db
        for player in data:
            player["_id"] = str(player["_id"])
        # returning all players
        return Response(
            response= json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message": "cannot read players"}),
            status=500,
            mimetype="application/json"
        )

# function to add player to db
def create_player(name):
    # creating dictionary to represent new player
    
    try:
        new_player = {
            "Name": name,
            "Wins": 0,
            "Losses": 0,
            "Sets Played": 0,
            "Sets Won": 0,
            "Sets Lost": 0,
            "Sets Played": 0,
            "3 Set Matches": 0
            }
        dbResponse = db.player_stats.insert_one(new_player)
        print(dbResponse.inserted_id)
        return Response(
            response= json.dumps(
            {"message": "player created",
            "name": f"{name}"}
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps(
            {"message": "user not created",
            "name": f"{dbResponse.player}"}
            ),
            status=500,
            mimetype="application/json"
        )
    
# function to add match to matches db
def add_match(winner, loser, sets, score):
    try:
        # create dictionary representing new match
        new_match = {
            "Winner": winner,
            "Loser": loser,
            "Number of Sets": int(sets),
            "Set Scores": json.loads(score)
            }
        
        
        # check if winner of match is a player in db, if not, player is added
        player_w = db.player_stats.find_one({"Name": {"$regex": f"^{winner}$", "$options": "i"}})
        # number of sets in match
        sets_played = len(json.loads(score))

        # whether there was a third set
        if sets_played == 3:
            was_third_set = 1
        else:
            was_third_set = 0
        if player_w is None:
            create_player(winner)

        # updating winner's stats
        db.player_stats.update_one(
            {"Name": {"$regex": f"^{winner}$", "$options": "i"}},
            {"$inc":
            {"Wins": 1,
            "Sets Played": sets_played,
            "Sets Won": 2,
            "Sets Lost": was_third_set,
            "3 Set Matches": was_third_set
            }
            }
            )

        # check if loser of match is a player in db, if not, player is added
        player_l = db.player_stats.find_one({"Name": {"$regex": f"^{loser}$", "$options": "i"}})
        if player_l is None:
            create_player(loser)

        # updating loser's stats
        db.player_stats.update_one(
            {"Name": {"$regex": f"^{loser}$", "$options": "i"}},
            {"$inc":
            {"Losses": 1,
            "Sets Played": sets_played,
            "Sets Won": was_third_set,
            "Sets Lost": 2,
            "3 Set Matches": was_third_set
            }
            }
            )

        # adds match to matches db
        db.matches.insert_one(new_match)
        
        return Response(
            response= json.dumps(
            {"message": "match created",
            }
            ),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps(
            {"message": "match not added"}),
            status=500,
            mimetype="application/json"
        )

# function to parse csv file with match data
def add_match_from_csv(filepath):
    file_found = False
    try:
        try:
            with open(filepath, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                print("file read in")
                        
                new_match = {}
                    
                for row in reader:
                    new_match = {**new_match, **row}
                file_found = True
        except Exception as ex:
            print(ex)

        if not file_found:
            try:
                with open("/" + filepath, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    print("file read in")
                            
                    new_match = {}
                        
                    for row in reader:
                        new_match = {**new_match, **row}
                    file_found = True
            except Exception as ex:
                print(ex)

        
        if not file_found:
                try:
                    with open("." + filepath, newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        print("file read in")
                                
                        new_match = {}
                            
                        for row in reader:
                            new_match = {**new_match, **row}
                        file_found = True
                except Exception as ex:
                    print(ex)    

        
        if not file_found:
                try:
                    with open("./" + filepath, newline='') as csvfile:
                        reader = csv.DictReader(csvfile)
                        print("file read in")
                                
                        new_match = {}
                            
                        for row in reader:
                            new_match = {**new_match, **row}
                        file_found = True
                except Exception as ex:
                    print(ex)    
                
        winner = new_match['Winner']
        loser = new_match['Loser']
        n_sets = new_match['Number of Sets']
        score = new_match['Score']

        add_match(winner, loser, n_sets, score)
        return Response(
        response= json.dumps(
        {"message": "match read"}),
        status=200,
        mimetype="application/json")
    except Exception as ex:
        return Response(
            response= json.dumps(
            {"message": "match not read"}),
            status=500,
            mimetype="application/json"
        )

# function to update a current player name
def update_name(id):
    try:
        name = request.form["Name"]
        dbResponse = db.player_stats.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"Name": name}}
        )
        if dbResponse.modified_count == 1:
            return Response(
                response= json.dumps({"message": "player name updated", "name": f"{name}"}),
                status=200,
                mimetype="application/json"
        )
        else:
            return Response(
                response= json.dumps({"message": "nothing to update"}),
                status=500,
                mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message": "didn't work"}),
            status=500,
            mimetype="application/json"
        )

# function to delete player given id
def delete_player_id(id):
    try:
        dbResponse = db.Matches.delete_one({"_id":ObjectId(id)})
        if dbResponse.deleted_count == 1:
            return Response(
                response= json.dumps({"message": "player deleted"}),
                status=200,
                mimetype="application/json"
            )


    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message": "player not deleted"}),
            status=500,
            mimetype="application/json"
        )

# function to delete player given name
def delete_player_name(name):
    try:
        dbResponse = db.player_stats.delete_one({"Name": {"$regex": f"^{name}$", "$options": "i"}})
        if dbResponse.deleted_count == 1:
            return Response(
                response= json.dumps({"message": "player deleted", "name": f"{name}"}),
                status=200,
                mimetype="application/json"
            )


    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message": "player not deleted"}),
            status=500,
            mimetype="application/json"
        )

