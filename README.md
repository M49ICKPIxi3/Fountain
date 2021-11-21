# fountain
Sublime Text plugin for GPT-3
- To Use: Highlight the text you want to use as a prompt, then run either the Completion or CompletionUsing commands to generate a completion using the default or selected preset.

To Install: 
- Navigate to the packages folder for sublime text.
- `git clone https://github.com/M49ICKPIxi3/fountain.git`
- `pip install openai` using python 3.8.0+ (ST Packages are either ran in 3.3.0 or 3.8.0)
- Find the 'site_packages' directory of your python installation and change the 'SITE_PACKAGES_DIR' variable on line 51 in fountain.py (Not yet working with os.getenv)
- Restart Sublime Text and that's it!

If you want to add your own fine-tuned model to the list of presets, you need to copy one of the defaults in Packages directory, and change the 'engine' field to 'model' and the value to the name of your fine-tuned model. Add that filename (name only) to the "presets_list" field in the settings.

This is very much a work in progress...