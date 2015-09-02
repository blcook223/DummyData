"""
Basic DummyData commands
"""

from os import path
from json import loads, dumps
from collections import OrderedDict

from sublime import Region, active_window, status_message, error_message
from sublime_plugin import TextCommand, WindowCommand

from .exceptions import DDEvaluatorException, DDFunctionException
from .evaluators import evaluate_json


TEMPLATE = (
    '{\n\t"organization":{\n\t\t"name":"{% company %}",\n\t\t"address1":"{% in'
    'teger 1000 9999 %} {% street %}",\n\t\t"address2":"{% city %}, {% state %'
    '} {% postal %}",\n\t\t"country":"{% country %}",\n\t\t"website":"{% url %'
    '}",\n\t\t"mission":"{% sentence %}",\n\t\t"description":"{% paragraph %}"'
    ',\n\t\t"market share":"{% number 0 100 2 %}"\n\t},\n\t"staff":[\n\t\t"{% '
    'repeat 10 %}",\n\t\t{\n\t\t\t"hire date":"{% date 01/01/1970 01/01/2015 %'
    '}",\n\t\t\t"shift start time":"{% time 7:00AM 10:00AM %}",\n\t\t\t"ID car'
    'd number":"{% uid %}",\n\t\t\t"employee ID":"{% index %}",\n\t\t\t"first '
    'name":"{% first_name %}",\n\t\t\t"last name":"{% last_name %}",\n\t\t\t"e'
    'mail":"{% email %}",\n\t\t\t"phone number":"{% phone %}",\n\t\t\t"part-ti'
    'me":"{% boolean %}",\n\t\t\t"department":["{% random %}","Facilities","Sa'
    'les","IT"]\n\t\t}\n\t]\n}'
)


class GenerateDummyDataCommand(TextCommand):
    """
    Generate dummy data based on the current model.
    """

    def run(self, edit):
        """
        Generate new dummy file based on the current model.
        """
        status_message('Generating DummyData...')

        try:
            data = evaluate_json(
                loads(self.view.substr(Region(0, self.view.size())), object_pairs_hook=OrderedDict)
            )
        except (DDFunctionException, DDEvaluatorException) as error:
            error_message('DummyData encountered an error: %s' % error.args[0])
            status_message('DummyData not generated')
            return
        text = dumps(data, indent=4, separators=(',', ': '))
        new_view = active_window().new_file()
        new_view.set_scratch(True)
        new_view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')
        new_view.set_name('results.json')
        status_message('DummyData generated')
        new_view.insert(edit, 0, text)

    def description(self):
        """
        Return a description of the command.
        """
        return (
            'Generate a new JSON file based on the currently open DummyData '
            'model'
        )

    def is_visible(self):
        """
        Return true if current view is a JSON file.
        """
        try:
            file_name = path.basename(self.view.file_name())
        except AttributeError:
            file_name = self.view.name()
        file_ext = file_name.split('.')[-1]
        syntax = self.view.settings().get('syntax')
        return (
            'JSON' in syntax
            or 'Plain text' in syntax
            or file_ext == 'json'
        )


class PopulateDummyDataTemplate(TextCommand):
    """
    Populate the open view with a template model.
    """

    def run(self, edit):
        """
        Populate the open view with a template model.
        """
        self.view.insert(edit, 0, TEMPLATE)

    def is_visible(self):
        """
        Command used internally; always return false
        """
        return False


class NewDummyDataModelCommand(WindowCommand):
    """
    Create a new model.
    """

    def run(self):
        """
        Open a new file and populate it with a template.
        """
        new_view = self.window.new_file()
        new_view.set_scratch(True)
        new_view.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')
        new_view.set_name('dummy_data_model.json')
        self.window.focus_view(new_view)
        active_window().active_view().run_command(
            'populate_dummy_data_template'
        )

    def description(self):
        """
        Return a description of the command.
        """
        return 'Create a new template for a JSON DummyData model.'
