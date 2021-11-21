# fountain
Sublime Text plugin for GPT-3
- To Use: Highlight the text you want to use as a prompt, then run either the Completion or CompletionUsing commands to generate a completion using the default or selected preset.

![screen_shot_1](https://user-images.githubusercontent.com/43641857/142745626-6a263c55-047b-408f-8d3f-9e1914b6b1f5.png)
![screen_shot_2](https://user-images.githubusercontent.com/43641857/142745631-0fdd3293-5059-4df6-99b6-d5945334c60d.png)
![screen_shot_3](https://user-images.githubusercontent.com/43641857/142745633-4986569f-d1bb-4438-a4c6-42fe86dc4d17.png)

To Install: 
- Navigate to the packages folder for sublime text.
- `git clone https://github.com/M49ICKPIxi3/fountain.git`
- `pip install openai` using python 3.8.0+ (ST Packages are either ran in 3.3.0 or 3.8.0)
- Find the 'site_packages' directory of your python installation and add the "FOUNTAIN_SITE_PACKAGES" variable to either your .bash_profile, ( or .bashrc, .zshrc, etc.)
  - `export FOUNTAIN_SITE_PACKAGES='path_to_your_site_packages'`
  - While you're there add your api key `export OPENAI_API_KEY="your api key here"`
- Restart Sublime Text and that's it!

If you want to add your own fine-tuned model to the list of presets, you need to copy one of the defaults in Packages directory, and change the 'engine' field to 'model' and the value to the name of your fine-tuned model. Add that filename (name only) to the "presets_list" field in the settings.

This is very much a work in progress...

Features / Improvements:
- Create presets easily, open newly created preset in a new tab.