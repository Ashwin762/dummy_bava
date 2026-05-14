import pandas as pd

from openpyxl.styles import Font
from openpyxl.styles import PatternFill
from openpyxl.styles import Alignment


def export_to_excel(df, filename="internships.xlsx"):

    with pd.ExcelWriter(
        filename,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Internships"
        )

        worksheet = writer.sheets["Internships"]

        # Header styling
        header_fill = PatternFill(
            start_color="1F4E78",
            end_color="1F4E78",
            fill_type="solid"
        )

        for cell in worksheet[1]:

            cell.font = Font(
                bold=True,
                color="FFFFFF"
            )

            cell.fill = header_fill

            cell.alignment = Alignment(
                horizontal="center"
            )

        # Auto-size columns
        for column_cells in worksheet.columns:

            max_length = 0

            column_letter = column_cells[0].column_letter

            for cell in column_cells:

                try:
                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )

                except:
                    pass

            worksheet.column_dimensions[
                column_letter
            ].width = max_length + 5

    print(f"Excel exported -> {filename}")