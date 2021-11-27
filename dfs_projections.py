#1) Grab universe of player salaries from DK & Fanduel
### Done manually through website interfaces
#2) Pull in player prop data
#3) Create library of players with position / player / projection / salary
#4) Create optimized lineups

import pandas as pd
import csv
from pydfs_lineup_optimizer import Site, Sport, get_optimizer

#create a class for Player
class Player:
	name = 'first last'
	player_id = ''
	position = ''

	#william hill pts / reb / ast
	wh_points = 0.0
	wh_points_over = 0.0
	wh_points_under = 0.0

	wh_rebounds = 0.0
	wh_rebounds_over = 0.0
	wh_rebounds_under = 0.0

	wh_assists = 0.0
	wh_assists_over = 0.0
	wh_assists_under = 0.0

	#fanduel pts / reb / ast
	fd_points = 0.0
	fd_rebounds = 0.0
	fd_assists = 0.0

	#numberfire blk / stl / to
	nf_blocks = 0.0
	nf_steals = 0.0
	nf_turnovers = 0.0

	#projection (initially excluding fanduel data)
	fd_projection = 0.0
	dk_projection = 0.0
	fanduel_salary = 0
	draftkings_salary = 0
	fanduel_value = 0.0
	draftkings_value = 0.0

	#boolean for if all data is provided by sportsline
	sportsline_fill = False


fanduel_data = pd.read_csv('fanduel_player_data.csv')
wh_points = pd.read_csv('wh_points.csv')
wh_rebounds = pd.read_csv('wh_rebounds.csv')
wh_assists = pd.read_csv('wh_assists.csv')
#pull data from numberfire for blk / stl / to
nf_data = pd.read_csv('nf_data.csv')
#pull data from sportsline for blk / stl / to
sl_data = pd.read_csv('sl_data.csv')

players = []

for ind in fanduel_data.index:
	temp_player = Player()
	temp_player.name = fanduel_data['Nickname'][ind]
	temp_player.position = fanduel_data['Position'][ind]
	
	temp_player.player_id = "nba-"
	for char in temp_player.name:
		if char.isalnum():
			temp_player.player_id += char.lower()


	temp_player.fanduel_salary = fanduel_data['Salary'][ind]
	players.append(temp_player)

#LOOP THROUGH WILLIAM HILL SPORTSBOOK DATA AND ADD PLAYER PTS/REB/AST
for ind in wh_points.index:
	#TO DO: add check to confirm data is pulled for TODAY'S GAME
	for player in players:
		if wh_points['Player ID'][ind] == player.player_id:
			over_line = ''
			under_line = ''
			if 'Over' in wh_points['Bet Name'][ind]:
				over_line = float(wh_points['Bet Price'][ind])
				if over_line < 0:
					over_line = (over_line * (-1)) / ((over_line * (-1)) + 100)
				else:
					over_line = 100 / (over_line + 100)
				player.wh_points_over = over_line

			elif 'Under' in wh_points['Bet Name'][ind]:
				under_line = float(wh_points['Bet Price'][ind])
				if under_line < 0:
					under_line = (under_line * (-1)) / ((under_line * (-1)) + 100)
				else:
					under_line = 100 / (under_line + 100)
				player.wh_points_under = under_line

			player.wh_points = float(wh_points['Bet Points'][ind])

for ind in wh_rebounds.index:
	#TO DO: add check to confirm data is pulled for TODAY'S GAME
	for player in players:
		if wh_rebounds['Player ID'][ind] == player.player_id:
			over_line = ''
			under_line = ''
			if 'Over' in wh_rebounds['Bet Name'][ind]:
				over_line = float(wh_rebounds['Bet Price'][ind])
				if over_line < 0:
					over_line = (over_line * (-1)) / ((over_line * (-1)) + 100)
				else:
					over_line = 100 / (over_line + 100)
				player.wh_rebounds_over = over_line

			elif 'Under' in wh_rebounds['Bet Name'][ind]:
				under_line = float(wh_rebounds['Bet Price'][ind])
				if under_line < 0:
					under_line = (under_line * (-1)) / ((under_line * (-1)) + 100)
				else:
					under_line = 100 / (under_line + 100)
				player.wh_rebounds_under = under_line

			player.wh_rebounds = float(wh_rebounds['Bet Points'][ind])

