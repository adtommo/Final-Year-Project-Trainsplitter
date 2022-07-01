#File Purpose: -Gathers all the data files into relevant folders
import requests, json, io, zipfile, shutil, os

def token(u,p): #Gets the token to request data
    # defining the api-endpoint  
    URL = "https://opendata.nationalrail.co.uk/authenticate"
    # data to be sent to api 
    data = {'Content-Type':'application/x-www-form-urlencoded', 
            'Accept':'application/json, text/plain, */*', 
            'username':u,
            'password':p} 
    # sending post request and saving response as response object 
    r = requests.post(url = URL, data = data) 
    # extracting response text  
    json_data = r.text
    get_data = json.loads(json_data)
    return get_data["token"] #The generated token

def timetable(): #used for switcher
    return '.MCA'
def fares():    #used for switcher
    return '.NFO'

def switcher_data(argument): #switcher used for erasing data
    switcher = {
    'timetable':'.MCA',
    'fares':'.NFO'
    }
    return switcher.get(argument, "Invalid")

def erase_old(data):
    for file in os.listdir(os.getcwd()+'\\'+data):  #The fares/timetable folder
        if file.endswith(switcher_data(data)):      #Uses switcher to check if file in folder
            shutil.rmtree(os.getcwd() + '\\'+data)  #If the file is in the folder it will delete
                                                    #all contents of the folder
def get_data_files(u,p):
    data_list = ['timetable','fares']
    for data in data_list:
        erase_old(data)
        auth_token = token(u,p)
        if data == "timetable":
            URL = "https://opendata.nationalrail.co.uk/api/staticfeeds/3.0/timetable"
        if data == "fares":
            URL = "https://opendata.nationalrail.co.uk/api/staticfeeds/2.0/fares"

        # sending post request and saving response as response object 
        r = requests.get(url = URL, headers = {'X-Auth-Token':auth_token,'Content-Type':'application/json','Accept':'*/*'}) 
        # extracting response text  
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall("./"+data)
        
get_data_files('adam.tommo@hotmail.co.uk','RedDog1029!')
#Requires for user to register at https://opendata.nationalrail.co.uk/ to get
# username and password to gather data
