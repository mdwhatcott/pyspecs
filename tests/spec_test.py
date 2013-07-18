from pyspecs import given, when, then, and_, the, this


with given.two_operands:
    a = 2
    b = 3

    with when.supplied_to_the_add_function:
        total = a + b

        with then.the_total_should_be_mathmatically_correct:
            the(total).should.equal(5)

        with and_.the_total_should_be_greater_than_either_operand:
            the(total).should.be_greater_than(a)
            the(total).should.be_greater_than(b)

    with when.supplied_to_the_subtract_function:
        difference = b - a

        with then.the_difference_should_be_mathmatically_correct:
            the(difference).should.equal(1)

    # cleanup is just based on scope
    del a, b, total, difference


with given.an_error_prone_situation:
    with when.an_error_occurs:
        result = 1 / 0

        with then.the_result_will_not_be_available:
            the(dir()).should_NOT.contain('result')


with given.an_assertion_error:
    with when.the_assertion_error_occurs:
        with then.the_error_should_be_displayed:
            this(True).should.equal(False)


with when.there_are_several_asserts:
    with then.the_first_should_pass:
        this(True).should.equal(True)
    with then.the_second_should_fail:
        this(False).should.equal(True)
    with then.the_third_has_an_error:
        this(int('asdf')).should_NOT.be_an(int)