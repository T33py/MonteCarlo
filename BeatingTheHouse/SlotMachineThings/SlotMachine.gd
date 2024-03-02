extends Node2D

var wheels = []
var positions = []
var highlight_colors = [Color(1,0,0),Color(0,1,0),Color(0,0,1),Color(1,1,0),Color(1,0,1),Color(0,1,1),]

var balance = 100
var betting = 1
var playing = false
var games_played = 0
var wheel_start_stop_delay = 0.15

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
		pass
	
	games_played += 1
	print("Game" + str(games_played))
	balance -= betting
	display_balance()
	
	var delay = 0
	for w in wheels:
		w.spin(delay)
		delay += wheel_start_stop_delay
	
	playing = true
	pass
	
func determine_win():
	var endstate = []
	for wheel in wheels:
		endstate.append(wheel.get_result())
	print(endstate)
	
	return determine_win_by_hits(endstate)

func determine_win_by_hits(endstate):
	'''
	If we have enough symbols the win is based on the total number shown than the lenght and number of lines
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
	if endstate[0][1] == endstate[1][1]:
		return 1
	return 0
	

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
