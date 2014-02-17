pyspecs - Minimalistic BDD in Python
====================================

https://travis-ci.org/mdwhatcott/pyspecs.png

pyspecs is a testing framework that strives to achieve more readable
specifications (tests) by leveraging some fancy syntactic sugar and
auto-discovery of tests/specs.  WARNING: version 2.0 introduces breaking
changes if you've been using 1.0 or 1.1.

Installation is straightforward:

    $ pip install pyspecs

or...

    $ easy_install pyspecs

or...

    $ git clone https://mdwhatcott@github.com/mdwhatcott/pyspecs.git
    $ cd pyspecs
    $ python setup.py


## Assertions

The main tool for verifying behavior is an assertion of some kind. The
simplest assertion can be made by using the built-in assert statement:

    assert 42 == 'The answer the life, the universe and everything'

For readability this project provides a more fluent method for making
assertions:


	# These imported names are all synonyms for the class that
	# provides fluent assertions (Should). Use whichever provides
	# the best readability.  The general patter is:
	# >>> the([value]).should.[condition_method]([comparison_args])
	#  or...
	# >>> the([value]).should_NOT.[condition_method]([comparison_args]) # negated!

	from pyspecs import the, this, that, it


	this(42).should.equal(42) # this passes

	this([1, 2, 3]).should.contain(2) # this also passes

	the(list()).should.be_empty() # passes

	it(1).should_NOT.be_greater_than(100) # passes

	# raises AssertionError, caught by framework, logged as failure
	that(200).should.be_less_than(0)



## Writing complete specs

    from pyspecs import given, when, then, and_, the


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


Notice that the names of each step are supplied as dynamic attributes of the
`given`, `when`, `then`, and `and_` step keywords. These user-created attributes
are used in the output (below).  Here is a listing of words that can be
used as steps:

- `given`
- `provided`
- `when`
- `then`
- `and_`
- `so`
- `therefore`
- `however`
- `as_well_as`

These steps can be arranged in any order and hierarchy for compose a
specification (spec).  You can even create your own steps that suit your needs 
(see the source code for how that's done).


## Execution of specs

Beyond providing the python library which will be explained below, installation
provides a command-line script into the environment, meant to be invoked
from the root of your project.  The script will execute all specs in .py files
ending in 'test.py' or 'tests.py' or beginning with 'test'.

To begin an auto-test loop (runs all specs anytime a .py file is saved):


    $ run_pyspecs.py


To run all tests once:

    $ pyspecs_.py  # note the trailing underscore

### Complete Example

There's a complete example of specs, code, and output in the
[examples folder](https://github.com/mdwhatcott/pyspecs/tree/master/examples).
