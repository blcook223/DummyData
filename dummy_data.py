import os

from json import loads, dumps

from sublime import Region, active_window, packages_path, installed_packages_path
from sublime_plugin import TextCommand, WindowCommand

from .evaluators import evaluate_json


class GenerateDummyDataCommand(TextCommand):
    """
    Generate dummy data based on the current model.
    """

    def run(self, edit):
        """
        Generate new dummy file based on the current model.
        """
        data = evaluate_json(
            loads(self.view.substr(Region(0, self.view.size())))
        )
        v = active_window().new_file()
        v.set_scratch(True)
        v.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')
        v.set_name('results.json')
        v.insert(edit, 0, dumps(data, indent=4, separators=(',', ': ')))

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
            file_name = os.path.basename(self.view.file_name())
        except AttributeError:
            file_name = self.view.name()
        file_ext = file_name.split('.')[-1]
        syntax = self.view.settings().get('syntax')
        return (
            'JSON' in syntax
            or 'Plain text' in syntax
            or file_ext == 'json'
        )


class NewDummyDataModelCommand(WindowCommand):
    """
    Create a new model.
    """

    class PopulateDummyDataTemplate(TextCommand):
        """
        Populate the open view with a template model.
        """

        def run(self, edit):
            """
            Populate the open view with a template model.
            """
            v = active_window().active_view()
            path = os.path.join(packages_path(), 'DummyData', 'template.json')
            f = open(path, 'r') # TODO: fix this so it will work for other package locations
            v.insert(edit, 0, f.read())
            f.close()

    def run(self):
        """
        Open a new file and populate it with a template.
        """
        v = self.window.new_file()
        v.set_scratch(True)
        v.set_syntax_file('Packages/JavaScript/JSON.tmLanguage')
        v.set_name('dummy_data_model.json')
        self.window.focus_view(v)
        self.window.run_command('populate_dummy_data_template')

    def description(self):
        """
        Return a description of the command.
        """
        return 'Create a new template for a JSON DummyData model.'

# TODO: add threading support