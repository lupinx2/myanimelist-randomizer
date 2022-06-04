# Returns a random anime from your MAL Plan-to-Watch list
# Using either the API or a local xml file.
#
# TODO
# Update readme with pictures
#
# Test with: Debian / fresh python install / no internet.
# Test with empty ptw list.
# Test if no_movies and only_movies are working correctly.
# Test if prevAPIcall is working correctly when username changes or settings are changed.
#
# PySimpleGUI:
#   Add xml selection.
#   Add randomize button XML function.
#   Improve output formatting, aspect.
#       Add placeholder cover art.
#       Add link to MAL page/streaming.
#
# Use the API key from the GUI.
#   Add save to config button functionality.
# 
# rename variables to be less confusing.
#
# Handle all errors in the GUI with user friendly messages.
#
# narrow scope of imports to only what is needed.
#
# Remove console output before pull request?

from json import loads as jsonLoads
import xml.etree.ElementTree as ET
import PySimpleGUI as Gooey
from random import randint
from config import API_key
from time import sleep
from PIL import Image
import requests
import glob
import io


if __name__ == '__main__':

    list_titles = list()
    list_id = list()
    list_coverImg = list()
    no_movies = False
    only_movies = False
    prevAPIcall = ""

# ------------------------------------------------------------------------------
# API Functions
# ------------------------------------------------------------------------------
    # Pull user's animelist by calling the MAL API, save the response to a dictionary.
    def APIgetAnimeList(user_name):
        global prevAPIcall
        if user_name == prevAPIcall:  # prevents unnecessary API calls
            return
        try:
            url = 'https://api.myanimelist.net/v2/users/' + str(user_name) +\
                '/animelist?fields=list_status,media_type&status=plan_to_watch&limit=1000'  # 1000 is the max allowed by MAL.
            headers = {'X-MAL-CLIENT-ID': API_key}
            sleep(0.7)  # Sleep to prevent rate limiting.
            response = requests.get(url, headers=headers)            
            if response.status_code != 200:
                raise Exception("API call error")
            responseBytes = (response.content)
            responseString = responseBytes.decode("utf-8")
        except:
            print("Error: API call failed Status code: " +
                  str(response.status_code) + "\n")
            window['-OUTPUT-'].update("Error: API call failed.")
            return 
        outputDict = jsonLoads(responseString) # convert response to dictionary

        # This block poulates the list objects from the API response.
        def gen_dict_extract(var, key):
            if isinstance(var, dict):
                for dictKey, dictValue in var.items():  # for every (key:value) pair in var...
                    if dictKey == key:  # where the key matches the parameter...
                        yield dictValue  # yield the value...
                    # if you run into a list, recursively call this function.
                    if isinstance(dictValue, list):
                        for listItem in dictValue:
                            for result in gen_dict_extract(listItem, key):
                                yield result
        for item in gen_dict_extract(outputDict, 'node'):
            list_titles.append(item['title'] + " [" + item['media_type'] + "]")
            list_id.append(item['id'])
            list_coverImg.append(item['main_picture']['medium'])
            if (no_movies == True and item['media_type'] == "movie"):
                list_titles.pop()
                list_id.pop()
                list_coverImg.pop()
            if (only_movies == True and not item['media_type'] == "movie"):
                list_titles.pop()
                list_id.pop()
                list_coverImg.pop()
        prevAPIcall = user_name

    # Returns a tuple with the title, MAL page, and URL for the cover art.
    def GetRandomAnime():
        try:
            rand_index = randint(0, len(list_titles)-1)
            return "{}".format(list_titles[rand_index]), \
                ('https://myanimelist.net/anime/' + str(list_id[rand_index])), \
                list_coverImg[rand_index]
        except:
            print ("Error: Failed to get anime data from list object.\n")
            return "Error: Failed to get anime from PTW list.", "https://myanimelist.net/anime/20"

    def GetCoverArt(coverURL):
        try:
            url = coverURL
            response = requests.get(url, stream=True)
            response.raw.decode_content = True
        except: 
           print("Error: Failed to get cover art.\n")
        try:
            jpg_img = Image.open(io.BytesIO(response.content)) # get jpg formated bytes from response
            png_img = io.BytesIO() # create BytesIO object to store png
            jpg_img.save(png_img, format="PNG") # convert jpg data to png format
            png_data = png_img.getvalue() # create return object
            return png_data
        except: 
           print("Error: Failed jpg to png conversion.\n")
        
