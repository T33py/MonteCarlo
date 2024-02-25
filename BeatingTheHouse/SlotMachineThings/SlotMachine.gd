extends Node2D

var wheels = []
var positions = []

# Called when the node enters the scene tree for the first time.
func _ready():
	wheels.append(get_node("Wheel1"))
#	tiles.append(get_node("Tile1"))
#	tiles.append(get_node("Tile2"))
#	tiles.append(get_node("Tile3"))
#	tiles.append(get_node("Tile4"))
	
	
	pass # Replace with function body.

func play():
#	print("Play")
	for w in wheels:
		w.spin()
	pass
	

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
