extends Node2D

var wheels = []
var positions = []
var utility

var highlight_colors = [
	Color(1,0,0),
	Color(0,1,0),
	Color(0,0,1),
	Color(1,1,0),
	Color(1,0,1),
	Color(0,1,1),
	]
var lines = [
	[1,1,1,1,1],
	[0,0,0,0,0],
	[2,2,2,2,2],
	[0,1,2,1,0],
	[2,1,0,1,2],
]

var linepays
var hitpays

var balance = 100
var betting = 1
var freespins = 0
var hits_to_win = 2
var playing = false
var games_played = 0
var wheel_start_stop_delay = 0.15

var playing_lines = true
var play_lines = 5

# Called when the node enters the scene tree for the first time.
func _ready():
	wheels.append(get_node("Wheel1"))
	wheels.append(get_node("Wheel2"))
	wheels.append(get_node("Wheel3"))
	wheels.append(get_node("Wheel4"))
	wheels.append(get_node("Wheel5"))
	
	var delay = 0
	for i in range(len(wheels)):
		var wheel = wheels[i]
		wheel.stop_delay = delay
		delay += wheel_start_stop_delay
	
	wheels[2].tiles[2].change_odds("S", 100)
	wheels[0].tiles[2].change_odds("B2", 25)
	wheels[1].tiles[2].change_odds("B2", 25)
	wheels[2].tiles[2].change_odds("B2", 25)
	wheels[3].tiles[2].change_odds("B2", 25)
	wheels[4].tiles[2].change_odds("B2", 25)
	
	linepays = get_node("PayoutTables").linepays
	hitpays = get_node("PayoutTables").hitpays
	utility = get_node("Utility")
	
	
	display_bet()
	display_balance()
	display_lines()
	pass # Replace with function body.
	

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	
	if playing:
		var finished = true
		for wheel in wheels:
			if wheel.spinning:	
				finished = false
				break
		
		if finished:
			playing = false
			var won = determine_win()
			display_win(won)
			balance += won
			display_balance()
	
	pass
	

func play():
	'''
	Player pressed the play button
	'''
	if playing:
		print("??")
		return
	playing = true
	
	games_played += 1
	print("Game" + str(games_played))
	balance -= betting
	display_balance()
	
	var delay = 0
	for w in wheels:
		w.spin(delay)
		delay += wheel_start_stop_delay
	
	pass
	
func determine_win():
	'''
	Figure out whether and how much was won this spin.
	Also handles highlighting the winning tiles.
	'''
	var endstate = []
	for wheel in wheels:
		endstate.append(wheel.get_result())
	print(endstate)
	
	if playing_lines:
		return determine_win_by_lines(endstate)
	return determine_win_by_hits(endstate)

func determine_win_by_hits(endstate):
	'''
	If we have enough symbols the win is based on the total number shown rather than the lenght and number of lines
	'''
	var winnings = 0
	var info = ""
	var won_on = []
	for symbol in endstate[0]:
		if (not symbol in won_on) and (symbol in endstate[1]) and (symbol in endstate[2]):
			var count = count_symbol(symbol, endstate)
			winnings += count * hitpays[symbol]
			won_on.append(symbol)
			info += symbol + ": " + str(count) + " (" + str(winnings) + "), "
			highlight_by_hits(symbol, endstate, highlight_colors.pick_random())
			
	display_info(info)
	return winnings

func count_symbol(symbol, endstate):
	'''
	Count the symbols that win
	'''
	if len(endstate) == 0:
		return 0
	
	var _endstate = endstate.duplicate()
	var count = 0
	var wheel = _endstate[0]
	_endstate.remove_at(0)
	
	for _symbol in wheel:
		if symbol == _symbol:
			count += 1
	
	# only count the next wheel if there are winning symbols in this one
	if count == 0:
		return count
		
	count += count_symbol(symbol, _endstate)
	return count

func highlight_by_hits(symbol:String, endstate, color:Color):
	'''
	Highlight symbols that have been hit based on the by hit rule
	'''
	for i in range(len(endstate)):
		if symbol in endstate[i]:
			for j in range(len(endstate[i])):
				if endstate[i][j] == symbol:
					wheels[i].highlight(j+1, color)
		else:
			break
	
	pass

