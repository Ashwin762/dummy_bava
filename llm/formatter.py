import pandas as pd


EXPECTED_COLUMNS = [
    "Company",
    "Role",
    "Location",
    "Internship URL",
    "Skills",
    "Posted Date"
]


def standardize_text(value):
    return str(value).strip().title()


def clean_data(records):

    cleaned_records = []

    for item in records:

        skills = item.get("Skills", [])

        if isinstance(skills, list):
            skills = ", ".join(skills)

        cleaned = {
            "Company": standardize_text(
                item.get("Company", "")
            ),

            "Role": standardize_text(
                item.get("Role", "")
            ),

            "Location": standardize_text(
                item.get("Location", "")
            ),

            "Internship URL": str(
                item.get("Internship URL", "")
            ).strip(),

            "Skills": skills,

            "Posted Date": str(
                item.get("Posted Date", "")
            ).strip()
        }

        cleaned_records.append(cleaned)

    df = pd.DataFrame(cleaned_records)

    # Ensure all columns exist
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = df[EXPECTED_COLUMNS]

    # Remove duplicates
    df.drop_duplicates(
        subset=[
            "Company",
            "Role",
            "Internship URL"
        ],
        inplace=True
    )

    return df