# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 22:41:12 2022

@author: Ilka
"""

from skimage import io 
from image_registration import chi2_shift 

image=io.imread()
offset_image=io.imread()

