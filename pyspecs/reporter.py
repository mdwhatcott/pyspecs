# Several flavors (
#   DotConsoleReporter,
#   StoryConsoleReporter,
#   HtmlReporter,
#
#   JsonReporter,
#   GrowlReporter,
#   etc...,
# )
# 1. Receive executed step
# 2. Formulate representation of step and its parent spec for report (text, html, etc...)
# 3. Show overview/stats


from abc import abstractmethod


class Reporter(object):
    @abstractmethod
    def success(self, step):
        pass

    @abstractmethod
    def failure(self, step, exc_stuff):
        pass

    @abstractmethod
    def error(self, step, exc_stuff):
        pass


class DotReporter(Reporter):
    pass
