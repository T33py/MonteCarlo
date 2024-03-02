extends Node2D

var tiles = []
var positions = []

var spin_time = 0
var max_spin_time = 2
var stop_delay = 0
var spinning = false
var stopping = false
var frames_between_check_if_stopped = 4
var frames_since_check_if_stopped = 10

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
	if spinning and !stopping and spin_time > max_spin_time:
			stop_spin(stop_delay)
	if stopping:
		if frames_since_check_if_stopped >= frames_between_check_if_stopped:
			var stopped = true
			for tile in tiles:
				if tile.moving:
					stopped = false
					break
			if stopped:
				spinning = false
				stopping = false
		frames_since_check_if_stopped += 1
	pass


func get_result():
	var outcome = []
	for i in range(len(tiles)):
		if i > 0 and i < len(tiles)-1:
			outcome.append(tiles[i].symbols[tiles[i].currently_am])
	return outcome

func spin(delay = 0):
	'''
	Start spinning the wheel.
	'''
#	print("Spin")
	for tile in tiles:
		tile.border.visible = false
		tile.spin(delay)
		
	spinning = true
	stopping = false
	spin_time = 0
	pass

func stop_spin(delay=0):
	'''
	Force the wheel to stop spinning
	'''
#	print("Stop Spin")
	for tile in tiles:
		tile.stop_spinning(delay)

	stopping = true
	spin_time = max_spin_time +1
#	spinning = false
	pass
		
		
func highlight(tile, color):
	var t = tiles[tile]
	t.border.modulate = color
	t.border.visible = true
	pass
