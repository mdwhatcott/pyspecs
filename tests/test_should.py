from unittest.case import TestCase, skip
from mock import Mock
from pyspecs._should import _Should as this
from pyspecs._should import should_expectation
from pyspecs._should import PREPARATION_ERROR
from pyspecs._step import Step, StepFactory


class TestStepAssertions(TestCase):
    def setUp(self):
        registry = Mock()

    def test_passing_when_equal(self):
        this('foo').should.equal('foo')

    def test_failing_when_not_equal(self):
        with self.assertRaises(AssertionError):
            this('foo').should.equal('bar')

    def test_NOT_inverts_assertion_logic(self):
        this('foo').should_not.equal('bar')

    def test_NOT_embellishes_syntax_error(self):
        with self.assertRaises(AssertionError) as e:
            this('foo').equal('foo')
        self.assertEquals(PREPARATION_ERROR, str(e.exception))

    def test_NOT_embellishes_error_message_on_failure_accordingly(self):
        with self.assertRaises(AssertionError) as e:
            this('foo').should_not.equal('foo')

        self.assertEquals("Expected 'foo' NOT to equal 'foo'.", str(e.exception))

    def test_passing_should_be_a(self):
        this('foo').should.be_a(str)


    def test_failing_should_be_a(self):
        with self.assertRaises(AssertionError) as e:
            this('foo').should.be_a(list)

    def test_passing_should_contain(self):
        this('foo').should.contain('o')


    def test_failing_should_contain(self):
        with self.assertRaises(AssertionError) as e:
            this('foo').should.contain('x')

    def test_passing_should_be_in(self):
        this('f').should.be_in('foo')

    def test_failing_should_be_in(self):
        with self.assertRaises(AssertionError) as e:
            this('x').should.be_in('foo')

    def test_passing_should_be_greater_than(self):
        this(1).should.be_greater_than(0)

    def test_failing_should_be_greater_than(self):
        with self.assertRaises(AssertionError) as e:
            this(0).should.be_greater_than(1)

    def test_passing_should_be_less_than(self):
        this(0).should.be_less_than(1)

    def test_failing_should_be_less_than(self):
        with self.assertRaises(AssertionError) as e:
            this(1).should.be_less_than(0)

    def test_passing_should_be_greater_than_or_equal_to(self):
        this(0).should.be_greater_than_or_equal_to(0)
        this(1).should.be_greater_than_or_equal_to(0)

    def test_failing_should_be_greater_than_or_equal_to(self):
        with self.assertRaises(AssertionError) as e:
            this(0).should.be_greater_than_or_equal_to(1)

    def test_passing_should_be_less_than_or_equal_to(self):
        this(0).should.be_less_than_or_equal_to(0)
        this(-1).should.be_less_than_or_equal_to(0)

    def test_failing_should_be_less_than_or_equal_to(self):
        with self.assertRaises(AssertionError) as e:
            this(0).should.be_less_than_or_equal_to(-1)

    def test_passing_should_be(self):
        this(True).should.be(True)

    def test_failing_should_be(self):
        with self.assertRaises(AssertionError) as e:
            this(True).should.be(False)

    def test_passing_be_between(self):
        this(2).should.be_between(1, 3)

    def test_failing_be_between(self):
        with self.assertRaises(AssertionError) as e:
            this(1).should.be_between(2, 3)

    def test_raises_with_unspecified_message(self):
        def raise_():
            raise KeyError()

        this(raise_).should.raise_a(KeyError)
        this(raise_).should.raise_an(KeyError)

    def test_raises_no_error(self):
        def no_error():
            pass

        with self.assertRaises(AssertionError):
            this(no_error).should.raise_a(Exception)
        with self.assertRaises(AssertionError):
            this(no_error).should.raise_an(Exception)

    def test_raises_with_incorrect_error_message(self):
        def raise_():
            raise KeyError("Specific Error Message")

        with self.assertRaises(AssertionError):
            this(raise_).should.raise_a(KeyError, "Wrong Error Message")
        with self.assertRaises(AssertionError):
            this(raise_).should.raise_an(KeyError, "Wrong Error Message")

    def test_raises_with_correct_error_message(self):
        def raise_():
            raise KeyError("Message 123")

        this(raise_).should.raise_a(KeyError, "Message 123")
        this(raise_).should.raise_an(KeyError, "Message 123")

    def test_raises_incorrect_exception(self):
        def raise_():
            raise KeyError()

        with self.assertRaises(AssertionError):
            this(raise_).should.raise_a(IndexError)
        with self.assertRaises(AssertionError):
            this(raise_).should.raise_an(IndexError)

    def test_decorate_with_custom_assertion(self):
        def be_5(this):
            this._assert(
                action=lambda: this._value == 5,
                report=lambda: "'{0}' should equal '5'.".format(this._value)
            )
        should_expectation(be_5)

        this(5).should.be_5()
        with self.assertRaises(AssertionError):
            this(4).should.be_5()

    def test_passing_empty(self):
        this(list()).should.be_empty()
        this(str()).should.be_empty()
        this(dict()).should.be_empty()
        this(tuple()).should.be_empty()
        this(set()).should.be_empty()

    def test_failing_empty(self):
        with self.assertRaises(AssertionError):
            this('asdf').should.be_empty()


