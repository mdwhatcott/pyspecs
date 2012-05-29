pyspecs - Minimalistic BDD in Python.
=====================================

pyspecs is a testing framework that strives to achieve more readable
specifications (tests) by leveraging some fancy syntactic sugar (python
decorators) and auto-discovery of tests/specs.  Installation is straightforward:

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

### Output

<pre>
$ pyspecs

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