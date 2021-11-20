import sys
import os
import sublime_plugin
import sublime
from collections import defaultdict

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))



"""
Takes a string and filters out everything but alphanumeric characters.
"""

# Someone somewhere probably wants a cooler filename, this is V where V you V do that...
def filter_arb(_string):
    return ''.join(ch for ch in _string if ch.isalpha() or ch in ['.', '-', '_'])  # Here

import subprocess
import os
import sys









def write_text(path, output):
    with open(path, 'w+') as file:
        file.write(output)


def write_json(path, data):
    with open(path, 'w+') as outfile:
        json.dump(data, outfile, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)


# How to do this: command to edit the settings for a model, open the settings file in a new scratch window and
# allow the user to fill it in, save it

def get_fountain_settings():
    fountain_settings = sublime.load_settings('fountain.sublime-settings')
    return fountain_settings.to_dict()

FOUNTAIN_LIBRARY_PATH = CURRENT_DIR + '/lib'

#SITE_PACKAGES_DIR = '/Users/saya/.pyenv/versions/3.8.0/lib/python3.8/site-packages'
SITE_PACKAGES_DIR = '/Users/saya/.pyenv/versions/3.8.0/lib/python3.8/site-packages/' #get_fountain_settings()['site_packages'] # os.environ['SITE_PACKAGES'] if not None else get_fountain_settings()['site_packages']
os.environ['PYTHONPACKAGES'] = SITE_PACKAGES_DIR

FOUNTAIN_PRESETS_DIR = os.path.join(sublime.packages_path(), 'fountain')


sys.path.append(FOUNTAIN_LIBRARY_PATH)
sys.path.append(CURRENT_DIR)
sys.path.append(os.environ['PYTHONPACKAGES'])



#if not os.path.exists(FOUNTAIN_PRESETS_DIR):
#    os.makedirs(FOUNTAIN_PRESETS_DIR)



from lib.gpt3_api import GPT3API, CompletionPreset, make_default_presets



import json
import decimal






def read_text(path):
    with open(path, encoding='utf-8', errors="replace") as file:
        text = file.read()
    return text





from typing import List
# import pysnooper

import inspect

#inspect.getmembers(sublime)


""" TODO: ...
    Models list is the displayed models on CompletionUsing ( yes )
    There's also SetDefaultEngine ( yes )
    Completion ( yes )
    CompletionFromDocument ( no )   
    CreatePreset ( no )
    CreatePresetFrom ( yes )
    
"""




gpt3_api = GPT3API()

make_default_presets(FOUNTAIN_PRESETS_DIR)



# Command using a settings reader, menu, on_done

class CompletionUsingCommand(sublime_plugin.TextCommand):

    def run(self, edit_token, preset):
        text_gen_params = preset

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




class DefaultCompletionCommand(sublime_plugin.TextCommand):

    def run(self, edit_token):
        default_preset = get_fountain_settings()['default_preset']

        preset = sublime.load_settings('fountain_' + default_preset + '.sublime-settings')
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

        preset = sublime.load_settings('fountain_' + preset_name + '.sublime-settings')
        preset_data = preset.to_dict()

        print(str(preset_data).replace(',',',\n'))
        print('\n\n\n')

        self.view.run_command('completion_using', args={
            'preset': preset_data
        })


