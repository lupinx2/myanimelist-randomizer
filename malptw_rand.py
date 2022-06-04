# Returns a random anime from your MAL Plan-to-Watch list
# Using either the API or a local xml file.
#
# TODO
# Update readme with pictures
#
# Test with: Debian / fresh python install / no internet.
# Test if no_movies and only_movies are working correctly.
#  or rename only_movies to exclude_tv shows isntead.
#
# XML:
#   XML files do not contain cover art links,
#    so currently GetRandomAnime() breaks in XML mode. 
#    so might need to use the API to get the cover art.
#
#   Improve output formatting, style.
#       Add placeholder cover art?
#       Add link to MAL page/streaming.
#       Make cover art clickable?
#       Enter button to randomize
# 
#  Add manga support?
#  pick one, Cover, CoverArt, or img; not all three.
#
#  Add non-Naruto based exception handling.
#    no, but seriously the exception handling is a mess.
#    make every except clause pass an error code to a function that prints the error.
#
#  preserve some settings between runs (e.g. xml file), use config file.
#
#  Forced image size is not working correctly.

from json import loads as jsonLoads
import xml.etree.ElementTree as ET
import PySimpleGUI as Gooey # pip isntall pysimplegui
from random import randint
from config import API_key
from time import sleep
from PIL import Image # pip isntall pillow
import requests
import io


if __name__ == '__main__':

    list_titles = list()
    list_id = list()
    list_coverImg = list()
    no_movies = False
    only_movies = False
    prevAPIcall = ""

# ------------------------------------------------------------------------------
# API Functions - Maintain feature parity with XML functions.
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
                if response.status_code == 404:
                    window.Element('-OUTPUT-').Update('Username not found.')
                    return
                else:
                    raise Exception("API call error")
            responseBytes = (response.content)
            responseString = responseBytes.decode("utf-8")
        except:
            window.Element('-OUTPUT-').Update("Error: API call failed Status code: " + str(response.status_code))
        # convert response to dictionary
        outputDict = jsonLoads(responseString)
        # Clear the lists when username or settings change
        list_titles.clear()
        list_id.clear()
        list_coverImg.clear()
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
            #list_titles.append(item['title'] + " [" + item['media_type'] + "]") # old version
            list_titles.append(item['title'])
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

# ------------------------------------------------------------------------------
# XML Functions - Maintain feature parity with API functions.
# ------------------------------------------------------------------------------

    # Pull anime list from MAL xml file, save directly to lists.
    def XMLgetAnimeList(XMLfile):
        list_tree = ET.parse(XMLfile)
        tree_root = list_tree.getroot()
        for anime in tree_root.findall("anime"):# from each <anime> in the xml...
            if anime.find("my_status").text == "Plan to Watch":# where my_status == PTW...
                list_titles.append(anime.find("series_title").text )  # append the series_title to ptw_list...
                list_id.append(anime.find("series_animedb_id").text)# then, append its series_animedb_id to ptw_list_id.
                if (anime.find("series_type").text == "Movie") and (no_movies == True):
                    list_titles.pop()
                    list_id.pop()
                if (anime.find("series_type").text != "Movie") and (only_movies == True):
                    list_titles.pop()
                    list_id.pop()

    # Get URL for cover art of a single anime, using the API.
    def XMLgetCoverURL(animeID):
        try:
            url = 'https://api.myanimelist.net/v2/anime/' + str(animeID) + '?fields=main_picture'
            headers = {'X-MAL-CLIENT-ID': API_key}
            sleep(0.5)  # Sleep to prevent rate limiting.
            response = requests.get(url, headers=headers)            
            if response.status_code != 200:
                if response.status_code == 404:
                    window.Element('-OUTPUT-').Update('Error: cover art not found.')
                    return
                else:
                    raise Exception("API call error")
            responseBytes = (response.content)
            responseString = responseBytes.decode("utf-8")
        except:
            window.Element('-OUTPUT-').Update("Error: API call failed Status code: " + str(response.status_code))
        outputDict = jsonLoads(responseString)
        return outputDict['main_picture']['medium']
        

