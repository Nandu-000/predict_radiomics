import SimpleITK as sitk
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(data_dir, exist_ok=True)

for i in range(5):  # create 5 different patients
    
    size = (64, 64, 64)
    image_np = np.random.normal(0, 50, size)

    # Add variable calcium
    num_lesions = np.random.randint(1, 10)

    for _ in range(num_lesions):
        x, y, z = np.random.randint(10, 54, size=3)
        intensity = np.random.randint(200, 600)
        image_np[x-3:x+3, y-3:y+3, z-3:z+3] = intensity

    image = sitk.GetImageFromArray(image_np.astype(np.float32))
    image.SetSpacing((1.0, 1.0, 1.0))

    output_path = os.path.join(data_dir, f"synthetic_{i}.nii.gz")
    sitk.WriteImage(image, output_path)

print("Generated multiple synthetic scans")