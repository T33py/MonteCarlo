extends AnimatedSprite2D

var time = 0
var rand = RandomNumberGenerator.new()

# variables for display
var border
var am_supposed_to_be = 0
var currently_am = "7"
var current_frame = 8
var in_lines = []
var current_line_idx = 0
var line_border_timer = 0
var line_border_show_time = 1

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

# Name your symbols anything but "" its the no symbol selected value
var symbols = ["7", "10", "J", "Q", "K", "A", "777", "B1", "B2", "T1", "T2", "S"]
var odds =    [100,  100, 100, 100, 100, 100,   100,  50,     0,  100,  100,   0]
var sum_of_odds = 0

var frames = {
	"7": 8,
	"10": 0,
	"J": 1,
	"Q": 2,
	"K": 3,
	"A": 4,
	"777": 9,
	"B1": 5,
	"B2": 10,
	"T1": 6,
	"T2": 7,
	"S": 11,
}

# Called when the node enters the scene tree for the first time.
func _ready():
	border = get_node("TileBorder")
	line_border_timer = line_border_show_time
	sum_of_odds = sum(odds)
	pass # Replace with function body.



# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if current_frame != am_supposed_to_be:
		frame = am_supposed_to_be
		current_frame = am_supposed_to_be
	
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
	
	
	# show the border of lines we are currently in
	if line_border_timer > -1:
		line_border_timer -= delta
	if len(in_lines) > 0 and line_border_timer <= 0:
		line_border_timer = line_border_show_time
		border.modulate = in_lines[current_line_idx]
		border.visible = true
		current_line_idx = (current_line_idx + 1) % len(in_lines)
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
		choose_symbol()
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
	in_lines.clear()
	current_line_idx = 0
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

func in_line(color:Color):
	in_lines.append(color)
	pass

func choose_symbol():
	'''
	Choose which symbol to display in this sqare
	'''
	var num = rand.randi_range(0, sum_of_odds)
	var choise = ""
	for i in range(len(odds)):
		num -= odds[i]
		if num <= 0 and odds[i] != 0:
			choise = symbols[i]
			break
	
	if choise == "":
		choise = symbols[len(symbols)-1]
	
	currently_am = choise
	am_supposed_to_be = frames[currently_am]
	pass
	

func change_odds(symbol, change):
	'''
	Change the odds of the provided symbol for this wheel
	'''
	var i = symbols.find(symbol)
	odds[i] += change
	sum_of_odds += change
	print("Odss of " + symbol + " -> " + str(odds[i]))
	pass

func sum(list):
	var s = 0
	for n in list:
		s += n
	return s
