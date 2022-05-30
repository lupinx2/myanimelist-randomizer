# malptw-rand
Randomly selects an anime listing from your MAL plan to watch section.

## Requirements
- Python 3.2+
- An .xml file or MAL API key

## How to get your exported XML MAL file
Go to your MAL anime list page and locate the sidebar on the right. Then click the `Export` button.

![Export Button](https://i.ibb.co/TB9rnhX/mal1.png)

Select anime list from the dropdown.

![Dropdown Selection](https://i.ibb.co/VNGjrLR/image.png)

Then click the following link to download your list. Make sure to extract it into the same folder that has the `malptw_rand.py` script.

![Download list](https://i.ibb.co/rfB7GJf/image.png)

## How to get a MAL API key
Go to your account settings on MAL and locate the API tab on the right. Then click the `Create ID` button.

$picutre of tab, highlighting the button$

Fill out the form's required fields, I *recommend* putting in the following information:

App Name: `myanimelist-randomizer`

App Type: `Other`

App Description: `I am a user of this app, which requires me to provide my own API key.`

App Redirect URL: `localhost/oatuh`

Homepage URL: `https://github.com/lupinx2/myanimelist-randomizer`

Commercial/Non-Commercial: `Non-Commercial`

Purpose of Use: `Other`, or `Hobbyist` if you intend to edit this app.

Once you have clicked `Submit`, navigate back to the API tab of your MAL account settings, you should see a new button called `Edit`.

{picture highligting edit button}

Click the `Edit` button and you should see the same form again with a new string of red text called `Client ID`, copy that string. 

**NOTE: Sharing your Client ID with other people runs the risk that they might use it badly and you get in trouble for it; treat it like you would a password.**

Now that you have your API key, open the `config.py` file in any text editor (Notepad will do) and paste it inside the quotes, replacing the placeholder asterisks.

{picture of config.py file}

## Usage
First clone/download this repo and make sure to follow the steps above to either get your XML MAL file or API Key.

If you're on Windows, you can just double-click the `run-malptw_rand.bat` file.

If you're not on Windows, or would prefer to use a terminal just `cd` into the repo folder. Then type:

`python malptw_rand.py` or `python3 malptw_rand.py`

to get a random anime from your PTW list.

## Contributions

This application is built based on code originally written by [renellc](https://github.com/renellc)
