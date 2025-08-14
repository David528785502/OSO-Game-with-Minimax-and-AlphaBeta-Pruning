class GameManager:
    def __init__(self, board_size=5):
        self.board_size = board_size
        self.board = [['' for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = 1
        self.players_points = {1: 0, 2: 0}
        self.selected_letter = 'S'

    def get_board(self):
        return self.board

    def set_selected_letter(self, letter):
        self.selected_letter = letter

    def get_selected_letter(self):
        return self.selected_letter

    def place_letter(self, row, col):
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False, 0
        if self.board[row][col] != '':
            return False, 0

        self.board[row][col] = self.selected_letter
        puntos = self.count_oso_points(row, col)
        self.players_points[self.current_player] += puntos

        if puntos == 0:
            self.current_player = 2 if self.current_player == 1 else 1
        return True, puntos

    def count_oso_points(self, row, col):
        total_points = 0
        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]
        for dr, dc in directions:
            for start in range(-2, 1):
                r0 = row + start * dr
                c0 = col + start * dc
                r1 = r0 + dr
                c1 = c0 + dc
                r2 = r0 + 2 * dr
                c2 = c0 + 2 * dc
                if all(0 <= x < self.board_size for x in (r0, r1, r2)) and all(0 <= y < self.board_size for y in (c0, c1, c2)):
                    seq = [self.board[r0][c0], self.board[r1][c1], self.board[r2][c2]]
                    if seq == ['O', 'S', 'O']:
                        total_points += 1
        return total_points

    def is_full(self):
        return all(cell != '' for row in self.board for cell in row)

    def get_winner(self):
        p1 = self.players_points[1]
        p2 = self.players_points[2]
        if p1 > p2:
            return 1
        elif p2 > p1:
            return 2
        else:
            return 0

    def get_current_player(self):
        return self.current_player

    def get_player_points(self, player):
        return self.players_points.get(player, 0)