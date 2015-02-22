from re import compile, VERBOSE, sub

from DummyData import functions
from DummyData.exceptions import DDEvaluatorException


TAG_PATTERN = compile(r"""
    \{% \s*                             # open tag
    (?P<function> \b \w+ \b)            # function name
    (?P<args> (?: \s* [\w\.\+\-]+ )* )? # function arguments
    \s* %\}                             # close tag
""", VERBOSE)


ARG_PATTERN = compile(r"""
    -?                                  # negative sign
    (?= [1-9]|0(?!\d) )                 # digits or zero before decimal
    \d+                                 # pre-decimal digits
    (?: \.                              # decimal
    \d+ )?                              # post-decimal digits
    (?:[eE] [+-]? \d+)?                 # scientific notation
""", VERBOSE)


def evaluate_json(json, allow_function=False):
    """
    Traverse parsed JSON data and evaluate tags.
    """

    def call_function(match):
        """
        Call matched function.
        """
        args = ARG_PATTERN.findall(match.group('args'))
        value = getattr(functions, match.group('function'))(*args)
        if hasattr(json, '__call__') and not allow_function:
            raise DDEvaluatorException(
                'function %s called from illegal location'
                % match.group('function')
            )
        if match.start() != 0 or match.end() != len(match.string):
            value = str(value)
        return value

    def evaluate_object(json):
        """
        Evaluate tags in parsed JSON object.
        """
        evaluated = {}
        for k in json:
            match = TAG_PATTERN.search(k)
            if match:
                evaluated[str(call_function(match))] = evaluate_json(json.pop(k))
            else:
                evaluated[k] = evaluate_json(json[k])
        return evaluated

    def evaluate_array(json):
        """
        Evaluate tags in parsed JSON array.
        """
        evaluated = []
        if json:
            evaluated.append(evaluate_json(json[0], True))
            if hasattr(evaluated[0], '__call__'):
                return evaluated[0](json[1:], evaluate_json)
            for val in json[1:]:
                evaluated.append(evaluate_json(val))
        return evaluated

    if type(json) is dict:
        evaluated = evaluate_object(json)
    elif type(json) is list:
        evaluated = evaluate_array(json)
    elif type(json) is str:
        try:
            evaluated = sub(TAG_PATTERN, call_function, json)
        except TypeError:
            # function returned a type other than string
            evaluated = call_function(TAG_PATTERN.search(json))
    return evaluated