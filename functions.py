from random import randint, getrandbits, uniform, choice

from DummyData.constants import (
    CITIES,
    STATES,
    STREETS,
    COUNTRIES,
    COMPANIES,
    FIRST_NAMES,
    LAST_NAMES,
)


class DummyDataException(Exception):
    pass


def integer(*args):
    """
    Return random integer between parameter min a max.
    """
    length = len(args)
    if length != 0 and length != 2:
        raise DummyDataException(
            'integer function does not except %s args' % length
        )
    if args:
        return randint(int(args[0]), int(args[1]))
    return randint(0, 1)


def number(*args):
    """
    Return random float between parameter min a max.
    """
    length = len(args)
    if length != 0 and length != 2:
        raise DummyDataException(
            'number function does not except %s args' % length
        )
    if args:
        return uniform(float(args[0]), float(args[1]))
    return uniform(0, 1)


def boolean(*args):
    """
    Return random boolean.
    """
    if args:
        raise DummyDataException('boolean function does not accept args')
    return bool(getrandbits(1))


def postal(*args):
    """
    Return a random postal code.
    """
    if args:
        raise DummyDataException('postal function does not accept args')
    return str(integer(10000, 99999))


def phone(*args):
    """
    Return a random phone number.
    """
    if args:
        raise DummyDataException('phone function does not accept args')
    return ''.join(
        [
            '(', str(integer(100, 999)), ') ',
            str(integer(100, 999)), '-', str(integer(1000,9999))
        ]
    )


def paragraph(*args):
    """
    Return a paragraph of text.
    """
    if args:
        raise DummyDataException('paragraph function does not accept args')
    return (
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '
        'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim '
        'ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut '
        'aliquip ex ea commodo consequat. Duis aute irure dolor in '
        'reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla '
        'pariatur. Excepteur sint occaecat cupidatat non proident, sunt in '
        'culpa qui officia deserunt mollit anim id est laborum.'
    )


def sentence(*args):
    """
    Return a paragraph of text.
    """
    if args:
        raise DummyDataException('sentence function does not accept args')
    return (
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '
        'eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    )


def city(*args):
    """
    Return a random city.
    """
    if args:
        raise DummyDataException('city function does not accept args')
    return choice(CITIES)


def state(*args):
    """
    Return a random state.
    """
    if args:
        raise DummyDataException('state function does not accept args')
    return choice(STATES)


def street(*args):
    """
    Return a random street name.
    """
    if args:
        raise DummyDataException('street function does not accept args')
    return choice(STREETS)


def country(*args):
    """
    Return a random country name.
    """
    if args:
        raise DummyDataException('country function does not accept args')
    return choice(COUNTRIES)


def company(*args):
    """
    Return a random company name.
    """
    if args:
        raise DummyDataException('company function does not accept args')
    return choice(COMPANIES)


def url(*args):
    """
    Return a random URL.
    """
    if args:
        raise DummyDataException('url function does not accept args')
    return ''.join(['http://www.', company().lower(), '.com/'])


def first_name(*args):
    """
    Return a random first name.
    """
    if args:
        raise DummyDataException('first_name function does not accept args')
    return choice(FIRST_NAMES)


def last_name(*args):
    """
    Return a random last name.
    """
    if args:
        raise DummyDataException('last_name function does not accept args')
    return choice(LAST_NAMES)


def email(*args):
    """
    Return a random email address.
    """
    if args:
        raise DummyDataException('last_name function does not accept args')
    return ''.join(
        [
            first_name().lower(), '.', last_name().lower(),
            '@', company().lower(), '.com'
        ]
    )



# TODO: implement these

# repeat
# index
# random


# TODO: implement these with and without args

# date
# time
