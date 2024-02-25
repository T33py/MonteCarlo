extends AnimatedSprite2D

var time = 0

var am_supposed_to_be = 0
var currently_am = 0

# variables for rotating to the next position on the wheel
var positions = []
var moving = false
var stop = false
var current_position = 0
var next_position = 0
var speed = 500


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

var frames = {
	"A": 0,
	"Q": 1,
}

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	time += delta
	if time >= 1:
		time = 0
		if frame == 0:
			am_supposed_to_be = 1
		else: 
			am_supposed_to_be = 0
	if currently_am != am_supposed_to_be:
		frame = am_supposed_to_be
		currently_am = am_supposed_to_be
	
	if moving:
		move_towards_next_position(delta)
	pass




func goto_next_position():
	'''
	Start the process of having this tile go to the next spot it belongs
	'''
#	print("Go to next position")
	stop = false
	
	# if we are hidden below the bottom row
	if current_position == len(positions) - 1:
		next_position = 0
		position = positions[next_position]
		current_position = 0
		moving = false
		pass
	
	# if we are anywhere else
	next_position = current_position + 1 
	moving = true
	pass
	
func move_towards_next_position(delta):
	if position.distance_to(positions[next_position]) > delta * speed:
		position = position.move_toward(positions[next_position], delta * speed)
	elif !stop:
		current_position = next_position
		goto_next_position()
		position = position.move_toward(positions[next_position], delta * speed)
	else:
		position = positions[next_position]
		current_position = next_position
		moving = false
	
	
	pass
