import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_modality_lut
import matplotlib.pyplot as plt
from PIL import Image
from PIL.TiffTags import TAGS


def load_dcm_as_np(path = None, plot = False, norm = True):
    """
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

    """
    if path != None:
        dcm = pydicom.read_file(path + '.dcm')
        
        #meta = str(dcm.file_meta)
        meta = str(dcm)
            
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
    Image.fromarray(x).save(path + '.tif',description=meta)
    
    
def dcm2tif(path = None, plot = False, norm = True):
    """
    Parameters
    ----------
    path : string, optional
        The location of the image on disk without the .dcm extension. ex- "C:\image" The default is None.
    plot : binary, optional
        Prints the .dcm image. The default is False.
    norm : binary, optional
        Does the image need to be normalized before return. The default is True.
    """
    x,meta = load_dcm_as_np(path, plot, norm)
    save_as_tif(path,x,meta)
    
    
    
def load_tif(path = None):
    with Image.open(path + '.tif') as img:
        data = np.array(img)
        meta = {TAGS[key] : img.tag[key] for key in img.tag.keys()}
        orignal_meta_description = meta['ImageDescription'][0]
    return data, meta, orignal_meta_description
    
    
if __name__ == "__main__":
    #path = input('Enter full file path. (ex- ../xyz) DO NOT ENTER FILE EXTENSION .dcm, etc!\n')
    for i in range(4):
        path = 'R:\Ilka_NU\img (%d)'%(i+1)
        dcm2tif(path = path,norm = True)
        x,_,meta = load_tif(path)
        
        print(x.shape, type(x))
        print(meta)
        plt.imshow(x,cmap='gray')
        plt.show()
