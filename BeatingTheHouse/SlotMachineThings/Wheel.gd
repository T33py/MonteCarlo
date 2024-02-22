extends Node2D


var tiles = []

# Called when the node enters the scene tree for the first time.
func _ready():
	tiles.append(get_node("Tile1"))
	tiles.append(get_node("Tile2"))
	tiles.append(get_node("Tile3"))
	tiles.append(get_node("Tile4"))
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	var mess_with = tiles[0] as AnimatedSprite2D
	mess_with.am_supposed_to_be = mess_with.frames["A"]
	pass
