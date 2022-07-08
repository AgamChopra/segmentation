import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_modality_lut
import matplotlib.pyplot as plt
from PIL import Image


def load_dcm_as_np(path = None, plot = False, norm = True):

    if path != None:
        dcm = pydicom.read_file(path + '.dcm')
        print(dcm)
            
        data = apply_modality_lut(dcm.pixel_array, dcm)
        
        if norm:
            data = (data - np.min(data))/(np.max(data) - np.min(data))
        
        if plot:
            plt.imshow(data,cmap='gray')
            plt.show()
            print(data.shape)
        return data
        
    else:
        print('Warning: No file path detected!')
        return None
    
    
def save_as_png(x,path):
    Image.fromarray(x).save(path + '.tif')
    
    
def dcm2tif(path = None, plot = False, norm = True):
    x = load_dcm_as_np(path, plot, norm)
    save_as_png(x, path)
    
    
def load_tif(path = None):
    return np.array(Image.open(path + '.tif'))
    
    
if __name__ == "__main__":
    path = input('Enter full file path. (ex- ../xyz) DO NOT ENTER FILE EXTENSION .dcm, etc!\n')
    dcm2tif(path,True,True)
    x = load_tif(path)
    print(x.shape, type(x))
    print(x)
    plt.imshow(x,cmap='gray')
    plt.show()