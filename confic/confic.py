from confic.const import *
class Confic:
    _boardType = "BROWN"
    _pieceType = 'type1_'
    _backgroundType = "bg"

    @staticmethod
    def loadConfic():
        f = open(SETTING_FILE, "r")
        try:
            lines = f.readlines()
            Confic._boardType = lines[0].split("=")[1][0:-1]
            Confic._pieceType = lines[1].split("=")[1][0:-1]
            Confic._backgroundType = lines[2].split("=")[1][0:-1]
        finally:
            f.close()

    @staticmethod
    def saveBackground(style: str):
        if style == Confic._backgroundType:
            return False
        bg = Confic.getBackgrounds()
        if style in bg:
            Confic.saveConfic(background=style, board=Confic._boardType, piece=Confic._pieceType)
            Confic.loadConfic()

    @staticmethod
    def saveBoard(style: str):
        if style == Confic._boardType:
            return False
        boards = Confic.getBoards()
        if style in boards:
            Confic.saveConfic(background=Confic._backgroundType, board=style, piece=Confic._pieceType)
            Confic.loadConfic()

    @staticmethod
    def savePiece(style: str):
        if style == Confic._pieceType:
            return False
        pieces = Confic.getPieces()
        if style in pieces:
            Confic.saveConfic(background=Confic._backgroundType, board=Confic._boardType, piece=style)
            Confic.loadConfic()

    @staticmethod
    def saveConfic(background: str, board: str, piece: str):
        f = open(SETTING_FILE, "w")
        try:
            f.write("board-type=" + board)
            f.write("\n")
            f.write("piece-type=" + piece)
            f.write("\n")
            f.write("background-type=" + background)
            f.write("\n")
        finally:
            f.close()

    @staticmethod
    def getBoards():
        return ["brown", 'blue', 'dark', 'green', 'icy_sea', 'light', 'lolz', 'marble', "neon", "newspaper", "orange", "pink", "wook"]

    @staticmethod
    def getPieces():
        return ["3D", "classical", "condal", "tournament", "wood"]

    @staticmethod
    def getBackgrounds():
        return ["bg", "web2", "web3", "web4"]
