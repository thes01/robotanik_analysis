

class User:
    def __init__(self, uid):
        self.games = []
        self.uid = uid

    def submitCount(self):
        count = 0
        for game in self.games:
            count += len(game.submits)

        return count


class Game:
    def __init__(self):
        self.submits = []

    def successful(self):
        return self.submits[-1].is_solution


# i.e. _L_FgRgRgF_1
class Sequence:
    def __init__(self, seqid, parse_str):
        self.moves = []
        self.id = seqid
        self.is_empty = parse_str == ''

        read_index = 0

        while read_index < len(parse_str):
            substr = parse_str[read_index:read_index + 2]
            self.moves.append(Move(substr))
            read_index += 2

    def deleteMoves(self, indexes: list):
        # remove higher indexes first so that the lower stay preserved
        for index in sorted(indexes, reverse=True):
            del self.moves[index]

    def equalsByMoves(self, sequence):
        if len(self.moves) != len(sequence.moves):
            return False
        
        for i in range(len(self.moves)):
            if not self.moves[i].equals(sequence.moves[i]):
                return False
        
        return True

    def __str__(self):
        ret = ""

        for move in self.moves:
            ret += move.__str__()
        
        return ret

    def __repr__(self):
        return __str__()


class Move:
    CONDITION_NONE = '_'
    CONDITION_BLUE = 'b'
    CONDITION_RED = 'r'
    CONDITION_GREEN = 'g'

    ACTION_FRONT = 'F'
    ACTION_RIGHT = 'R'
    ACTION_LEFT = 'L'

    def __init__(self, parse_str):
        self.condition = parse_str[0]
        self.action = parse_str[1]

    def isConditional(self):
        return self.condition != self.CONDITION_NONE

    def isLRF(self):
        return self.action in 'LRF'

    def equals(self, move):
        return self.action == move.action and self.condition == move.condition

    def __str__(self):
        return self.condition + self.action

    def __repr__(self):
        return self.__str__()

