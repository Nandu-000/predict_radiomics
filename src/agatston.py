import SimpleITK as sitk
import numpy as np
import scipy.ndimage as ndi


def agatston_score(image):
    """Compute Agatston score"""
    img = sitk.GetArrayFromImage(image)
    spacing = image.GetSpacing()

    score = 0

    for slice_idx in range(img.shape[0]):
        slice_img = img[slice_idx]

        lesions = slice_img > 130
        labeled, num = ndi.label(lesions)

        for i in range(1, num + 1):
            region = slice_img[labeled == i]

            if len(region) == 0:
                continue

            max_hu = region.max()

            if max_hu < 200:
                weight = 1
            elif max_hu < 300:
                weight = 2
            elif max_hu < 400:
                weight = 3
            else:
                weight = 4

            area = len(region) * spacing[0] * spacing[1]
            score += area * weight

    return score


def agatston_category(score):
    """Categorize Agatston score"""
    if score == 0:
        return 0
    elif score < 100:
        return 1
    elif score < 400:
        return 2
    else:
        return 3