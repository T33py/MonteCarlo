extends Node2D

var wheels = []
var positions = []

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
			var state = []
			for wheel in wheels:
				state.append(wheel.get_result())
			var won = determine_win(state)
			balance += won
			display_win(won)
			display_balance()
	
	pass
	

func play():
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
func determine_win(endstate):
	print(endstate)
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
