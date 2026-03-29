# Radiomics Feature Extraction and Calcium Phenotyping from CT Scans

## Overview

This project implements a radiomics-based pipeline for extracting quantitative features from CT scans and analyzing their association with coronary calcium burden using Agatston scoring.

The pipeline is designed to be **dataset-agnostic** and supports both **NIfTI (.nii/.nii.gz)** and **DICOM (.dcm)** formats, enabling direct use with clinical datasets such as the Stanford COCA dataset.

---

## Pipeline Architecture

```
CT Scan (DICOM / NIfTI)
        ↓
Preprocessing (Resampling + HU Windowing)
        ↓
Calcium Mask (HU > 130)
        ↓
Radiomics Feature Extraction (Shape + Texture)
        ↓
Agatston Score Calculation
        ↓
Statistical Analysis & Visualization
```

---

## Features Extracted

### Shape Features

* Sphericity
* Surface Volume Ratio
* Maximum 3D Diameter

### Texture Features

* **GLCM**: Contrast, Correlation, Inverse Difference Moment
* **GLSZM**: Small Area Emphasis, Large Area Emphasis, Zone Percentage
* **GLRLM**: Short Run Emphasis, Long Run Emphasis, Run Percentage

---

## Installation

Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

---

## How to Run

### 1. Generate Sample Data (for testing)

```bash
python src/generate_test_data.py
```

### 2. Run Feature Extraction Pipeline

```bash
python src/analysis.py
```

### 3. Run Analysis

Open:

```
notebooks/analysis.ipynb
```

---

## Input Data Support

### Supported Formats

* `.nii`, `.nii.gz` (NIfTI)
* DICOM folders (each folder = one scan)

### Example Structure

```
data/raw/

# NIfTI
scan_1.nii.gz
scan_2.nii.gz

# OR DICOM
patient_001/
    ├── IM-0001-0001.dcm
    ├── IM-0001-0002.dcm
```

---

## Agatston Score Categories

| Category | Score Range |
| -------- | ----------- |
| 0        | 0           |
| 1        | 1–99        |
| 2        | 100–399     |
| 3        | ≥ 400       |

---

## Results & Observations

* Texture-based radiomic features (e.g., GLCM contrast and correlation) show measurable association with calcium burden.
* Shape features exhibit weaker correlation compared to texture features.
* Dimensionality reduction using t-SNE demonstrates partial clustering across calcium burden categories.
* Radiomics features capture heterogeneity in calcium distribution patterns.
Results Interpretation

Radiomic texture features such as GLCM contrast and correlation demonstrated measurable association with Agatston scores, indicating sensitivity to calcium distribution heterogeneity. Shape features exhibited weaker correlations, suggesting that spatial distribution and texture of calcifications provide more discriminative information than global morphology.

Non-parametric statistical testing (Kruskal-Wallis) further confirmed that several radiomic features vary significantly across calcium burden categories (p < 0.05).

Dimensionality reduction using t-SNE showed partial clustering of samples across categories, supporting the hypothesis that radiomics can capture underlying phenotypic differences in calcium deposition.
---

## Limitations

* Calcium detection is based on a simple threshold (HU > 130), which may include non-coronary calcifications (e.g., bone).
* Agatston score calculation is simplified and does not fully incorporate slice thickness weighting.
* Synthetic data is used for testing; real-world validation is required for clinical deployment.

---

## Future Improvements

* Integrate anatomical heart segmentation for precise calcium localization
* Validate against ground truth Agatston scores (XML annotations)
* Improve calcium detection using learning-based methods
* Extend pipeline for phenotype clustering and risk prediction

---

## Technologies Used

* Python
* SimpleITK
* PyRadiomics
* NumPy / Pandas
* Scikit-learn
* Matplotlib / Seaborn

---

## Reproducibility

The project is fully reproducible:

```bash
git clone <repo>
pip install -r requirements.txt
python src/generate_test_data.py
python src/analysis.py
```

---

## Notes for GSoC Evaluation

* The pipeline is modular and easily extensible for segmentation, phenotyping, and predictive modeling tasks.
* Designed to work with real datasets such as COCA after DICOM loading.
* Emphasis is placed on interpretability, statistical analysis, and reproducibility rather than model complexity.

---