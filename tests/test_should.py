from unittest.case import TestCase
from pyspecs.should import this, expectation, ShouldError, PREPARATION_ERROR


class TestShouldAssertions(TestCase):
  def setUp(self):
    self.lower = 'string'
    self.upper = 'STRING'

  def test_asserting_before_proper_method_chaining_raises_error(self):
    self._fails(lambda: this(self.lower).equal(self.lower),
      PREPARATION_ERROR
    )

  def test_passing_should_equal(self):
    self._passes(lambda: this(self.lower).should.equal(self.lower))

  def test_failing_should_equal(self):
    self._fails(lambda: this(self.lower).should.equal(self.upper),
      "Expected 'string' to equal 'STRING'."
    )

  def test_NOT_inverts_assertion_logic(self):
    self._passes(lambda: this(self.lower).should_NOT.equal(self.upper))

  def test_NOT_embellishes_error_message_on_failure_accordingly(self):
    self._fails(lambda: this(self.lower).should_NOT.equal(self.lower),
      "Expected 'string' NOT to equal 'string'."
    )

  def test_passing_should_be_a(self):
    self._passes(lambda: this(self.lower).should.be_a(type(str())))

  def test_failing_should_be_a(self):
    self._fails(lambda: this(self.lower).should.be_a(type(list())),
      "Expected 'string' to be a <type 'list'> (was a <type 'str'>)."
    )

  def test_passing_should_contain(self):
    self._passes(lambda: this(self.lower).should.contain(self.lower[0]))

  def test_failing_should_contain(self):
    self._fails(lambda: this(self.lower).should.contain('x'),
      "Expected 'string' to contain 'x'."
    )

  def test_passing_should_be_in(self):
    self._passes(lambda: this(self.lower[0]).should.be_in(self.lower))

  def test_failing_should_be_in(self):
    self._fails(lambda: this('x').should.be_in(self.lower),
      "Expected 'x' to be in 'string'."
    )

  def test_passing_should_be_greater_than(self):
    self._passes(lambda: this(1).should.be_greater_than(0))

  def test_failing_should_be_greater_than(self):
    self._fails(lambda: this(0).should.be_greater_than(1),
      "Expected '0' to be greater than '1'."
    )

  def test_passing_should_be_less_than(self):
    self._passes(lambda: this(0).should.be_less_than(1))

  def test_failing_should_be_less_than(self):
    self._fails(lambda: this(1).should.be_less_than(0),
      "Expected '1' to be less than '0'."
    )

  def test_passing_should_be_greater_than_or_equal_to(self):
    self._passes(lambda: this(0).should.be_greater_than_or_equal_to(0))
    self._passes(lambda: this(1).should.be_greater_than_or_equal_to(0))

  def test_failing_should_be_greater_than_or_equal_to(self):
    self._fails(lambda: this(0).should.be_greater_than_or_equal_to(1),
      "Expected '0' to be greater than or equal to '1'."
    )

  def test_passing_should_be_less_than_or_equal_to(self):
    self._passes(lambda: this(0).should.be_less_than_or_equal_to(0))
    self._passes(lambda: this(-1).should.be_less_than_or_equal_to(0))

  def test_failing_should_be_less_than_or_equal_to(self):
    self._fails(lambda: this(0).should.be_less_than_or_equal_to(-1),
      "Expected '0' to be less than or equal to '-1'."
    )

  def test_passing_should_be(self):
    self._passes(lambda: this(True).should.be(True))

  def test_failing_should_be(self):
    self._fails(lambda: this(True).should.be(False),
      "Expected 'True' to be 'False'."
    )

  def test_passing_be_between(self):
    self._passes(lambda: this(2).should.be_between(1, 3))

  def test_failing_be_between(self):
    self._fails(lambda: this(1).should.be_between(2, 3),
      "Expected '1' to be between '2' and '3'."
    )

  def test_raises_with_unspecified_message(self):
    def raise_():
      raise KeyError()

    self._passes(lambda: this(raise_).should.raise_a(KeyError))
    self._passes(lambda: this(raise_).should.raise_an(KeyError))

  def test_raises_no_error(self):
    def no_error():
        pass

    self._fails(lambda: this(no_error).should.raise_a(Exception),
      "'no_error' executed successfully but should have raised 'Exception'!"
    )
    self._fails(lambda: this(no_error).should.raise_an(Exception),
      "'no_error' executed successfully but should have raised 'Exception'!"
    )

  def test_raises_with_incorrect_error_message(self):
    def raise_():
      raise KeyError("Specific Error Message")

    self._fails(lambda:
      this(raise_).should.raise_a(KeyError, "Wrong Error Message"),
        "Raised 'KeyError' as expected but with an incorrect error message:\n" +
        "Expected: 'Wrong Error Message'\n" +
        "Received: 'Specific Error Message'"
    )
    self._fails(lambda:
      this(raise_).should.raise_an(KeyError, "Wrong Error Message"),
        "Raised 'KeyError' as expected but with an incorrect error message:\n" +
        "Expected: 'Wrong Error Message'\n" +
        "Received: 'Specific Error Message'"
    )

  def test_raises_with_correct_error_message(self):
    def raise_():
      raise KeyError("Message 123")

    self._passes(lambda: this(raise_).should.raise_a(KeyError, "Message 123"))
    self._passes(lambda: this(raise_).should.raise_an(KeyError, "Message 123"))

  def test_raises_incorrect_exception(self):
    def raise_():
      raise KeyError()

    self._fails(lambda: this(raise_).should.raise_a(IndexError),
      "Should have raised 'IndexError' but raised 'KeyError' instead.")
    self._fails(lambda: this(raise_).should.raise_an(IndexError),
      "Should have raised 'IndexError' but raised 'KeyError' instead.")

  def test_decorate_with_custom_assertion(self):
    def be_5(this):
      this._assert(
        action=lambda: this._value == 5,
        report=lambda: "'{0}' should equal '5'.".format(this._value)
      )
    expectation(be_5)
    self._passes(lambda: this(5).should.be_5())
    self._fails(lambda: this(4).should.be_5(), "'4' should equal '5'.")

  def test_passing_empty(self):
    self._passes(lambda: this(list()).should.be_empty())
    self._passes(lambda: this(str()).should.be_empty())
    self._passes(lambda: this(dict()).should.be_empty())
    self._passes(lambda: this(tuple()).should.be_empty())
    self._passes(lambda: this(set()).should.be_empty())

  def test_failing_empty(self):
    self._fails(lambda: this('asdf').should.be_empty(),
      "Expected 'asdf' to be empty."
    )

  def _passes(self, action):
    try:
      action()
    except AssertionError:
      raise AssertionError('This test should have passed!')

  def _fails(self, action, report):
    try:
      action()
    except ShouldError as error:
      assert error.message == report,\
        'Assertion failed as expected but gave the wrong error message!' + \
        '\nExpected: "{0}"'.format(report) + \
        '\nReceived: "{0}"'.format(error.message)
    else:
      raise AssertionError('This should have failed ' +
        'with this error message: {0}'.format(report))