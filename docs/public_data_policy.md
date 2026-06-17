# Public data policy

This repository is public-facing.

Allowed content:
- synthetic data;
- public datasets with clear license and citation;
- code;
- documentation;
- figures generated from synthetic or public datasets.

Forbidden content:
- hospital data;
- private patient data;
- direct identifiers;
- pseudonymization keys;
- sensitive derived datasets;
- confidential clinical notes.

Before committing data files, run:

git status --short
git diff --cached --name-only

and manually verify that no private or sensitive file is included.
