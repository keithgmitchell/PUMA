import os

def check_dependencies():
    pass
    
def make_directories():
    try:
        os.mkdir("output")
    except:
        print ("Unable to make directory 'output', it may already exist.")
        
    try:    
        os.mkdir("temp")
    except:
        print ("Unable to make directory 'temp', it may already exist.")
