extends AnimatedSprite2D

var time = 0

var am_supposed_to_be = 0
var currently_am = 0

# variables for rotating on the wheel
var my_home = 0
var positions = []
var moving = false
var stop = false
var current_position = 0
var next_position = 0
var speed = 750
var wait_to_move = 0
var wait_to_stop = 0

var symbols = ["10", "J", "Q", "K", "A"]
var frames = {
	"10": 0,
	"J": 1,
	"Q": 2,
	"K": 3,
	"A": 4,
}

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.



# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if currently_am != am_supposed_to_be:
		frame = am_supposed_to_be
		currently_am = am_supposed_to_be
	
	# if we are waiting for something
	if wait_to_stop > 0:
		wait_to_stop -= delta
		if wait_to_stop <= 0:
			stop = true
	if wait_to_move > 0:
		wait_to_move -= delta
		if wait_to_move <= 0:
			moving = true
			
	# I LIKE TO MOVE IT
	if moving:
		move_towards_next_position(delta)
	
	pass




func goto_next_position():
	'''
	Start the process of having this tile go to the next spot it belongs
	'''
#	print("Go to next position")
	
	# if we are hidden below the bottom row
	if current_position == len(positions) - 1:
		next_position = 0
		position = positions[next_position]
		current_position = 0
		choose_random_symbol()
		wait_to_move = positions[current_position].distance_to(positions[1]) / speed
		moving = false
	
	# if we are anywhere else
	else:
		next_position = current_position + 1 
		moving = true
#	print("Moved {my_home} {should_stop}".format({"my_home": my_home, "should_stop": stop}))
#	if my_home == 0:
#		print("{my_home} -> {next_position}".format({"my_home": my_home, "next_position": next_position}))
	pass
	
func move_towards_next_position(delta):
	'''
	Manages moving this tile to the next position for the rotation.
	When "stop_spinning" is called this will stop the tile once it reaches its home position.
	'''
	
	# if we are moving without any concern
	if position.distance_to(positions[next_position]) > delta * speed:
		position = position.move_toward(positions[next_position], delta * speed)
	# if we are moving but should stop when we are home
	elif !stop or (stop and next_position != my_home):
		current_position = next_position
		goto_next_position()
		position = position.move_toward(positions[next_position], delta * speed)
	# when we want to stop moving
	else:
		position = positions[my_home]
		current_position = my_home
		next_position = my_home
		moving = false
		stop = false
		wait_to_move = 0
	
	pass

func spin(delay=0):
	stop = false
	goto_next_position()
	if delay > 0:
		wait_to_move += delay
		moving = false
	pass

func stop_spinning(delay=0):
#	stop = true
#	print("STOP {my_home} {should_stop}".format({"my_home": my_home, "should_stop": stop}))
	if delay > 0:
		wait_to_stop = delay
	else:
		stop = true
		
	pass
	
func choose_random_symbol():
	am_supposed_to_be = frames[symbols.pick_random()]
	pass
	
