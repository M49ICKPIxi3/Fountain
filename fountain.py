import sys
import os
import sublime_plugin
import sublime

def write_text(path, output):
    with open(path, 'w+') as file:
        file.write(output)


def write_json(path, data):
    with open(path, 'w+') as outfile:
        json.dump(data, outfile, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)

def read_json(path):
    with open(path, 'r') as outfile:
        _data =  json.load(outfile)
    return _data

# How to do this: command to edit the settings for a model, open the settings file in a new scratch window and
# allow the user to fill it in, save it

def get_fountain_settings():
    fountain_settings = sublime.load_settings('fountain.sublime-settings')
    return fountain_settings.to_dict()

def append_sys_path(paths):
    for path in paths:
        if path not in sys.path:
            sys.path.append(path)


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ST_USER_SITE_PACKAGES = os.getenv('ST_USER_SITE_PACKAGES')
FOUNTAIN_PRESETS_DIR = os.path.join(sublime.packages_path(), 'User', 'fountain')
FOUNTAIN_SETTINGS_PATH = os.path.join('Packages', 'fountain', 'fountain.sublime-settings')
FOUNTAIN_SETTINGS_FULL_PATH = os.path.join(sublime.packages_path(), 'fountain', 'fountain.sublime-settings')

append_sys_path([
    ST_USER_SITE_PACKAGES
])

if not os.path.exists(FOUNTAIN_PRESETS_DIR):
    os.makedirs(FOUNTAIN_PRESETS_DIR)


from .lib.gpt3_api import GPT3API, make_default_presets

import json
import glob



def get_all_presets_list():
    presets = []
    for preset_file_name in glob.iglob(FOUNTAIN_PRESETS_DIR + '/*', recursive=True):
        presets.append(preset_file_name.split('/')[-1].split('.')[0])
    return presets


def read_text(path):
    with open(path, encoding='utf-8', errors="replace") as file:
        text = file.read()
    return text

def reload_presets():
    presets = get_all_presets_list()
    fountain_settings = get_fountain_settings()
    fountain_settings['presets_list'] = presets
    write_json(FOUNTAIN_SETTINGS_FULL_PATH, fountain_settings)
    sublime.load_resource(FOUNTAIN_SETTINGS_PATH)
    sublime.save_settings('fountain.sublime-settings')



gpt3_api = GPT3API()

make_default_presets(FOUNTAIN_PRESETS_DIR, gpt3_api.openai_api.Engine.list())

#reload_presets()

# Command using a settings reader, menu, on_done

class CompletionUsingCommand(sublime_plugin.TextCommand):

    def run(self, edit_token, preset):
        text_gen_params = preset

        for region in self.view.sel():
            print(region.to_tuple())
            if not region.empty():
                content = self.view.substr(region)
                text_gen_params['prompt'] = content
                if 'name' in text_gen_params:
                    del(text_gen_params['name'])
                if 'preset_type' in text_gen_params:
                    del(text_gen_params['preset_type'])

                completion = gpt3_api.completion(text_gen_params)
                content_with_completion = content + completion
                self.view.replace(edit_token, region, content_with_completion)
                self.view.sel().clear()
                break




class DefaultCompletionCommand(sublime_plugin.TextCommand):

    def run(self, edit_token):
        default_preset = get_fountain_settings()['default_preset']

        preset = sublime.load_settings(default_preset + '.sublime-settings')
        preset_data = preset.to_dict()

        text_gen_params = preset_data

        for region in self.view.sel():
            print(region.to_tuple())
            if not region.empty():
                content = self.view.substr(region)
                text_gen_params['prompt'] = content
                completion = gpt3_api.completion(text_gen_params)
                content_with_completion = content + completion
                self.view.replace(edit_token, region, content_with_completion)
                self.view.sel().clear()
                break





# Opens a popup menu that allows for selection of which model will be used in completions
class SelectPresetCommand(sublime_plugin.TextCommand):

    def get_preset_list(self):
        fountain_settings = sublime.load_settings('fountain.sublime-settings')
        return fountain_settings.to_dict()['preset_list']

    def run(self, edit_token):
        presets = self.get_preset_list()
        self.view.window().show_quick_panel(presets, self.on_done)


    def on_done(self, index):
        preset_name = 'davinci' # replace with default

        index_to_preset = {i: preset for i, preset in enumerate(self.get_preset_list())}
        print(index_to_preset)
        if index in index_to_preset:
            preset_name = index_to_preset[index]

        print(index_to_preset)

        #preset = sublime.load_settings(preset_name + '.sublime-settings')
        preset_data = read_json(os.path.join(sublime.packages_path(), 'User', 'fountain', preset_name + '.sublime-settings'))
        #preset_data = preset.to_dict()
        #preset_data = preset.to_dict()

        self.view.run_command('completion_using', args={
            'preset': preset_data
        })


# Opens a popup menu that allows for selection of which model will be used in completions
class ChangeDefaultPresetCommand(sublime_plugin.TextCommand):

    def get_preset_list(self):
        fountain_settings = sublime.load_settings('fountain.sublime-settings')
        return fountain_settings.to_dict()

    def run(self, edit_token):
        presets = get_all_presets_list()
        self.view.window().show_quick_panel(presets, self.on_done)


    def on_done(self, index):
        preset_name = 'davinci' # replace with default

        index_to_preset = {i: preset for i, preset in enumerate(get_all_presets_list())}
        print(index_to_preset)
        if index in index_to_preset:
            preset_name = index_to_preset[index]

        fountain_settings = get_fountain_settings()
        fountain_settings['default_preset'] = preset_name
        presets_filename = CURRENT_DIR + 'fountain.sublime-settings'
        write_json(presets_filename, fountain_settings)


# Opens a popup menu that allows for selection of which model will be used in completions
class NameNewPresetCommand(sublime_plugin.TextCommand):
    _template_preset = 'davinci'

    def get_preset_list(self):
        fountain_settings = sublime.load_settings('fountain.sublime-settings')
        return fountain_settings.to_dict()

    def run(self, edit_token, template_preset):
        self._preset_from_engine = template_preset
        presets = get_all_presets_list()
        self.view.window().show_input_panel("Name:", "", self.on_done, None, None)

    def on_done(self, preset_name):
        preset = sublime.load_settings(self._preset_from_engine + '.sublime-settings')
        self._preset_from_engine = 'davinci'
        preset_data = preset.to_dict()
        preset_data['name'] = preset_name
        write_json(FOUNTAIN_PRESETS_DIR + preset_name, preset_data)

# Opens a popup menu that allows for selection of which model will be used in completions
class CreatePresetFromCommand(sublime_plugin.TextCommand):

    def get_preset_list(self):
        fountain_settings = sublime.load_settings('fountain.sublime-settings')
        return fountain_settings.to_dict()

    def run(self, edit_token):
        presets = get_all_presets_list()
        print(presets)
        self.view.window().show_quick_panel(presets, self.on_done)


    def on_done(self, index):
        preset_name = 'davinci'  # replace with default

        index_to_preset = {i: preset for i, preset in enumerate(get_all_presets_list())}
        print(index_to_preset)
        if index in index_to_preset:
            preset_name = index_to_preset[index]

        self.view.run_command('name_new_preset', args={
            'template_preset': preset_name
        })






