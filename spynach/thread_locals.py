try:
    #If we are using greenlets use the greenlet id
    from greenlet import getcurrent as get_ident
except ImportError:
    #Otherwise use the plain thread id
    try:
        from thread import get_ident
    except ImportError: # pragma: no cover
        from dummy_thread import get_ident

class ThreadLocalProxy(object):
    def __init__(self):
        object.__setattr__(self, '__locals__', {})

    def _get_object(self):
        return self.__locals__[get_ident()]

    def _set_object(self, value):
        self.__locals__[get_ident()] = value

    def _pop_object(self):
        self.__locals__.pop(get_ident(), None)

    @property
    def __dict__(self):
        try:
            return self._get_object().__dict__
        except RuntimeError:
            raise AttributeError('__dict__')

    def __getattr__(self, attr):
        return getattr(self._get_object(), attr)

    def __setattr__(self, attr, value):
        setattr(self._get_object(), attr, value)

    def __delattr__(self, name):
        delattr(self._get_object(), name)

    def __getitem__(self, key):
        return self._get_object()[key]

    def __setitem__(self, key, value):
        self._get_object()[key] = value

    def __delitem__(self, key):
        del self._get_object()[key]

    def __call__(self, *args, **kw):
        return self._get_object()(*args, **kw)

    def __repr__(self):
        try:
            return repr(self._get_object())
        except RuntimeError:
            return '<%s.%s object at 0x%x>' % (self.__class__.__module__,
                                               self.__class__.__name__,
                                               id(self))

    def __iter__(self):
        return iter(self._get_object())

    def __len__(self):
        return len(self._get_object())

    def __contains__(self, key):
        return key in self._get_object()

    def __nonzero__(self):
        return bool(self._get_object())
