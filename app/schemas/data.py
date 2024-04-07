from typing import NamedTuple


class FieldInfo(NamedTuple):
    label: str
    unit: str
    input_type: str


dnam_pheno_age_levine2018_test_fields = {
    "albumin": FieldInfo("Albumin", "g/dL", "number"),
    "creatinine": FieldInfo("Creatinine", "mg/dL", "number"),
    "glucose": FieldInfo("Glucose", "mg/dL", "number"),
    "c_reactive_protein": FieldInfo("C-Reactive Protein", "mg/L", "number"),
    "lymphocytes_percentage": FieldInfo("Lymphocytes Percentage", "%", "number"),
    "mean_corpuscular_volume": FieldInfo("Mean Corpuscular Volume", "fL", "number"),
    "red_blood_cell_distribution_width": FieldInfo(
        "Red Blood Cell Distribution Width", "%", "number"
    ),
    "alkaline_phosphatase": FieldInfo("Alkaline Phosphatase", "U/L", "number"),
    "white_blood_cell_count": FieldInfo("White Blood Cell Count", "10^9/L", "number"),
}

ba_estimation_test_fields = {
    "albumin": FieldInfo("Albumin", "g/dL", "number"),
    "alkaline_phosphatase": FieldInfo("Alkaline Phosphatase", "U/L", "number"),
    "urea": FieldInfo("Urea", "mg/dL", "number"),
    "cholesterol": FieldInfo("Cholesterol", "mg/dL", "number"),
    "creatinine": FieldInfo("Creatinine", "mg/dL", "number"),
    "cystatin_c": FieldInfo("Cystatin C", "mg/L", "number"),
    "glycated_haemoglobin": FieldInfo("Glycated Haemoglobin", "%", "number"),
    "log_c_reactive_protein": FieldInfo("Log C-Reactive Protein", "mg/L", "number"),
    "log_gamma_glutamyltransf": FieldInfo(
        "Log Gamma-Glutamyltransferase", "U/L", "number"
    ),
    "red_blood_cell_erythrocyte_count": FieldInfo(
        "Red Blood Cell (Erythrocyte) Count", "million/μL", "number"
    ),
    "mean_corpuscular_volume": FieldInfo("Mean Corpuscular Volume", "fL", "number"),
    "red_blood_cell_erythrocyte_distribution_width": FieldInfo(
        "Red Blood Cell (Erythrocyte) Distribution Width", "%", "number"
    ),
    "monocyte_count": FieldInfo("Monocyte Count", "cells/μL", "number"),
    "neutrophill_count": FieldInfo("Neutrophil Count", "cells/μL", "number"),
    "lymphocyte_percentage": FieldInfo("Lymphocyte Percentage", "%", "number"),
    "mean_sphered_cell_volume": FieldInfo("Mean Sphered Cell Volume", "fL", "number"),
    "log_alanine_aminotransfe": FieldInfo(
        "Log Alanine Aminotransferase", "U/L", "number"
    ),
    "log_shbg": FieldInfo("Log Sex Hormone-Binding Globulin", "nmol/L", "number"),
    "log_vitamin_d": FieldInfo("Log Vitamin D", "ng/mL", "number"),
    "high_light_scatter_reticulocyte_percentage": FieldInfo(
        "High Light Scatter Reticulocyte Percentage", "%", "number"
    ),
    "glucose": FieldInfo("Glucose", "mg/dL", "number"),
    "platelet_distribution_width": FieldInfo(
        "Platelet Distribution Width", "%", "number"
    ),
    "mean_corpuscular_haemoglobin": FieldInfo(
        "Mean Corpuscular Haemoglobin", "pg", "number"
    ),
    "platelet_crit": FieldInfo("Plateletcrit", "%", "number"),
    "apolipoprotein_a": FieldInfo("Apolipoprotein A", "mg/dL", "number"),
}

tests = [
    {
        "name": "PhenoAGE",
        "url": "/tests/phenoage-2018",
        "description": "PhenoAge is a biological age estimate derived from a linear combination of chronological age and 9 blood biomarkers that were selected and weighted based on their ability to predict mortality in a large dataset using a Cox penalized regression survival model.",
        "year": "2018",
        "paper_url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5940111/",
        "paper_title": "An epigenetic biomarker of aging for lifespan and healthspan",
    },
    {
        "name": "Blood Marker BA Estimation Test",
        "url": "tests/ba-estimation",
        "description": "This test builds on PhenoAGE, using 25 blood biomarkers and a more precise model, with a dataset of 500,000 participants. It is still relatively accessible, since most labs do test for necessary biomarkers",
        "year": "2023",
        "paper_url": "https://www.nature.com/articles/s42003-023-05456-z",
        "paper_title": "Biological age estimation using circulating blood biomarkers ",
    },
]
