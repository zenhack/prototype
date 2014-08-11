from sterling.model import Model


class Test(Model):

    def __init__(self):
        super(Test, self).__init__()
        self.first = 'hello'
        self.last = 'goodbye'

    def do_it(self, o):
        print("Done!")

Test().run()
