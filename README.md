# Fountain
Sublime Text plugin for GPT-3

## Usage

Highlight the text you want to use as a prompt, then run either the Completion or CompletionUsing commands to generate a completion using the default or selected preset.

### CompletionUsing:
![screen_shot_1](https://user-images.githubusercontent.com/43641857/142745626-6a263c55-047b-408f-8d3f-9e1914b6b1f5.png)
![screen_shot_2](https://user-images.githubusercontent.com/43641857/142745631-0fdd3293-5059-4df6-99b6-d5945334c60d.png)
![screen_shot_3](https://user-images.githubusercontent.com/43641857/142745633-4986569f-d1bb-4438-a4c6-42fe86dc4d17.png)

## Installation
Navigate to the packages folder for sublime text:

  `git clone https://github.com/M49ICKPIxi3/fountain.git`

Install the Python Library for OpenAI's API:

  `pip install openai`

Next, find the 'site-packages' directory of your local python installation. For example: `~/.pyenv/versions/3.8.0/lib/python3.8/site-packages`

Export the site-packages path to ST_USER_SITE_PACKAGES. This allows Sublime to add the site-packages to sys.path at runtime. This allows Fountain to make use of 3rd party libraries (ex. `openai`).

  `export ST_USER_SITE_PACKAGES="path/to/your/site-packages"`
  
While you're there add your OpenAI API key:

`export OPENAI_API_KEY="your api key here"`

Restart Sublime Text and that's it!

Note: If you are running Sublime Text from a terminal don't forget to run `source .zshrc` for the shell you're using.

### Features / Improvements:
- Create presets easily, open newly created preset in a new tab.
- Add support for Fine-Tune models.
- Store prompts used for each preset into a local 'Prompts' database to create a 'Prompts History'.