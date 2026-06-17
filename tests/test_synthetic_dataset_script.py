from scripts.create_synthetic_dataset import create_synthetic_cll_dataset


def test_create_synthetic_cll_dataset_shape():
    df = create_synthetic_cll_dataset(n_patients=10, random_state=42)

    assert df.shape[0] == 10
    assert "patient_id" in df.columns
    assert "time_to_first_treatment_months" in df.columns
    assert "progression" in df.columns