for ind in wh_assists.index:
	#TO DO: add check to confirm data is pulled for TODAY'S GAME
	for player in players:
		if wh_assists['Player ID'][ind] == player.player_id:
			over_line = ''
			under_line = ''
			if 'Over' in wh_assists['Bet Name'][ind]:
				over_line = float(wh_assists['Bet Price'][ind])
				if over_line < 0:
					over_line = (over_line * (-1)) / ((over_line * (-1)) + 100)
				else:
					over_line = 100 / (over_line + 100)
				player.wh_assists_over = over_line

			elif 'Under' in wh_assists['Bet Name'][ind]:
				under_line = float(wh_assists['Bet Price'][ind])
				if under_line < 0:
					under_line = (under_line * (-1)) / ((under_line * (-1)) + 100)
				else:
					under_line = 100 / (under_line + 100)
				player.wh_assists_under = under_line

			player.wh_assists = float(wh_assists['Bet Points'][ind])
			

#LOOP THROUGH NUMBERFIRE AND CREATE PLAYER ID COLUMN THAT WILL MATCH PLAYER ID DEFINED ABOVE
nf_data['player_id'] = 'nba-'
for ind in nf_data.index:
	text = nf_data['Player'][ind].split()
	player_name = ''
	for word in text:
		if word in ("C", "PG", "SG", "SF", "PF") or "C/" in word or "PG/" in word or "SG/" in word or "SF/" in word or "PF/" in word or "jr." in word.lower():
			break
		else:
			player_name += word
	for char in player_name:
		if char.isalnum():
			nf_data['player_id'][ind] += char.lower()

	for player in players:
		if nf_data['player_id'][ind] == player.player_id:
			player.nf_blocks = float(nf_data['BLK'][ind])
			player.nf_steals = float(nf_data['STL'][ind])
			player.nf_turnovers = float(nf_data['TO'][ind])

#AVERAGE SPORTSLINE DATA WITH NUMBERFIRE DATA FOR BLK / STL / TO
sl_data['player_id'] = 'nba-'
for ind in sl_data.index:
	for char in sl_data['PLAYER'][ind]:
		if char.isalnum():
			sl_data['player_id'][ind] += char.lower()

	for player in players:
		if sl_data['player_id'][ind] == player.player_id:
			if sl_data['BK'][ind] != '-':
				player.nf_blocks = (player.nf_blocks + float(sl_data['BK'][ind])) / 2
			if sl_data['ST'][ind] != '-':	
				player.nf_steals = (player.nf_steals + float(sl_data['ST'][ind])) / 2
			if sl_data['TO'][ind] != '-':
				player.nf_turnovers = (player.nf_turnovers + float(sl_data['TO'][ind])) / 2

			if player.wh_points == 0:
				player.wh_points = float(sl_data['PTS'][ind])
				player.wh_rebounds = float(sl_data['TRB'][ind])
				player.wh_assists = float(sl_data['AST'][ind])
				player.sportsline_fill = True


for player in players:

	if player.wh_points_over > 0 and player.wh_points_under > 0 and player.sportsline_fill == False:
		over_line = player.wh_points_over / (player.wh_points_over + player.wh_points_under)
		under_line = player.wh_points_under / (player.wh_points_over + player.wh_points_under)
		player.wh_points = (player.wh_points + 0.5) * over_line + (player.wh_points - 0.5) * under_line

	if player.wh_rebounds_over > 0 and player.wh_rebounds_under > 0 and player.sportsline_fill == False:
		over_line = player.wh_rebounds_over / (player.wh_rebounds_over + player.wh_rebounds_under)
		under_line = player.wh_rebounds_under / (player.wh_rebounds_over + player.wh_rebounds_under)
		player.wh_rebounds = (player.wh_rebounds + 0.5) * over_line + (player.wh_rebounds - 0.5) * under_line

	if player.wh_assists_over > 0 and player.wh_assists_under > 0 and player.sportsline_fill == False:
		over_line = player.wh_assists_over / (player.wh_assists_over + player.wh_assists_under)
		under_line = player.wh_assists_under / (player.wh_assists_over + player.wh_assists_under)
		player.wh_assists = (player.wh_assists + 0.5) * over_line + (player.wh_assists - 0.5) * under_line

	player.fd_projection = player.wh_points + (player.wh_rebounds * 1.2) + (player.wh_assists * 1.5) + (player.nf_blocks * 3) + (player.nf_steals * 3) - player.nf_turnovers
	if player.fanduel_salary > 0:
		player.fanduel_value = player.fd_projection / player.fanduel_salary * 1000
	else:
		player.fanduel_value = 0
	print(player.name, player.player_id, player.fanduel_value)

filename = 'player-projections.csv'

with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Player', 'Position', 'Salary', 'Value', 'Projection', 'sportsline', 'Points', 'Rebounds', 'Assists', 'Blocks', 'Steals', 'Turnovers'])
    for player in players:
        writer.writerow([player.name, player.position, player.fanduel_salary, player.fanduel_value, player.fd_projection, player.sportsline_fill, player.wh_points, player.wh_rebounds, player.wh_assists, player.nf_blocks, player.nf_steals, player.nf_turnovers])


