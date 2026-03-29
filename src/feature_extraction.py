from radiomics import featureextractor


def get_extractor():
    """Initialize PyRadiomics extractor"""
    extractor = featureextractor.RadiomicsFeatureExtractor()

    # Disable everything first
    extractor.disableAllFeatures()

    # Enable required feature classes
    extractor.enableFeatureClassByName("shape")
    extractor.enableFeatureClassByName("glcm")
    extractor.enableFeatureClassByName("glszm")
    extractor.enableFeatureClassByName("glrlm")

    return extractor


def extract_features(image, mask, extractor):
    """Extract selected radiomics features"""
    result = extractor.execute(image, mask)

    selected = {
        # Shape
        "Sphericity": result.get("original_shape_Sphericity"),
        "SurfaceVolumeRatio": result.get("original_shape_SurfaceVolumeRatio"),
        "Maximum3DDiameter": result.get("original_shape_Maximum3DDiameter"),

        # GLCM
        "GLCM_Contrast": result.get("original_glcm_Contrast"),
        "GLCM_Correlation": result.get("original_glcm_Correlation"),
        "GLCM_IDM": result.get("original_glcm_Idmn"),

        # GLSZM
        "GLSZM_SAE": result.get("original_glszm_SmallAreaEmphasis"),
        "GLSZM_LAE": result.get("original_glszm_LargeAreaEmphasis"),
        "GLSZM_ZP": result.get("original_glszm_ZonePercentage"),

        # GLRLM
        "GLRLM_SRE": result.get("original_glrlm_ShortRunEmphasis"),
        "GLRLM_LRE": result.get("original_glrlm_LongRunEmphasis"),
        "GLRLM_RP": result.get("original_glrlm_RunPercentage"),
    }

    return selected