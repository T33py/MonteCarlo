extends AnimatedSprite2D

var time = 0

var am_supposed_to_be = 0
var currently_am = 0

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
			print("Q")
			am_supposed_to_be = 1
		else: 
			print("A")
			am_supposed_to_be = 0
	if currently_am != am_supposed_to_be:
		frame = am_supposed_to_be
		currently_am = am_supposed_to_be
	pass


