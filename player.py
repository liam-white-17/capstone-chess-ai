from abc import abstractmethod

class Player:
    """
    A superclass to represent the player of an actual chess game, whether human or AI
    """
    def init(self):
        pass
    @abstractmethod
    def get_move(self,board):
        pass