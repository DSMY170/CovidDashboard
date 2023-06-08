#Request module is used for making HTTP requests call to covid-19 API
import requests
from tkinter import *
import json
import speech_recognition as sr
from PIL import Image,ImageTk
import random
from time import sleep
import os

#os.chdir("./COVID_TRACKER")

countryNames = []

#This function is used to make http call to grab covid-19 data
def grabApiData():
    global countryNames
    #This variable stores respons object of our api when its called
    
    try:
        response1 = requests.get("https://disease.sh/v3/covid-19/all/")
        response = requests.get("https://disease.sh/v3/covid-19/countries/")
        #our response is then converted to JSON (Javascript object notation)
        data = response.json()
        data1 = response1.json() 

        for d in data:
            countryNames.append(d["country"].lower())
        
        data , data1 = list(data), dict(data1)
        data1["country"] = "the world"
        data1["countryInfo"] =  {
            "flag": "https://www.burningcompass.com/world/maps/world-map.jpg"
        }
        data.append(data1)
        
        print(len(data))
        with open("data.json","w") as jsFile:
            jsFile.write(json.dumps(data,indent=4))

        return data
    except: 
        with open("./data.json","r") as json_file:
            data = json.loads(json_file.read())

            for d in data:
                countryNames.append(d["country"].lower())
            
            return data
    
#This function grabs covid data of a specific country from the JSON data of countries
def getCountry(country :str):
    covid_data = grabApiData()

    countryData = dict()

    for data in covid_data:
        if data["country"].lower() == country.lower():
            countryData = data
    
    return countryData


# This func fetches logo of country
def loadCountryImage(country :str):
    # if country == "world":
    #     return requests.get("https://www.pngmart.com/files/5/World-PNG-HD.png", stream = True).raw
    # else:
    countryData = getCountry(country)

    try:
        return  requests.get(countryData["countryInfo"]["flag"], stream = True).raw
    except:
        return "virusD.png"
    #_ = Image.open(countryImg).save("CountryLogo.png")
    

