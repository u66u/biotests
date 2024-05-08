from app.schemas.requests import (
    BloodMarketBAEstimationTestCreateRequest,
    DNAmPhenoAgeLevine2018TestRequest,
)
import math
from datetime import date, datetime


def calculate_dnam_pheno_age_levine_2018(test_data: DNAmPhenoAgeLevine2018TestRequest):
    albumin = float(test_data.albumin)
    creatinine = float(test_data.creatinine)
    glucose = float(test_data.glucose)
    c_reactive_protein = float(test_data.c_reactive_protein)
    lymphocytes_percentage = float(test_data.lymphocytes_percentage)
    mean_corpuscular_volume = float(test_data.mean_corpuscular_volume)
    red_blood_cell_distribution_width = float(
        test_data.red_blood_cell_distribution_width
    )
    alkaline_phosphatase = float(test_data.alkaline_phosphatase)
    white_blood_cell_count = float(test_data.white_blood_cell_count)

    today = date.today()
    age = float(
        today.year
        - test_data.birthday.year
        - (
            (today.month, today.day)
            < (test_data.birthday.month, test_data.birthday.day)
        )
    )

    weights = {
        "albumin": -0.336,
        "creatinine": 0.8398095,
        "glucose": 0.01083915,
        "c_reactive_protein": 0.0954,
        "lymphocytes_percentage": -0.0120,
        "mean_corpuscular_volume": 0.0268,
        "red_blood_cell_distribution_width": 0.3306,
        "alkaline_phosphatase": 0.0019,
        "white_blood_cell_count": 0.0554,
        "age": 0.0804,
    }

    linear_combination = (
        -19.9067
        + albumin * weights["albumin"]
        + creatinine * weights["creatinine"]
        + glucose * weights["glucose"]
        + math.log(c_reactive_protein * 0.1) * weights["c_reactive_protein"]
        + lymphocytes_percentage * weights["lymphocytes_percentage"]
        + mean_corpuscular_volume * weights["mean_corpuscular_volume"]
        + red_blood_cell_distribution_width
        * weights["red_blood_cell_distribution_width"]
        + alkaline_phosphatase * weights["alkaline_phosphatase"]
        + white_blood_cell_count * weights["white_blood_cell_count"]
        + age * weights["age"]
    )

    g = 0.0076927
    age_delta = 120  # 10 years

    mortality_score_10_years = 1 - math.exp(
        -math.exp(linear_combination) * (math.exp(g * age_delta) - 1) / g
    )

    ptypic_age = (
        141.50225
        + math.log(-0.00553 * math.log(1 - mortality_score_10_years)) / 0.090165
    )
    DNAmAge = ptypic_age / (1 + 1.28047 * math.exp(0.0344329 * (-182.344 + ptypic_age)))
    D_Mscore = 1 - math.exp(-0.000520363523 * math.exp(0.090165 * DNAmAge))

    return {
        "linear_combination": linear_combination,
        "mortality_score_10_years": mortality_score_10_years,
        "ptypic_age": ptypic_age,
        "DNAmAge": DNAmAge,
        "D_Mscore": D_Mscore,
    }


