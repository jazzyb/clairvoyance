import unittest
from clairvoyance.memoization import memoize, MemoizationError

class FooBar(object):
    def __init__(self, value):
        self.count = self.value = value

    def __hash__(self):
        return hash(self.value)

    @memoize
    def foo(self):
        self.count += 1
        return 'foo: ' + str(self.count)

    @memoize
    def bar(self, string=None, integer=''):
        self.count += 1
        return str(string) + str(integer) + ': ' + str(self.count)

class TestMemoization(unittest.TestCase):
    def test_memo_instance(self):
        fb = FooBar(0)
        self.assertEqual(fb.foo(), fb.foo())

    def test_memo_different_instances(self):
        fb1 = FooBar(1)
        fb2 = FooBar(2)
        self.assertNotEqual(fb1.foo(), fb2.foo())

    def test_memo_different_arguments(self):
        fb = FooBar(0)
        self.assertEqual('foo: 1', fb.bar('foo'))
        self.assertEqual('bar: 2', fb.bar('bar'))
        self.assertEqual('foo: 1', fb.bar('foo'))

    def test_memo_bad_type(self):
        fb = FooBar({})
        with self.assertRaises(MemoizationError):
            fb.foo()

    def test_memo_kwarg_order(self):
        fb = FooBar(0)
        self.assertEqual(fb.bar(string='foo', integer=9),
                         fb.bar(integer=9, string='foo'))
