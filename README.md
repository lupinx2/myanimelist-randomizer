# myanimelist-randomizer
Randomly selects an anime listing from your MAL plan to watch section.

![myannimelist-randomizer GUI](https://i.ibb.co/bFZXFRG/image.png)

## Requirements
For the .exe version:  
- An .xml file or MAL API key  
  
Aditionally, if you just download the repo:  
- Python 3.2+  
- pysimplegui (`pip install pysimplegui`)  
- tkinter (`sudo apt-get install python3-tk`)  
- PIL (`pip install pillow`)  

## How to get your exported XML MAL file
Go to your MAL anime list page and locate the sidebar on the right. Then click the `Export` button.

![Export Button](https://i.ibb.co/TB9rnhX/mal1.png)

Select anime list from the dropdown.

![Dropdown Selection](https://i.ibb.co/VNGjrLR/image.png)

Then click the following link to download your list. Make sure to extract it into the same folder that has the `malptw_rand.py` script.

![Download list](https://i.ibb.co/rfB7GJf/image.png)

## How to get a MAL API key
Go to your account settings on MAL and locate the API tab on the right. Then click the `Create ID` button.

![Create ID button](https://i.ibb.co/9NcHkXT/image.png)

Fill out the form's required fields, I *recommend* putting in the following information:

**App Name:** `myanimelist-randomizer`  
**App Type:** `Other`  
**App Description:** `I am a user of this app, which requires me to provide my own API key.`  
**App Redirect URL:** `http://localhost/oauth`  
**Homepage URL:** `https://github.com/lupinx2/myanimelist-randomizer`  
**Commercial/Non-Commercial:** `Non-Commercial`  
**Name/Company Name** [Your MAL username]  
**Purpose of Use:** `Other`, or `Hobbyist` if you intend to edit this app.  

Once you have clicked `Submit`, navigate back to the API tab of your MAL account settings, you should see a new button called `Edit`.

![Edit button](https://i.ibb.co/P6J2XFg/image.png)

Click the `Edit` button and you should see the same form again with a new string of red text called `Client ID`, copy that string. 

**NOTE: Sharing your Client ID runs the risk that others might use it badly and you get in trouble; treat it like you would a password.**

Now that you have your API key, run the program (see Usage below) and go to the settings tab, paste your API Key and hit Save, this will save it to the `config.py` file, so you don't have to enter it again every time you open the program.  

If you want, you can also manually paste it into the file using any text editor like notepad.  

![Config file](https://i.ibb.co/prwnmh4/image.png)

## Usage
Make sure to follow the steps above to either get your XML MAL file or API Key.  
The easiest way to use this is to download the mal-randomizer.exe release to a folder and double clicking it.  

If a .exe file doesn't suit your needs (or you don't trust them), you can just clone/download this repo  
(the download on this website is hidden behind a button labeled `code`)  

Then if you're on Windows, just double-click the `run-mal-randomizer.bat` file.  
If you're not on Windows, or would prefer to use a terminal just `cd` into the repo folder. Then type:  

`python mal_randomizer.py` or `python3 mal_randomizer.py`

## Support

This repository is actively mantained! if you encounter any issues or difficulties, or have a suggestion,  
please feel free to open a thread in the Issues tab.  

## FAQ

**Q:** This seems like way too much effort just to pick a random anime.

**A:** [Spin.moe](https://spin.moe/) is usually a far more convenient way to do it, this app is mostly a learning project for myself.

## Contributions

This application is built based on code originally written by [renellc](https://github.com/renellc)