#This function controls our GUI in Tkinter
def interface(anyCountry :str):
    #Here we are creating window by instantiating the Tkinter class
    window = Tk()

    #We are then specifying the height and with of our window
    window.geometry("1500x1500")

    #This displays a title on our user interface
    window.title("MY COVID-19 Dashboard")

    window.configure(bg="black")

    # Here we are using a label widget to display text on our GUI
    heading1 = Label(window,text="COVID-19 Report for various Countries ",font=("Courier New",20,"bold","underline"),width=50,height=1,fg="white")

    # We are then specifying the position of our label so we can center it alongside giving a space on the y axis
    heading1.config(anchor=CENTER, bg="black")
    heading1.pack(pady=10)

    # making three(3 divisions)
    flagslabel = Frame(window).pack(side= LEFT)
    caseDispLabel = Frame(window).pack(side= LEFT)
    selectCountryLabel = Frame(window).pack(side= LEFT)

    #Here we use the PIL module to display an image
    img = Image.open("virusE.png").resize((255,255))
    img = ImageTk.PhotoImage(img)
    img1 = Label(flagslabel, image=img)
    img1.place(x=25,y=70)

    #loadCountryImage(anyCountry)
    img2 = Image.open(loadCountryImage(anyCountry)).resize((255,255))
    img2 = ImageTk.PhotoImage(img2)
    img21 = Label(flagslabel, image=img2)
    img21.place(x=25,y=140+255)

    #Here we are passing an argument to our getCountry function in order to grab all world cases and displaying them using labels
    CountryCase = getCountry(anyCountry)

    k = "Statistics in "+CountryCase["country"].capitalize()
    countryHeader = Label(caseDispLabel,text=k,font=("Times Bold",20), fg="white")
    countryHeader.config(bg="black")
    countryHeader.place(x=400,y=70)
    
    lbtotalCases = Label(caseDispLabel, text="   Total Cases :".center(len(k)+(len(k)-10)), font=("Roquen", 16,"bold"),fg="#2dc7c7",bg="black")
    lbtotalCases.place(x=410,y=120)

    totalCases = Label(caseDispLabel,text=str("{:,}".format(CountryCase["cases"])).center(len(k)+(len(k)-10)//2),font=("Roquen",25,"bold"),fg="bisque",bg="black")
    totalCases.place(x=400,y=150)

    lbtotalDeaths = Label(caseDispLabel, text="   Total Deaths :".center(len(k)+(len(k)-10)), font=("Roquen", 16,"bold"),fg="red",bg="black")
    lbtotalDeaths.place(x=410,y=190)

    totalDeaths = Label(caseDispLabel,text=str("{:,}".format(CountryCase["deaths"])).center(len(k)+(len(k)-10)//2),font=("Roquen",25,"bold"),fg="bisque",bg="black")
    totalDeaths.place(x=400,y=220)

    lbtodayCases = Label(caseDispLabel, text="   Today's Cases :".center(len(k)+(len(k)-10)), font=("Roquen", 16,"bold"),fg="gold",bg="black")
    lbtodayCases.place(x=410,y=260)

    todayCases = Label(caseDispLabel,text=str("{:,}".format(CountryCase["todayCases"])).center(len(k)+(len(k)-10)//2),font=("Roquen",25,"bold"),fg="bisque",bg="black")
    todayCases.place(x=400,y=290)

    lbrecovered = Label(caseDispLabel, text="   Recovered Cases :".center(len(k)+(len(k)-10)), font=("Roquen", 16,"bold"),fg="greenyellow",bg="black")
    lbrecovered.place(x=410,y=330)

    recovered = Label(caseDispLabel,text=str("{:,}".format(CountryCase["recovered"])).center(len(k)+(len(k)-10)//2),font=("Roquen",25,"bold"),fg="bisque",bg="black")
    recovered.place(x=400,y=360)

    if anyCountry != "the world":
        lbrisk = Label(caseDispLabel, text="Risk Of Contraction (Cases Per People) :".center(len(k)+(len(k)-10)), font=("Roquen", 18,"bold"),fg="turquoise",bg="black")
        lbrisk.place(x=370,y=450)

        risk = Label(caseDispLabel,text=str("{:,}".format(CountryCase["oneCasePerPeople"])).center(len(k)+(len(k)-10)//2),font=("Roquen",30,"bold"),fg="bisque",bg="black")
        risk.place(x=400,y=480)
    else:
        lbrisk = Label(caseDispLabel, text="   Affected Countries:".center(len(k)+(len(k)-10)), font=("Roquen", 18,"bold"),fg="turquoise",bg="black")
        lbrisk.place(x=410,y=450)

        risk = Label(caseDispLabel,text=str("{:,}".format(CountryCase["affectedCountries"])).center(len(k)+(len(k)-10)//2),font=("Roquen",30,"bold"),fg="bisque",bg="black")
        risk.place(x=400,y=480)


    # the input field for Differnet countries
    searchField = Canvas(selectCountryLabel, width=400, height=400, relief='raised',bg="#1e0a5a")
    searchField.place(x=900,y=150)

    label1 = Label(selectCountryLabel, text='Search for other countries',bg="#1e0a5a",fg="bisque")
    label1.config(font=('helvetica', 15))
    searchField.create_window(200, 25, window=label1)

    label11 = Label(selectCountryLabel, text='Select Search method',bg="#1e0a5a",fg="bisque")
    label11.config(font=('helvetica', 15))
    searchField.create_window(200, 65, window=label11)

    options = [
        "Use text",
        "Use audio"
    ]

    clicked = StringVar()

    clicked.set(options[0])

    drop = OptionMenu(selectCountryLabel, clicked ,*options)
    searchField.create_window(200, 115, window=drop, width = 150,height = 40)

    # Create button, it will change label text
    button = Button(selectCountryLabel, text = "Done" , command = lambda : [configureSelection(clicked.get())], bg="green", fg="white")
    searchField.create_window(330, 115, window=button, width = 70,height = 40)

    label2 = Label(selectCountryLabel, text=' ',bg="#1e0a5a",fg="bisque")
    label2.config(font=('helvetica', 15))
    searchField.create_window(200, 155, window=label2)

    entry1 = Entry(selectCountryLabel,bg="#1e0a5a") 
    searchField.create_window(200, 205, window=entry1)
    
    submit = Button(selectCountryLabel, text = "Search" , command = "",bg="#1e0a5a")
    searchField.create_window(200, 255, window=submit, width = 90,height = 40)
    
   
    # This func records user input sound
    def get_audio():
        r = sr.Recognizer()
        myMic = sr.Microphone(device_index=1)
        said = ""
        with myMic as source:
            print("Wooorrrking!!")
            print("Record Voice...")
            audio = r.listen(source)

            try:
                said = r.recognize_google(audio)
                #label2.config(text=said)
                print(said)
                
            except Exception as e:
                print("Exception: err")
            
            label2.config(text="Voice Recorded...")
            said = said.lower()  if said.lower() in countryNames else anyCountry 
            entry1.delete(0,END)
            entry1.insert(0,said)

    # This function evaluated ropdown menu options
    def configureSelection(selection :str):
        if selection.find("text") >= 0:
            label2.config(text="Enter country name")
            entry1.configure(bg="white", fg="black")
            
            submit.configure(bg="green", fg="white") 
            submit.configure(command=lambda : [makeQuery(entry1.get())])
        
        elif selection.find("audio") >= 0:
            label2.config(text="Click record")
            entry1.configure(fg="white", bg="black")
            submit.configure(bg="green", fg="white") 
            submit.configure(command=lambda : [makeQuery(entry1.get())])
            
            record = Button(selectCountryLabel, text = "Record", command = lambda : [get_audio()], bg="green", fg="white")
            searchField.create_window(200, 305, window=record, width = 90,height = 40)
                   
    # This function enables us to query the data
    def makeQuery(name :str):
        window.destroy()
        if name.lower() in countryNames:
            print("here")
            interface(name)
        else:

            interface(anyCountry)
    

        # submit = Button(selectCountryLabel, text = "Search" , command= lambda : [makeQuery(entry1.get())])
        # searchField.create_window(200, 235, window=submit, width = 90,height = 40)


    window.mainloop()


grabApiData()
interface("the world")

