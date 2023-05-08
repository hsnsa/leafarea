from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time
import cv2
import tkinter as tk
from tkinter import Label
import numpy as np
import csv
##import sys

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640,480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
    Button: 
        text: 'Save'
        size_hint_y: None
        height: '48dp'
        on_press: root.save()
''')


class CameraClick(BoxLayout):
    contours = ''
    sorted_areas = ''
    ContoursNum = ''
    LeafArea = ''

    def capture(self):
    
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("img.png".format(timestr))
        img = cv2.imread("img.png",cv2.IMREAD_UNCHANGED)
        trans_mask = img[:, :, 3] == 0
        img[trans_mask] = [255, 255, 255, 255]
        new_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
             
        imgcontour = img.copy()
        # edit photo and find contours

        imggrey = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
        imgblur = cv2.GaussianBlur(imggrey, (7, 7), 0)
        (thresh, blackAndWhiteImage) = cv2.threshold(imgblur, 100,255 , cv2.THRESH_BINARY)
        InRange = cv2.inRange(blackAndWhiteImage, 0, 10)
        #imgcanny = cv2.Canny(blackAndWhiteImage, 100, 100)

        contours, hierarchy = cv2.findContours(InRange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        #print("Number of contours detected = %d" % len(contours),timestr)
        #global ContoursNum
        #ContoursNumber = (len(contours))
        #ContoursNum = ContoursNumber
        

        # Get contour areas and sort them in ascending order
        areas = [cv2.contourArea(c) for c in contours]
        sorted_areas = sorted(areas)

        # Draw contours with numbers
        for i, area in enumerate(sorted_areas):
              # Get index of current contour based on its area
            index = areas.index(area)
            contour = contours[index]

             # Draw contour
            cv2.drawContours(imgcontour, [contour], -1, (255, 0, 0), 3)

              # Add contour number as text
            x, y, w, h = cv2.boundingRect(contour)
            cv2.putText(imgcontour, str(i+1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)


        


        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.015 * cv2.arcLength(contour, True), True)
            area1 = cv2.contourArea(contour)
            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5
            if len(approx) == 4:

                (x, y, w, h) = cv2.boundingRect(approx)
                ar = w / float(h)

                # A square will have an aspect ratio that is approximately
                # equal to one, otherwise, the shape is a rectangle
                shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
                cv2.putText(img, shape, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                
                


                if shape == "square" or shape == "rectangle":

                    for cnt in contours:
                        area2 = cv2.contourArea(cnt)
                        cv2.drawContours(imgcontour, cnt, -1, (255, 0, 0), 3)
                        global LeafArea
                        LeafArea = area2 / area1
                        

        cv2.imshow("KKK", blackAndWhiteImage)
        #cv2.imshow("drowcontour", imgcanny)
        cv2.imshow("contour", imgcontour)
        cv2.imshow("shapes", img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        print("Captured")
                    
                 

    def save (self):

        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")

        
        # get contour area and sort them in ascending order
        areas = [cv2.contourArea(c) for c in self.contours]
        sorted_areas = sorted(areas)
        num_contrours = len(self.contours)


        #write data to csv file
        with open("laefarea.csv", mode = 'a') as file:
            writer = csv. writer(file)
        
            header =['ContourIndex', 'contourArea']
            for i in range(num_contrours):
                area = areas[i]
                index = sorted_areas.index(area)
                writer.writer([i+1, area])
        print("Saved")

        

        #area_data = [timestr,ContoursNum, LeafArea]
        #with open("leafArea.csv", "a") as file:
         #writer = csv.writer(file)
         #writer.writerow(area_data)
                          
          
        
        


class AreaMaster(App):

    def build(self):
        return CameraClick()


AreaMaster().run()

