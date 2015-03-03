"""
Functions used by evaluators to produce dummy data.
"""

import re
from uuid import uuid4
from datetime import datetime, timedelta, date as dt
from random import randint, getrandbits, uniform, choice

from .constants import (
    CITIES,
    STATES,
    STREETS,
    COUNTRIES,
    COMPANIES,
    FIRST_NAMES,
    LAST_NAMES,
)
from .exceptions import DDFunctionException


INDEX_TAG_PATTERN = re.compile(r"""
    \{% \s*                             # open tag
    index                               # function name
    \s* %\}                             # close tag
""", re.VERBOSE)


def integer(*args, **_):
    """
    Return random integer between parameter min a max.
    """
    length = len(args)
    if length != 0 and length != 2:
        raise DDFunctionException(
            'integer function does not except %d arg(s)' % length
        )
    if args:
        return randint(int(args[0]), int(args[1]))
    return randint(0, 1)


def number(*args, **_):
    """
    Return random float between parameter min a max.
    """
    length = len(args)
    if length < 0 or length > 3 or length == 1:
        raise DDFunctionException(
            'number function does not except %d arg(s)' % length
        )

    if args:
        if len(args) == 3:
            return round(uniform(float(args[0]), float(args[1])), int(args[2]))
        return uniform(float(args[0]), float(args[1]))
    return uniform(0, 1)


def boolean(*args, **_):
    """
    Return random boolean.
    """
    if args:
        raise DDFunctionException(
            'boolean function does not accept args, %d given' % len(args)
        )
    return bool(getrandbits(1))


def postal(*args, **_):
    """
    Return a random postal code.
    """
    if args:
        raise DDFunctionException(
            'postal function does not accept args, %d given' % len(args)
        )
    return str(integer(10000, 99999))


def phone(*args, **_):
    """
    Return a random phone number.
    """
    if args:
        raise DDFunctionException(
            'phone function does not accept args, %d given' % len(args)
        )
    return ''.join(
        [
            '(', str(integer(100, 999)), ') ',
            str(integer(100, 999)), '-', str(integer(1000, 9999))
        ]
    )


def paragraph(*args, **_):
    """
    Return a paragraph of text.
    """
    if args:
        raise DDFunctionException(
            'paragraph function does not accept args, %d given' % len(args)
        )
    return (
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '
        'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim '
        'ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut '
        'aliquip ex ea commodo consequat. Duis aute irure dolor in '
        'reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla '
        'pariatur. Excepteur sint occaecat cupidatat non proident, sunt in '
        'culpa qui officia deserunt mollit anim id est laborum.'
    )


def sentence(*args, **_):
    """
    Return a paragraph of text.
    """
    if args:
        raise DDFunctionException(
            'sentence function does not accept args, %d given' % len(args)
        )
    return (
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do '
        'eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    )


def city(*args, **_):
    """
    Return a random city.
    """
    if args:
        raise DDFunctionException(
            'city function does not accept args, %d given' % len(args)
        )
    return choice(CITIES)


def state(*args, **_):
    """
    Return a random state.
    """
    if args:
        raise DDFunctionException(
            'state function does not accept args, %d given' % len(args)
        )
    return choice(STATES)


def street(*args, **_):
    """
    Return a random street name.
    """
    if args:
        raise DDFunctionException(
            'street function does not accept args, %d given' % len(args)
        )
    return choice(STREETS)


def country(*args, **_):
    """
    Return a random country name.
    """
    if args:
        raise DDFunctionException(
            'country function does not accept args, %d given' % len(args)
        )
    return choice(COUNTRIES)


def company(*args, **_):
    """
    Return a random company name.
    """
    if args:
        raise DDFunctionException(
            'company function does not accept args, %d given' % len(args)
        )
    return choice(COMPANIES)


def url(*args, **_):
    """
    Return a random URL.
    """
    if args:
        raise DDFunctionException(
            'url function does not accept args, %d given' % len(args)
        )
    return ''.join(
        [
            'http://www.',
            company().lower().replace(' ', '-'),
            '.com/'
        ]
    )


def first_name(*args, **_):
    """
    Return a random first name.
    """
    if args:
        raise DDFunctionException(
            'first_name function does not accept args, %d given' % len(args)
        )
    return choice(FIRST_NAMES)


def last_name(*args, **_):
    """
    Return a random last name.
    """
    if args:
        raise DDFunctionException(
            'last_name function does not accept args, %d given' % len(args)
        )
    return choice(LAST_NAMES)


def email(*args, **_):
    """
    Return a random email address.
    """
    if args:
        raise DDFunctionException(
            'last_name function does not accept args, %d given' % len(args)
        )
    return ''.join(
        [
            first_name().lower(), '.', last_name().lower(),
            '@', company().lower().replace(' ', '-'), '.com'
        ]
    )


def random(*args, iteration=None):
    """
    Return a random arg or a random selection function.
    """
    if args:
        return choice(args)

    def evaluate_random(array, evaluator):
        """
        Choose from among items in the array.
        """
        return evaluator(choice(array), iteration)

    return evaluate_random


def repeat(*args, **_):
    """
    Return a function that will repeat a list.
    """
    length = len(args)
    if length != 1:
        raise DDFunctionException(
            'repeat function requires 1 arg, %d given' % length
        )

    def evaluate_repeat(array, evaluator):
        """
        Repeat the array the given number of times.
        """

        evaluated = []
        for num in range(0, int(args[0])):
            evaluated.append(evaluator(array[0], iteration=num))
        return evaluated

    return evaluate_repeat


def index(*args, iteration):
    """
    Return index value if currently in repeat structure.
    """
    if args:
        raise DDFunctionException(
            'index function does not accept args, %d given' % len(args)
        )
    if iteration is None:
        raise DDFunctionException(
            'index function called outside of repeat function structure'
        )
    return iteration


def uid(*args, **_):
    """
    Return a random unique ID.
    """
    if args:
        raise DDFunctionException(
            'uid function does not accept args, %d given' % len(args)
        )
    return str(uuid4())


def date(*args, **_):
    """
    Return a random date between the parameter dates.
    """
    length = len(args)
    if length != 0 and length != 2:
        raise DDFunctionException(
            'date function does not except %d arg(s)' % length
        )
    if args:
        start = datetime.strptime(args[0], '%m/%d/%Y')
        end = datetime.strptime(args[1], '%m/%d/%Y')
        delta = end - start
        days = randint(0, delta.days)
        return_date = start + timedelta(days=days)
        return return_date.strftime('%m/%d/%Y')
    return dt.today().strftime('%m/%d/%Y')


def time(*args, **_):
    """
    Return a random time between the parameter times.
    """
    length = len(args)
    if length != 0 and length != 2:
        raise DDFunctionException(
            'time function does not except %d arg(s)' % length
        )
    if args:
        start = datetime.strptime(args[0], '%I:%M%p')
        end = datetime.strptime(args[1], '%I:%M%p')
        delta = end - start
        seconds = randint(0, delta.seconds)
        return_time = start + timedelta(seconds=seconds)
        return return_time.strftime('%I:%M%p')
    return datetime.now().strftime('%I:%M%p')
