# Synthetic CLL datasets

These files are fully synthetic and do not contain real patient data.

## Files

- `synthetic_cll_public_baseline.csv`: patient-level synthetic CLL-like dataset with clinical, biological, genetic and endpoint variables.
- `synthetic_cll_public_longitudinal.csv`: visit-level synthetic longitudinal dataset for dynamic biological-clinical mapping.

## Intended use

These files are designed for public demonstrations of:

- data audit and preprocessing;
- endpoint definition;
- baseline Machine Learning;
- survival analysis with time-to-first-treatment;
- PCA and UMAP patient-space visualization;
- TDA feature extraction;
- hybrid TDA + ML modelling;
- dynamic biological-clinical mapping.

## Variables included

The baseline dataset includes synthetic variables inspired by CLL risk stratification:

- age;
- sex;
- Rai stage;
- Binet stage;
- hemoglobin;
- platelets;
- lymphocytes;
- beta-2 microglobulin;
- LDH;
- IGHV status;
- TP53 mutation;
- del(17p);
- del(11q);
- trisomy 12;
- del(13q);
- CD38 positivity;
- ZAP70 positivity;
- synthetic risk group;
- progression at 24 months;
- time-to-first-treatment;
- follow-up time.

## Important warning

The data are simulated for educational and methodological purposes only.
They must not be interpreted as real clinical evidence.