# ------------------------------------------------------------------------------
# Output Functions
# ------------------------------------------------------------------------------

    # Returns a tuple with the title, MAL page, and URL for the cover art.
    def GetRandomAnime():
        try:
            rand_index = randint(0, len(list_titles)-1)
            if values['-useXML-'] == True:
                return "{}".format(list_titles[rand_index]), \
                    ('https://myanimelist.net/anime/' + str(list_id[rand_index])), \
                    XMLgetCoverURL(list_id[rand_index])
            else:
                return "{}".format(list_titles[rand_index]), \
                    ('https://myanimelist.net/anime/' + str(list_id[rand_index])), \
                    list_coverImg[rand_index]
        except:
            # on an error, the randomizer returns Naruto.
            return "Error: Failed to get anime from PTW list.", \
                "https://myanimelist.net/anime/20", \
                "https://api-cdn.myanimelist.net/images/anime/13/17405l.jpg"

    # Returns png image of the cover art from the URL.
    def GetCoverArt(coverURL):
        try:
            url = coverURL
            response = requests.get(url, stream=True)
            response.raw.decode_content = True
        except:
            raise("Error: Failed to get cover art.")
        try:
            # get jpg formated bytes from response
            jpg_img = Image.open(io.BytesIO(response.content))
            png_img = io.BytesIO()  # create BytesIO object to store png
            # convert jpg data to png format
            jpg_img.save(png_img, format="PNG")
            png_data = png_img.getvalue()  # create return object
            return png_data
        except:
            raise("Error: Failed jpg to png conversion.")

# ------------------------------------------------------------------------------
# GUI
# ------------------------------------------------------------------------------
    # This is spaghetti code, clean it up later.
    Gooey.theme('LightGrey1')
    # The main tab.
    tab1_layout = [[Gooey.Text('MAL username:'),
                     Gooey.InputText(key='-username-', right_click_menu=[[''], ['Paste Username']])],
                   [Gooey.Radio("Exclude Movies", 666, False, False, key='-no_Movies-'),  # Radio buttons
                     Gooey.Radio("Only Movies", 666, False, False, key='-only_Movies-'),
                     Gooey.Radio("Any anime", 666, True, False, key='-any_Anime-')],  # <-default selection
                   [Gooey.Image(key="-OUTPUT_IMG-",size=(61,85)), Gooey.Text("", font='Verdana 13 bold', size=(35, 2), key='-OUTPUT-')]]
    # The settings tab.
    tab2_layout = [[Gooey.T('Your API Key:'),
                     Gooey.In(key='-apiKeyInput-', default_text=API_key , password_char='●', right_click_menu=[[''], ['Paste API key']]),
                     Gooey.Button('Save', key='-SAVE-')],
                   [Gooey.Checkbox('Use local XML file', key='-useXML-'),
                     Gooey.Input(key='-XMLfileInput-'), Gooey.FileBrowse()],
                   [Gooey.Checkbox('Show mean score', key='-ShowScore-')],
                   [Gooey.Checkbox('Show additional info', key='-ShowInfo-')], # episodes, duration, rating, (genres/themes?)
                   [Gooey.Checkbox('Show english title', key='-ShowEnglish-')]]
    # The main layout.
    layout = [
        [Gooey.TabGroup([
            [Gooey.Tab('Main', tab1_layout),
              Gooey.Tab('Settings', tab2_layout)]
        ])],
        [Gooey.Push(), Gooey.Button('Randomize!'), Gooey.Button(
            'Exit')]  # The buttons at the bottom
    ]
    window = Gooey.Window('MAL Randomizer', layout)  # Create the window.

    # Loop listening for GUI events.
    while True:
        event, values = window.read()
        if event == 'Paste Username':
            window['-username-'].update(Gooey.clipboard_get(), paste=True)
        if event == 'Paste API key':
            window['-apiKeyInput-'].update(Gooey.clipboard_get(), paste=True)
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
            if values['-useXML-'] == True: # use local XML file
                try:
                    XMLgetAnimeList(values['-XMLfileInput-'])
                except:
                    window['-OUTPUT-'].update("Error: Failed to parse XML file.")
                if not list_titles and not list_id: # if the lists are empty after parsing the xml
                    window['-OUTPUT-'].update("Error: No anime found in XML file.")
                else:
                    Rnd_title, Rnd_url, Rnd_CoverURL = GetRandomAnime()
                    window['-OUTPUT_IMG-'].update(GetCoverArt(Rnd_CoverURL))
                    window['-OUTPUT-'].update(Rnd_title)
            else:  # use API.
                try:
                    APIgetAnimeList(values['-username-'])
                except: # if the API call fails, return Naruto.
                    window['-OUTPUT_IMG-'].update(GetCoverArt( \
                        "https://api-cdn.myanimelist.net/images/anime/13/17405l.jpg"))
                    continue
                if not list_titles and not list_id and not list_coverImg:# if the list is empty after API call
                    prevAPIcall = values['-username-']
                    window['-OUTPUT-'].update("Error: No anime found in PTW list.")
                else: # if the API call was successful 
                    Rnd_title, Rnd_link, Rnd_CoverURL = GetRandomAnime()
                    window['-OUTPUT-'].update(Rnd_title)
                    window['-OUTPUT_IMG-'].update(GetCoverArt(Rnd_CoverURL))
        if event in ('-SAVE-'):
            API_key = values['apiKeyInput']
            with open('config.py', 'w') as file:
                file.write("API_key = \"" + API_key + "\"")
    window.close()
