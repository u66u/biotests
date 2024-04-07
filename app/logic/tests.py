import os
import pandas as pd
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
    dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(dir, "data/bloodmarker_ba_coefficients_and_means.csv")

    data_dict = test_data.model_dump()
    birthday = data_dict["birthday"]
    del data_dict["sex"]  # Sex is not used in the BAA calculation
    sample_df = pd.DataFrame([data_dict])

    model_data = pd.read_csv(csv_file_path)

    # Calculate age
    current_date = datetime.now().date()
    birth_date = datetime.strptime(str(birthday), "%Y-%m-%d").date()
    age = current_date.year - birth_date.year
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        age -= 1

    sample_df["age"] = age

    # Filter out 'sexM' from the model data
    model_data_adj = model_data[model_data["feature"] != "sexM"].copy()
    model_data_adj["BAA_coefficient"] = (
        model_data_adj["coefficient_ENET"] - model_data_adj["coefficient_SexAge"]
    )

    # Join model data with sample data on 'feature'
    sample_df_melted = sample_df.melt(var_name="feature")
    joined_data = pd.merge(sample_df_melted, model_data_adj, on="feature")
    joined_data["centeredValue"] = joined_data["value"] - joined_data["featureMean"]

    BAA = sum(joined_data["centeredValue"] * joined_data["BAA_coefficient"]) * 10

    return BAA
