# Downloads translations and images. 

from flask import Flask, redirect, render_template, request
from helpers import apology
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile # for Tor browser
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC # waiting for expected condition ( ect. the input element appears on a website...) 
from selenium.webdriver.common.by import By # selection By ....id, class, ect...
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
import os, requests, re, sys, time, pyperclip


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded - obtained from CS50 finance problem set
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached - obtained from CS50 finance problem set
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":

        # get number of images (1-20) for each search query and translation language
        imagesNumber = int(request.form.get("imageQueryNo"))
        translationLang = request.form.get("language")

        # makes a list from all the form elements with name="word" <-- VERY USEFUL
        wordsListRaw = request.form.getlist("word")

        # remove leading and trailing white space for each search query. Make a new list
        wordsList = []
        for item in wordsListRaw:
            newItem = item.strip() # need to create new string... strings are immutable
            wordsList.append(newItem)

        # ensure no empty words input (server side input check )
        for i in range(len(wordsList)):
            if wordsList[i] == '':
                return apology("Must enter search query in each input box", 400)

        # join words to translate into a single string \n separated... easy to write all to .txt file
        wordsToTranslate = '\n'.join(wordsList)

        # create language name from lang url (for text file). There is probably a better way to write this...
        langName = ""
        if translationLang =="ko&hn=1":
            langName = "Korean (Honorific)"
        if translationLang =="ko&hn=0":
            langName = "Korean (Informal)"
        if translationLang =="ja":
            langName = "Japanese"
        if translationLang =="zh-CN":
            langName = "Chinese (Simplified)"
        if translationLang =="zh-TW":
            langName = "Chinese (Traditional)"
        if translationLang =="es":
            langName = "Spanish"
        if translationLang =="fr":
            langName = "French"
        if translationLang =="de":
            langName = "German"
        if translationLang =="ru":
            langName = "Russian"
        if translationLang =="pt":
            langName = "Portuguese"
        if translationLang =="it":
            langName = "Italian"
        if translationLang =="vi":
            langName = "Vietnamese"
        if translationLang =="th":
            langName = "Thai"
        if translationLang =="id":
            langName = "Indonesian"
        if translationLang =="hi":
            langName = "Hindi"


        # makes folder and prevents function causing an error if the folder already exists. Overwrites any previous translations 
        os.makedirs('C:\multiImageSearchDownloads', exist_ok=True)

        # Selenium setup
        # make webbdriver headless (does not open GUI)
        options = Options()
        options.headless = False  # headless was not working for translations... Selenium could not click the copy button to copy the translations
        # FirefoxBinary class is used to find Firefox exe (executable binary... start Firefox)
        binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
        # DesiredCapabilities is a class used to set the properties of the browser e.g. set browser name, platform, browser version
        caps = DesiredCapabilities().FIREFOX
        # GeckoDriver is an exe that will start the Mozilla Firefox browser. Marionette is an automation driver, it uses the remote protocol of Firefox
        # (to control the UI). Marionette accepts requests and executes them in Gecko
        caps["marionette"] = True


        # DOWNLOADING TRANSLATIONS
        # setup webbdriver
        print("Downloading translations...")
        browser = webdriver.Firefox(capabilities=caps, firefox_binary=binary, options=options)

        # make search query, concatenate search queries with %0A (adds empty line after each item)
        url = 'https://papago.naver.com/?sk=en&tk=' + translationLang + '&st=' + '%0A'.join(wordsList)
        # load search query
        browser.get(url)
        
        # wait for translation (each translation is within a span element)
        WebDriverWait(browser, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".edit_box___1KtZ3.active___3VPGL span")))

        # click on clipboard copy button (there are 2... second one copies translated text)
        textCopyButtons = browser.find_elements_by_class_name("btn_copy___3T223")

        # click close on pop-up banner (if there)
        try:
            browser.find_element_by_class_name("evt_close___2B5rg").click()
        except:
            print("No pop-up banner (or different one or class name changed...)")
        finally:
            textCopyButtons[1].click()
            # save translated words that were copied to the clipboard (paste to pyperclip clipboard)
            text = str(pyperclip.paste())
            textNew = text.replace('\n', '') # papago clipboard copy has empty lines... found emperically... newline can be \n or \r or \r\n\... mac or pc...
 
            # overwrites file if it exists
            with open("C:\multiImageSearchDownloads\\translation.txt", "w", encoding="utf-8") as file:  # needs the encoding... else issue with Hangul (and prob other languages)
                writer = file.write("\nEnglish words:\n")
                writer = file.write(wordsToTranslate)
                writer = file.write("\n\nTranslated" + " " + langName + " words:\n")
                writer = file.write(textNew)

            print("Translations downloaded")

            # count the number of new tabs
            windowCount = 0


        # DOWNLOADING IMAGES
        print("Downloading images...")
        # extract file extension (only jpg, jpeg, gif, png, bmp) may be capitalized...(does not need to be in for loop)
        fileExtensionRegex = re.compile(r'\.jpg|\.gif|\.png|\.bmp|\.jpeg', re.IGNORECASE)

        # loop through each item in the search query list
        for i in wordsList:

            # Open a new window
            browser.execute_script("window.open('');")
            # count the number of new tabs
            windowCount += 1
            # Switch to the new window 
            browser.switch_to.window(browser.window_handles[windowCount])

            listCount = wordsList.index(i) + 1
            listLen = len(wordsList)
            # make search query, make the image wide, free to share and use (select required properties in bing image search and check url)
            url = 'https://www.bing.com/images/search?q=' + ''.join(i) + '&qft=+filterui:aspect-wide+filterui:license-L2_L3_L4_L5_L6_L7+filterui:imagesize-large&FORM=IRFLTR' 
            print("Getting images for search query %i of %i: %s" % (listCount, listLen, i))
            browser.get(url)

            # find all image thumbnails (store in a list)
            for j in range(imagesNumber): 
                # image number counter
                imageCount = j + 1
                print("downloading image %s of %s..." % (imageCount, imagesNumber))

                # try clicking back button again... sometimes back button does not work... 
                browser.execute_script("window.history.go(-1)")

                # get a list of all image thumbnails
                try:
                    imageThumbList = WebDriverWait(browser, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".mimg")))
                except Exception:
                    print('There was a problem locating the image thumbnails') 
                    print("Thumbnail number %i (zero indexed) could not be located..." % (j))
                    # Sometimes browser opens on first image and back click does not work... 2nd image does not download
                    continue            

                # click on jth image
                try:
                    imageThumbList[j].click()
                except Exception:
                    print('There was a problem clicking on the jth image')
                    continue

                currentUrl = browser.current_url
                
                # try clicking back button again... sometimes back button does not work... 
                browser.execute_script("window.history.go(-1)")

                fileExtensionMatch = fileExtensionRegex.search(currentUrl)
                try:
                    fileExtension = fileExtensionMatch.group()
                except Exception:
                    print('No img url to extract')
                    continue
                

                # find url between &mediaurl= and the file extension.
                # greedy match (python regexes are greedy by default)... finds longest match (this deals with wikimedia images that seem to often have .jpg 2x in the url)
                subStrList = re.findall(r'(?<=&mediaurl=).*(?={})'.format(fileExtension), currentUrl)
                try:
                    subStr = subStrList[0]
                except IndexError:
                    print("Image url %s of %s could not be found" % (imageCount, imagesNumber))
                    continue

                # replace characters (uppercase and lowercase... case may change)
                subStr = subStr.replace("%3a%2f%2f", "://").replace("%2f", "/").replace("%2b", "+").replace("%e2%80%93", "-").replace("%25e2%2580%2593", "–").replace("%2528", "(").replace("%2529", ")").replace("%2c", ",").replace("%3A%2F%2F", "://").replace("%2F", "/").replace("%2B", "+").replace("%E2%80%93", "-").replace("%25E2%2580%2593", "–").replace("%2C", ",")
                subStr = subStr.replace("%25", "%").replace("%2c", ",").replace("%2C", ",") # the url encoding of % is %25... found this through a problem... website double decoded...
                newSubStr = subStr + "".join(fileExtension)
                # make image name
                imageName = str(listCount) + ". " + i + " " + str(imageCount) + fileExtension


                # open a new window in FireFox Developer Edition (using Tor) if Max Retries Error occurs
                # (Tor uses a different ip) --> slower and opens each new word search in a new window (not tab). 
                # reference: https://stackoverflow.com/questions/53696032/accessing-tor-with-selenium-in-python
                try:
                    res = requests.get(newSubStr)
                except:
                    print("Connection refused by the server...")
                    print("Let me sleep for 10 seconds")
                    print("ZZZzzz...")
                    time.sleep(10)

                    print("Open tor browser in Firefox Developer Edition and try continue...(changes ip address)")     
                    torexe = os.popen(r"C:\Program Files (x86)\Tor Browser\Browser\TorBrowser\Tor\tor.exe")
                    profile = FirefoxProfile(r"C:\Program Files (x86)\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default")
                    # Configure Tor as PROXY (proxy server btn me and internet, SOCKS is the protocol for exchanging network packets thro proxy server) Tor listens for SOCKS connections on Port 9050
                    profile.set_preference('network.proxy.type', 1)
                    profile.set_preference('network.proxy.socks', '127.0.0.1')
                    profile.set_preference('network.proxy.socks_port', 9050)
                    profile.set_preference("network.proxy.socks_remote_dns", False)
                    profile.update_preferences()
                    # opens FireFox Developer Edition...
                    driver = webdriver.Firefox(firefox_profile= profile, executable_path=r'C:\Utility\BrowserDrivers\geckodriver.exe')
                            
                    browser.get(url)
                    # number of tabs open
                    windowCount = 0
                    continue

                try:
                    res.raise_for_status()
                    # handle errors (if any)
                except Exception as exc:
                    # Some urls forbidden...
                    print('There was a problem: %s' % (exc))
                    print("Downloading image url %s of %s failed" % (imageCount, imagesNumber))
                    continue
                        
                # download image, save it in the multiImageDownloads file
                try:
                    imageFile = open(os.path.join('C:\multiImageSearchDownloads', imageName), 'wb') 
                    # save file, one chunk at a time
                    for chunk in res.iter_content(100000):
                        imageFile.write(chunk)
                    imageFile.close()
                except Exception as exc:
                    print("There was a problem: %s" % (exc))
                    continue


        # if you want to close the browser afterwards...
        # browser.quit()
        # browser.stop_client() 

        print("Download complete")

        # redirect to download complete page ...flash did not work... copies message to clipboard... interfers with pyperclip
        return redirect("/complete")


@app.route("/complete")
def complete():
    return render_template("complete.html")

@app.route("/downloader")
def downloader():
    return render_template("downloader.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