func determine_win_by_lines(endstate):
	'''
	Handle winning on lines
	'''
	var info = ""
	var winnings = 0 as float
	for l in range(play_lines):
		var line = lines[l]
		var symbol = endstate[0][line[0]]
		var line_result = check_line(symbol, line, endstate)
		var hits = line_result[0]
		winnings += line_result[1]
		print("spin result: " + str(line_result))
		if hits >= hits_to_win and symbol != "B2":
			info += symbol + ": " + str(hits) + " (" + str(line_result[1]) + "), "
			highlight_line(line, hits, highlight_colors[l])

		# if the player hit the 1st BONUS
		if line_result[2]:
			info += str(hits) + " free spins won! "

		# if the player hit the 2nd BONUS
		if line_result[3]:
			highlight_bonus(line, "B2")
			info += "BONUS HIT! "
			pass
		
	display_info(info)
	return winnings

func check_line(symbol, line, endstate):
	'''
	Get number of hits on the line
	'''
	var hits = 0
	var winnings = 0 
	var can_be_b1 = symbol == "B1"
	# normal line
	for idx in range(len(line)):
		if endstate[idx][line[idx]] == symbol:
			hits += 1
		else:
			break
	
	# bonus line
	var bonus1 = 0
	var bonus2 = 0
	var b1 = false
	var b2 = false
	for idx in range(len(line)):
		if can_be_b1 and endstate[idx][line[idx]] == "B1":
			bonus1 += 1
		elif endstate[idx][line[idx]] == "B2":
			bonus2 += 1
			print("BONUS2")
		pass

	if can_be_b1 and bonus1 > hits_to_win:
		b1 = true
	if bonus2 >= 3:
		b2 = true
	
		
	if b1 and can_be_b1:
		freespins += hits
		print("Won " + str(hits) + " free spins")
	if b2:
		winnings += linepays["B2"][hits-1]
		print("Won " + str(winnings) + " on " + str(bonus2) + " BONUS2's")
	if hits >= 2 and symbol != "B2":
		var base_win = linepays[symbol][hits-1]
		var mult = (betting as float / play_lines as float)
		winnings += base_win * mult
		print("wins " + str(base_win) + " * " + str(mult) + " = " + str(base_win * mult))
	
	return [hits, winnings, b1, b2]

func highlight_line(line, length, color):
	for i in range(len(line)):
		if i == length:
			break
		wheels[i].highlight(line[i]+1, color)
	pass

func highlight_bonus(line, symbol):
	for i in range(len(line)):
		var t = wheels[i].tiles[line[i]+1]
		print(t.currently_am)
		if t.currently_am == symbol:
			for c in highlight_colors:
				wheels[i].highlight(line[i]+1, c)
			
			
		
	pass

func bet_up():
	if betting >= 1:
		betting += 1
	elif betting >= 0.9:
		betting = 1
	else:
		betting += 0.1
	display_bet()
	pass

func bet_down():
	if betting <= 0.1:
		return
		
	if betting <= 1:
		betting -= 0.1
	else:
		betting -= 1
	display_bet()
	pass
	
func lines_up():
	if play_lines < len(lines):
		play_lines += 1
	display_lines()
	pass
	
func lines_down():
	if play_lines > 1:
		play_lines -= 1
	display_lines()
	pass

func display_balance():
	get_node("BalanceDisplayText").set_text("Balance: " + utility.two_decimals(balance))
	pass

func display_win(value):
	get_node("WinDisplayText").set_text("WON: " + utility.two_decimals(value))
	pass

func display_bet():
	get_node("BetDisplay").get_node("BetDisplayText").set_text("Bet: " + utility.two_decimals(betting))
	pass
	
func display_lines():
	get_node("LinesDisplay").get_node("LinesDisplayText").set_text("Lines: " + str(play_lines))
	pass
	
func display_info(message):
	get_node("InfoDisplayText").set_text("Info: " + str(message))
	pass
