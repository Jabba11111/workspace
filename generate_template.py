"""
Generate an Excel template file with all supported field types,
including defense/military HR fields, with 5 example rows.
"""

import pandas as pd
from testdata_generator.generators import TestDataGenerator
from testdata_generator.field_detector import FIELD_LABELS

# Define all columns in logical groups with their field types
TEMPLATE_COLUMNS = {
    # --- Persoonlijke gegevens ---
    "Personeelsnummer": "id",
    "Voornaam": "first_name",
    "Achternaam": "last_name",
    "Geslacht": "gender",
    "Geboortedatum": "date_of_birth",
    "Geboorteplaats": "birth_place",
    "Leeftijd": "age",
    "Nationaliteit": "nationality",
    "Burgerlijke staat": "marital_status",
    "Rijksregisternummer": "national_register",
    "Paspoortnummer": "passport",
    "Identiteitskaartnummer": "id_card",
    "Bloedgroep": "blood_type",

    # --- Contactgegevens ---
    "E-mail": "email",
    "Telefoon": "phone",
    "Straat": "street",
    "Huisnummer": "house_number",
    "Postcode": "postcode",
    "Gemeente": "city",
    "Land": "country",

    # --- Noodcontact ---
    "Noodcontact naam": "emergency_contact_name",
    "Noodcontact telefoon": "emergency_contact_phone",
    "Noodcontact relatie": "emergency_contact_relation",

    # --- Militaire gegevens ---
    "Militaire rang": "military_rank",
    "Stamnummer": "military_id",
    "Dienstnummer": "service_number",
    "Eenheid": "unit",
    "Divisie": "division",
    "Kazerne": "base",
    "Beroepsspecialisatie (MOS)": "mos",
    "Datum indiensttreding": "enlistment_date",
    "Datum uitdiensttreding": "end_of_service",
    "Dienstjaren": "years_of_service",
    "Inzetstatus": "deployment_status",
    "Veiligheidsmachtiging": "security_clearance",
    "Loonschaal": "pay_grade",

    # --- Kwalificaties & prestaties ---
    "Wapenkwalificatie": "weapon_qualification",
    "Fitness score": "fitness_score",
    "Militair rijbewijs": "driver_license_military",
    "Taalvaardigheid": "language_proficiency",
    "Medailles": "medals",
    "Dog tag": "dog_tag",

    # --- Financieel ---
    "IBAN": "iban",

    # --- Overig ---
    "Bedrijf/Onderdeel": "company",
    "BTW-nummer": "vat_number",
    "EAN-code": "ean",
}


def main():
    generator = TestDataGenerator(locale="nl_BE")
    rows = generator.generate_rows(TEMPLATE_COLUMNS, num_rows=5)
    df = pd.DataFrame(rows)

    output_file = "template_defensie_hr.xlsx"

    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Testdata")

        workbook = writer.book
        worksheet = writer.sheets["Testdata"]

        # Header format
        header_fmt = workbook.add_format({
            "bold": True,
            "bg_color": "#2B5797",
            "font_color": "#FFFFFF",
            "border": 1,
            "text_wrap": True,
            "valign": "vcenter",
        })

        # Category header colors
        category_colors = {
            "Persoonlijk": "#2B5797",
            "Contact": "#217346",
            "Noodcontact": "#BF4B28",
            "Militair": "#4A2B7A",
            "Kwalificaties": "#7A6B28",
            "Financieel": "#28707A",
            "Overig": "#555555",
        }

        # Write headers with formatting
        for col_num, col_name in enumerate(df.columns):
            worksheet.write(0, col_num, col_name, header_fmt)
            # Auto-width based on content
            max_width = max(
                len(str(col_name)),
                df[col_name].astype(str).str.len().max() if len(df) > 0 else 10
            )
            worksheet.set_column(col_num, col_num, min(max_width + 2, 40))

        worksheet.set_row(0, 30)

        # Add a legend sheet
        legend_df = pd.DataFrame([
            {"Kolomnaam": col, "Veldtype": FIELD_LABELS.get(ft, ft), "Technisch type": ft}
            for col, ft in TEMPLATE_COLUMNS.items()
        ])
        legend_df.to_excel(writer, index=False, sheet_name="Legenda")

        legend_ws = writer.sheets["Legenda"]
        legend_header_fmt = workbook.add_format({
            "bold": True,
            "bg_color": "#333333",
            "font_color": "#FFFFFF",
            "border": 1,
        })
        for col_num, col_name in enumerate(legend_df.columns):
            legend_ws.write(0, col_num, col_name, legend_header_fmt)
        legend_ws.set_column(0, 0, 35)
        legend_ws.set_column(1, 1, 35)
        legend_ws.set_column(2, 2, 30)

    print(f"Template gegenereerd: {output_file}")
    print(f"  - {len(TEMPLATE_COLUMNS)} kolommen")
    print(f"  - 5 voorbeeld-rijen")
    print(f"  - Legenda sheet met veldtype-uitleg")


if __name__ == "__main__":
    main()
