# Size
WINDOWN_WIDTH=960
WINDOWN_HEIGHT=720
CONTAINER_WIDTH = 860	#container is layer that contain content such as board, setting,..
CONTAINER_HEIGHT = 640
BOARD_HEIGHT=640
BOARD_WIDTH=640
SQUARE_SIZE=80
PEICES=64
ROW = 10	# Number row of board
COL = 9		# Number col or board
# Color
PRIMARY = (2, 117, 216)
SUCCESS = (92, 184, 92)
INFOR = (91, 192, 222)
DANGER = (217, 83, 79)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
PIECES=['bb', 'wb', 'bk', 'wk', 'bn', 'wn', 'bp', 'wp', 'bq', 'wq', 'br', 'wr']
'''
    first letter is color of piece
        'w' - white maximizing player
        'b' - black minimizing player
    second letter is type of piece
        'b' - bishop
        'k' - king
        'n' - knight
        'r' - rook
        'p' - pawn
        'q' - queen
'''
SQUARE_NAME = [['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'],
                ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'],
                ['a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6'],
                ['a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5'],
                ['a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4'],
                ['a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3'],
                ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2'],
                ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']]
SETTING_FILE = "confic\\setting.txt"