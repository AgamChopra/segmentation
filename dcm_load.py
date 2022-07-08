import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_modality_lut
import matplotlib.pyplot as plt


def load_dcm_as_norm_np(path = None, plot = False):

    if path != None:
        dcm = pydicom.read_file(path)
        print(dcm)
            
        data = apply_modality_lut(dcm.pixel_array, dcm)
            
        data_norm = (data - np.min(data))/(np.max(data) - np.min(data))
        
        if plot:
            plt.imshow(data_norm,cmap='gray')
            plt.show()
            print(data_norm.shape)
        return data_norm
        
    else:
        print('Warning: No file path detected!')
        return None
    
    
if __name__ == "__main__":
    path = input('Enter full file path. (ex- ../xyz.dcm)\n')
    load_dcm_as_norm_np(path,True)