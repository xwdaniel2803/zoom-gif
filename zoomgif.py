import os
import sys
import glob
import cv2
import numpy as np

def clipped_zoom(img, zoom_factor=0): # code taken from https://stackoverflow.com/questions/37119071/scipy-rotate-and-zoom-an-image-without-changing-its-dimensions, written by users MohamedEzz and Aelius

    """
    Center zoom in/out of the given image and returning an enlarged/shrinked view of 
    the image without changing dimensions
    ------
    Args:
        img : ndarray
            Image array
        zoom_factor : float
            amount of zoom as a ratio [0 to Inf). Default 0.
    ------
    Returns:
        result: ndarray
           numpy ndarray of the same shape of the input img zoomed by the specified factor.          
    """
    if zoom_factor == 0:
        return img


    height, width = img.shape[:2] # It's also the final desired shape
    new_height, new_width = int(height * zoom_factor), int(width * zoom_factor)
    
    ### Crop only the part that will remain in the result (more efficient)
    # Centered bbox of the final desired size in resized (larger/smaller) image coordinates
    y1, x1 = max(0, new_height - height) // 2, max(0, new_width - width) // 2
    y2, x2 = y1 + height, x1 + width
    bbox = np.array([y1,x1,y2,x2])
    # Map back to original image coordinates
    bbox = (bbox / zoom_factor).astype(np.int)
    y1, x1, y2, x2 = bbox
    cropped_img = img[y1:y2, x1:x2]
    
    # Handle padding when downscaling
    resize_height, resize_width = min(new_height, height), min(new_width, width)
    pad_height1, pad_width1 = (height - resize_height) // 2, (width - resize_width) //2
    pad_height2, pad_width2 = (height - resize_height) - pad_height1, (width - resize_width) - pad_width1
    pad_spec = [(pad_height1, pad_height2), (pad_width1, pad_width2)] + [(0,0)] * (img.ndim - 2)
    
    result = cv2.resize(cropped_img, (resize_width, resize_height))
    result = np.pad(result, pad_spec, mode='constant')
    assert result.shape[0] == height and result.shape[1] == width
    return result

cwd = os.getcwd()
imagename = sys.argv[1]
imagetype = sys.argv[2]
zoom = float(sys.argv[3])
iterations = int(sys.argv[4])

img = cv2.imread(cwd + "/" + imagename + "." + imagetype)
path = os.path.join(cwd, imagename)
if not os.path.exists(path): 
    os.mkdir(path)
else:
    files = glob.glob(path + "/*")
    for f in files:
        os.remove(f)
os.chdir(imagename)

for x in range(iterations):
    zoomed_image = clipped_zoom(img, zoom)
    img = zoomed_image
    filename = str(x) + ".jpg"
    cv2.imwrite(filename, zoomed_image)