from re import compile, VERBOSE
from json import loads, dumps

from sublime import Region, active_window
from sublime_plugin import TextCommand

from DummyData import functions


class DummyDataCommand(TextCommand):

    def run(self, edit):
        """
        Generate new JSON file based on template.
        """

        tagPattern = compile(r"""
            ^\{%\s*(?P<function>\b\w+\b)(?P<args>(?:\s*\S+)*)?\s*%\}$
        """, VERBOSE)
        argPattern = compile(r"""
            -? (?= [1-9]|0(?!\d) ) \d+ (?:\.\d+)? (?:[eE] [+-]? \d+)?
        """, VERBOSE)

        def function(match):
            """
            Call function in the parameter regex match.
            """
            args = argPattern.findall(match.group('args'))
            return getattr(functions, match.group('function'))(*args)

        def traverse(parsed):
            """
            Traverse parsed JSON data and evaluate functions.
            """
            if type(parsed) is dict:
                for k in parsed:
                    match = tagPattern.search(k)
                    if match:
                        newKey = function(match)
                        parsed[newKey] = traverse(parsed.pop(k))
                    else:
                        parsed[k] = traverse(parsed[k])
            elif type(parsed) is list:
                for i, val in enumerate(parsed):
                    parsed[i] = traverse(val)
            elif type(parsed) is str:
                match = tagPattern.search(parsed)
                if match:
                    return function(match)
            return parsed

        evaluated = traverse(
            loads(self.view.substr(Region(0, self.view.size())))
        )
        f = active_window().new_file()
        f.set_scratch(True)
        f.set_name('results.json')
        f.insert(edit, 0, dumps(evaluated, indent=4, separators=(',', ': ')))





    # print(dumps(bytes('"a string with \\"double quotes\\""', "utf-8").decode("unicode_escape")))

   #   (?P<number>   -? (?= [1-9]|0(?!\d) ) \d+ (?:\.\d+)? (?:[eE] [+-]? \d+)? )
   # | (?P<boolean>  true | false | null )
   # | (?P<string>   " (?:[^"\\]* | \\ ["\\bfnrt\/] | \\ u [0-9a-f]{4} )* (?<!\\ \\ \\) " )
   # | (?P<array>    \[ (?: (?P=json)  (?: , (?P=json)  )*  )?  \s* \] )
   # | (?P<pair>     \s* (?P=string) \s* : (?P=json)  )
   # | (?P<object>   \{  (?:  (?P=pair)  (?: , (?P=pair)  )*  )?  \s* \} )
   # | (?P<json>     \s* (?: (?P=number) | (?P=boolean) | (?P=string) | (?P=array) | (?P=object) ) \s* )
