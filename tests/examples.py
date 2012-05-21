from pyspecs import given, when, collect, then, after, spec, this


class fully_implemented_and_passing(spec):
    def __init__(self):
        pass

    @given
    def some_scenario(self):
        pass

    @when
    def something_is_invoked(self):
        pass

    @collect
    def results(self):
        pass

    @then
    def something_happens(self):
        pass

    @then
    def something_is_calculated(self):
        pass

    @after
    def cleanup(self):
        pass


class spec_with_failure(spec):
    @then
    def it_should_fail(self):
        this(False).should.be(True)

    @then
    def it_should_run_other_assertions(self):
        this(True).should.be(True)


class spec_with_assertion_error(spec):
    @then
    def it_should_raise_an_error(self):
        raise KeyError

    @then
    def it_should_run_other_assertions(self):
        pass

    @after
    def cleanup(self):
        pass


class spec_with_error_before_assertions(spec):
    @given
    def an_exception_is_raised(self):
        raise KeyError

    @when
    def this_should_NOT_execute(self):
        pass

    @collect
    def this_should_NOT_execute_either(self):
        pass

    @then
    def should_NOT_be_executed(self):
        pass

    @after
    def should_be_executed_to_clean_up(self):
        pass


class spec_with_error_before_assertions_without_cleanup(spec):
    @when
    def an_exception_is_raised(self):
        raise KeyError

    @then
    def this_should_NOT_execute(self):
        pass



class spec_with_error_after_assertions(spec):
    @given
    def setup(self):
        pass

    @when
    def action(self):
        pass

    @collect
    def result(self):
        pass

    @then
    def something(self):
        pass

    @then
    def something_else(self):
        pass

    @after
    def an_exception_is_raised(self):
        raise KeyError


class spec_with_error_before_and_after_assertions(spec):
    @given
    def setup(self):
        pass

    @when
    def action(self):
        pass

    @collect
    def result(self):
        raise KeyError

    @then
    def something(self):
        pass

    @then
    def something_else(self):
        pass

    @after
    def an_exception_is_raised(self):
        raise ValueError


class spec_without_assertions(spec):
    @given
    def setup(self):
        pass

    @when
    def action(self):
        pass

    @collect
    def result(self):
        pass

    @after
    def cleanup(self):
        pass


class spec_that_fails_initialization(spec):
    def __init__(self):
        raise ValueError