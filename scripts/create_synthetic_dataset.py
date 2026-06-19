from pathlib import Path

import numpy as np
import pandas as pd


def create_synthetic_cll_dataset(n_patients=300, random_state=42):
    rng = np.random.default_rng(random_state)

    age = rng.normal(68, 10, n_patients).clip(35, 95)
    sex = rng.choice(["F", "M"], size=n_patients, p=[0.45, 0.55])

    ighv_status = rng.choice(["mutated", "unmutated"], size=n_patients, p=[0.55, 0.45])
    tp53_mutation = rng.binomial(1, 0.12, n_patients)
    del_17p = rng.binomial(1, 0.10, n_patients)
    del_11q = rng.binomial(1, 0.17, n_patients)
    trisomy_12 = rng.binomial(1, 0.16, n_patients)
    del_13q = rng.binomial(1, 0.45, n_patients)

    hemoglobin = rng.normal(13.2, 1.7, n_patients).clip(7.5, 17.5)
    platelets = rng.normal(180, 60, n_patients).clip(30, 450)
    lymphocytes = rng.lognormal(mean=2.7, sigma=0.65, size=n_patients).clip(4, 250)
    beta2_microglobulin = rng.normal(3.1, 1.2, n_patients).clip(0.8, 9.5)
    ldh = rng.normal(220, 70, n_patients).clip(90, 700)

    cd38_positive = rng.binomial(1, 0.30, n_patients)
    zap70_positive = rng.binomial(1, 0.35, n_patients)

    risk_score = (
        0.03 * (age - 65)
        + 0.85 * (ighv_status == "unmutated")
        + 1.20 * tp53_mutation
        + 1.10 * del_17p
        + 0.50 * del_11q
        + 0.35 * cd38_positive
        + 0.35 * zap70_positive
        + 0.018 * (lymphocytes - np.median(lymphocytes))
        + 0.28 * (beta2_microglobulin - 3)
        + 0.004 * (ldh - 220)
        - 0.08 * (hemoglobin - 13)
        - 0.003 * (platelets - 180)
    )

    risk_noise = risk_score + rng.normal(0, 0.5, n_patients)

    rai_stage = pd.cut(
        risk_noise,
        bins=[-np.inf, -0.7, 0.1, 0.9, 1.7, np.inf],
        labels=["0", "I", "II", "III", "IV"],
    ).astype(str)

    binet_stage = pd.cut(
        risk_noise,
        bins=[-np.inf, 0.2, 1.2, np.inf],
        labels=["A", "B", "C"],
    ).astype(str)

    probability_progression_24m = 1 / (1 + np.exp(-risk_score))
    progression_24m = rng.binomial(1, probability_progression_24m)

    baseline_time = rng.exponential(scale=55, size=n_patients)
    time_to_first_treatment_months = baseline_time * np.exp(-0.40 * risk_score)
    time_to_first_treatment_months = time_to_first_treatment_months.clip(1, 120)

    followup_months = rng.uniform(24, 120, n_patients).round(1)
    event_ttft = (time_to_first_treatment_months <= followup_months).astype(int)
    observed_ttft_months = np.minimum(time_to_first_treatment_months, followup_months)

    risk_group = pd.cut(
        risk_score,
        bins=[-np.inf, -0.3, 0.8, np.inf],
        labels=["low", "intermediate", "high"],
    ).astype(str)

    df = pd.DataFrame({
        "patient_id": [f"SYN_{i:04d}" for i in range(n_patients)],
        "age": age.round(1),
        "sex": sex,
        "rai_stage": rai_stage,
        "binet_stage": binet_stage,
        "hemoglobin": hemoglobin.round(2),
        "platelets": platelets.round(1),
        "lymphocytes": lymphocytes.round(2),
        "beta2_microglobulin": beta2_microglobulin.round(2),
        "ldh": ldh.round(1),
        "ighv_status": ighv_status,
        "tp53_mutation": tp53_mutation,
        "del_17p": del_17p,
        "del_11q": del_11q,
        "trisomy_12": trisomy_12,
        "del_13q": del_13q,
        "cd38_positive": cd38_positive,
        "zap70_positive": zap70_positive,
        "risk_score_synthetic": risk_score.round(3),
        "risk_group_synthetic": risk_group,
        "progression_24m": progression_24m,
        "event_ttft": event_ttft,
        "time_to_first_treatment_months": observed_ttft_months.round(1),
        "followup_months": followup_months,
    })

    return df


def create_synthetic_longitudinal_dataset(baseline_df, random_state=123):
    rng = np.random.default_rng(random_state)
    visits = [0, 6, 12, 18, 24, 36]
    rows = []

    for _, row in baseline_df.iterrows():
        risk = row["risk_score_synthetic"]
        treated_month = row["time_to_first_treatment_months"] if row["event_ttft"] == 1 else 999

        for month in visits:
            if month > row["followup_months"]:
                continue

            growth = np.exp(0.015 * month * max(risk + 1, 0.2))
            lymphocytes = row["lymphocytes"] * growth * rng.normal(1, 0.12)
            beta2 = row["beta2_microglobulin"] + 0.025 * month * max(risk, 0) + rng.normal(0, 0.25)
            hemoglobin = row["hemoglobin"] - 0.015 * month * max(risk, 0) + rng.normal(0, 0.25)
            platelets = row["platelets"] - 0.35 * month * max(risk, 0) + rng.normal(0, 8)

            if month >= treated_month:
                clinical_state = "treated"
            elif month >= 24 and row["progression_24m"] == 1:
                clinical_state = "progression"
            else:
                clinical_state = "watch_and_wait"

            rows.append({
                "patient_id": row["patient_id"],
                "visit_month": month,
                "lymphocytes": round(max(1, lymphocytes), 2),
                "beta2_microglobulin": round(max(0.5, beta2), 2),
                "hemoglobin": round(max(6.5, hemoglobin), 2),
                "platelets": round(max(20, platelets), 1),
                "clinical_state": clinical_state,
                "risk_group_synthetic": row["risk_group_synthetic"],
            })

    return pd.DataFrame(rows)


def main():
    output_dir = Path("data/synthetic")
    output_dir.mkdir(parents=True, exist_ok=True)

    baseline = create_synthetic_cll_dataset()
    longitudinal = create_synthetic_longitudinal_dataset(baseline)

    baseline_file = output_dir / "synthetic_cll_public_baseline.csv"
    longitudinal_file = output_dir / "synthetic_cll_public_longitudinal.csv"

    baseline.to_csv(baseline_file, index=False)
    longitudinal.to_csv(longitudinal_file, index=False)

    print(f"Created: {baseline_file} | shape={baseline.shape}")
    print(f"Created: {longitudinal_file} | shape={longitudinal.shape}")


if __name__ == "__main__":
    main()
