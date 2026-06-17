from pathlib import Path

import numpy as np
import pandas as pd


def create_synthetic_cll_dataset(n_patients=200, random_state=42):
    rng = np.random.default_rng(random_state)

    age = rng.normal(68, 10, n_patients).clip(35, 95)
    lymphocytes = rng.lognormal(mean=2.6, sigma=0.6, size=n_patients)
    beta2_microglobulin = rng.normal(3.2, 1.2, n_patients).clip(0.8, 9.0)

    ighv_status = rng.choice(["mutated", "unmutated"], size=n_patients)
    tp53_mutation = rng.binomial(1, 0.12, n_patients)
    del_17p = rng.binomial(1, 0.10, n_patients)

    risk_score = (
        0.03 * (age - 65)
        + 0.8 * (ighv_status == "unmutated")
        + 1.2 * tp53_mutation
        + 1.0 * del_17p
        + 0.25 * (beta2_microglobulin - 3)
    )

    probability_progression = 1 / (1 + np.exp(-risk_score))
    progression = rng.binomial(1, probability_progression)

    time_to_first_treatment_months = rng.exponential(scale=48, size=n_patients)
    time_to_first_treatment_months = time_to_first_treatment_months * np.exp(-0.45 * risk_score)
    time_to_first_treatment_months = time_to_first_treatment_months.clip(1, 120)

    df = pd.DataFrame({
        "patient_id": [f"SYN_{i:04d}" for i in range(n_patients)],
        "age": age.round(1),
        "lymphocytes": lymphocytes.round(2),
        "beta2_microglobulin": beta2_microglobulin.round(2),
        "ighv_status": ighv_status,
        "tp53_mutation": tp53_mutation,
        "del_17p": del_17p,
        "progression": progression,
        "time_to_first_treatment_months": time_to_first_treatment_months.round(1),
    })

    return df


def main():
    output_dir = Path("data/synthetic")
    output_dir.mkdir(parents=True, exist_ok=True)

    df = create_synthetic_cll_dataset()
    output_file = output_dir / "synthetic_cll_dataset.csv"
    df.to_csv(output_file, index=False)

    print(f"Created: {output_file}")
    print(f"Shape: {df.shape}")


if __name__ == "__main__":
    main()
