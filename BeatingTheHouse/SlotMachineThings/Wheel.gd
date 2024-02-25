extends Node2D

var tiles = []
var positions = []

var spin_time = 0
var max_spin_time = 2
var spinning = false

# Called when the node enters the scene tree for the first time.
func _ready():
	tiles.append(get_node("Tile0"))
	tiles.append(get_node("Tile1"))
	tiles.append(get_node("Tile2"))
	tiles.append(get_node("Tile3"))
	tiles.append(get_node("Tile4"))
	
	var i = 0
	for t in tiles:
		var tile = t as AnimatedSprite2D
		positions.append(tile.position)
		t.positions = positions
		t.current_position = i
		t.my_home = i
		i += 1
		
	
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
#	var mess_with = tiles[0] as AnimatedSprite2D
#	mess_with.am_supposed_to_be = mess_with.frames["A"]
	
	if spinning:
		spin_time += delta
		if spin_time > max_spin_time:
			stop_spin()
	pass


func spin():
	'''
	Start spinning the wheel.
	'''
#	print("Spin")
	for tile in tiles:
		tile.goto_next_position()
		
	spinning = true
	spin_time = 0
	pass

func stop_spin():
	'''
	Force the wheel to stop spinning
	'''
#	print("Stop Spin")
	for tile in tiles:
		tile.stop_spinning()

	spinning = false
	pass
		
