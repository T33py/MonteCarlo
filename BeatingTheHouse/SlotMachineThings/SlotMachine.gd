extends Node2D

var wheels = []
var positions = []
var highlight_colors = [Color(1,0,0),Color(0,1,0),Color(0,0,1),Color(1,1,0),Color(1,0,1),Color(0,1,1),]
var lines_5x3 = [
	[0,0,0,0,0],
	[1,1,1,1,1],
	[2,2,2,2,2],
	[0,1,2,1,0],
	[2,1,0,1,2],
]

var balance = 100
var betting = 1
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
#	tiles.append(get_node("Tile1"))
#	tiles.append(get_node("Tile2"))
#	tiles.append(get_node("Tile3"))
#	tiles.append(get_node("Tile4"))
	
	display_bet()
	display_balance()
	pass # Replace with function body.
	

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	
	if playing:
		var finished = true
		for wheel in wheels:
			if wheel.spinning:	
				finished = false
		
		if finished:
			playing = false
			var won = determine_win()
			balance += won
			playing = false
			display_win(won)
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
			winnings += count
			won_on.append(symbol)
			info += symbol + ": " + str(count) + ", "
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
	var winnings = 0
	for l in range(play_lines):
		var line = lines_5x3[l]
		var symbol = endstate[0][line[0]]
		var hits = check_line(symbol, line, endstate)
		if hits >= 2:
			winnings += hits
			info += symbol + ": " + str(hits) + ", "
			highlight_line(line, hits, highlight_colors[l])
		
	display_info(info)
	return winnings

func check_line(symbol, line, endstate):
	'''
	Get number of hits on the line
	'''
	var length = 0
	for idx in range(len(line)):
		if endstate[idx][line[idx]] == symbol:
			length += 1
		else:
			break
	return length

func highlight_line(line, len, color):
	for i in range(len(line)):
		if i == len:
			break
		wheels[i].highlight(line[i]+1, color)
	pass

func display_balance():
	get_node("BalanceDisplayText").set_text("Balance: " + str(balance))
	pass

func display_win(value):
	get_node("WinDisplayText").set_text("WON: " + str(value))
	pass

func display_bet():
	get_node("BetDisplayText").set_text("Bet: " + str(betting))
	pass
	
func display_info(message):
	get_node("InfoDisplayText").set_text("Info: " + str(message))
	pass
