import copy

from connect4 import Connect4


class AlphaBetaAgent:
    def __init__(self, x):
        self.my_token = x
        self.opponent_token = 'o' if x == 'x' else 'x'

    def decide(self, connect4):
        max_depth = 4
        best_score = float('-inf')
        best_move = None
        for move in connect4.possible_drops():
            new_board = copy.deepcopy(connect4)
            new_board.drop_token(move)
            score = self._alphabeta(new_board, max_depth, float('-inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def _alphabeta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.game_over:
            return self._score(board)

        if maximizing_player:
            max_score = float('-inf')
            for move in board.possible_drops():
                new_board = copy.deepcopy(board)
                new_board.drop_token(move)
                score = self._alphabeta(new_board, depth - 1, alpha, beta, False)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score
        else:
            min_score = float('inf')
            for move in board.possible_drops():
                new_board = copy.deepcopy(board)
                new_board.drop_token(move)
                score = self._alphabeta(new_board, depth - 1, alpha, beta, True)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score

    def _score(self, board):
        if board.wins == self.my_token:
            return 1
        elif board.wins == self.opponent_token:
            return -1
        else:
            return 0
