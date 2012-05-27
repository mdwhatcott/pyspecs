# Thanks to Uncle Bob Martin for this canonical example:
# http://butunclebob.com/ArticleS.UncleBob.TheBowlingGameKata


from pyspecs import spec, given, when, collect, then, the


class using_a_bowling_game(object):
    @given
    def a_fresh_game(self):
        self.game = BowlingGame()

    @collect
    def result(self):
        self.score = self.game.score()

    def _roll_many(self, pins, times):
        for x in range(times):
            self.game.roll(pins)


class gutter_game(spec, using_a_bowling_game):
    @when
    def all_gutter_balls_are_thrown(self):
        self._roll_many(0, 20)

    @then
    def the_final_score_should_be_zero(self):
        the(self.score).should.equal(0)


class all_ones(spec, using_a_bowling_game):
    @when
    def all_throws_know_down_one_pin(self):
        self._roll_many(1, 20)

    @then
    def the_final_score_should_be_twenty(self):
        the(self.score).should.equal(20)


class spare(spec, using_a_bowling_game):
    @when
    def a_spare_is_thrown(self):
        self.game.roll(5)
        self.game.roll(5)
        self.game.roll(3)
        self._roll_many(0, 17)

    @then
    def the_final_score_should_be_16(self):
        the(self.score).should.equal(16)


class strike(spec, using_a_bowling_game):
    @when
    def a_strike_is_thrown(self):
        self.game.roll(10)
        self.game.roll(3)
        self.game.roll(4)
        self._roll_many(0, 16)

    @then
    def the_the_final_score_should_be_24(self):
        the(self.score).should.equal(24)


class perfect_game(spec, using_a_bowling_game):
    @when
    def all_throws_are_strikes(self):
        self._roll_many(10, 12)

    @then
    def the_final_score_should_be_300(self):
        the(self.score).should.equal(300)


class BowlingGame(object):
    def __init__(self):
        self._rolls = []

    def roll(self, pins):
        self._rolls.append(pins)

    def score(self):
        total = 0
        roll = 0
        for frame in range(10):
            if self._is_strike(roll):
                total += self._strike_bonus(roll)
                roll += 1
            elif self._is_spare(roll):
                total += self._spare_bonus(roll)
                roll += 2
            else:
                total += self._current_frame(roll)
                roll += 2
        return total

    def _is_spare(self, roll):
        return self._current_frame(roll) == 10

    def _current_frame(self, roll):
        return self._rolls[roll] + self._rolls[roll + 1]

    def _spare_bonus(self, roll):
        return 10 + self._rolls[roll + 2]

    def _is_strike(self, roll):
        return self._rolls[roll] == 10

    def _strike_bonus(self, roll):
        return 10 + self._rolls[roll + 1] + self._rolls[roll + 2]