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

    # =============================================
    # SAP MODULES
    # =============================================

    # --- SAP Basis / Algemeen ---
    "SAP Mandant (MANDT)": "sap_client",
    "SAP Bedrijfscode (BUKRS)": "sap_company_code",
    "SAP Werk (WERKS)": "sap_plant",
    "SAP Belegnummer": "sap_document_number",
    "SAP Boekjaar (GJAHR)": "sap_fiscal_year",
    "SAP Boekingsdatum (BUDAT)": "sap_posting_date",
    "SAP Valuta (WAERS)": "sap_currency",
    "SAP Taalsleutel (SPRAS)": "sap_language_key",

    # --- SAP MM (Materials Management) ---
    "SAP Materiaalnummer (MATNR)": "sap_material_number",
    "SAP Materiaalomschrijving (MAKTX)": "sap_material_description",
    "SAP Materiaalgroep (MATKL)": "sap_material_group",
    "SAP Materiaaltype (MTART)": "sap_material_type",
    "SAP Opslaglocatie (LGORT)": "sap_storage_location",
    "SAP Leveranciersnummer (LIFNR)": "sap_vendor_number",
    "SAP Leveranciersnaam": "sap_vendor_name",
    "SAP Bestelbon (EBELN)": "sap_purchase_order",
    "SAP Bestelbon positie (EBELP)": "sap_po_item",
    "SAP Inkoopgroep (EKGRP)": "sap_purchasing_group",
    "SAP Inkooporganisatie (EKORG)": "sap_purchasing_org",
    "SAP Hoeveelheid (MENGE)": "sap_quantity",
    "SAP Eenheid (MEINS)": "sap_unit_of_measure",
    "SAP Nettoprijs (NETPR)": "sap_net_price",
    "SAP Goederenontvangst (MBLNR)": "sap_goods_receipt",
    "SAP Factuurnummer": "sap_invoice_number",
    "SAP Bewegingssoort (BWART)": "sap_movement_type",
    "SAP Batchnummer (CHARG)": "sap_batch_number",
    "SAP Waarderingsklasse (BKLAS)": "sap_valuation_class",
    "SAP MRP-type (DISMM)": "sap_mrp_type",

    # --- SAP SD (Sales & Distribution) ---
    "SAP Klantnummer (KUNNR)": "sap_customer_number",
    "SAP Klantnaam": "sap_customer_name",
    "SAP Verkooporder (VBELN)": "sap_sales_order",
    "SAP Verkooporder positie (POSNR)": "sap_so_item",
    "SAP Verkooporganisatie (VKORG)": "sap_sales_org",
    "SAP Distributiekanaal (VTWEG)": "sap_distribution_channel",
    "SAP Verkoopdivisie (SPART)": "sap_sales_division",
    "SAP Verzendpunt (VSTEL)": "sap_shipping_point",
    "SAP Leveringsnummer": "sap_delivery_number",
    "SAP Factuurdocument": "sap_billing_document",
    "SAP Prijsconditie (KSCHL)": "sap_pricing_condition",
    "SAP Incoterms": "sap_incoterms",
    "SAP Betalingsconditie (ZTERM)": "sap_payment_terms",
    "SAP Klantengroep (KDGRP)": "sap_customer_group",
    "SAP Verkoopdistrict (BZIRK)": "sap_sales_district",

    # --- SAP FI (Financial Accounting) ---
    "SAP Grootboekrekening (SAKNR)": "sap_gl_account",
    "SAP Grootboek omschrijving": "sap_gl_account_desc",
    "SAP Kostenplaats (KOSTL)": "sap_cost_center",
    "SAP Winstcentrum (PRCTR)": "sap_profit_center",
    "SAP FI Documentsoort (BLART)": "sap_fi_document_type",
    "SAP Debet/Credit (SHKZG)": "sap_debit_credit",
    "SAP Bedrag (DMBTR)": "sap_amount",
    "SAP BTW-code (MWSKZ)": "sap_tax_code",
    "SAP Verrekeningsbeleg (AUGBL)": "sap_clearing_document",
    "SAP Bedrijfstak (GSBER)": "sap_business_area",

    # --- SAP CO (Controlling) ---
    "SAP Interne order (AUFNR)": "sap_internal_order",
    "SAP Kostensoort (KSTAR)": "sap_cost_element",
    "SAP Activiteitssoort (LSTAR)": "sap_activity_type",
    "SAP WBS-element (POSID)": "sap_wbs_element",
    "SAP Kostenrekeningschema (KOKRS)": "sap_controlling_area",

    # --- SAP HR/HCM ---
    "SAP Personeelsnummer (PERNR)": "sap_personnel_number",
    "SAP Personeelsgebied": "sap_personnel_area",
    "SAP Personeelsdeelgebied (BTRTL)": "sap_personnel_subarea",
    "SAP Werknemersgroep (PERSG)": "sap_employee_group",
    "SAP Werknemersdeelgroep (PERSK)": "sap_employee_subgroup",
    "SAP Organisatie-eenheid (ORGEH)": "sap_org_unit",
    "SAP Positie (PLANS)": "sap_position",
    "SAP Functie (STELL)": "sap_job",
    "SAP Salarisgebied (ABKRS)": "sap_payroll_area",
    "SAP Loonsoort (LGART)": "sap_wage_type",
    "SAP Infotype (INFTY)": "sap_infotype",

    # --- SAP PP (Production Planning) ---
    "SAP Productieorder": "sap_production_order",
    "SAP Stuklijst (STLNR)": "sap_bom_number",
    "SAP Bewerkingsplan (PLNNR)": "sap_routing",
    "SAP Werkplaats (ARBPL)": "sap_work_center",
    "SAP Planorder (PLNUM)": "sap_planned_order",
    "SAP Productieversie (VERID)": "sap_production_version",

    # --- SAP PM (Plant Maintenance) ---
    "SAP Equipmentnummer (EQUNR)": "sap_equipment_number",
    "SAP Technische plaats (TPLNR)": "sap_functional_location",
    "SAP Onderhoudsorder": "sap_maintenance_order",
    "SAP Melding (QMNUM)": "sap_notification",
    "SAP Onderhoudsplan (WARPL)": "sap_maintenance_plan",
    "SAP Objecttype": "sap_object_type",

    # --- SAP QM (Quality Management) ---
    "SAP Inspectielot": "sap_inspection_lot",
    "SAP Inspectieplan": "sap_inspection_plan",
    "SAP Catalogustype": "sap_catalog_type",
    "SAP Gebruiksbeslissing": "sap_usage_decision",

    # --- SAP WM/EWM (Warehouse Management) ---
    "SAP Magazijnnummer (LGNUM)": "sap_warehouse_number",
    "SAP Opslagtype (LGTYP)": "sap_storage_type",
    "SAP Opslagplaats (LGPLA)": "sap_storage_bin",
    "SAP Transportopdracht (TANUM)": "sap_transfer_order",
    "SAP Handling Unit (HU)": "sap_handling_unit",

    # --- SAP SCM (Supply Chain Management) ---
    "SAP SCM Locatie": "sap_scm_location",
    "SAP SCM Product": "sap_scm_product",
    "SAP Vraagplan": "sap_demand_plan",
    "SAP Transportroute": "sap_transport_lane",
    "SAP Leveringsbron": "sap_supply_source",
    "SAP Quotaregeling": "sap_quota_arrangement",
    "SAP Afleveringsplan (LPEIN)": "sap_scheduling_agreement",
    "SAP Prognoseprofiel": "sap_forecast_profile",

    # --- SAP IS-U (Industry Solution Utilities) ---
    "SAP IS-U Contractrekening (VKONT)": "sap_isu_contract_account",
    "SAP IS-U Zakenpartner (GPART)": "sap_isu_business_partner",
    "SAP IS-U Aansluitobject (HAUS)": "sap_isu_connection_object",
    "SAP IS-U Verblijf (VSTELLE)": "sap_isu_premise",
    "SAP IS-U Installatie (ANLAGE)": "sap_isu_installation",
    "SAP IS-U Toestel/Meter": "sap_isu_device",
    "SAP IS-U Teller/Register": "sap_isu_register",
    "SAP IS-U Meterstand": "sap_isu_meter_reading",
    "SAP IS-U Tariefcategorie": "sap_isu_rate_category",
    "SAP IS-U Divisie": "sap_isu_division",
    "SAP IS-U Intrekdatum": "sap_isu_move_in_date",
    "SAP IS-U Uittrekdatum": "sap_isu_move_out_date",
    "SAP IS-U Point of Delivery (EXT_UI)": "sap_isu_pod",
    "SAP IS-U Verbruik": "sap_isu_consumption",

    # --- SAP PS (Project System) ---
    "SAP Projectdefinitie (PSPID)": "sap_project_definition",
    "SAP Netwerk (NPLNR)": "sap_network",
    "SAP Netwerkactiviteit (VORNR)": "sap_network_activity",
    "SAP Mijlpaal": "sap_milestone",
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
