from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TeamsModel(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key = True)
    team_name = db.Column(db.String(255), nullable = False)
    coach_name = db.Column(db.String(255), nullable = True)
    captain_name = db.Column(db.String(255), nullable = False)
    matches_played = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return f"Team: {self.id} :- Team name: {self.team_name}, Coach name: {self.coach_name}, Captain name: {self.captain_name}"

    def serialize(self):
        return {
            'id' : self.id,
            'team_name' : self.team_name,
            'coach_name' : self.coach_name,
            'captain_name' : self.captain_name,
            'total matches played' : self.matches_played
        }

class MatchModel(db.Model):
    __tablename__ = "matches"
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable = False)
    team_1 = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable = False)
    team_2 = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable = False)
    team1 = db.relationship("TeamsModel", foreign_keys = [team_1])
    team2 = db.relationship("TeamsModel", foreign_keys = [team_2])
    runs_by_1 = db.Column(db.Integer, nullable = False)
    runs_by_2 = db.Column(db.Integer, nullable = False)
    wickets_lost_1 = db.Column(db.Integer, default = 0)
    wickets_lost_2 = db.Column(db.Integer, default = 0)
    fours_by_1 = db.Column(db.Integer, default = 0)
    fours_by_2 = db.Column(db.Integer, default = 0)
    sixes_by_1 = db.Column(db.Integer, default = 0)
    sixes_by_2 = db.Column(db.Integer, default = 0)
    winner = db.Column(db.Integer, nullable = False)
    motm = db.Column(db.String(255), nullable = False)
    overs = db.Column(db.Integer, nullable = False)


    def serialize(self):
        return {
            'id': self.id,
            'date' : self.date,
            'team_1' : self.team_1,
            'team_2' : self.team_2,
            'runs_by_1' : self.runs_by_1,
            'runs_by_2' : self.runs_by_2,
            'wickets_lost_1' : self.wickets_lost_1,
            'wickets_lost_2' : self.wickets_lost_2,
            'fours_by_1' : self.fours_by_1,
            'fours_by_2' : self.fours_by_2,
            'sixes_by_1' : self.sixes_by_1,
            'sixes_by_2' : self.sixes_by_2,
            'motm' : self.motm,
            'winner' : self.winner, 
            'overs' : self.overs
        }
