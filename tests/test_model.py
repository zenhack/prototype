import unittest
from sterling.model import Model


class TestModel(unittest.TestCase):
    """Test that subscribers are called/not called as appropriate."""

    def setUp(self):
        # We get a new model for each test function, and reset the number of
        # times `set_called` has been called.
        self.model = Model()
        self.called = 0

    def test_01_changed_called(self):
        """If the subscriber's attr has changed, do_updates should call it."""
        self.model.subscribe('foo', self.set_called)
        self.model.foo = 1
        self.model.do_updates()
        assert self.called == 1

    def test_02_notchanged_notcalled(self):
        """If the subscriber's attr hasn't changed,
        do_updates shouldn't call it."""
        self.model.subscribe('foo', self.set_called)
        self.model.do_updates()
        assert self.called == 0

    def test_03_diffchanged_notcalled(self):
        """If an attr other than the subscriber's is changed,
        do_updates shouldn't call it."""
        self.model.subscribe('foo', self.set_called)
        self.model.bar = 1
        self.model.do_updates()
        assert self.called == 0

    def test_04_multi_subscriber_called(self):
        """If there are multiple subscribers to an attribute, they should both
        be called."""
        self.model.subscribe('foo', self.set_called)
        self.model.subscribe('foo', self.set_called)
        self.model.foo = 1
        self.model.do_updates()
        assert self.called == 2

    def set_called(self, model):
        """Increment self.called.

        The indended use of this is to detect if a subscriber is being called.
        A test function can register this as a subscriber, call do_udpates,
        and examine self.called to determine how many times the subscriber
        has been called.
        """
        self.called += 1
