import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_modality_lut
from PIL import Image
from PIL.TiffTags import TAGS

import matplotlib.pyplot as plt


def load_dcm_as_np(path = None, plot = False, norm = True):
    '''
    Parameters
    ----------
    path : string, optional
        The location of the image on disk without the .dcm extension. ex- "C:\image" The default is None.
    plot : binary, optional
        Prints the .dcm image. The default is False.
    norm : binary, optional
        Does the image need to be normalized before return. The default is True.

    Returns
    -------
    data : numpy float array
        The .dcm image as a numpy 2D array.
    '''
    if path != None:
        dcm = pydicom.read_file(path + '.dcm')
        
        meta = str(dcm) #meta = str(dcm.file_meta)
            
        data = apply_modality_lut(dcm.pixel_array, dcm)
        
        if norm:
            data = (data - np.min(data))/(np.max(data) - np.min(data))
        
        if plot:
            print(dcm)
            plt.imshow(data,cmap='gray')
            plt.show()
            print(data.shape)
            
        return data, meta
        
    else:
        print('Warning: No file path detected!')
        return None
    
    
def save_as_tif(path,x,meta = None):
    '''
    Parameters
    ----------
    path : string
        The location of the image on disk without the .dcm extension. ex- "C:\image" The default is None.
    x : numpy array
        2x2 numpy array holding the pixel values of the loaded image.
    meta : string, optional
        Meta data of the orignal dicom file. The default is None.

    Returns
    -------
    None.
    '''
    Image.fromarray(x).save(path + '.tif',description = meta)
    
    
def dcm2tif(path = None, plot = False, norm = True):
    '''
    Parameters
    ----------
    path : string, optional
        The location of the image on disk without the .dcm extension. ex- "C:\image" The default is None.
    plot : binary, optional
        Prints the .dcm image. The default is False.
    norm : binary, optional
        Does the image need to be normalized before return. The default is True.
    '''
    x,meta = load_dcm_as_np(path, plot, norm)
    save_as_tif(path,x,meta)
    
    
    
def load_tif(path = None):
    '''
    Parameters
    ----------
    path : string, optional
        The location of the image on disk without the .dcm extension. ex- "C:\image" The default is None.

    Returns
    -------
    data : numpy array
        2x2 numpy array holding the pixel values of the loaded image.
    tif_meta : dict
        The entire meta data of the tif file.
    orignal_meta_description : string
        Meta data of the orignal dicom file.
    '''
    with Image.open(path + '.tif') as img:
        data = np.array(img)
        tif_meta = {TAGS[key] : img.tag[key] for key in img.tag.keys()}
        orignal_meta_description = tif_meta['ImageDescription'][0]
    return data, tif_meta, orignal_meta_description
    
    
if __name__ == "__main__":
    #path = input('Enter full file path. (ex- ../xyz) DO NOT ENTER FILE EXTENSION .dcm, etc!\n')
    for i in range(150):
        path = 'C:/Users/Ilka/Desktop/ilka dicom data/RM-S302 NIRC-8791-2001_S302-Zr89-VRC01-aCARIAS-24h-5Nov2020_PT_2020-11-05_115710_._(WB.CTAC).Body_n150__00000/image (%d)'%(i+1)
        dcm2tif(path = path,norm = True)
        
        x,_,meta = load_tif(path)       
        print(x.shape, type(x))
        print(meta)
        plt.imshow(x,cmap='gray')
        plt.show()

