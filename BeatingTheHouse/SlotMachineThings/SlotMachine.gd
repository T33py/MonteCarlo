extends Node2D

var wheels = []
var positions = []

var playing = false
var games_played = 0

# Called when the node enters the scene tree for the first time.
func _ready():
	wheels.append(get_node("Wheel1"))
	wheels.append(get_node("Wheel2"))
	wheels.append(get_node("Wheel3"))
	wheels.append(get_node("Wheel4"))
	wheels.append(get_node("Wheel5"))
#	tiles.append(get_node("Tile1"))
#	tiles.append(get_node("Tile2"))
#	tiles.append(get_node("Tile3"))
#	tiles.append(get_node("Tile4"))
	
	
	pass # Replace with function body.

func play():
	games_played += 1
	print("Game" + str(games_played))
	for w in wheels:
		w.spin()
	
	playing = true
	pass
	

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
			display_win(determine_win(state))
	
	pass
	
func determine_win(endstate):
	print(endstate)
	if endstate[0][1] == endstate[1][1]:
		return 1
	
	return 0
	
func display_win(value):
	get_node("WinDisplayText").set_text("WON: " + str(value))
	pass
