import os

def check_dependencies():
    #os.system('pip install biopython')
    pass
    
def make_directories():
    try:
        os.mkdir("output")#os.system('mkdir output')
    except:
        print ("Unable to make directory 'output', it may already exist.")
        
    try:    
        os.mkdir("temp") #os.system('mkdir temp')
    except:
        print ("Unable to make directory 'temp', it may already exist.")
