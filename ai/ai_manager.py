import math
import copy

class AIManager:
    def __init__(self, game_manager, ai_player=2, max_depth=3):
        self.game_manager = game_manager
        self.ai_player = ai_player

        if self.game_manager.board_size >= 9:
            self.max_depth = 1
        elif self.game_manager.board_size >= 5:
            self.max_depth = 2
        else:
            self.max_depth = 3

    def best_move(self):
        best_score = -math.inf
        best_move = None

        for r in range(self.game_manager.board_size):
            for c in range(self.game_manager.board_size):
                if self.game_manager.board[r][c] == '':
                    for letter in ['O', 'S']:
                        sim_game = copy.deepcopy(self.game_manager)
                        sim_game.set_selected_letter(letter)
                        valid, points = sim_game.place_letter(r, c)
                        if not valid:
                            continue

                        score = self.minimax(sim_game, False, 1, -math.inf, math.inf)

                        if score > best_score:
                            best_score = score
                            best_move = (r, c, letter)
        return best_move

    def minimax(self, state, is_maximizing, depth, alpha, beta):
        if depth == self.max_depth or state.is_full():
            return self.evaluate(state)

        if is_maximizing:
            max_eval = -math.inf
            for r in range(state.board_size):
                for c in range(state.board_size):
                    if state.board[r][c] == '':
                        for letter in ['O', 'S']:
                            new_state = copy.deepcopy(state)
                            new_state.set_selected_letter(letter)
                            valid, points = new_state.place_letter(r, c)
                            if not valid:
                                continue
                            eval = self.minimax(new_state, False, depth + 1, alpha, beta)
                            max_eval = max(max_eval, eval)
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
            return max_eval
        else:
            min_eval = math.inf
            for r in range(state.board_size):
                for c in range(state.board_size):
                    if state.board[r][c] == '':
                        for letter in ['O', 'S']:
                            new_state = copy.deepcopy(state)
                            new_state.set_selected_letter(letter)
                            valid, points = new_state.place_letter(r, c)
                            if not valid:
                                continue
                            eval = self.minimax(new_state, True, depth + 1, alpha, beta)
                            min_eval = min(min_eval, eval)
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break
            return min_eval

    def evaluate(self, state):
        ai_points = state.players_points.get(self.ai_player, 0)
        human_player = 1 if self.ai_player == 2 else 2
        human_points = state.players_points.get(human_player, 0)
        return ai_points - human_points
