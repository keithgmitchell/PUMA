import webbrowser
import subprocess

webbrowser.open('http://127.0.0.1:8000')
subprocess.call(['python', 'puma/manage.py', 'runserver', '127.0.0.1:8000'])

