# coding=utf-8


"""
An example of the alternative syntax, using strings instead of properties.

This example solves the FizzBuzz problem:

  Given a number, it will returns:
    - "Fizz" if is divisible by 3.
    - "Buzz" if it is divisible by 5.
    - "FizzBuzz" if it is divisible by 3 and 5.
    - The number otherwise.

This file is divided into 3 segments:

1. Sample output of the pyspecs framework when executing this module.
2. Production code (the system under test).
3. The test code that relies on and is run by the pyspecs framework to verify
   that the Production Code is correct.

########### 1. Sample Output ###########
"""


########## Production Code ###########


def fizzbuzz(n):
    def is_divisible_by(d):
        return n % d == 0
    result = ''
    if is_divisible_by(3):
        result += 'Fizz'
    if is_divisible_by(5):
        result += 'Buzz'
    return n if result == '' else result

############## Test Code ###############

from pyspecs import given, when, then, the, finish


with given('the number 2, which is not divisible by 3 nor 5'):
    number = 2

    with when('the function is called'):
        result = fizzbuzz(number)

    with then('the result is the same number'):
        the(result).should.equal(number)


with given('the number 3, which is divisible by 3 but not by 5'):
    number = 3

    with when('the function is called'):
        result = fizzbuzz(number)

    with then('the result is the same number'):
        the(result).should.equal('Fizz')


with given('the number 5, which is divisible by 5 but not by 3'):
    number = 5

    with when('the function is called'):
        result = fizzbuzz(number)

    with then('the result is the same number'):
        the(result).should.equal('Buzz')


with given('the number 15, which is divisible by 3 and 5'):
    number = 15

    with when('the function is called'):
        result = fizzbuzz(number)

    with then('the result is the same number'):
        the(result).should.equal('FizzBuzz')


if __name__ == '__main__':
    import sys
    limit = sys.argv[1] if len(sys.argv) > 0 else 10
    for n in range(limit):
        print fizzbuzz(limit+1)
