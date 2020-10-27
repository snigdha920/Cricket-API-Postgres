from re import match
from models import db, TeamsModel, MatchModel
import os
import datetime
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def verifyRuns(runs, fours, sixes):
    if runs < 4*fours or runs < 6*sixes or runs < (4*fours + 6*sixes) :
        return 0
    return 1

@app.route('/addteam')
def add_team():
    team_id = request.args.get('id')
    team_name=request.args.get('team_name')
    coach_name=request.args.get('coach_name')
    captain_name=request.args.get('captain_name')
    matches_played = request.args.get('matches_played')
    team_id = int(team_id)
    matches_played = int(matches_played)
    try :
        new_team = TeamsModel(
            id = team_id, 
            team_name = team_name, 
            coach_name = coach_name, 
            captain_name = captain_name,
            matches_played = matches_played
            )
        db.session.add(new_team)
        db.session.commit()
        return jsonify({'team added' : new_team.serialize()}), 201
    except Exception as e:
        return {'message' : str(e)}

@app.route('/get_team')
def get_team():
    team_id = request.args.get('team_id')
    team_id = int(team_id)
    try:
        team = TeamsModel.query.filter_by(id = team_id).first()
        if team :
            return jsonify({'team details' : team.serialize()})
        return {'message' : 'Team does not exist'}
    except Exception as e:
        return {'message' : str(e)}

@app.route('/addmatch')
def add_match():
    match_id = request.args.get('id')
    date = request.args.get('date')
    team_1 = request.args.get('team_1')
    team_2 = request.args.get('team_2')
    runs_by_1 = request.args.get('runs_by_1')
    runs_by_2 = request.args.get('runs_by_2')
    wickets_lost_1 = request.args.get('wickets_lost_1')
    wickets_lost_2 = request.args.get('wickets_lost_2')
    fours_by_1 = request.args.get('fours_by_1')
    fours_by_2 = request.args.get('fours_by_2')
    sixes_by_1 = request.args.get('sixes_by_1')
    sixes_by_2 = request.args.get('sixes_by_2')
    motm = request.args.get('motm')
    overs = request.args.get('overs')
    date_time_obj = datetime.datetime.strptime(date, '%d/%m/%Y')
    outcome = 3
    if runs_by_1 > runs_by_2:
        outcome = 1
    if runs_by_1 < runs_by_2:
        outcome = 2
    if team_1 == team_2:
        return {"message" : "Team ID cannot be same for both teams..."}
    if not verifyRuns(int(runs_by_1), int(fours_by_1), int(sixes_by_1)):
        return {"message" : "Number of runs entered for team 1 are invalid..."}
    if not verifyRuns(int(runs_by_2), int(fours_by_2), int(sixes_by_2)):
        return {"message" : "Number of runs entered for team 2 are invalid..."}
    if int(wickets_lost_1) > 11:
        return {"message" : "Number of wickets lost entered for team 1 are invalid..."}
    if int(wickets_lost_2) > 11:
        return {"message" : "Number of wickets lost entered for team 2 are invalid..."}
    try :
        match = MatchModel(
            id = int(match_id),
            date = date_time_obj.date(),
            team_1 = int(team_1),
            team_2 = int(team_2),
            runs_by_1 = int(runs_by_1),
            runs_by_2 = int(runs_by_2),
            wickets_lost_1 = int(wickets_lost_1),
            wickets_lost_2 = int(wickets_lost_2),
            fours_by_1 = int(fours_by_1),
            fours_by_2 = int(fours_by_2),
            sixes_by_1 = int(sixes_by_1),
            sixes_by_2 = int(sixes_by_2),
            winner = int(outcome),
            motm = motm,
            overs = int(overs)
            )
        db.session.add(match)
        db.session.commit()
        team = TeamsModel.query.filter_by(id = match.team_1).first()
        team.matches_played += 1
        db.session.commit()
        team = TeamsModel.query.filter_by(id = match.team_2).first()
        team.matches_played += 1
        db.session.commit()
        return jsonify({'match added' : match.serialize()})
    except Exception as e:
        return {'message' : str(e)}

@app.route('/get_all_matches')
def get_all_matches():
    try:
        matches = MatchModel.query.order_by('date').all()
        all_matches = []
        for match in matches:
            dict = {}
            dict['date'] = str(match.date)
            team1 = TeamsModel.query.filter_by(id = match.team_1).first()
            dict['Team 1'] = team1.team_name
            team2 = TeamsModel.query.filter_by(id = match.team_2).first()
            dict['Team 2'] = team2.team_name
            if match.winner == 1:
                if match.wickets_lost_1 == match.wickets_lost_2:
                    dict['details'] = team1.team_name + " won by " + str(match.runs_by_1 - match.runs_by_2) + " runs."
                else:
                    dict['details'] = team1.team_name + " won by " + str(match.wickets_lost_2 - match.wickets_lost_1) + " wickets."
                dict['winning score'] = str(match.runs_by_1) + "/" + str(match.wickets_lost_1)
            elif match.winner == 2:
                if match.wickets_lost_1 == match.wickets_lost_2:
                    dict['details'] = team2.team_name + " won by " + str(match.runs_by_2 - match.runs_by_1) + " runs."
                else:
                    dict['details'] = team2.team_name + " won by " + str(match.wickets_lost_1 - match.wickets_lost_2) + " wickets."
                dict['winning score'] = str(match.runs_by_2) + "/" + str(match.wickets_lost_2)
            else:
                dict['winning score'] = str(match.runs_by_1) + "/" + str(match.wickets_lost_1)
                dict['details'] = "Match was drawn since both teams scored " + str(match.runs_by_1) + "/" + str(match.wickets_lost_1)
            all_matches.append(dict)
        return jsonify({'all matches' : all_matches})
    except Exception as e:
        return {'message' : str(e)}

@app.route('/get_match')
def get_match():
    match_id = request.args.get('match_id')
    match_id = int(match_id)
    try:
        match = MatchModel.query.filter_by(id = match_id).first()
        if not match :
            return {'message' : 'Match ID does not exist...'}
        dict = {}
        dict['match details'] = match.serialize()
        team = TeamsModel.query.filter_by(id = match.team_1).first()
        dict['Team 1 details'] = team.serialize()
        team = TeamsModel.query.filter_by(id = match.team_2).first()
        dict['Team 2 details'] = team.serialize()
        return jsonify({'about the match' : dict})
    except Exception as e:
        return {'message' : str(e)}
        

if __name__ == "__main__":
    app.run(debug = True)