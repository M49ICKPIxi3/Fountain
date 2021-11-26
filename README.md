# Fountain
Sublime Text plugin for GPT-3

## Usage

Highlight the text you want to use as a prompt, then run either the Completion or CompletionUsing commands to generate a completion using the default or selected preset.

### CompletionUsing:
![st_fountain_image1](https://user-images.githubusercontent.com/43641857/143515081-206a699d-3cee-445a-82f9-4379e329abaf.png)
![st_fountain_image2](https://user-images.githubusercontent.com/43641857/143515082-b080635f-6781-4e5d-b72c-50973f212b8c.png)
![st_fountain_image3](https://user-images.githubusercontent.com/43641857/143515085-833d12b5-c242-464d-8649-5c407eab4cce.png)
![st_fountain_image4](https://user-images.githubusercontent.com/43641857/143515131-1a7052ff-acf1-4d8f-bcea-ef958a8e0dcb.png)

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
