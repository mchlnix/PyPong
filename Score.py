class Score:
    def __init__(self):
        self._score_left = 0
        self._score_right = 0

    def score_left(self):
        self._score_left += 1

    def score_right(self):
        self._score_right += 1

    def get_score(self):
        return "{}:{}".format(self._score_left, self._score_right)
