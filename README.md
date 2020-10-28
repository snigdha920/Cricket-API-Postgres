# Cricket API 

Built using Flask & Postgres

# Features

1. Get all matches from database

2. Get a match's details

3. Add a team

4. Add a match

# Usage 

1. http://127.0.0.1:5000/get_all_matches

This endpoint will return list of matches with details 
- Teams who participated 
- Winner
- Team X won by A runs / wickets

2. http://127.0.0.1:5000/addteam?id={team_id}&team_name={team_name}&coach_name={coach_name}&captain_name={captain_name}&matches_played={matches_played}

This endpoint is used to add a team having details
- Team ID (primary key)
- Team name
- Captain name
- Coach name

3. http://127.0.0.1:5000/get_team?team_id={team_id}

This endpoint is used to get a team having details 
- Team ID (primary key)
- Team name
- Captain name
- Coach name
- Matches played till date

4. http://127.0.0.1:5000/addmatch?id={match_id}?team_1={team_1_id}&team_2={team_2_id}&runs_by_1={runs_by_1}&runs_by_2={runs_by_2}&fours_by_1={fours_by_1}&fours_by_2={fours_by_2}&wickets_lost_1={wickets_lost_1}&wickets_lost_2={wickets_lost_2}&sixes_by_1={sixes_by_1}&sixes_by_2={sixes_by_2}&overs={overs}&motm={motm}&date={date}

This endpoint is used to add a match having details 
- Teams who participated 
- Winner
- Match ID of the match
- Runs scored by each team
- Fours scored by each team
- Sixes scored by each team
- Wickets lost by each team
- Overs played in the match

5. http://127.0.0.1:5000/get_match?match_id={match_id}

This endpoint is used to get the following details of a match -
- Teams who participated 
- Winner
- Match ID of the match
- Runs scored by each team
- Fours scored by each team
- Sixes scored by each team
- Wickets lost by each team
- Overs played in the match
- Details of teams that participated such as team name, coach name, captain name, number of matches played till date

# How to use
(Prerequisite : PostgreSQL on local machine)
1. Download the code
2. Install the requirements by running pip install -r requirements.txt
3. Create database cricketdb in PostgreSQL ( run CREATE DATABASE cricketdb in psql command line prompt)
4. Run export APP_SETTINGS="config.DevelopmentConfig" in terminal
5. Run export DATABASE_URL="postgresql://localhost/cricketdb" in terminal
6. Put these two environment variables in a file called .env
    export APP_SETTINGS="config.DevelopmentConfig"
    export DATABASE_URL="postgresql://localhost/books_store"
7. Run python manage.py db init in terminal
8. Run python manage.py db migrate in terminal
9. Run python manage.py db upgrade in terminal
10. Run server by python app.py
