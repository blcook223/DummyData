from re import compile, VERBOSE
from json import loads, dumps

from sublime import Region, active_window
from sublime_plugin import TextCommand

from DummyData import functions


class DDException(Exception):
    pass


class DummyDataCommand(TextCommand):

    def run(self, edit):
        """
        Generate new JSON file based on template.
        """

        def evaluate_json(json, allow_function=False):
            """
            Traverse parsed JSON data and evaluate tags.
            """

            def call_function(match):
                """
                Call matched function.
                """
                args = argPattern.findall(match.group('args'))
                return getattr(functions, match.group('function'))(*args)

            def evaluate_object(json):
                """
                Evaluate tags in parsed JSON object.
                """
                for k in json:
                    match = tagPattern.search(k)
                    if match:
                        newKey = call_function(match)
                        json[newKey] = evaluate_json(json.pop(k))
                    else:
                        json[k] = evaluate_json(json[k])
                return json

            def evaluate_array(json):
                """
                Evaluate tags in parsed JSON array.
                """
                if json:
                    first_item = evaluate_json(json[0], True)
                    if hasattr(first_item, '__call__'):
                        return first_item(json[1:], evaluate_json)
                    for i, val in enumerate(json):
                        json[i] = evaluate_json(val)
                return json

            if type(json) is dict:
                return evaluate_object(json)
            elif type(json) is list:
                return evaluate_array(json)
            elif type(json) is str:
                match = tagPattern.search(json)
                if match:
                    json = call_function(match)
                    if (hasattr(json, '__call__') and not allow_function):
                        raise DDException('TODO: improve all messages')
            return json

        tagPattern = compile(r"""
            ^\{% \s* (?P<function> \b\w+\b) (?P<args> (?: \s*\S+ )* )? \s* %\}$
        """, VERBOSE)
        argPattern = compile(r"""
            -? (?= [1-9]|0(?!\d) ) \d+ (?:\.\d+)? (?:[eE] [+-]? \d+)?
        """, VERBOSE)

        data = evaluate_json(
            loads(self.view.substr(Region(0, self.view.size())))
        )
        f = active_window().new_file()
        f.set_scratch(True)
        f.set_name('results.json')
        f.insert(edit, 0, dumps(data, indent=4, separators=(',', ': ')))





    # print(dumps(bytes('"a string with \\"double quotes\\""', "utf-8").decode("unicode_escape")))

   #   (?P<number>   -? (?= [1-9]|0(?!\d) ) \d+ (?:\.\d+)? (?:[eE] [+-]? \d+)? )
   # | (?P<boolean>  true | false | null )
   # | (?P<string>   " (?:[^"\\]* | \\ ["\\bfnrt\/] | \\ u [0-9a-f]{4} )* (?<!\\ \\ \\) " )
   # | (?P<array>    \[ (?: (?P=json)  (?: , (?P=json)  )*  )?  \s* \] )
   # | (?P<pair>     \s* (?P=string) \s* : (?P=json)  )
   # | (?P<object>   \{  (?:  (?P=pair)  (?: , (?P=pair)  )*  )?  \s* \} )
   # | (?P<json>     \s* (?: (?P=number) | (?P=boolean) | (?P=string) | (?P=array) | (?P=object) ) \s* )
