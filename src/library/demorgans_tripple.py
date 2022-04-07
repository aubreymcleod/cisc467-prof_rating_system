from abc import ABC


# abstract base classes for fuzzy operations
class Triple(ABC):
    @staticmethod
    def t(a, b):
        return NotImplemented

    @staticmethod
    def s(a, b):
        return NotImplemented

    @staticmethod
    def neg(a):
        return 1 - a


# concrete implementations
class Godel(Triple):
    @staticmethod
    def t(a, b):
        return min(a, b)

    @staticmethod
    def s(a, b):
        return max(a, b)


class Goguen(Triple):
    @staticmethod
    def t(a, b):
        return a*b

    @staticmethod
    def s(a, b):
        return 1 - (1 - a) * (1 - b)


class Lukasiewicz(Triple):
    @staticmethod
    def t(a, b):
        return max(0, a+b-1)

    @staticmethod
    def s(a, b):
        return min(a+b, 1)



class Drastic(Triple):
    @staticmethod
    def t(a, b):
        if a == 1:
            return b
        elif b == 1:
            return a
        else:
            return 0

    @staticmethod
    def s(a, b):
        if a == 0:
            return b
        elif b == 0:
            return a
        else:
            return 1


class Nilpotent(Triple):
    @staticmethod
    def t(a, b):
        if a+b > 1:
            return min(a, b)
        else:
            return 0

    @staticmethod
    def s(a, b):
        if a+b < 1:
            return max(a, b)
        else:
            return 1


class Hamacher(Triple):
    @staticmethod
    def t(a, b):
        if a == b == 0:
            return 0
        else:
            return (a*b)/(a+b-a*b)

    @staticmethod
    def s(a, b):
        return (a+b)/(1+a*b)
