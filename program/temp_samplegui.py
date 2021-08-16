# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 20:16:09 2021

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 20:40:54 2021

@author: Admin
"""

import PySimpleGUI as sg

import cv2
import mediapipe as mp

from pygame import mixer
from PIL import Image, ImageTk
import time
import os
import sys
import io
import eyed3
from mutagen.mp3 import MP3



import math
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


mixer.init()
t = time.time()
t1,t2=0,0
progresstime=0
duration=0
song=None


song_num = 0
a=None
call = False

filepath = []
#dir_path = os.path.dirname(os.path.realpath(__file__))

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

def play(alb):
    mixer.music.load(alb)
    mixer.music.play()
    
def pause():
    mixer.music.pause()
    
def resume():
    mixer.music.unpause()

def stop():
    mixer.music.stop()
    
def get_img_data(f, maxsize=(1200, 850), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    img = img.resize((150,150))
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

def funcButton(key_,img_name):
    return(sg.B('',key=key_,button_color=(sg.theme_background_color(), sg.theme_background_color()),image_filename=img_name, image_size=(50, 50), image_subsample=2, border_width=0))

def findHandLandMarks(originalImage,image, handNumber=0, draw=False):
    
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # mediapipe needs RGB
    results = hands.process(image)
    landMarkList = []

    if results.multi_hand_landmarks:  # returns None if hand is not found
        hand = results.multi_hand_landmarks[handNumber] #results.multi_hand_landmarks returns landMarks for all the hands

        for id, landMark in enumerate(hand.landmark):
            # landMark holds x,y,z ratios of single landmark
            imgH, imgW, imgC = originalImage.shape  # height, width, channel for image
            xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
            landMarkList.append([id, xPos, yPos])

        if draw:
            mpDraw.draw_landmarks(originalImage, hand, mpHands.HAND_CONNECTIONS)
            #cv2.imshow('original',originalImage)
    else:
        #cv2.destroyAllWindows()
        pass
    return landMarkList

for root, dirs, files in os.walk('D:\\proj_songs'):#dir_path
    for file in files: 
  
        # change the extension from '.mp3' to 
        # the one of your choice.
        if file.endswith('.mp3'):
            #print (root+'/'+str(file))
            filepath.append(root+'/'+str(file))
            
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# This bit gets the taskbar icon working properly in Windows
if sys.platform.startswith('win'):
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'CompanyName.ProductName.SubProduct.VersionInformation') # Arbitrary string

read_button = sg.ReadFormButton('',key='-playpause-', bind_return_key=True,button_color=(sg.theme_background_color(), sg.theme_background_color()),image_filename='play.png',image_size=(50, 50), image_subsample=2, border_width=0)

layout1 = [
            [sg.Text('sample 1'),sg.Text(size=(40,1),key='-output1-')],[sg.Button('ok',key='-button1-')],[sg.Text('sample 2'),sg.Text(size=(20,1),key='-output2-')]
        ]

layout2 = [
            [sg.Text('sample 3'),sg.Text(size=(10,1),key='-output3-')],[sg.Button('ok',key='-button2-')],[sg.Text('sapmle 4'),sg.Text(size=(10,1),key='-output4-')]
        ]

#layout3 = [[sg.Button(f'{i},{j}') for i in range(3)] for j in range(3)]

layout = [[[sg.Image('nodes2.gif',key='-gif-',tooltip='music nodes'),sg.Image('empty_album2.png',key='-albumcover-2-',tooltip='album cover'),sg.Image('empty_album2.png',key='-albumcover-1-',tooltip='album cover'),sg.Image('empty_album2.png',key='-albumcover-',tooltip='album cover'),sg.Image('empty_album2.png',key='-albumcover1-',tooltip='album cover'),sg.Image('empty_album2.png',key='-albumcover2-',tooltip='album cover')]],[sg.HSeparator()],[sg.Image('bars.png',size=(750,480),key='-beams-'),sg.Image(None,size=(10,10),tooltip='loading...',key='-CV-')],[sg.ProgressBar(duration, orientation='h', size=(50, 20), key='-progressbar-')],[funcButton('-PREV-','Restart.png'),read_button,funcButton('-NEXT-','Next.png'),funcButton('-STOP-','stop.png'),funcButton('-REWIND-','rewind.png')]]
 
#background = '#9FB8AA'
#sg.set_options(background_color=background,element_background_color=background)
#sg.theme('Dark Blue 3')
   
window = sg.Window('GCMP',layout,icon=r'C:\Users\Admin\Desktop\3.ico',no_titlebar=False, resizable=True).Finalize()
#window.Size = (1000,1000)
window.maximize()
cap = cv2.VideoCapture(0)#cv2.CAP_DSHOW

#t1 = threading.Thread(target=play,args=('Vellipomaakey.mp3',))
#t2 = threading.Thread(target=pause)

l=[0,0]

img_list = [0,0,0,0,0]

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
print(volume.GetVolumeRange())

with mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5) as hands:
    while True:
        _,frame = cap.read()
        event,values = window.read(timeout=10)
        
        
        image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(cv2.flip(frame, 1),cv2.COLOR_BGR2RGB)
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        
        handLandmarks = findHandLandMarks(frame,image,draw=True)
        
        '''image.flags.writeable = False
        results = hands.process(image)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)'''
                
        if(len(handLandmarks) != 0):
            #for volume control we need 4th and 8th landmark
            #details: https://google.github.io/mediapipe/solutions/hands
            x1, y1 = handLandmarks[4][1], handLandmarks[4][2]
            x2, y2 = handLandmarks[8][1], handLandmarks[8][2]
            length = math.hypot(x2-x1, y2-y1)
            #print(length)
    
            #Hand range(length): 50-250
            #Volume Range: (-65.25, 0.0)
    
            volumeValue = np.interp(length, [50, 250], [-65.25, 0.0]) #coverting length to proportionate to volume range
            volume.SetMasterVolumeLevel(volumeValue, None)
    
    
            cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(image, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 3)
                
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        imgbytes = cv2.imencode('.png', image)[1].tobytes()
        window['-CV-'].update(data=imgbytes)
    
        if event == sg.WINDOW_CLOSED:
            stop()
            break
        
        elif event == '-PREV-':
            song_num-=1
            l[0]=0
            read_button.Update('',image_filename='play.png',image_size=(50, 50), image_subsample=2)#PLAY
            stop()
            call = True
            
            
        elif event == '-NEXT-':
            song_num+=1
            l[0]=0
            read_button.Update('',image_filename='play.png',image_size=(50, 50), image_subsample=2)#PLAY
            stop()
            call =True
            
        
        elif((time.time()>t+duration)and(l[0]==1)):
            stop()
            l[0]=0
            window['-beams-'].update('bars.png',size=(750,480))
            read_button.Update('',image_filename='play.png',image_size=(50, 50), image_subsample=2)#PLAY
            if l[1]==0:
                song_num+=1
            else:
                song_num = song_num
            print(song_num)
            call = True
            
        elif event == '-submit-':
            window['-output1-'].update('hai '+values['-input-']+" are you good")
        
        elif event == '-button1-':
            window['-output2-'].update('this is for button')
        
        elif event == '-button2-':
            pass
        #window['-image-'].update_animation(r'C:\Users\Admin\Desktop\shots.gif',time_between_frames=0)
        if song_num <= -157 and song_num >=156:
            song_num == 0
        
        if event == '-playpause-' or call == True: 
            #playsound('Vellipomaakey.mp3')
            #window['-playpause-'].update(button_text='pause')
            if l[0]==0:                                       #41 song is small try that
                read_button.Update('',image_filename='pause.png',image_size=(50, 50), image_subsample=2)#PAUSE
                song = filepath[song_num]
                play(song)
                audio = MP3(song)
                duration = audio.info.length
                window['-progressbar-'].UpdateBar(0,duration) 
                t = time.time()
                t1,t2=0,0
                progresstime = t
                window['-beams-'].update_animation(r'download4.gif')
                
                try:
                    song_two = filepath[song_num-2]
                    audio_file_two = eyed3.load(song_two)
                    time.sleep(0.001)
                    album_name_two = audio_file_two.tag.album
                    artist_name_two = audio_file_two.tag.artist
                    for image_two in audio_file_two.tag.images:
                        image_file_two = open("{0} - {1}({2}).jpg".format(artist_name_two, album_name_two, image_two.picture_type), "wb")
                        a_two = "{0} - {1}({2}).jpg".format(artist_name_two, album_name_two, image_two.picture_type)
                        image_file_two.write(image_two.image_data)
                        image_file_two.close()
                        #imagefrom = cv2.imread(a)
                    window['-albumcover-2-'].update(data=get_img_data(a_two, first=True))
                except:
                    window['-albumcover-2-'].update(data=get_img_data('empty_album.png'))
                #use to update new cover
                finally:
                    l[0]=1
                
                try:
                    song_one = filepath[song_num-1]
                    audio_file_one = eyed3.load(song_one)
                    time.sleep(0.001)
                    album_name_one = audio_file_one.tag.album
                    artist_name_one = audio_file_one.tag.artist
                    for image_one in audio_file_one.tag.images:
                        image_file_one = open("{0} - {1}({2}).jpg".format(artist_name_one, album_name_one, image_one.picture_type), "wb")
                        a_one = "{0} - {1}({2}).jpg".format(artist_name_one, album_name_one, image_one.picture_type)
                        image_file_one.write(image_one.image_data)
                        image_file_one.close()
                        #imagefrom = cv2.imread(a)
                    window['-albumcover-1-'].update(data=get_img_data(a_one, first=True))
                except:
                    window['-albumcover-1-'].update(data=get_img_data('empty_album.png'))    
                
                try:
                    audio_file = eyed3.load(song)
                    time.sleep(0.001)
                    album_name = audio_file.tag.album
                    artist_name = audio_file.tag.artist
                    for image in audio_file.tag.images:
                        image_file = open("{0} - {1}({2}).jpg".format(artist_name, album_name, image.picture_type), "wb")
                        a = "{0} - {1}({2}).jpg".format(artist_name, album_name, image.picture_type)
                        image_file.write(image.image_data)
                        image_file.close()
                        #imagefrom = cv2.imread(a)
                    window['-albumcover-'].update(data=get_img_data(a, first=True))
                except:
                    window['-albumcover-'].update(data=get_img_data('empty_album.png'))
                
                try:
                    songone = filepath[song_num+1]
                    audio_fileone = eyed3.load(songone)
                    time.sleep(0.001)
                    album_nameone = audio_fileone.tag.album
                    artist_nameone = audio_fileone.tag.artist
                    for imageone in audio_fileone.tag.images:
                        image_fileone = open("{0} - {1}({2}).jpg".format(artist_nameone, album_nameone, imageone.picture_type), "wb")
                        aone = "{0} - {1}({2}).jpg".format(artist_nameone, album_nameone, imageone.picture_type)
                        image_fileone.write(imageone.image_data)
                        image_fileone.close()
                        #imagefrom = cv2.imread(a)
                    window['-albumcover1-'].update(data=get_img_data(aone, first=True))
                except:
                    window['-albumcover1-'].update(data=get_img_data('empty_album.png'))
                
                try:
                    songtwo = filepath[song_num+2]
                    audio_filetwo = eyed3.load(songtwo)
                    time.sleep(0.001)
                    album_nametwo = audio_filetwo.tag.album
                    artist_nametwo = audio_filetwo.tag.artist
                    for imagetwo in audio_filetwo.tag.images:
                        image_filetwo = open("{0} - {1}({2}).jpg".format(artist_nametwo, album_nametwo, imagetwo.picture_type), "wb")
                        atwo = "{0} - {1}({2}).jpg".format(artist_nametwo, album_nametwo, imagetwo.picture_type)
                        image_filetwo.write(imagetwo.image_data)
                        image_filetwo.close()
                        #imagefrom = cv2.imread(a)
                    window['-albumcover2-'].update(data=get_img_data(atwo, first=True))
                except:
                    window['-albumcover2-'].update(data=get_img_data('empty_album.png'))
                
            elif l[0]==1:
                read_button.Update('',image_filename='play.png',image_size=(50, 50), image_subsample=2)#PLAY
                t1 = time.time()
                pause()
                l[0]=2
                #window['-beams-'].update_animation(r'0equilizer.png')
            else:
                read_button.Update('',image_filename='pause.png',image_size=(50, 50), image_subsample=2)#PAUSE
                t2 = time.time()
                duration += (t2-t1)
                progresstime+=(t2-t1)
                resume()
                l[0]=1
       
        elif event == '-STOP-':
            stop()
            l[0]=0
            window['-beams-'].update('bars.png',size=(750,480))
            window['-progressbar-'].UpdateBar(0)
            read_button.Update('',image_filename='play.png',image_size=(50, 50), image_subsample=2)#PLAY
            
        elif event == '-REWIND-':
            if l[1]==0:
                l[1]=1
                window['-REWIND-'].Update('',image_filename='unwind.png',image_size=(50, 50), image_subsample=2)#UNWIND
            else:
                l[1]=0
                window['-REWIND-'].Update('',image_filename='rewind.png',image_size=(50, 50), image_subsample=2)#REWIND
            
        if l[0]==1:
            window['-beams-'].update_animation(r'download4.gif')
            window['-progressbar-'].UpdateBar(time.time()-progresstime)
            
        call = False
        window['-gif-'].update_animation(r'nodes2.gif')

cap.release()      
window.close()
print('completed')








'''
theames = ['Black', 'BlueMono', 'BluePurple', 'BrightColors', 'BrownBlue', 'Dark', 'Dark2', 'DarkAmber', 'DarkBlack', 'DarkBlack1', 'DarkBlue', 'DarkBlue1', 'DarkBlue10', 'DarkBlue11', 'DarkBlue12', 'DarkBlue13', 'DarkBlue14', 'DarkBlue15', 'DarkBlue16', 'DarkBlue17', 'DarkBlue2',
 'DarkBlue3', 'DarkBlue4', 'DarkBlue5', 'DarkBlue6', 'DarkBlue7', 'DarkBlue8', 'DarkBlue9', 'DarkBrown', 'DarkBrown1', 'DarkBrown2', 'DarkBrown3', 'DarkBrown4', 'DarkBrown5', 'DarkBrown6', 'DarkBrown7', 'DarkGreen', 'DarkGreen1', 'DarkGreen2', 'DarkGreen3', 'DarkGreen4',
 'DarkGreen5', 'DarkGreen6', 'DarkGreen7', 'DarkGrey', 'DarkGrey1', 'DarkGrey10', 'DarkGrey11', 'DarkGrey12', 'DarkGrey13', 'DarkGrey14', 'DarkGrey2', 'DarkGrey3', 'DarkGrey4', 'DarkGrey5', 'DarkGrey6', 'DarkGrey7', 'DarkGrey8', 'DarkGrey9', 'DarkPurple', 'DarkPurple1',
 'DarkPurple2', 'DarkPurple3', 'DarkPurple4', 'DarkPurple5', 'DarkPurple6', 'DarkPurple7', 'DarkRed', 'DarkRed1', 'DarkRed2', 'DarkTanBlue', 'DarkTeal', 'DarkTeal1', 'DarkTeal10', 'DarkTeal11', 'DarkTeal12', 'DarkTeal2', 'DarkTeal3', 'DarkTeal4', 'DarkTeal5', 'DarkTeal6',
 'DarkTeal7', 'DarkTeal8', 'DarkTeal9', 'Default', 'Default1', 'DefaultNoMoreNagging', 'GrayGrayGray', 'Green', 'GreenMono', 'GreenTan', 'HotDogStand', 'Kayak', 'LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightBlue5', 'LightBlue6', 'LightBlue7', 
 'LightBrown', 'LightBrown1', 'LightBrown10', 'LightBrown11', 'LightBrown12', 'LightBrown13', 'LightBrown2', 'LightBrown3', 'LightBrown4', 'LightBrown5', 'LightBrown6', 'LightBrown7', 'LightBrown8', 'LightBrown9', 'LightGray1', 'LightGreen', 'LightGreen1', 'LightGreen10',
 'LightGreen2', 'LightGreen3', 'LightGreen4', 'LightGreen5', 'LightGreen6', 'LightGreen7', 'LightGreen8', 'LightGreen9', 'LightGrey', 'LightGrey1', 'LightGrey2', 'LightGrey3', 'LightGrey4', 'LightGrey5', 'LightGrey6', 'LightPurple', 'LightTeal', 'LightYellow', 'Material1',
 'Material2', 'NeutralBlue', 'Purple', 'Python', 'Reddit', 'Reds', 'SandyBeach', 'SystemDefault', 'SystemDefault1', 'SystemDefaultForReal', 'Tan', 'TanBlue', 'TealMono', 'Topanga']
'''




