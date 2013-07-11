from spec import given, when, then, and_, the


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
        difference = a - b

        with then.the_difference_should_be_mathmatically_correct:
            the(difference).should.equal(1)

    # cleanup is just based on scope
    del a, b, total, difference


output = """
 |   given two operands
 |-   when supplied to the add function
 |--  then the sum should be mathematically correct
 |--   and the sum should be greater than either operand
 |-   when supplied to the subtract function
 |--  then the difference should be mathematically correct
 |
 |   given something else
 |-   when asdfasdf



given two operands
 when  supplied to the add function
 then   the sum should be mathematically correct
  and   the sum should be greater than either operand
 when  supplied to the subtract function
 then   the difference should be mathematically correct

"""
