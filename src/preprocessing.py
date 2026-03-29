import SimpleITK as sitk
import numpy as np
import os


def load_image(path):
    #  NIfTI file
    if path.endswith(".nii") or path.endswith(".nii.gz"):
        return sitk.ReadImage(path)
    
    #  DICOM folder
    elif os.path.isdir(path):
        return load_dicom_series(path)
    
    else:
        raise ValueError(f"Unsupported format: {path}")
    

def load_dicom_series(dicom_folder):
    """Load DICOM folder as 3D image"""
    reader = sitk.ImageSeriesReader()
    
    dicom_names = reader.GetGDCMSeriesFileNames(dicom_folder)
    reader.SetFileNames(dicom_names)
    
    image = reader.Execute()
    return image

def resample_image(image, new_spacing=[1.0, 1.0, 1.0]):
    """Resample image to isotropic spacing"""
    original_spacing = image.GetSpacing()
    original_size = image.GetSize()

    new_size = [
        int(round(original_size[i] * (original_spacing[i] / new_spacing[i])))
        for i in range(3)
    ]

    resampler = sitk.ResampleImageFilter()
    resampler.SetOutputSpacing(new_spacing)
    resampler.SetSize(new_size)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetOutputDirection(image.GetDirection())
    resampler.SetOutputOrigin(image.GetOrigin())

    return resampler.Execute(image)


def window_image(image, min_hu=-200, max_hu=800):
    """Apply HU windowing"""
    image = sitk.Clamp(image, sitk.sitkFloat32, min_hu, max_hu)
    return image


def get_calcium_mask(image, threshold=130):
    """Create calcium mask based on HU threshold"""
    img_np = sitk.GetArrayFromImage(image)
    mask = (img_np > threshold).astype(np.uint8)

    mask_itk = sitk.GetImageFromArray(mask)
    mask_itk.CopyInformation(image)

    return mask_itk


def preprocess_pipeline(path):
    """Full preprocessing pipeline"""
    image = load_image(path)
    image = resample_image(image)
    image = window_image(image)
    mask = get_calcium_mask(image)

    return image, mask