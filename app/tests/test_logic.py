from datetime import date

from app.logic.tests import calculate_blood_market_ba_estimation
from app.schemas.requests import BloodMarketBAEstimationTestCreateRequest


def test_calculate_baa():
    request_data = BloodMarketBAEstimationTestCreateRequest(
        birthday=date(1956, 1, 1),  # Assuming age is 68 in 2024
        sex="M",
        albumin=46.59,
        alkaline_phosphatase=66.1,
        urea=8.77,
        cholesterol=4.047,
        creatinine=105.2,
        cystatin_c=1.212,
        glycated_haemoglobin=41.2,
        log_c_reactive_protein=0.8754687,
        log_gamma_glutamyltransf=3.580737,
        red_blood_cell_erythrocyte_count=4.17,
        mean_corpuscular_volume=89.2,
        red_blood_cell_erythrocyte_distribution_width=14.8,
        monocyte_count=0.5,
        neutrophill_count=6.7,
        lymphocyte_percentage=11.7,
        mean_sphered_cell_volume=80.6,
        log_alanine_aminotransfe=2.98214,
        log_shbg=3.404525,
        log_vitamin_d=4.592085,
        high_light_scatter_reticulocyte_percentage=0.35,
        glucose=4.641,
        platelet_distribution_width=15.7,
        mean_corpuscular_haemoglobin=30.3,
        platelet_crit=0.298,
        apolipoprotein_a=1.647,
    )

    BAA = calculate_blood_market_ba_estimation(request_data)

    assert 1.52 <= BAA <= 1.54
