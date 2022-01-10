class DataProperty:
    def __init__(
        self,
        fget=None,
        fset=None,
        fdel=None,
        fview=None
    ):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.fview = fview

    def __get__(self, instance, cls):
        if self.fget is not None:
            return self.fget(instance)

    def __set__(self, instance, value):
        import pdb; pdb.set_trace()
        if self.fset is not None:
            self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is not None:
            self.fdel(instance)

    def __view__(self, instance):
        if self.fview is not None:
            self.fview(instance)

    def getter(self, fn):
        self.fget = fn

    def setter(self, fn):
        self.fset = fn

    def deleter(self, fn):
        self.fdel = fn

    def view(self, fn):
        self.fview = fn


props = DataProperty
