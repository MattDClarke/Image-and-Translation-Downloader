# Image and translation downloader

Simplify your PowerPoint workflow. Type in your search words and get images and translations downloaded automatically.
Image and translation downloader is a Python Selenium web scraping application
that uses Flask. 



## Browser Requirements
- Firefox Browser. 

- Firefox Developer Edition Browser and Tor Browser are used if too many url requests 
are made (If 100s - 1000s of images are downloaded in a short period of time). 



## Full set up instructions for Windows 10

1. Copy project to your pc
2. Install Firefox and Chrome (and Firefox Developer Edition and Tor Browser if many images will be downloaded)
3. Install VSCode and Git (for BASH terminal... so that you can use LINUX commands)
4. Install Python 3.7.5 (not sure if newer versions work...) on PC and Python extension for VSCode (in VSCode 
   Marketplace)
5. Install Node JS (add to PATH then close all files and restart PC)
6. In VSCode, cd into ppt_project file and select python interpreter (ctrl + shift + p) 
7. In VSCode command line: ```npm i```
8. In pyvenv.cfg change home = (your python 3.7 installation path)
9. Create a virtual environment (isolation of packages to environment --> avoids version conflict... best practice)
   In the terminal: ```py -3 -m venv .venv```
   Open venv in new window ```code .```
10. Install pylint 
11. '''pip install --upgrade pip'''
12. ```pip install flask```  web framework
13. ```pip install selenium``` web driver
14. ```pip install requests```  makes HTTP requests easier (get website url, see response, get image from url address)
15. ```pip install pyperclip```   clipboard copy and paste
16. Install Geckodriver onto your PC (v.0.26.0), extract .exe file needed for automated browsing 
17. Add .exe file to your PATH (where python is installed) e.g. C:\Users\user\AppData\Local\Programs\Python\Python37

To run:
```py -m flask run```
