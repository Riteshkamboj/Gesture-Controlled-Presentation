import os
from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

class GestureControlledPresentation(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gesture Controlled Presentation")
        self.attributes('-fullscreen', True)  # Make the window fullscreen
        # self.geometry("1280x720")
        self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()
        self.Folder = str(Path(__file__).resolve().parent)
        self.folderPath = "Presentation"
        self.imgNumber = 0
        self.hs, self.ws = 120, 213
        self.gestureThreshold = 300
        self.buttonPressed = False
        self.buttonCounter = 0
        self.buttonDelay = 25
        self.annotations = [[]]
        self.annotationNumber = 0
        self.annotationStart = False
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0
        self.smoothening = 3

        # Camera Setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.width)
        self.cap.set(4, self.height)

        # Get the list of Presentation Images
        self.pathImages = sorted(os.listdir(self.folderPath), key=len)

        # Hand Detector
        self.detector = HandDetector(detectionCon=0.8, maxHands=1)

        # Create a canvas to display the slides
        # self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        # self.canvas.pack()

        # Create a close button
        self.close_button = tk.Button(self, text="Close", command=self.close_app, width=20, bg="RED", fg="WHITE")
        self.close_button.pack(side=tk.BOTTOM, pady=10)

        # Create a canvas to display the slides
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create a close button
        # self.close_button = tk.Button(self, text="Close", command=self.close_app)
        # self.close_button.pack(side=tk.TOP, pady=10)

        self.update_slide()

    def close_app(self):
        self.cap.release()  # Release the camera resource
        self.destroy()  # Close the Tkinter window

    def update_slide(self):
        # Import Images
        success, img = self.cap.read()
        img = cv2.flip(img, 1)
        pathFullImage = os.path.join(self.folderPath, self.pathImages[self.imgNumber])
        imgCurrent = cv2.imread(pathFullImage)

        hands, img = self.detector.findHands(img)
        cv2.line(img, (0, self.gestureThreshold), (self.width, self.gestureThreshold), (0, 255, 0), 5)

        if hands and self.buttonPressed is False:
            hand = hands[0]
            fingers = self.detector.fingersUp(hand)
            cx, cy = hand['center']
            lmList = hand['lmList']

            # Constrain Values for easier drawing
            # xVal = int(np.interp(lmList[8][0], [self.width // 2, self.width - 50], [0, self.width]))
            # yVal = int(np.interp(lmList[8][1], [150, self.height - 200], [0, self.width]))
            # indexFinger = xVal, yVal

            xVal = int(np.interp(lmList[8][0], [self.cap.get(3) // 2, self.cap.get(3) - 50], [0, self.width]))
            yVal = int(np.interp(lmList[8][1], [150, self.cap.get(4)-200], [0, self.height]))
            indexFinger = xVal, yVal

            # Smoothen Values
            # self.clocX = int(self.plocX + (xVal - self.plocX) / self.smoothening)
            # self.clocY = int(self.plocY + (yVal - self.plocY) / self.smoothening)
            # indexFinger = self.clocX, self.clocY

            # If hand is at height of the Face
            if cy <= self.gestureThreshold:

                # Gesture 1 - Left
                if fingers == [1, 0, 0, 0, 0]:
                    self.annotationStart = False
                    # print("Left")
                    if self.imgNumber > 0:
                        self.annotations = [[]]
                        self.annotationNumber = 0
                        self.buttonPressed = True
                        self.imgNumber -= 1

                # Gesture 2 - Right
                if fingers == [0, 0, 0, 0, 1]:
                    self.annotationStart = False
                    # print("Right")
                    if self.imgNumber < len(self.pathImages) - 1:
                        self.annotations = [[]]
                        self.annotationNumber = 0
                        self.buttonPressed = True
                        self.imgNumber += 1

            # Gesture 3 - Show Pointer
            if fingers == [0, 1, 1, 0, 0]:
                cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
                self.annotationStart = False

            # Gesture 4 - Draw Pointer
            if fingers == [0, 1, 0, 0, 0]:
                if self.annotationStart is False:
                    self.annotationStart = True
                    self.annotationNumber += 1
                    self.annotations.append([])
                cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
                self.annotations[self.annotationNumber].append(indexFinger)
            else:
                self.annotationStart = False

            # Gesture 5 - Erase
            if fingers == [0, 1, 1, 1, 0]:
                if self.annotations:
                    if self.annotationNumber > -1:
                        self.annotations.pop(-1)
                        self.annotationNumber -= 1
                        self.buttonPressed = True

        else:
            self.annotationStart = False

        if self.buttonPressed:
            self.buttonCounter += 1
            if self.buttonCounter > self.buttonDelay:
                self.buttonCounter = 0
                self.buttonPressed = False

        for i in range(len(self.annotations)):
            for j in range(len(self.annotations[i])):
                if j != 0:
                    cv2.line(imgCurrent, self.annotations[i][j - 1], self.annotations[i][j], (0, 0, 200), 12)
                    self.plocX, self.plocY = self.clocX, self.clocY

        # Adding webcam images on slides
        imgSmall = cv2.resize(img, (self.ws, self.hs))
        h, w, _ = imgCurrent.shape
        imgCurrent[0:self.hs, w - self.ws:w] = imgSmall

        # Convert the OpenCV image to a Tkinter-compatible image
        img_pil = Image.fromarray(cv2.cvtColor(imgCurrent, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(image=img_pil)

        # Clear the canvas and display the updated slide
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        self.canvas.image = img_tk  # Keep a reference to prevent garbage collection

        # Schedule the next update
        self.after(10, self.update_slide)

if __name__ == "__main__":
    app = GestureControlledPresentation()
    app.mainloop()