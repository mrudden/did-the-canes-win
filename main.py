print("Starting app...")

import requests
from flask import Flask

# For debugging request parsing:
#response = requests.get('https://statsapi.web.nhl.com/api/v1/teams/12?expand=team.schedule.previous')

#prev_response_data = response.json()

#print(prev_response_data['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['away']['score'])

app = Flask('app')

@app.route('/')
def index():
  try:
    previous_game_response = requests.get('https://statsapi.web.nhl.com/api/v1/teams/12?expand=team.schedule.previous')
  except:
    print('Request to the penalty box!')

  try:
    next_game_response = requests.get('https://statsapi.web.nhl.com/api/v1/teams/12?expand=team.schedule.next')
  except:
    print('Request to the penalty box!')

  prev_response_data = previous_game_response.json()

  next_response_data = next_game_response.json()
  
  last_game_date = prev_response_data['teams'][0]['previousGameSchedule']['dates'][0]['date']

  last_game_home_team_name = prev_response_data['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['home']['team']['name']

  last_game_away_team_name = prev_response_data['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['away']['team']['name']


  previous_opponent = 'placeholder hockey people'

  canes_home = True
  if 'Carolina Hurricanes' in last_game_away_team_name:
    canes_home = False

  if canes_home:
    previous_opponent = last_game_away_team_name
  else:
    previous_opponent = last_game_home_team_name

  previous_game_venue = prev_response_data['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['venue']['name'] + '.'

  if 'PNC Arena' in previous_game_venue:
    previous_game_venue += ', the LOUDEST HOUSE in the NHL!'

  previous_game_state = prev_response_data['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['status']['detailedState']

  final_score_home = prev_response_data['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['home']['score']

  final_score_away = prev_response_data['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['away']['score']

  if canes_home:    
    final_score_hurricanes = final_score_home
    final_score_opponent = final_score_away
  else :
    final_score_hurricanes = final_score_away
    final_score_opponent = final_score_home

  next_game_home_team_name = next_response_data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']['team']['name']

  next_game_away_team_name = next_response_data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['away']['team']['name']

  next_opponent = 'placeholder hockey people'

  if 'Carolina Hurricanes' in next_game_home_team_name:
    next_opponent = next_game_away_team_name
  else: 
    next_opponent = next_game_home_team_name

  next_game_date = next_response_data['teams'][0]['nextGameSchedule']['dates'][0]['date']


  style = '<style type="text/css">\nbody {\n  padding: 1rem;\n}\nh1 { \n  font-family: sans-serif;\n  font-size: 3.5rem;\n  font-weight: 600;\n  -webkit-text-fill-color: rgb(226,24,54);\n  -webkit-text-stroke-width: thin;\n  -webkit-text-stroke-color: #000000;\n}\n</style>'
  
  # Initialize HTML body to return
  body_contents = '<body>\n'

  page_title = 'Did the Canes win?'

  # Make sure score is final
  if 'Final' in previous_game_state:
    if final_score_hurricanes > final_score_opponent:
      body_contents += '<h1>CAROLINA HURRICANES WIN!!!!!\n<!--<br/>\n🚨🏒🚨-->\n</h1>\n'
      page_title = '🚨CANES WIN!🚨'
    else:
      body_contents += '<h2>The Carolina Hurricanes did not win.</h2>\n'
      page_title = '😢Sad day for Carolina'
    
    body_contents += 'The last Carolina Hurricanes game was on ' + last_game_date + ' against the ' + previous_opponent + ' at ' + previous_game_venue + '\n'

    body_contents += '<br/>\n<br/>\nThe final score was\n<br/>\nCarolina Hurricanes: ' + str(final_score_hurricanes) + '\n<br/>\n' + previous_opponent + ': ' + str(final_score_opponent) + '\n'
    
    body_contents += '<br/>\n<br/>\n'
    

  body_contents += 'The Hurricanes\' next game will be against the ' + next_opponent + ' on ' + next_game_date + '.\n'

  body_contents += '<br/>\n<br/>\n'

  body_contents += '🎺🎺🎺 LET\'S GO CANES!'
  
  body_contents += '\n</body>'

  page_contents = '<html>\n'
  page_contents += '<head>\n'
  page_contents += '<title>' + page_title + '</title>\n'
  page_contents += style
  page_contents += '\n</head>\n'
  page_contents += body_contents
  page_contents += '\n</html>'
  return page_contents

app.run(host='0.0.0.0', port=8080)
