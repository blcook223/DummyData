"""
Evaluators to produce dummy data from DummyData models.
"""

import re
from collections import OrderedDict

from . import functions
from .exceptions import DDEvaluatorException


TAG_PATTERN = re.compile(r"""
    \{% \s*                             # open tag
    (?P<function> \b \w+ \b)            # function name
    (?P<args>                           # function arguments
    (?: \s*                             # separated by white-space
    [^\s]+ )*? )?                       # non-white-space, allowed characters
    \s* %\}                             # close tag
""", re.VERBOSE)


ARG_PATTERN = re.compile(r"""
    (?<!\S)                             # do not allow non-white-space
    (?<![:/\d])                         # do not match date or time
    -?                                  # negative sign
    (?= [1-9]|0(?!\d) )                 # digits or zero before decimal
    \d+                                 # pre-decimal digits
    (?: \.                              # decimal
    \d+ )?                              # post-decimal digits
    (?:[eE] [+-]? \d+)?                 # scientific notation
    (?![:/\d])                          # do not match date or time
    (?!\S)                              # do not allow non-white-space
    |
    (?<!\S)                             # do not allow non-white-space
    "                                   # begin quote
    (?:[^"\\]                           # non-control characters
    | \\ ["\\bfnrt/]                    # escaped characters
    | \\ u [0-9a-f]{4}                  # Unicode characters
    | \\\\ \\\" )*?                     # double-escaped quotation mark
    "                                   # end quote
    (?!\S)                              # do not allow non-white-space
    |
    (?<!\S)                             # do not allow non-white-space
    (?:0?[1-9]|1[012])                  # hours
    :[0-5][0-9]                         # minutes
    (?:AM|PM)                           # AM or PM
    (?!\S)                              # do not allow non-white-space
    |
    (?<!\S)                             # do not allow non-white-space
    (?:(?:0?[1-9]|1[012])               # months
    \/(?:0?[1-9]                        # days 0-9
    |[12][0-9]                          # days 10-29
    |3[01])                             # days 30-31
    \/\d{4})                            # year
    (?!\S)                              # do not allow non-white-space
""", re.VERBOSE)


def evaluate_json(json, allow_callable=False, iteration=None):
    """
    Traverse parsed JSON data and evaluate tags.
    """

    def call_function(match):
        """
        Call matched function.
        """
        args = ARG_PATTERN.findall(match.group('args'))
        args = [x[1:-1] if x[0] == '"' and x[-1] == '"' else x for x in args]
        try:
            value = getattr(
                functions,
                match.group('function')
            )(*args, iteration=iteration)
        except AttributeError:
            raise DDEvaluatorException(
                'attempted call to non-existent function {0}'.format(
                    match.group('function')
                )
            )
        if hasattr(json, '__call__') and not allow_callable:
            raise DDEvaluatorException(
                'function {0} called from illegal location'.format(
                    match.group('function')
                )
            )
        if match.start() != 0 or match.end() != len(match.string):
            value = str(value)
        return value

    def evaluate_object(json):
        """
        Evaluate tags in parsed JSON object.
        """
        evaluated = OrderedDict()
        for k in json:
            evaluated[
                evaluate_json(k, iteration=iteration)
            ] = evaluate_json(json[k], iteration=iteration)
        return evaluated

    def evaluate_array(json):
        """
        Evaluate tags in parsed JSON array.
        """
        evaluated = []
        index = 0
        while index < len(json):
            item = evaluate_json(
                json[index],
                allow_callable=True,
                iteration=iteration
            )
            if hasattr(item, '__call__'):
                if index + 1 >= len(json):
                    raise DDEvaluatorException(
                        'invalid use of {0} function at end of array'.format(
                            item.parent_function
                        )
                    )
                if 'repeat' == item.parent_function:
                    evaluated.extend(item(json[index + 1], evaluate_json))
                    index += 1
                elif 'random' == item.parent_function:
                    return item(json[index + 1:], evaluate_json)
            else:
                evaluated.append(item)
            index += 1
        return evaluated

    if isinstance(json, dict):
        return evaluate_object(json)
    elif isinstance(json, list):
        return evaluate_array(json)
    elif isinstance(json, str):
        try:
            return re.sub(TAG_PATTERN, call_function, json)
        except TypeError:
            # function returned a type other than string
            return call_function(TAG_PATTERN.search(json))
