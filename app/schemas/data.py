from typing import NamedTuple


class FieldInfo(NamedTuple):
    label: str
    unit: str
    input_type: str


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
        "description": "Assesses the length of telomere sequences.",
        "year": "2018",
        "paper_url": "https://example.com/paper/telomere-length",
        "paper_title": "Telomere Length as a Biomarker",
    },
    {
        "name": "Blood Marker BA Estimation Test",
        "url": "tests/ba-estimation",
        "description": "Measures the level of CRP to assess inflammation.",
        "year": "2021",
        "paper_url": "https://example.com/paper/crp-levels",
        "paper_title": "Inflammatory Markers and Aging",
    },
    {
        "name": "Blood Glucose Test",
        "url": "https://example.com/test/telomere-length",
        "description": "Evaluates fasting blood sugar levels to gauge insulin resistance.",
        "year": "2022",
        "paper_url": "https://example.com/paper/blood-glucose",
        "paper_title": "Glucose Metabolism in Aging",
    },
]
