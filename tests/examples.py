from pyspecs import given, when, collect, then, after, spec, this
from pyspecs._steps import \
    GIVEN_STEP, WHEN_STEP, COLLECT_STEP, THEN_STEP, AFTER_STEP
from tests import raise_error


class fully_implemented_and_passing(spec):
    def __init__(self):
        self.executed_steps = []

    @given
    def some_scenario(self):
        self.executed_steps.append('given')

    @when
    def something_is_invoked(self):
        self.executed_steps.append('when')

    @collect
    def results(self):
        self.executed_steps.append('collect')

    @then
    def something_happens(self):
        self.executed_steps.append('then1')

    @then
    def something_is_calculated(self):
        self.executed_steps.append('then2')

    @after
    def cleanup(self):
        self.executed_steps.append('after')


class spec_with_failure(spec):
    @then
    def it_should_fail(self):
        print "Hello, World!"
        this(False).should.be(True)


class spec_with_assertion_error(spec):
    @then
    def it_should_raise_an_error(self):
        print "Hello, World!"
        raise KeyError('Missing key!')

    @then
    def it_should_run_other_assertions(self):
        self.other_assertion = True

    @after
    def cleanup(self):
        print AFTER_STEP,


class spec_with_error_before_assertions(spec):
    @given
    def an_exception_is_raised(self):
        print GIVEN_STEP
        raise_error(KeyError, 'Exception in "given"')

    @when
    def this_should_NOT_execute(self):
        print WHEN_STEP

    @collect
    def this_should_NOT_execute_either(self):
        print COLLECT_STEP

    @then
    def should_NOT_be_executed(self):
        print THEN_STEP

    @after
    def should_be_executed_to_clean_up(self):
        print AFTER_STEP

class spec_with_error_after_assertions(spec):
    @given
    def setup(self):
        print GIVEN_STEP

    @when
    def action(self):
        print WHEN_STEP

    @collect
    def result(self):
        print COLLECT_STEP

    @then
    def something(self):
        print THEN_STEP

    @then
    def something_else(self):
        print THEN_STEP

    @after
    def an_exception_is_raised(self):
        raise_error(KeyError, "Exception from 'after' step.")
        print AFTER_STEP


class spec_with_error_before_and_after_assertions(spec):
    @given
    def setup(self):
        print GIVEN_STEP

    @when
    def action(self):
        print WHEN_STEP

    @collect
    def result(self):
        print COLLECT_STEP
        raise_error(KeyError, "Exception from 'collect' step.")

    @then
    def something(self):
        print THEN_STEP

    @then
    def something_else(self):
        print THEN_STEP

    @after
    def an_exception_is_raised(self):
        print AFTER_STEP
        raise_error(ValueError, "Exception from 'after' step.")


class spec_without_assertions(spec):
    def __init__(self):
        self.executed = []

    @given
    def setup(self):
        self.executed.append(GIVEN_STEP)

    @when
    def action(self):
        self.executed.append(WHEN_STEP)

    @collect
    def result(self):
        self.executed.append(COLLECT_STEP)

    @after
    def cleanup(self):
        self.executed.append(AFTER_STEP)