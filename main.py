import json

from llm.extractor import extract_internship_data
from llm.formatter import clean_data
from export.excel_writer import export_to_excel


def main():

    with open(
        "data/raw_input.json",
        "r",
        encoding="utf-8"
    ) as file:

        raw_data = json.load(file)

    all_records = []

    for item in raw_data:

        raw_text = item.get("text", "")

        extracted = extract_internship_data(raw_text)

        if extracted:
            all_records.extend(extracted)

    if not all_records:
        print("No data extracted.")
        return

    cleaned_df = clean_data(all_records)

    export_to_excel(
        cleaned_df,
        "internships.xlsx"
    )

    print(cleaned_df)


if __name__ == "__main__":
    main()