# ------------------------------------------------------------------------------
# GUI
# ------------------------------------------------------------------------------
    # This is spaghetti code, clean it up later.
    Gooey.theme('LightGray')
    # The main tab.
    tab1_layout = [[Gooey.Text('Allof which makes me anxious:')],
                   [Gooey.Text('MAL username:'),
                    Gooey.InputText(key='-username-')],
                   [Gooey.Radio("Exclude Movies", 666, False, False, key='-no_Movies-'),  # Radio buttons
                    Gooey.Radio("Only Movies", 666, False, False, key='-only_Movies-'),
                    Gooey.Radio("Any anime", 666, True, False, key='-any_Anime-')],  # <-default selection
                   [Gooey.Image(key="-OUTPUT_IMG-"), Gooey.Text("this is the output object", size=(40, 2), key='-OUTPUT-')]]
    # The settings tab.
    tab2_layout = [[Gooey.T('Your API Key:')],
                   [Gooey.In(key='apiKeyInput', password_char='●'), Gooey.Button('Save', key='-SAVE-')],
                   [Gooey.Checkbox('Use local XML file', key='-useXML-')]]
    # The main layout.
    layout = [
        [Gooey.TabGroup([
            [Gooey.Tab('Main', tab1_layout),
             Gooey.Tab('Settings', tab2_layout)]
        ])],
        [Gooey.Button('Randomize!'), Gooey.Button(
            'Exit')]  # The buttons at the bottom
    ]
    window = Gooey.Window('MAL Randomizer', layout)  # Create the window.

    # Loop listening for GUI events.
    while True:
        event, values = window.read()
        if event in (666, '-no_Movies-'):
            no_movies = True
            only_movies = False
            prevAPIcall = ""
        if event in (666, '-only_Movies-'):
            no_movies = False
            only_movies = True
            prevAPIcall = ""
        if event in (666, '-any_Anime-'):
            no_movies = False
            only_movies = False
            prevAPIcall = ""
        if event in (Gooey.WIN_CLOSED, 'Exit'):
            exit()
        if event == 'Randomize!':
            if values['-useXML-'] == True:
                # do nothing
                break
            else:  # use API.
                APIgetAnimeList(values['-username-'])
                Rnd_title, Rnd_link, Rnd_CoverArt = GetRandomAnime() 
                window['-OUTPUT-'].update(Rnd_title)
                window['-OUTPUT_IMG-'].update(GetCoverArt(Rnd_CoverArt))
    window.close()
# ------------------------------------------------------------------------------
# XML Functions
# ------------------------------------------------------------------------------

    # Prompt user to pick an .xml file from the working directory.
    ListOfXML = (glob.glob('*.xml'))
    while True:
        print('Select an xml file:')
        i = int(0)
        for each in ListOfXML:
            print(i, ':', ListOfXML[i])
            i = (i+1)
        choice = input()
        try:
            choice = int(choice)
            break
        except ValueError:
            print("Invalid input!\n")
    selectedMALfile = ListOfXML[choice]
    print(selectedMALfile, ' selected.\n')
    list_tree = ET.parse(selectedMALfile)
    tree_root = list_tree.getroot()

    # This block populates the list objects from the local xml file.
    # from each <anime> in the xml...
    for anime in tree_root.findall("anime"):
        # where my_status == PTW...
        if anime.find("my_status").text == "Plan to Watch":
            list_titles.append(anime.find("series_title").text +  # append the series_title to ptw_list...
                            " [" + anime.find("series_type").text + "]")  # also include its series_type...
            # then, append its series_animedb_id to ptw_list_id.
            list_id.append(anime.find("series_animedb_id").text)
            if (anime.find("series_type").text == "Movie") and (no_movies == "y"):
                list_titles.pop()
                list_id.pop()
            if (anime.find("series_type").text != "Movie") and (only_movies == "y"):
                list_titles.pop()
                list_id.pop()
