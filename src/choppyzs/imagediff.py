#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare the differences between two images and export as csv or image."""
import os
from collections import Counter
import numpy as np
import pandas as pd
try:
    from scipy.misc import imread
except ImportError:  # if using new scipy, use imageio
    from imageio import imread
from scipy.linalg import norm
from scipy import sum, average
from PIL import Image
from PIL import ImageFile
import cv2
import imagehash


def check_if_file_exists(file_name):
    """Check if a file exists and if not, return FileNotFoundError."""
    if os.path.isfile(file_name) is not True:
        raise FileNotFoundError(f'{file_name} not found!')


def compare_images_directly(image_1, image_2):
    """Compare to see if the images are different."""
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    check_if_file_exists(image_1)
    check_if_file_exists(image_2)
    if image_1 == image_2:
        return True
    with open(image_1, 'rb') as fp1:
        img1 = Image.open(fp1)
    with open(image_2, 'rb') as fp2:
        img2 = Image.open(fp2)
    compare_results = img1 == img2
    return compare_results


def get_hash_from_image(image_file):
    """Get hash dictionary from an image."""
    check_if_file_exists(image_file)
    with open(image_file, 'rb') as image:
        hash_image = imagehash.average_hash(Image.open(image))
    return hash_image


def compare_image_with_hash(image_1, image_2, max_diff=0):
    """Compare the images for a maximum difference of hash."""
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    hash_1 = get_hash_from_image(image_1)
    hash_2 = get_hash_from_image(image_2)
    hash_dif = hash_1 - hash_2
    if hash_dif < 0:
        hash_dif = -hash_dif
    if hash_dif <= max_diff:
        return True
    return False


def to_grayscale_array(arr):
    """Convert an image to grayscale for comparison."""
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channel)
    return arr


def normalize(arr, factor=255):
    """Normalize the array."""
    rng = arr.max() - arr.min()
    amin = arr.min()
    return (arr - amin) * factor / rng


def compare_images(image_file_1, image_file_2, normalize_images=True,
                   normalize_factor=255):
    """Compare two images by converting them to 2D SciPy Arrays."""
    check_if_file_exists(image_file_1)
    check_if_file_exists(image_file_2)
    image_1 = to_grayscale_array(imread(image_file_1).astype(float))
    image_2 = to_grayscale_array(imread(image_file_2).astype(float))
    if normalize_images is True:
        image_1 = normalize(image_1, factor=normalize_factor)
        image_2 = normalize(image_2, factor=normalize_factor)
    diff = image_1 - image_2
    m_norm = sum(abs(diff))  # Manhattan norm
    z_norm = norm(diff.rave(), 0)  # Zero norm
    return (m_norm, z_norm)


def convert_image_to_list_of_pixel_values(image_file):
    """Convert an image to a list of lists of pixel values."""
    check_if_file_exists(image_file)
    # convert image to 8-bit grayscale
    image = Image.open(image_file).convert('L')
    width, height = image.size
    data = list(image.getdata())
    # convert that list to 2D list (list of lists of integers)
    data = [data[offset:offset + width] for offset in range(0, width)]
    return data


def image_to_dataframe(image_file, method="pil"):
    """Use cv2 to convert an image to a dataframe."""
    check_if_file_exists(image_file)
    if method.lower() == "cv2":
        image_df = cv2.imread(image_file)
    elif method.lower() == "pil":
        imframe = Image.open(image_file)
        npframe = np.array(imframe.getdata())
        image_df = pd.DataFrame(npframe)
    else:
        raise RuntimeError(f'Unknown method "{method}" chosen.')
    return image_df


def compare_dataframes(df_1, df_2, method="merge", on=None):
    """Compare two dataframes and retrieve the difference."""
    if method.lower == 'concat':
        diff = pd.concat([df_1, df_2]).drop_duplicates(keep=False)
    elif method.lower == 'isin':
        diff = df_1[~df_1.apply(tuple, 1).isin(df_2.apply(tuple, 1))]
    elif method.lower == 'merge':
        diff = df_1.merge(
            df_2, indicator=True, how='left'
        ).loc[lambda x: x['_merge'] != 'both']
    elif method.lower() == 'counter':
        on = on if on is not None else df_1.columns
        df1_on = df_1[on]
        df2_on = df_2[on]
        c1 = Counter(df1_on.apply(tuple, 'columns'))
        c2 = Counter(df2_on.apply(tuple, 'columns'))
        c1c2 = c1 - c2
        c2c1 = c2 - c1
        df1ondf2on = pd.DataFrame(list(c1c2.elements()), columns=on)
        df2ondf1on = pd.DataFrame(list(c2c1.elements()), columns=on)
        df1df2 = df_1.merge(df1ondf2on).drop_duplicates(subset=on)
        df2df1 = df_2.merge(df2ondf1on).drop_duplicates(subset=on)
        diff = pd.concat([df1df2, df2df1])
    else:
        raise RuntimeError(f'Unknown method "{method}" chosen.')
    return diff
