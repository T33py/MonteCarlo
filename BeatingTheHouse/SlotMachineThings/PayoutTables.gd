extends Node

# "7", "10", "J", "Q", "K", "A", "777", "B1", "B2", "T1", "T2", "S"
var linepays = {
	"7":  [0.1, 0.3, 0.5, 0.75, 1],
	"777":[0.5, 2.5,   5,  7.5, 10],
	"10": [0.1, 0.5,   1,  1.5, 2],
	"J" : [0.2,   1,   2,    3, 4],
	"Q" : [0.3, 1.5,   3,  4.5, 6],
	"K" : [0.4,   2,   4,    6, 8],
	"A" : [0.5, 2.5,   5,  7.5, 10],
	"T1": [0.6,   3,   6,    9, 12],
	"T2": [0.7, 3.5,   7, 10.5, 14],
	"B1": [  5,  10,  20,   50, 100],
	"B2": [  5,  10,  20,   50, 100],
	"S":  [  0,   0,   0,    0, 0],
}

var hitpays = {
	"7"  : 0.1,
	"777": 0.1,
	"10" : 0.2,
	"J"  : 0.4,
	"Q"  : 0.6,
	"K"  : 0.8,
	"A"  : 1,
	"T1" : 1.2,
	"T2" : 1.4,
	"B1" : 2,
	"B2" : 2,
	"S"  : 0,
}
