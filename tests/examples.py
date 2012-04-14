from pyspecs.should import this
from pyspecs.spec import Spec
from pyspecs.steps import then, collect, when, after, given


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
    this(False).should.be(True)