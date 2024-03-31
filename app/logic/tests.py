from app.schemas.requests import DNAmPhenoAgeLevine2018TestRequest


def calculate_dnam_pheno_age_levine_2018(
    test_data: DNAmPhenoAgeLevine2018TestRequest,
) -> float:
    values = [
        test_data.albumin,
        test_data.creatinine,
        test_data.glucose,
        test_data.c_reactive_protein,
        test_data.lymphocytes_percentage,
        test_data.mean_corpuscular_volume,
        test_data.red_blood_cell_distribution_width,
        test_data.alkaline_phosphatase,
        test_data.white_blood_cell_count,
    ]
    values = [v for v in values if v is not None]
    if not values:
        return 0.0
    return sum(values) / len(values)
