from sterling.model import Model
from sterling.app import run


class Hello(Model):

    def __init__(self):
        super(Hello, self).__init__()
        self.first = 'hello'
        self.last = 'goodbye'

    def do_it(self, o):
        print("Done!")

run(Hello())
