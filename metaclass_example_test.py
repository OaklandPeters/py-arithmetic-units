class MetaclassTests(unittest.TestCase):
    def test_metaclass__call__(self):
        # Override it, and confirm override method still calls new
        class Meta(type):
            def __call__(cls, *args, **kwargs):
                # This gets the arguments right, but there is an error in:
                return cls.__call__(*args, **kwargs)

                # This leads to duplication inside Container.__call__
                # where the arguments look like:
                # (cls, cls, *args)
                # return cls.__call__(cls, *args, **kwargs)


                # This leads to the trouble that Container.__call__ is never triggered
                #   although the child classes work fine
                # return type.__call__(cls, *args, **kwargs)


        class Container(object, metaclass=Meta):
            def __init__(self, *values):
                self.values = values

            def __repr__(self):
                return "{0}({1})".format(
                    self.__class__.__name__, self.values
                )

            @classmethod
            def __call__(cls, *args):
                if len(args) == 0:
                    return EmptyContainer(*args)
                else:
                    return NonemptyContainer(*args)


        class EmptyContainer(Container):
            @classmethod
            def __call__(cls, *args):
                self = object.__new__(cls)
                self.__init__(*args)
                return self

        class NonemptyContainer(Container):
            @classmethod
            def __call__(cls, *args):
                self = object.__new__(cls)
                self.__init__(*args)
                return self


        c0 = Container.__new__(Container, 'container')
        c0.__init__('container')
        c1 = Container('container stuff')
        c2 = Container()
        e = EmptyContainer()
        ne = NonemptyContainer("other words")


        self.assertEqual(type(c0), Container)
        self.assertEqual(type(c1), NonemptyContainer)
        self.assertEqual(type(c2), EmptyContainer)
        self.assertEqual(type(e), EmptyContainer)
        self.assertEqual(type(ne), NonemptyContainer)

        args = ('a', 'b')
        self.assertEqual(Container(*args).values, args)
