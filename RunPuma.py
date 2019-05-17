import webbrowser
from puma import *
import os
webbrowser.open('http://127.0.0.1:8000')
os.system("python puma/manage.py runserver 127.0.0.1:8000")