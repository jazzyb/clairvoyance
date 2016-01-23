class MemoizationError(Exception):
    pass


class _Memoization(object):
    memo_dict = {}

    @staticmethod
    def memoize(method):
        def method_wrapper(*args, **kwargs):
            try:
                key = int()
                for kw in sorted(kwargs.keys()):
                    key ^= hash((kw, kwargs[kw]))
                for arg in args:
                    if type(arg) == list:
                        arg = tuple(arg)
                    key ^= hash(arg)
                key ^= hash(method)
                if key in _Memoization.memo_dict:
                    return _Memoization.memo_dict[key]

            except TypeError:
                # one of our arguments is unhashable
                raise MemoizationError("unhashable value passed to '%s'" % method)

            results = method(*args, **kwargs)
            _Memoization.memo_dict[key] = results
            return results
        return method_wrapper


memoize = _Memoization.memoize