def calculate_blood_market_ba_estimation(
    test_data: BloodMarketBAEstimationTestCreateRequest,
):
    # fmt: off
    model_data = {
    'age': {'coefficient_ENET': 0.074763266, 'coefficient_genderAge': 0.100432393, 'featureMean': 56.0487752},
    'albumin': {'coefficient_ENET': -0.011331946, 'coefficient_genderAge': 0, 'featureMean': 45.1238763},
    'alkaline_phosphatase': {'coefficient_ENET': 0.00164946, 'coefficient_genderAge': 0, 'featureMean': 82.6847975},
    'urea': {'coefficient_ENET': -0.029554872, 'coefficient_genderAge': 0, 'featureMean': 5.3547152},
    'cholesterol': {'coefficient_ENET': -0.0805656, 'coefficient_genderAge': 0, 'featureMean': 5.6177437},
    'creatinine': {'coefficient_ENET': -0.01095746, 'coefficient_genderAge': 0, 'featureMean': 71.565605},
    'cystatin_c': {'coefficient_ENET': 1.859556436, 'coefficient_genderAge': 0, 'featureMean': 0.900946},
    'glycated_haemoglobin': {'coefficient_ENET': 0.018116675, 'coefficient_genderAge': 0, 'featureMean': 35.4785711},
    'log_c_reactive_protein': {'coefficient_ENET': 0.079109916, 'coefficient_genderAge': 0, 'featureMean': 0.3003624},
    'log_gamma_glutamyltransf': {'coefficient_ENET': 0.265550311, 'coefficient_genderAge': 0, 'featureMean': 3.3795613},
    'red_blood_cell_erythrocyte_count': {'coefficient_ENET': -0.204442153, 'coefficient_genderAge': 0, 'featureMean': 4.4994648},
    'mean_corpuscular_volume': {'coefficient_ENET': 0.017165356, 'coefficient_genderAge': 0, 'featureMean': 91.9251099},
    'red_blood_cell_erythrocyte_distribution_width': {'coefficient_ENET': 0.202009895, 'coefficient_genderAge': 0, 'featureMean': 13.4342296},
    'monocyte_count': {'coefficient_ENET': 0.36937314, 'coefficient_genderAge': 0, 'featureMean': 0.4746987},
    'neutrophill_count': {'coefficient_ENET': 0.06679092, 'coefficient_genderAge': 0, 'featureMean': 4.1849454},
    'lymphocyte_percentage': {'coefficient_ENET': -0.0108158, 'coefficient_genderAge': 0, 'featureMean': 28.5817604},
    'mean_sphered_cell_volume': {'coefficient_ENET': 0.006736204, 'coefficient_genderAge': 0, 'featureMean': 83.6363269},
    'log_alanine_aminotransfe': {'coefficient_ENET': -0.312442261, 'coefficient_genderAge': 0, 'featureMean': 3.077868},
    'log_shbg': {'coefficient_ENET': 0.292323186, 'coefficient_genderAge': 0, 'featureMean': 3.8202787},
    'log_vitamin_d': {'coefficient_ENET': -0.265467867, 'coefficient_genderAge': 0, 'featureMean': 3.6052878},
    'high_light_scatter_reticulocyte_percentage': {'coefficient_ENET': 0.169234165, 'coefficient_genderAge': 0, 'featureMean': 0.3988152},
    'glucose': {'coefficient_ENET': 0.032171478, 'coefficient_genderAge': 0, 'featureMean': 4.9563054},
    'platelet_distribution_width': {'coefficient_ENET': 0.071527711, 'coefficient_genderAge': 0, 'featureMean': 16.4543576},
    'mean_corpuscular_haemoglobin': {'coefficient_ENET': 0.02746487, 'coefficient_genderAge': 0, 'featureMean': 31.8396206},
    'platelet_crit': {'coefficient_ENET': -1.329561046, 'coefficient_genderAge': 0, 'featureMean': 0.2385396},
    'apolipoprotein_a': {'coefficient_ENET': -0.185139395, 'coefficient_genderAge': 0, 'featureMean': 1.5238771}
    }
    # fmt: on
    data_dict = test_data.model_dump()
    birthday = data_dict.pop("birthday")
    data_dict.pop("gender", None)

    # Calculate age
    current_date = datetime.now().date()
    birth_date = datetime.strptime(str(birthday), "%Y-%m-%d").date()
    age = current_date.year - birth_date.year
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    data_dict["age"] = age

    # Compute BAA
    BAA = 0
    for feature, value in data_dict.items():
        if feature in model_data:
            coeff_data = model_data[feature]
            centered_value = value - coeff_data["featureMean"]
            baa_coefficient = (
                coeff_data["coefficient_ENET"] - coeff_data["coefficient_genderAge"]
            )
            BAA += centered_value * baa_coefficient

    BAA *= 10

    return BAA
