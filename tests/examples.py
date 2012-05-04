from pyspecs.should import this
from pyspecs.spec import Spec
from pyspecs.steps import \
    then, collect, when, after, given, \
    WHEN_STEP, COLLECT_STEP, THEN_STEP, AFTER_STEP


class fully_implemented_and_passing(Spec):
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


class spec_with_failure(Spec):
    @then
    def it_should_fail(self):
        print "Hello, World!"
        this(False).should.be(True)


class spec_with_assertion_error(Spec):
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


class spec_with_error_before_assertions(Spec):
    @given
    def an_exception_is_raised(self):
        raise KeyError('Exception in "given"')

    @when
    def this_should_not_execute(self):
        print WHEN_STEP

    @collect
    def this_should_not_execute_either(self):
        print COLLECT_STEP

    @then
    def should_not_be_executed(self):
        print THEN_STEP

    @after
    def should_not_execute(self):
        print AFTER_STEP
