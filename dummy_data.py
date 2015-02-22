import os

from json import loads, dumps

from sublime import Region, active_window, packages_path, installed_packages_path
from sublime_plugin import TextCommand, WindowCommand

from DummyData.evaluators import evaluate_json


class GenerateDummyDataCommand(TextCommand):

    def run(self, edit):
        """
        Generate new dummy file based on the current template.
        """
        data = evaluate_json(
            loads(self.view.substr(Region(0, self.view.size())))
        )
        f = active_window().new_file()
        f.set_scratch(True)
        f.set_name('results.json')
        f.insert(edit, 0, dumps(data, indent=4, separators=(',', ': ')))


class NewDummyDataTemplateCommand(WindowCommand):
    def run(self):
        f = self.window.new_file()
        f.set_scratch(True)
        f.set_name('new_dummy_data.json')
        self.window.focus_view(f)
        self.window.run_command('populate_dummy_data_template')


class PopulateDummyDataTemplate(TextCommand):
    def run(self, edit):
        v = active_window().active_view()
        if os.path.isfile(os.path.join(packages_path(), 'DummyData', 'template.json')):
            f = open(os.path.join(packages_path(), 'DummyData', 'template.json'), 'r')
        elif os.path.isfile(os.path.join(installed_packages_path(), 'DummyData', 'template.json')):
            f = open(os.path.join(installed_packages_path(), 'DummyData', 'template.json'), 'r')
        v.insert(edit, 0, f.read())
        f.close()