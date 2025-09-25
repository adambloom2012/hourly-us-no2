import numpy as np
import copy
class ChangeBandOrder(object):
    def __call__(self, sample):
        """necessary if model was pre-trained on .npy files of BigEarthNet and should be used on other Sentinel-2 images

        move the channels of a sentinel2 image such that the bands are ordered as in the BigEarthNet dataset
        input image is expected to be of shape (200,200,12) with band order:
        ['B04', 'B03', 'B02', 'B08', 'B05', 'B06', 'B07', 'B8A', 'B11', 'B12', 'B01', 'B09'] (i.e. like my script on compute01 produces)

        output is of shape (12,120,120) with band order:
        ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B11", "B12"] (order in BigEarthNet .npy files)
        """
        img = copy.copy(sample["img"])
        img = np.moveaxis(img, -1, 0)
        reordered_img = np.zeros(img.shape)
        reordered_img[0, :, :] = img[10, :, :]
        reordered_img[1, :, :] = img[2, :, :]
        reordered_img[2, :, :] = img[1, :, :]
        reordered_img[3, :, :] = img[0, :, :]
        reordered_img[4, :, :] = img[4, :, :]
        reordered_img[5, :, :] = img[5, :, :]
        reordered_img[6, :, :] = img[6, :, :]
        reordered_img[7, :, :] = img[3, :, :]
        reordered_img[8, :, :] = img[7, :, :]
        reordered_img[9, :, :] = img[11, :, :]
        reordered_img[10, :, :] = img[8, :, :]
        reordered_img[11, :, :] = img[9, :, :]

        if img.shape[1] != 120 or img.shape[2] != 120:
            reordered_img = reordered_img[:, 40:160, 40:160]

        out = {}
        for k,v in sample.items():
            if k == "img":
                out[k] = reordered_img
            else:
                out[k] = v

        return out
    

img_array = np.load('/mnt/c/Users/abloom/Downloads/sentinel-2-epa/sentinel-2/06-037-1201/S2A_MSIL2A_20210612T182921_N0300_R027_T11SLT_20210612T225023.npy')
img_array

# Create a sample dictionary (mimicking what your dataset would provide)
sample = {
    "img": img_array,
    "no2": 25.5,  # example value
    "station_id": "example_station"  # example metadata
}

# Initialize the transform
change_band_order = ChangeBandOrder()

# Apply the transform
transformed_sample = change_band_order(sample)
image_vals = transformed_sample.get("img")
image_vals.shape
image_vals

import rasterio
import rasterio.plot as rplt
src = rasterio.open('data/1201_match_cal.tiff')
src_array = src.read()
src_array.shape
src_array
# compare values

# print correlation between the two arrays
np.corrcoef(image_vals.flatten(), src_array.flatten())
