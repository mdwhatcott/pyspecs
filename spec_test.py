from spec import given, when, then, the


with given.two_operands:
    a = 2
    b = 3

    with when.supplied_to_the_add_function:
        result = a + b

        with then.the_sum_should_be_mathmatically_correct:
            the(result).should.equal(5)

    with when.supplied_to_the_subtract_function:
        result = a - b

        with then.the_difference_should_be_mathmatically_correct:
            the(result).should.equal(1)

    # cleanup is just based on scope
    del a, b, result
