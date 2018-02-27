from bs4 import BeautifulSoup
from shutil import move
from selenium import webdriver
import selenium
import requests
import urllib
import time
import eyed3
import os

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
       
            coverArt = soup.find('img', attrs={'data-qa': "mini_track_image"}).get("src")
            coverArt = coverArt.replace('90W', '1080W') #re.sub('90W', '1080W', coverArt)
            coverArt = coverArt.replace('90H', '1080H') #re.sub('90H', '1080H', coverArt)

            num = links[0].get("id")
            num = int(num[-1:])
            #print("Num " + str(num))

            title = str(title)
            title = title.replace('/', '-')
            title = title.replace('\\', '-')
            print(title + " - " + artist + " - " + album)
        except Exception as e:
            print(e)
        
        try:
            driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/span/div/div[2]/div/button").click() #Try to click still listening
            print("Still Listening")
        except Exception as e:
            pass

        link = links[0]
        #print("ID:" + link.get("id"))
        #print("Matches num " + str(num) + " : " + str(int(link.get("id")[-1:]) == num))
        try:
            data = urllib.request.urlopen(link.get("src"))
            coverArtImg = urllib.request.urlopen(coverArt)

            fileName = root + "\\" + title + '-' + artist + '-' + album + ".mp3"
            artName = root + "\\" + title + '-' + artist + '-' + album + ".jpg"

            if not os.path.isfile(fileName) and int(link.get("id")[-1:]) == num:
                file = open(fileName, "wb")
                img = open(artName, "wb")
                file.write(data.read())
                img.write(coverArtImg.read())
                file.close()
                img.close()
            else:
                print("Didn't write")

        except Exception as e:
            print(e)

        numComp = num #int(links[len(links) - 1].get("id")[-1:])
        print(num)
        while numComp == num and numComp < songs - 1:
            print("Sleeping")
            time.sleep(120)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            links = soup.findAll('audio')
            numComp = int(links[len(links) - 1].get("id")[-1:])
            
    driver.close()

def writeTags():
    files = os.listdir(root)
    mp3s = []
    for file in files:
        if file.endswith('.mp3'):
            mp3s.append(file)

    pieces = []
    for mp3 in mp3s:
        pieces = mp3.split('-')

        song = pieces[0]
        artist = pieces[1]
        album = pieces[2]

        audioFile = eyed3.load(os.path.join(root, mp3))
        audioFile.initTag()

        audioFile.tag.artist = artist
        audioFile.tag.album = album
        audioFile.tag.album_artist = artist
        audioFile.tag.title = song
        audioFile.tag.save(os.path.join(root, mp3))

def sortMP3s(): #Sort files into folders by album to include cover art
    files = os.listdir(root)
    mp3s = []
    for file in files:
        if file.endswith('.mp3'):
            mp3s.append(file)

    for mp3 in mp3s:
        pieces = mp3.split('-')

        song = pieces[0] + '.mp3'
        artist = pieces[1]
        album = pieces[2][:-4]
        if not os.path.isdir(os.path.join(root, album)):
            os.mkdir(os.path.join(root,album))

        if not os.path.exists(os.path.join(root, album, album + '.jpg')):
            move(os.path.join(root, mp3[:-3] + 'jpg'), os.path.join(root, album, album + '.jpg'))
        
        move(os.path.join(root, mp3), os.path.join(root, album, song))


station = "https://www.pandora.com/station/play/3860379080856310864"
root = r'C:\Users\mmccutchan\Music\Pandora'
username = 'drewmccutchan@gmail.com'
password = 'drew0998'
driver = webdriver.Chrome(r'C:\Users\mmccutchan\OneDrive\ChromeDriver\ChromeDriver.exe')

signIn(username, password)
getMP3s(1000, station)
writeTags()
sortMP3s()