import cv2 
import os
import time

class Timelapse: 
    def __init__(self, imageFolder, outputVideoPath, fps=None):
        self.imageFolder = imageFolder
        self.outputVideoPath = outputVideoPath
        self.fps = fps if fps is not None else 10
    
    def createTimelapse(self): #Main function
        images = [img for img in os.listdir(self.imageFolder) if img.endswith (".jpg")] #Lists all images in a later specified folder and sorts out the ones ending with .jpg
        images.sort() #sorts the images in number order

        firstImagePath = os.path.join(self.imageFolder, images[0])
        frame = cv2.imread(firstImagePath)
        height, width, _ = frame.shape 

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.outputVideoPath, fourcc, self.fps, (width, height)) #VideoWriter setup, here with output path, XVID codec and frames per second. FourCC is for character code which specifies the video codec.

        for imageName in images:
            imagePath = os.path.join(self.imageFolder, imageName)
            frame = cv2.imread(imagePath) # This is where the pictures are made to a video
            frame = cv2.resize(frame, (width, height)) #resizes the images to it fits the first in the directory
            out.write(frame)

        out.release()

imageFolder = r"C:\Users\bo\Desktop\It teknolog\tema 3\timelapseattempt\timelapsefolder"
outputVideoPath = r"C:\Users\bo\Desktop\It teknolog\tema 3\timelapseattempt\timelapsefolder\timelapse.avi" #Adjust these to your directory
fps = 2

timelapseCreator = Timelapse(imageFolder, outputVideoPath, fps)
timelapseCreator.createTimelapse()