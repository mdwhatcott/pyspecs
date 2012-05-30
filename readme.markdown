
pyspecs - Minimalistic BDD in Python.
=====================================

pyspecs is a testing framework that strives to achieve more readable
specifications (tests) by leveraging some fancy syntactic sugar and
auto-discovery of tests/specs.  Installation is straightforward:

<pre>
    $ pip install pyspecs
</pre>

or...

<pre>
    $ easy_install pyspecs
</pre>

or...

<pre>
    $ git clone https://mdwhatcott@github.com/mdwhatcott/pyspecs.git
    $ cd pyspecs
    $ python setup.py
</pre>

## Writing specs

Specifications are identified by subclassing from the spec class.  From there
the idea is then to lay out the specification in steps (given-when-then). The
following steps are available to each subclass of spec as method decorators and
are executed in the order listed:

__given__ - The context for the specification, the initial setup phase.<br>
__when__ - This is where to invoke the action under test.<br>
__collect__ - Allows the aggregation of results for ease when making assertions.<br>
__then__ - This is where assertions are made (more details below) about the results arrived at in the when and collect steps.<br>
__after__ - Analogous to the tearDown method in unit-testing frameworks.<br>

## Assertions

The simplest assertion can be made by using the built-in assert statement:

<pre>
assert 42 == 'The answer the life, the universe and everything'
</pre>

For readability this project provides a more fluent method for making
assertions:

<pre>

# These imported names are all synonyms for the class that
# provides fluent assertions (Should). Use whichever provides
# the best readability.  The general patter is:
# >>> the([value]).should.[condition_method]([comparison_args])
#  or...
# >>> the([value]).should_NOT.[condition_method]([comparison_args]) # negated!

from pyspecs import the, this, that, it, then


this(42).should.equal(42) # this passes

this([1, 2, 3]).should.contain(2) # this also passes

the(list()).should.be_empty() # passes

it(1).should_NOT.be_greater_than(100) # passes

# raises AssertionError, caught by framework, logged as failure
that(200).should.be_less_than(0)

</pre>

## Example

<pre>

from pyspecs import spec, given, when, then, the


class simple_addition(spec):
    @given
    def two_numbers(self):
        self.first = 2
        self.second = 3

    @when
    def we_add_them(self):
        self.result = add(self.first, self.second)

    @then
    def the_sum_should_equal_5(self):
        the(self.result).should.equal(5)


def add(a, b):
    return a + b

</pre>


## Execution of specs

Beyond providing the python library which will be explained below, installation
provides two command-line scripts into the environment, meant to be invoked
from the root of your project.  Each will execute all specs in .py files
ending in 'spec.py' or 'specs.py'.

For one-time execution of specs:

<pre>
    $ pyspecs
</pre>

To begin an auto-test loop (runs all specs anytime a .py file is saved):

<pre>
    $ pyspecs_idle
</pre>

To increase verbosity (default is 'dot'):

<pre>
    $ pyspecs --verbosity=story
</pre>

or...

<pre>
    $ pyspecs_idle --verbosity=story
</pre>

### Output

<pre>
$ pyspecs --verbosity=story

------------------------------------ Specs ------------------------------------

"simple addition"
     given two numbers
     when we add them
     then the sum should equal 5

---------------------------------- Statistics ----------------------------------

1 specs
1 assertions passed

Duration: 0.081s

(ok)

</pre>
