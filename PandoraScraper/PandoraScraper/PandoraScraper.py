from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
import requests
import urllib
import time
import os

def getMP3s(songs, station):
    
    time.sleep(10)
    num = -1
    while num < songs - 1:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        links = soup.findAll('audio')
        try:
            title = soup.find('a', class_ = "Tuner__Audio__TrackDetail__title").contents[0]
            artist = soup.find('a', class_ = "Tuner__Audio__TrackDetail__artist").contents[0]
            album = soup.find('a', class_ = "nowPlayingTopInfo__current__albumName nowPlayingTopInfo__current__link").contents[0]
       
            #coverArt = soup.find('img', attrs={'data-qa': "mini_track_image"}).get("src")
            #coverArt = coverArt.replace('90W', '1080W') #re.sub('90W', '1080W', coverArt)
            #coverArt = coverArt.replace('90H', '1080H') #re.sub('90H', '1080H', coverArt)
            num = links[len(links) - 1].get("id")
            num = int(num[-1:])
            title = str(title)
            title = title.replace('/', '-')
            title = title.replace('\\', '-')
            print(title + " - " + artist + " - " + album)
        except Exception as e:
            print(e)
        
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/span/div/div[2]/div/button").click()
        except Exception as e:
            print(e)

        for link in links:
            #print(link.get("id"))
            try:
                data = urllib.request.urlopen(link.get("src"))

            #coverArtImg = urllib.request.urlopen(coverArt)
                fileName = root + "\\" + title + ".mp3"
                if not os.path.isfile(fileName) and link.get("id")[-1:] == num:
                    file = open(fileName, "wb")
                    file.write(data.read())
                    file.close()

                #print(ID3.Frame(fileName).pprint())
                #audio = MP3(fileName, ID3 = ID3)
                #audio.add_tags()
                #print(ID3.Frame(fileName).pprint())
                #print(audio)
                #audio["title"][0] = title
                #audio["artist"][0] = artist
                #audio["album"][0] = album
                #print(audio["artist"][0])
                #audio.add(id3.APIC(data=coverArtImg.read(), desc="Cover Art"))
                #audio.save(fileName)
            except Exception as e:
                print(e)
        numComp = num #int(links[len(links) - 1].get("id")[-1:])
        print(num)
        while numComp == num and numComp < songs - 1:
            print("sleeping")
            time.sleep(120)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            links = soup.findAll('audio')
            numComp = int(links[len(links) - 1].get("id")[-1:])
            
    driver.close()

def signIn(username, password): #No, I'm not going to steal your data

    login = "https://www.pandora.com/account/sign-in"
    
    driver.get(login)
    driver.implicitly_wait(10)

    usernameField = driver.find_element_by_name('username')
    passwordField = driver.find_element_by_name('password')
    usernameField.send_keys(username)
    passwordField.send_keys(password)
    driver.find_element_by_class_name("Login__form__row__button").click()

    try:
        driver.implicitly_wait(10)
        driver.find_element_by_class_name("ShuffleButton__button--compact--minimal").click()
    except Exception as e:
        print("Could not click shuffle")

station = "https://www.pandora.com/station/play/3860379080856310864"
root = r'C:\Users\drewm\Music\Pandora'
username = 'drewmccutchan@gmail.com'
password = 'drew0998'
driver = webdriver.Chrome(r'C:\Users\drewm\OneDrive\ChromeDriver\ChromeDriver.exe')

signIn(username, password)
getMP3s(1000, station)
