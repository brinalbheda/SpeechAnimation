from utils_ref import *
from config import *
import numpy as np
import tqdm
import glob
import cv2
import pickle as pkl
import os
import subprocess


############################################################
class testModel:
    
     def __init__(self):
         self.inputTestFolder = inputTestFolder
         self.inputToA2KeyModel = inputToA2KeyModel
         self.inputToA2KeyBlack = inputToA2KeyBlack
         self.outputFolderGroundTruth = outputFolderGroundTruth
         self.outputFolderKp = outputFolderKp
         self.saveFilename = saveFilename
         
         if not(os.path.exists(self.inputToA2KeyModel)):
             subprocess.call('mkdir -p ' + self.inputToA2KeyModel, shell=True)
         if not(os.path.exists(self.inputToA2KeyBlack)):
             subprocess.call('mkdir -p ' + self.inputToA2KeyBlack, shell=True)
         if not(os.path.exists(self.outputFolderKp)):
             subprocess.call('mkdir -p ' + self.outputFolderKp, shell=True)
             
         #remove previously contained files
         cmd = 'rm -rf ' + self.inputTestFolder + '*-square-x-100.jpeg'
         subprocess.call(cmd, shell=True)
             
         
     def test(self):
         #get all the file names in the folder
         searchNames = self.inputTestFolder + '*' + '.jpeg'
         filenames = sorted(glob.glob(searchNames))
         
         d = []
         for file in tqdm.tqdm(filenames):
             img = cv2.imread(file)
             x = int(np.floor((img.shape[1]-256)/2))
             
             # Crop to a square image
             crop_img = img[0:256, x:x+256]
             outputName = file[0:-len('.jpeg')]+'-square-x-100.jpeg'
             
             cv2.imwrite(outputName, crop_img) 
             
             keypoints = all_landmarks(outputName)
             l = getKP(keypoints)
             unit_kp, N, tilt, mean = l[0], l[1], l[2], l[3]
             kp_mouth = unit_kp[48:68]
             store_list = [kp_mouth, N, tilt, mean, unit_kp, keypoints]
             d.append(store_list)
         
            # create a patch based on the tilt, mean and the size of dface
             mean_x, mean_y = int(mean[0]), int(mean[1])
             size = int(N/15)
             aspect_ratio_mouth = 1.8
             
             patch_img = crop_img.copy()
             cv2.imwrite(self.inputToA2KeyModel + file[len(self.inputTestFolder):-len('.jpeg')] + '.png', patch_img)
             
             patch_black = np.zeros((256, 256))
             cv2.imwrite(self.inputToA2KeyBlack + file[len(self.inputTestFolder):-len('.jpeg')] + '.png', patch_black)
             
             
         with open(self.saveFilename, "wb") as output_file:
             pkl.dump(d, output_file)
         return
         

#read path from the user to the data folder
if __name__== "__main__":
    testModel_obj = testModel()
    testModel_obj.test()
    print("Testing in progress!!!!!!!!!!") 
    


