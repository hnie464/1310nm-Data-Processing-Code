# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 09:24:38 2020

@author: mbro632
"""

import os,sys

import matplotlib.pyplot as plt
import numpy as np
import time
import DirectorySetupGallery as directory
import glob
import tifffile as tf   # Install tifffle: conda install -c conda-forge tifffle
import TdmsCodeGallery as pytdms   # Install npTDMS: conda install -c conda-forge nptdms

plt.close('all')

tstart=time.time()

#Data location information  
folderLocation = 'C:/Users/User/Desktop/1310nm Data/G3' # File Path to Folder of Scanned Section                                              

npy = r'\npy_files'                                                             
output = r'\output_files'                                                        

#PS-OCT Image information - These values never change
spectra_num = 1024
A_scan_num = 714
padSize = 0 # How much zero padding do you want to do

B_scan_num = 220 # 220 default, but may change on file

dataLocation = folderLocation
print(dataLocation)
sampleName = os.path.basename(dataLocation)
imageFiles1 = sorted(glob.glob(dataLocation + '/' + 'Ch0_G*.tdms')) # Ch0_G*.tdms
imageFiles  = sorted(glob.glob(dataLocation + '/' + 'Ch1_G*.tdms')) # Ch1_G*.tdms
# File Name: SD-OCT_20220323221416-000.tdms

imageSize = np.array(())
stackedImages = np.array(())
for images in imageFiles:
    print(images)
    B_scan_num = int(images.split('_')[2]) # How many B-scans were in the volume image
    variableName = images.split('/')[-1].split('_',1)[-1].rsplit('.',1)[0] # Get the XXXXXX filename details after Ch1_XXXXXXX.tdms
    Int = []
    Ret = []
    Ch0Complex = []
    Ch1Complex = []
    t1 = time.time()
    Int,Ret = directory.loadData(dataLocation,npy,output,variableName,A_scan_num,B_scan_num,padSize)
    intdB = 10*np.log10(Int) # Put in log scale
    intdB[:,0:5,:] = 70 # Remove artifact noise values at the start of the array (noise level is ~70)
    
    imageSize = np.append(imageSize, B_scan_num)
    
    plt.figure()
    #plt.imshow(intdB[200,:,:],cmap='gray') # [100,...]    

    #Save tiff image - Can be used in ImageJ later.
    tf.imwrite(folderLocation + output + '/' + variableName + '/Int_{}.tif'.format(variableName.split('_')[2]) ,intdB.astype(np.float32),photometric='minisblack')
    stackedImages = np.append(stackedImages, intdB)
    
    
finalImage = stackedImages.reshape(int(np.sum(imageSize)),int(spectra_num/2),np.size(intdB,2))


# EN-FACE VIEW (PROJECTION)
projection = np.sum(finalImage[:,10:250,:],1)
plt.figure()
plt.imshow(projection, cmap='gray',clim = [1.6e4,1.75e4])







    

    


        