"""
Automatic field type detection based on column names and sample data.
"""

import re
from typing import Optional


# Field type constants
FIELD_FIRST_NAME = "first_name"
FIELD_LAST_NAME = "last_name"
FIELD_FULL_NAME = "full_name"
FIELD_EMAIL = "email"
FIELD_PHONE = "phone"
FIELD_STREET = "street"
FIELD_HOUSE_NUMBER = "house_number"
FIELD_POSTCODE = "postcode"
FIELD_CITY = "city"
FIELD_COUNTRY = "country"
FIELD_DATE_OF_BIRTH = "date_of_birth"
FIELD_DATE = "date"
FIELD_EAN = "ean"
FIELD_IBAN = "iban"
FIELD_COMPANY = "company"
FIELD_VAT = "vat_number"
FIELD_INTEGER = "integer"
FIELD_DECIMAL = "decimal"
FIELD_BOOLEAN = "boolean"
FIELD_GENDER = "gender"
FIELD_AGE = "age"
FIELD_ID = "id"
FIELD_UUID = "uuid"
FIELD_URL = "url"
FIELD_IP_ADDRESS = "ip_address"
FIELD_NATIONALITY = "nationality"
FIELD_BIRTH_PLACE = "birth_place"
FIELD_MARITAL_STATUS = "marital_status"
FIELD_NATIONAL_REGISTER = "national_register"
FIELD_PASSPORT = "passport"
FIELD_ID_CARD = "id_card"
FIELD_MILITARY_RANK = "military_rank"
FIELD_MILITARY_ID = "military_id"
FIELD_SERVICE_NUMBER = "service_number"
FIELD_UNIT = "unit"
FIELD_DIVISION = "division"
FIELD_BASE = "base"
FIELD_ENLISTMENT_DATE = "enlistment_date"
FIELD_END_OF_SERVICE = "end_of_service"
FIELD_DEPLOYMENT_STATUS = "deployment_status"
FIELD_SECURITY_CLEARANCE = "security_clearance"
FIELD_MOS = "mos"  # Military Occupational Specialty
FIELD_BLOOD_TYPE = "blood_type"
FIELD_DOG_TAG = "dog_tag"
FIELD_EMERGENCY_CONTACT_NAME = "emergency_contact_name"
FIELD_EMERGENCY_CONTACT_PHONE = "emergency_contact_phone"
FIELD_EMERGENCY_CONTACT_RELATION = "emergency_contact_relation"
FIELD_PAY_GRADE = "pay_grade"
FIELD_YEARS_OF_SERVICE = "years_of_service"
FIELD_MEDALS = "medals"
FIELD_FITNESS_SCORE = "fitness_score"
FIELD_WEAPON_QUALIFICATION = "weapon_qualification"
FIELD_LANGUAGE_PROFICIENCY = "language_proficiency"
FIELD_DRIVER_LICENSE_MILITARY = "driver_license_military"

# --- SAP General / Basis ---
FIELD_SAP_CLIENT = "sap_client"
FIELD_SAP_COMPANY_CODE = "sap_company_code"
FIELD_SAP_PLANT = "sap_plant"
FIELD_SAP_DOCUMENT_NUMBER = "sap_document_number"
FIELD_SAP_FISCAL_YEAR = "sap_fiscal_year"
FIELD_SAP_POSTING_DATE = "sap_posting_date"
FIELD_SAP_CURRENCY = "sap_currency"
FIELD_SAP_LANGUAGE_KEY = "sap_language_key"

# --- SAP MM (Materials Management) ---
FIELD_SAP_MATERIAL_NUMBER = "sap_material_number"
FIELD_SAP_MATERIAL_DESCRIPTION = "sap_material_description"
FIELD_SAP_MATERIAL_GROUP = "sap_material_group"
FIELD_SAP_MATERIAL_TYPE = "sap_material_type"
FIELD_SAP_STORAGE_LOCATION = "sap_storage_location"
FIELD_SAP_VENDOR_NUMBER = "sap_vendor_number"
FIELD_SAP_VENDOR_NAME = "sap_vendor_name"
FIELD_SAP_PURCHASE_ORDER = "sap_purchase_order"
FIELD_SAP_PO_ITEM = "sap_po_item"
FIELD_SAP_PURCHASING_GROUP = "sap_purchasing_group"
FIELD_SAP_PURCHASING_ORG = "sap_purchasing_org"
FIELD_SAP_QUANTITY = "sap_quantity"
FIELD_SAP_UNIT_OF_MEASURE = "sap_unit_of_measure"
FIELD_SAP_NET_PRICE = "sap_net_price"
FIELD_SAP_GOODS_RECEIPT = "sap_goods_receipt"
FIELD_SAP_INVOICE_NUMBER = "sap_invoice_number"
FIELD_SAP_MOVEMENT_TYPE = "sap_movement_type"
FIELD_SAP_BATCH_NUMBER = "sap_batch_number"
FIELD_SAP_VALUATION_CLASS = "sap_valuation_class"
FIELD_SAP_MRP_TYPE = "sap_mrp_type"

# --- SAP SD (Sales & Distribution) ---
FIELD_SAP_CUSTOMER_NUMBER = "sap_customer_number"
FIELD_SAP_CUSTOMER_NAME = "sap_customer_name"
FIELD_SAP_SALES_ORDER = "sap_sales_order"
FIELD_SAP_SO_ITEM = "sap_so_item"
FIELD_SAP_SALES_ORG = "sap_sales_org"
FIELD_SAP_DISTRIBUTION_CHANNEL = "sap_distribution_channel"
FIELD_SAP_SALES_DIVISION = "sap_sales_division"
FIELD_SAP_SHIPPING_POINT = "sap_shipping_point"
FIELD_SAP_DELIVERY_NUMBER = "sap_delivery_number"
FIELD_SAP_BILLING_DOCUMENT = "sap_billing_document"
FIELD_SAP_PRICING_CONDITION = "sap_pricing_condition"
FIELD_SAP_INCOTERMS = "sap_incoterms"
FIELD_SAP_PAYMENT_TERMS = "sap_payment_terms"
FIELD_SAP_CUSTOMER_GROUP = "sap_customer_group"
FIELD_SAP_SALES_DISTRICT = "sap_sales_district"

# --- SAP FI (Financial Accounting) ---
FIELD_SAP_GL_ACCOUNT = "sap_gl_account"
FIELD_SAP_GL_ACCOUNT_DESC = "sap_gl_account_desc"
FIELD_SAP_COST_CENTER = "sap_cost_center"
FIELD_SAP_PROFIT_CENTER = "sap_profit_center"
FIELD_SAP_FI_DOCUMENT_TYPE = "sap_fi_document_type"
FIELD_SAP_DEBIT_CREDIT = "sap_debit_credit"
FIELD_SAP_AMOUNT = "sap_amount"
FIELD_SAP_TAX_CODE = "sap_tax_code"
FIELD_SAP_CLEARING_DOCUMENT = "sap_clearing_document"
FIELD_SAP_BUSINESS_AREA = "sap_business_area"

# --- SAP CO (Controlling) ---
FIELD_SAP_INTERNAL_ORDER = "sap_internal_order"
FIELD_SAP_COST_ELEMENT = "sap_cost_element"
FIELD_SAP_ACTIVITY_TYPE = "sap_activity_type"
FIELD_SAP_WBS_ELEMENT = "sap_wbs_element"
FIELD_SAP_CONTROLLING_AREA = "sap_controlling_area"

# --- SAP HR/HCM ---
FIELD_SAP_PERSONNEL_NUMBER = "sap_personnel_number"
FIELD_SAP_PERSONNEL_AREA = "sap_personnel_area"
FIELD_SAP_PERSONNEL_SUBAREA = "sap_personnel_subarea"
FIELD_SAP_EMPLOYEE_GROUP = "sap_employee_group"
FIELD_SAP_EMPLOYEE_SUBGROUP = "sap_employee_subgroup"
FIELD_SAP_ORG_UNIT = "sap_org_unit"
FIELD_SAP_POSITION = "sap_position"
FIELD_SAP_JOB = "sap_job"
FIELD_SAP_PAYROLL_AREA = "sap_payroll_area"
FIELD_SAP_WAGE_TYPE = "sap_wage_type"
FIELD_SAP_INFOTYPE = "sap_infotype"

# --- SAP PP (Production Planning) ---
FIELD_SAP_PRODUCTION_ORDER = "sap_production_order"
FIELD_SAP_BOM_NUMBER = "sap_bom_number"
FIELD_SAP_ROUTING = "sap_routing"
FIELD_SAP_WORK_CENTER = "sap_work_center"
FIELD_SAP_PLANNED_ORDER = "sap_planned_order"
FIELD_SAP_PRODUCTION_VERSION = "sap_production_version"

# --- SAP PM (Plant Maintenance) ---
FIELD_SAP_EQUIPMENT_NUMBER = "sap_equipment_number"
FIELD_SAP_FUNCTIONAL_LOCATION = "sap_functional_location"
FIELD_SAP_MAINTENANCE_ORDER = "sap_maintenance_order"
FIELD_SAP_NOTIFICATION = "sap_notification"
FIELD_SAP_MAINTENANCE_PLAN = "sap_maintenance_plan"
FIELD_SAP_OBJECT_TYPE = "sap_object_type"

# --- SAP QM (Quality Management) ---
FIELD_SAP_INSPECTION_LOT = "sap_inspection_lot"
FIELD_SAP_INSPECTION_PLAN = "sap_inspection_plan"
FIELD_SAP_CATALOG_TYPE = "sap_catalog_type"
FIELD_SAP_USAGE_DECISION = "sap_usage_decision"

# --- SAP WM/EWM (Warehouse Management) ---
FIELD_SAP_WAREHOUSE_NUMBER = "sap_warehouse_number"
FIELD_SAP_STORAGE_TYPE = "sap_storage_type"
FIELD_SAP_STORAGE_BIN = "sap_storage_bin"
FIELD_SAP_TRANSFER_ORDER = "sap_transfer_order"
FIELD_SAP_HANDLING_UNIT = "sap_handling_unit"

# --- SAP SCM (Supply Chain Management) ---
FIELD_SAP_SCM_LOCATION = "sap_scm_location"
FIELD_SAP_SCM_PRODUCT = "sap_scm_product"
FIELD_SAP_DEMAND_PLAN = "sap_demand_plan"
FIELD_SAP_TRANSPORT_LANE = "sap_transport_lane"
FIELD_SAP_SUPPLY_SOURCE = "sap_supply_source"
FIELD_SAP_QUOTA_ARRANGEMENT = "sap_quota_arrangement"
FIELD_SAP_SCHEDULING_AGREEMENT = "sap_scheduling_agreement"
FIELD_SAP_FORECAST_PROFILE = "sap_forecast_profile"

# --- SAP IS-U (Industry Solution Utilities) ---
FIELD_SAP_ISU_CONTRACT_ACCOUNT = "sap_isu_contract_account"
FIELD_SAP_ISU_BUSINESS_PARTNER = "sap_isu_business_partner"
FIELD_SAP_ISU_CONNECTION_OBJECT = "sap_isu_connection_object"
FIELD_SAP_ISU_PREMISE = "sap_isu_premise"
FIELD_SAP_ISU_INSTALLATION = "sap_isu_installation"
FIELD_SAP_ISU_DEVICE = "sap_isu_device"
FIELD_SAP_ISU_REGISTER = "sap_isu_register"
FIELD_SAP_ISU_METER_READING = "sap_isu_meter_reading"
FIELD_SAP_ISU_RATE_CATEGORY = "sap_isu_rate_category"
FIELD_SAP_ISU_DIVISION_ISU = "sap_isu_division"
FIELD_SAP_ISU_MOVE_IN_DATE = "sap_isu_move_in_date"
FIELD_SAP_ISU_MOVE_OUT_DATE = "sap_isu_move_out_date"
FIELD_SAP_ISU_POD = "sap_isu_pod"
FIELD_SAP_ISU_CONSUMPTION = "sap_isu_consumption"

# --- SAP PS (Project System) ---
FIELD_SAP_PROJECT_DEFINITION = "sap_project_definition"
FIELD_SAP_NETWORK = "sap_network"
FIELD_SAP_NETWORK_ACTIVITY = "sap_network_activity"
FIELD_SAP_MILESTONE = "sap_milestone"

FIELD_UNKNOWN = "unknown"

# Header pattern matching - maps regex patterns to field types
# Order matters: more specific patterns first
HEADER_PATTERNS = [
    # Names
    (r"(?i)^(voornaam|first[\s_-]?name|prenom|vorname|nombre)$", FIELD_FIRST_NAME),
    (r"(?i)^(achternaam|familienaam|last[\s_-]?name|surname|family[\s_-]?name|nom[\s_-]?de[\s_-]?famille|nachname|apellido)$", FIELD_LAST_NAME),
    (r"(?i)^(naam|name|volledige[\s_-]?naam|full[\s_-]?name|nom[\s_-]?complet)$", FIELD_FULL_NAME),

    # Contact
    (r"(?i)^(e[\s_-]?mail|email[\s_-]?address|emailadres|courriel)$", FIELD_EMAIL),
    (r"(?i)^(telefoon|phone|tel|telephone|gsm|mobile|mobiel|telefon|t[eé]l[eé]phone)$", FIELD_PHONE),

    # Address
    (r"(?i)^(straat|straatnaam|street|street[\s_-]?name|rue|stra[sß]e|adres|address|adresse)$", FIELD_STREET),
    (r"(?i)^(huisnummer|huisnr|house[\s_-]?number|house[\s_-]?nr|num[eé]ro|hausnummer)$", FIELD_HOUSE_NUMBER),
    (r"(?i)^(postcode|post[\s_-]?code|zip|zip[\s_-]?code|plz|code[\s_-]?postal)$", FIELD_POSTCODE),
    (r"(?i)^(stad|gemeente|city|town|woonplaats|plaats|ville|stadt|localit[eé]|commune)$", FIELD_CITY),
    (r"(?i)^(land|country|pays|staat)$", FIELD_COUNTRY),

    # Dates
    (r"(?i)^(geboortedatum|date[\s_-]?of[\s_-]?birth|birth[\s_-]?date|dob|geburtsdatum|date[\s_-]?de[\s_-]?naissance)$", FIELD_DATE_OF_BIRTH),
    (r"(?i)^(datum|date|dag|jour)$", FIELD_DATE),

    # Business
    (r"(?i)^(ean|ean[\s_-]?code|ean[\s_-]?13|barcode|gtin)$", FIELD_EAN),
    (r"(?i)^(iban|bank[\s_-]?account|bankrekening|rekeningnummer)$", FIELD_IBAN),
    (r"(?i)^(bedrijf|company|firma|onderneming|entreprise|soci[eé]t[eé]|unternehmen)$", FIELD_COMPANY),
    (r"(?i)^(btw|btw[\s_-]?nummer|vat|vat[\s_-]?number|tva|ust[\s_-]?id)$", FIELD_VAT),

    # Personal
    (r"(?i)^(geslacht|gender|sex|sexe|geschlecht)$", FIELD_GENDER),
    (r"(?i)^(leeftijd|age|alter|[aâ]ge)$", FIELD_AGE),

    # Technical
    (r"(?i)^(id|identifier|personeelsnummer|nummer|number)$", FIELD_ID),
    (r"(?i)^(uuid|guid)$", FIELD_UUID),
    (r"(?i)^(url|website|link|site|webpage)$", FIELD_URL),
    (r"(?i)^(ip|ip[\s_-]?address|ip[\s_-]?adres)$", FIELD_IP_ADDRESS),

    # Personal extended
    (r"(?i)^(nationaliteit|nationality|nationalit[eé])$", FIELD_NATIONALITY),
    (r"(?i)^(geboorteplaats|birth[\s_-]?place|lieu[\s_-]?de[\s_-]?naissance|geburtsort)$", FIELD_BIRTH_PLACE),
    (r"(?i)^(burgerlijke[\s_-]?staat|marital[\s_-]?status|[eé]tat[\s_-]?civil|familienstand)$", FIELD_MARITAL_STATUS),
    (r"(?i)^(rijksregisternummer|national[\s_-]?register|rrn|bsn|niss|num[eé]ro[\s_-]?national)$", FIELD_NATIONAL_REGISTER),
    (r"(?i)^(paspoort|passport|paspoortnummer|passport[\s_-]?number|num[eé]ro[\s_-]?de[\s_-]?passeport)$", FIELD_PASSPORT),
    (r"(?i)^(identiteitskaart(?:nummer)?|id[\s_-]?card|id[\s_-]?kaart[\s_-]?nummer|carte[\s_-]?d[\s_-]?identit[eé]|personalausweis)$", FIELD_ID_CARD),

    # Military / Defense HR
    (r"(?i)^(rang|rank|grade|militaire[\s_-]?rang|dienstgraad)$", FIELD_MILITARY_RANK),
    (r"(?i)^(militair[\s_-]?id|military[\s_-]?id|stamnummer)$", FIELD_MILITARY_ID),
    (r"(?i)^(dienstnummer|service[\s_-]?number|matricule)$", FIELD_SERVICE_NUMBER),
    (r"(?i)^(eenheid|unit|unit[eé])$", FIELD_UNIT),
    (r"(?i)^(divisie|division|brigade|regiment)$", FIELD_DIVISION),
    (r"(?i)^(kazerne|basis|base|camp|garnizoen|garrison)$", FIELD_BASE),
    (r"(?i)^(datum[\s_-]?indienst(?:treding)?|enlistment[\s_-]?date|date[\s_-]?d[\s_-]?enr[oô]lement|indiensttreding)$", FIELD_ENLISTMENT_DATE),
    (r"(?i)^(datum[\s_-]?uitdienst(?:treding)?|einde[\s_-]?dienst|end[\s_-]?of[\s_-]?service|uitdiensttreding)$", FIELD_END_OF_SERVICE),
    (r"(?i)^(inzet[\s_-]?status|deployment[\s_-]?status|operationele[\s_-]?status)$", FIELD_DEPLOYMENT_STATUS),
    (r"(?i)^(veiligheids[\s_-]?machtiging|security[\s_-]?clearance|habilitation[\s_-]?s[eé]curit[eé])$", FIELD_SECURITY_CLEARANCE),
    (r"(?i)^(specialisatie|mos|military[\s_-]?occupational[\s_-]?specialty|functie[\s_-]?code|beroepsspecialisatie)$", FIELD_MOS),
    (r"(?i)^(bloedgroep|blood[\s_-]?type|groupe[\s_-]?sanguin|blutgruppe)$", FIELD_BLOOD_TYPE),
    (r"(?i)^(dog[\s_-]?tag|identificatieplaatje|plaque[\s_-]?d[\s_-]?identit[eé])$", FIELD_DOG_TAG),
    (r"(?i)^(noodcontact[\s_-]?naam|emergency[\s_-]?contact[\s_-]?name|contact[\s_-]?urgence[\s_-]?nom)$", FIELD_EMERGENCY_CONTACT_NAME),
    (r"(?i)^(noodcontact[\s_-]?telefoon|emergency[\s_-]?contact[\s_-]?phone|contact[\s_-]?urgence[\s_-]?t[eé]l)$", FIELD_EMERGENCY_CONTACT_PHONE),
    (r"(?i)^(noodcontact[\s_-]?relatie|emergency[\s_-]?contact[\s_-]?relation|lien[\s_-]?urgence)$", FIELD_EMERGENCY_CONTACT_RELATION),
    (r"(?i)^(loonschaal|pay[\s_-]?grade|salarisschaal|[eé]chelle[\s_-]?barémique)$", FIELD_PAY_GRADE),
    (r"(?i)^(dienstjaren|years[\s_-]?of[\s_-]?service|anciennet[eé])$", FIELD_YEARS_OF_SERVICE),
    (r"(?i)^(medailles|medals|onderscheidingen|d[eé]corations)$", FIELD_MEDALS),
    (r"(?i)^(fitness[\s_-]?score|fysieke[\s_-]?score|physical[\s_-]?fitness|conditietest)$", FIELD_FITNESS_SCORE),
    (r"(?i)^(wapen[\s_-]?kwalificatie|weapon[\s_-]?qualification|qualification[\s_-]?arme|schietvaardigheidsniveau)$", FIELD_WEAPON_QUALIFICATION),
    (r"(?i)^(taalvaardigheid|language[\s_-]?proficiency|comp[eé]tence[\s_-]?linguistique)$", FIELD_LANGUAGE_PROFICIENCY),
    (r"(?i)^(militair[\s_-]?rijbewijs|military[\s_-]?driver[\s_-]?license|permis[\s_-]?militaire)$", FIELD_DRIVER_LICENSE_MILITARY),

    # --- SAP General / Basis ---
    (r"(?i)^(mandt|client|sap[\s_-]?client|mandant)$", FIELD_SAP_CLIENT),
    (r"(?i)^(bukrs|company[\s_-]?code|bedrijfscode|buchungskreis)$", FIELD_SAP_COMPANY_CODE),
    (r"(?i)^(werks|plant|werk|usine)$", FIELD_SAP_PLANT),
    (r"(?i)^(belnr|document[\s_-]?number|belegnummer|documentnummer)$", FIELD_SAP_DOCUMENT_NUMBER),
    (r"(?i)^(gjahr|fiscal[\s_-]?year|boekjaar|gesch[aä]ftsjahr)$", FIELD_SAP_FISCAL_YEAR),
    (r"(?i)^(budat|posting[\s_-]?date|boekingsdatum|buchungsdatum)$", FIELD_SAP_POSTING_DATE),
    (r"(?i)^(waers|currency|valuta|w[aä]hrung)$", FIELD_SAP_CURRENCY),
    (r"(?i)^(spras|language[\s_-]?key|taalsleutel|sprachschl[uü]ssel)$", FIELD_SAP_LANGUAGE_KEY),

    # --- SAP MM ---
    (r"(?i)^(matnr|material[\s_-]?number|materiaalnummer|materialnummer)$", FIELD_SAP_MATERIAL_NUMBER),
    (r"(?i)^(maktx|material[\s_-]?description|materiaalomschrijving|materialkurztext)$", FIELD_SAP_MATERIAL_DESCRIPTION),
    (r"(?i)^(matkl|material[\s_-]?group|materiaalgroep|materialgruppe|warengruppe)$", FIELD_SAP_MATERIAL_GROUP),
    (r"(?i)^(mtart|material[\s_-]?type|materiaaltype|materialart)$", FIELD_SAP_MATERIAL_TYPE),
    (r"(?i)^(lgort|storage[\s_-]?location|opslaglocatie|lagerort)$", FIELD_SAP_STORAGE_LOCATION),
    (r"(?i)^(lifnr|vendor[\s_-]?number|leveranciersnummer|lieferantennummer)$", FIELD_SAP_VENDOR_NUMBER),
    (r"(?i)^(vendor[\s_-]?name|leveranciersnaam|lieferantenname|name1)$", FIELD_SAP_VENDOR_NAME),
    (r"(?i)^(ebeln|purchase[\s_-]?order|bestelbon|inkooporder|bestellnummer)$", FIELD_SAP_PURCHASE_ORDER),
    (r"(?i)^(ebelp|po[\s_-]?item|bestelbon[\s_-]?positie|bestellposition)$", FIELD_SAP_PO_ITEM),
    (r"(?i)^(ekgrp|purchasing[\s_-]?group|inkoopgroep|einkaufsgruppe)$", FIELD_SAP_PURCHASING_GROUP),
    (r"(?i)^(ekorg|purchasing[\s_-]?org|inkooporganisatie|einkaufsorganisation)$", FIELD_SAP_PURCHASING_ORG),
    (r"(?i)^(menge|quantity|hoeveelheid|menge)$", FIELD_SAP_QUANTITY),
    (r"(?i)^(meins|unit[\s_-]?of[\s_-]?measure|eenheid|mengeneinheit|uom)$", FIELD_SAP_UNIT_OF_MEASURE),
    (r"(?i)^(netpr|net[\s_-]?price|nettoprijs|nettopreis)$", FIELD_SAP_NET_PRICE),
    (r"(?i)^(mblnr|goods[\s_-]?receipt|goederenontvangst|wareneingang)$", FIELD_SAP_GOODS_RECEIPT),
    (r"(?i)^(invoice[\s_-]?number|factuurnummer|rechnungsnummer)$", FIELD_SAP_INVOICE_NUMBER),
    (r"(?i)^(bwart|movement[\s_-]?type|bewegingssoort|bewegungsart)$", FIELD_SAP_MOVEMENT_TYPE),
    (r"(?i)^(charg|batch[\s_-]?number|batch|chargenummer|charge)$", FIELD_SAP_BATCH_NUMBER),
    (r"(?i)^(bklas|valuation[\s_-]?class|waarderingsklasse|bewertungsklasse)$", FIELD_SAP_VALUATION_CLASS),
    (r"(?i)^(dismm|mrp[\s_-]?type|mrp|dispositionsverfahren)$", FIELD_SAP_MRP_TYPE),

    # --- SAP SD ---
    (r"(?i)^(kunnr|customer[\s_-]?number|klantnummer|debitorennummer)$", FIELD_SAP_CUSTOMER_NUMBER),
    (r"(?i)^(customer[\s_-]?name|klantnaam|kundenname)$", FIELD_SAP_CUSTOMER_NAME),
    (r"(?i)^(vbeln|sales[\s_-]?order|verkooporder|kundenauftrag)$", FIELD_SAP_SALES_ORDER),
    (r"(?i)^(posnr|so[\s_-]?item|verkooporder[\s_-]?positie|auftragsposition)$", FIELD_SAP_SO_ITEM),
    (r"(?i)^(vkorg|sales[\s_-]?org|verkooporganisatie|verkaufsorganisation)$", FIELD_SAP_SALES_ORG),
    (r"(?i)^(vtweg|distribution[\s_-]?channel|distributiekanaal|vertriebsweg)$", FIELD_SAP_DISTRIBUTION_CHANNEL),
    (r"(?i)^(spart|sales[\s_-]?division|verkoopdivisie|sparte)$", FIELD_SAP_SALES_DIVISION),
    (r"(?i)^(vstel|shipping[\s_-]?point|verzendpunt|versandstelle)$", FIELD_SAP_SHIPPING_POINT),
    (r"(?i)^(delivery[\s_-]?number|leveringsnummer|lieferscheinnummer)$", FIELD_SAP_DELIVERY_NUMBER),
    (r"(?i)^(billing[\s_-]?document|factuurdocument|factuurbelegnummer|fakturanummer)$", FIELD_SAP_BILLING_DOCUMENT),
    (r"(?i)^(kschl|pricing[\s_-]?condition|prijsconditie|konditionsart)$", FIELD_SAP_PRICING_CONDITION),
    (r"(?i)^(inco1|incoterms)$", FIELD_SAP_INCOTERMS),
    (r"(?i)^(zterm|payment[\s_-]?terms|betalingsconditie|zahlungsbedingung)$", FIELD_SAP_PAYMENT_TERMS),
    (r"(?i)^(kdgrp|customer[\s_-]?group|klantengroep|kundengruppe)$", FIELD_SAP_CUSTOMER_GROUP),
    (r"(?i)^(bzirk|sales[\s_-]?district|verkoopdistrict|verkaufsbezirk)$", FIELD_SAP_SALES_DISTRICT),

    # --- SAP FI ---
    (r"(?i)^(hkont|saknr|gl[\s_-]?account|grootboekrekening|sachkonto)$", FIELD_SAP_GL_ACCOUNT),
    (r"(?i)^(gl[\s_-]?account[\s_-]?desc|grootboek[\s_-]?omschrijving|sachkontobezeichnung)$", FIELD_SAP_GL_ACCOUNT_DESC),
    (r"(?i)^(kostl|cost[\s_-]?center|kostenplaats|kostenstelle)$", FIELD_SAP_COST_CENTER),
    (r"(?i)^(prctr|profit[\s_-]?center|winstcentrum|profitcenter)$", FIELD_SAP_PROFIT_CENTER),
    (r"(?i)^(blart|fi[\s_-]?document[\s_-]?type|documentsoort|belegart)$", FIELD_SAP_FI_DOCUMENT_TYPE),
    (r"(?i)^(shkzg|debit[\s_-]?credit|debet[\s_-]?credit|soll[\s_-]?haben)$", FIELD_SAP_DEBIT_CREDIT),
    (r"(?i)^(dmbtr|wrbtr|amount|bedrag|betrag)$", FIELD_SAP_AMOUNT),
    (r"(?i)^(mwskz|tax[\s_-]?code|btw[\s_-]?code|steuerkennzeichen)$", FIELD_SAP_TAX_CODE),
    (r"(?i)^(augbl|clearing[\s_-]?document|verrekeningsbeleg|ausgleichsbeleg)$", FIELD_SAP_CLEARING_DOCUMENT),
    (r"(?i)^(gsber|business[\s_-]?area|bedrijfstak|gesch[aä]ftsbereich)$", FIELD_SAP_BUSINESS_AREA),

    # --- SAP CO ---
    (r"(?i)^(aufnr|internal[\s_-]?order|interne[\s_-]?order|innenauftrag)$", FIELD_SAP_INTERNAL_ORDER),
    (r"(?i)^(kstar|cost[\s_-]?element|kostensoort|kostenart)$", FIELD_SAP_COST_ELEMENT),
    (r"(?i)^(lstar|activity[\s_-]?type|activiteitssoort|leistungsart)$", FIELD_SAP_ACTIVITY_TYPE),
    (r"(?i)^(posid|wbs[\s_-]?element|psp[\s_-]?element)$", FIELD_SAP_WBS_ELEMENT),
    (r"(?i)^(kokrs|controlling[\s_-]?area|kostenrekeningschema|kostenrechnungskreis)$", FIELD_SAP_CONTROLLING_AREA),

    # --- SAP HR/HCM ---
    (r"(?i)^(pernr|personnel[\s_-]?number|sap[\s_-]?personeelsnummer|personalnummer)$", FIELD_SAP_PERSONNEL_NUMBER),
    (r"(?i)^(werks.*hr|personnel[\s_-]?area|personeelsgebied|personalbereich)$", FIELD_SAP_PERSONNEL_AREA),
    (r"(?i)^(btrtl|personnel[\s_-]?subarea|personeelsdeelgebied|personalteilbereich)$", FIELD_SAP_PERSONNEL_SUBAREA),
    (r"(?i)^(persg|employee[\s_-]?group|werknemersgroep|mitarbeitergruppe)$", FIELD_SAP_EMPLOYEE_GROUP),
    (r"(?i)^(persk|employee[\s_-]?subgroup|werknemersdeelgroep|mitarbeiterkreis)$", FIELD_SAP_EMPLOYEE_SUBGROUP),
    (r"(?i)^(orgeh|org[\s_-]?unit|organisatie[\s_-]?eenheid|organisationseinheit)$", FIELD_SAP_ORG_UNIT),
    (r"(?i)^(plans|position|positie|planstelle)$", FIELD_SAP_POSITION),
    (r"(?i)^(stell|job|functie|stelle)$", FIELD_SAP_JOB),
    (r"(?i)^(abkrs|payroll[\s_-]?area|salarisgebied|abrechnungskreis)$", FIELD_SAP_PAYROLL_AREA),
    (r"(?i)^(lgart|wage[\s_-]?type|loonsoort|lohnart)$", FIELD_SAP_WAGE_TYPE),
    (r"(?i)^(infty|infotype|infotype)$", FIELD_SAP_INFOTYPE),

    # --- SAP PP ---
    (r"(?i)^(aufnr.*prod|production[\s_-]?order|productieorder|fertigungsauftrag)$", FIELD_SAP_PRODUCTION_ORDER),
    (r"(?i)^(stlnr|bom[\s_-]?number|stuklijst|st[uü]ckliste)$", FIELD_SAP_BOM_NUMBER),
    (r"(?i)^(plnnr|routing|bewerkingsplan|arbeitsplan)$", FIELD_SAP_ROUTING),
    (r"(?i)^(arbpl|work[\s_-]?center|werkplaats|arbeitsplatz)$", FIELD_SAP_WORK_CENTER),
    (r"(?i)^(plnum|planned[\s_-]?order|planorder|planauftrag)$", FIELD_SAP_PLANNED_ORDER),
    (r"(?i)^(verid|production[\s_-]?version|productieversie|fertigungsversion)$", FIELD_SAP_PRODUCTION_VERSION),

    # --- SAP PM ---
    (r"(?i)^(equnr|equipment[\s_-]?number|uitrustingsnummer|equipmentnummer)$", FIELD_SAP_EQUIPMENT_NUMBER),
    (r"(?i)^(tplnr|functional[\s_-]?location|technische[\s_-]?plaats|technischer[\s_-]?platz)$", FIELD_SAP_FUNCTIONAL_LOCATION),
    (r"(?i)^(aufnr.*maint|maintenance[\s_-]?order|onderhoudsorder|instandhaltungsauftrag)$", FIELD_SAP_MAINTENANCE_ORDER),
    (r"(?i)^(qmnum|notification|melding|meldung)$", FIELD_SAP_NOTIFICATION),
    (r"(?i)^(warpl|maintenance[\s_-]?plan|onderhoudsplan|wartungsplan)$", FIELD_SAP_MAINTENANCE_PLAN),
    (r"(?i)^(object[\s_-]?type|objecttype|objekttyp)$", FIELD_SAP_OBJECT_TYPE),

    # --- SAP QM ---
    (r"(?i)^(prueflos|inspection[\s_-]?lot|inspectielot|pr[uü]flos)$", FIELD_SAP_INSPECTION_LOT),
    (r"(?i)^(plnty|inspection[\s_-]?plan|inspectieplan|pr[uü]fplan)$", FIELD_SAP_INSPECTION_PLAN),
    (r"(?i)^(katalogart|catalog[\s_-]?type|catalogustype)$", FIELD_SAP_CATALOG_TYPE),
    (r"(?i)^(vcode|usage[\s_-]?decision|gebruiksbeslissing|verwendungsentscheid)$", FIELD_SAP_USAGE_DECISION),

    # --- SAP WM/EWM ---
    (r"(?i)^(lgnum|warehouse[\s_-]?number|magazijnnummer|lagernummer)$", FIELD_SAP_WAREHOUSE_NUMBER),
    (r"(?i)^(lgtyp|storage[\s_-]?type|opslagtype|lagertyp)$", FIELD_SAP_STORAGE_TYPE),
    (r"(?i)^(lgpla|storage[\s_-]?bin|opslagplaats|lagerplatz)$", FIELD_SAP_STORAGE_BIN),
    (r"(?i)^(tanum|transfer[\s_-]?order|transportopdracht|transportauftrag)$", FIELD_SAP_TRANSFER_ORDER),
    (r"(?i)^(handling[\s_-]?unit|hu|behandelingseenheid)$", FIELD_SAP_HANDLING_UNIT),

    # --- SAP SCM ---
    (r"(?i)^(scm[\s_-]?location|scm[\s_-]?locatie|apo[\s_-]?location)$", FIELD_SAP_SCM_LOCATION),
    (r"(?i)^(scm[\s_-]?product|apo[\s_-]?product|scm[\s_-]?materiaal)$", FIELD_SAP_SCM_PRODUCT),
    (r"(?i)^(demand[\s_-]?plan|vraagplan|bedarfsplan)$", FIELD_SAP_DEMAND_PLAN),
    (r"(?i)^(transport[\s_-]?lane|transportroute|transportstrecke)$", FIELD_SAP_TRANSPORT_LANE),
    (r"(?i)^(supply[\s_-]?source|leveringsbron|bezugsquelle)$", FIELD_SAP_SUPPLY_SOURCE),
    (r"(?i)^(quota[\s_-]?arrangement|quotaregeling|quotierung)$", FIELD_SAP_QUOTA_ARRANGEMENT),
    (r"(?i)^(lpein|scheduling[\s_-]?agreement|afleveringsplan|lieferplan)$", FIELD_SAP_SCHEDULING_AGREEMENT),
    (r"(?i)^(forecast[\s_-]?profile|prognose[\s_-]?profiel|prognoseprofil)$", FIELD_SAP_FORECAST_PROFILE),

    # --- SAP IS-U ---
    (r"(?i)^(vkont|contract[\s_-]?account|contractrekening|vertragskontonummer)$", FIELD_SAP_ISU_CONTRACT_ACCOUNT),
    (r"(?i)^(gpart|business[\s_-]?partner[\s_-]?isu|zakenpartner|gesch[aä]ftspartner)$", FIELD_SAP_ISU_BUSINESS_PARTNER),
    (r"(?i)^(haus|connection[\s_-]?object|aansluitobject|anschlussobjekt)$", FIELD_SAP_ISU_CONNECTION_OBJECT),
    (r"(?i)^(vstelle|premise|verblijf|verbrauchsstelle)$", FIELD_SAP_ISU_PREMISE),
    (r"(?i)^(anlage|installation|installatie)$", FIELD_SAP_ISU_INSTALLATION),
    (r"(?i)^(equnr.*isu|ger[aä]t|device[\s_-]?isu|toestel|meter)$", FIELD_SAP_ISU_DEVICE),
    (r"(?i)^(zwnummer|register[\s_-]?isu|teller|z[aä]hlwerk)$", FIELD_SAP_ISU_REGISTER),
    (r"(?i)^(ablbelnr|meter[\s_-]?reading|meterstand|ablesung)$", FIELD_SAP_ISU_METER_READING),
    (r"(?i)^(taession|rate[\s_-]?category|tariefcategorie|tariftyp)$", FIELD_SAP_ISU_RATE_CATEGORY),
    (r"(?i)^(sparte.*isu|is[\s_-]?u[\s_-]?division|is[\s_-]?u[\s_-]?divisie|isu[\s_-]?division|divisie[\s_-]?isu|sparte[\s_-]?isu)$", FIELD_SAP_ISU_DIVISION_ISU),
    (r"(?i)^(einzdat|move[\s_-]?in[\s_-]?date|intrekdatum|einzugsdatum)$", FIELD_SAP_ISU_MOVE_IN_DATE),
    (r"(?i)^(auszdat|move[\s_-]?out[\s_-]?date|uittrekdatum|auszugsdatum)$", FIELD_SAP_ISU_MOVE_OUT_DATE),
    (r"(?i)^(ext_ui|pod|point[\s_-]?of[\s_-]?delivery|afleveringspunt)$", FIELD_SAP_ISU_POD),
    (r"(?i)^(consumption|verbruik|verbrauch)$", FIELD_SAP_ISU_CONSUMPTION),

    # --- SAP PS ---
    (r"(?i)^(pspid|project[\s_-]?definition|projectdefinitie|projektdefinition)$", FIELD_SAP_PROJECT_DEFINITION),
    (r"(?i)^(nplnr|network|netwerk|netzplan)$", FIELD_SAP_NETWORK),
    (r"(?i)^(vornr|network[\s_-]?activity|netwerkactiviteit|netzplanvorgang)$", FIELD_SAP_NETWORK_ACTIVITY),
    (r"(?i)^(milestone|mijlpaal|meilenstein)$", FIELD_SAP_MILESTONE),
]

# Data pattern matching - used when header matching is inconclusive
DATA_PATTERNS = [
    (r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$", FIELD_EMAIL),
    (r"^(\+?\d{1,3}[\s-]?)?\(?\d{1,4}\)?[\s.-]?\d{2,4}[\s.-]?\d{2,4}[\s.-]?\d{0,4}$", FIELD_PHONE),
    (r"^\d{4,5}$", FIELD_POSTCODE),  # European postcodes (4-5 digits)
    (r"^\d{13}$", FIELD_EAN),
    (r"^[A-Z]{2}\d{2}\s?\d{4}\s?\d{4}\s?\d{4}\s?\d{0,4}\s?\d{0,2}$", FIELD_IBAN),
    (r"^(BE|NL|DE|FR|LU)\d{8,10}$", FIELD_VAT),
    (r"^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$", FIELD_DATE),
    (r"^\d{4}[/-]\d{1,2}[/-]\d{1,2}$", FIELD_DATE),
    (r"^(true|false|ja|nee|yes|no|0|1|oui|non)$", FIELD_BOOLEAN),
    (r"^(M|F|V|m|f|v|male|female|man|vrouw|homme|femme)$", FIELD_GENDER),
    (r"^https?://", FIELD_URL),
    (r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", FIELD_IP_ADDRESS),
    (r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", FIELD_UUID),
    # ISU consumption: number + energy/volume unit
    (r"^[\d.,]+\s*(kWh|MWh|GWh|m[³3]|GJ|MJ|l|L)$", FIELD_SAP_ISU_CONSUMPTION),
]


# Human-readable labels for field types (Dutch)
FIELD_LABELS = {
    FIELD_FIRST_NAME: "Voornaam",
    FIELD_LAST_NAME: "Achternaam",
    FIELD_FULL_NAME: "Volledige naam",
    FIELD_EMAIL: "E-mailadres",
    FIELD_PHONE: "Telefoonnummer",
    FIELD_STREET: "Straatnaam",
    FIELD_HOUSE_NUMBER: "Huisnummer",
    FIELD_POSTCODE: "Postcode",
    FIELD_CITY: "Stad/Gemeente",
    FIELD_COUNTRY: "Land",
    FIELD_DATE_OF_BIRTH: "Geboortedatum",
    FIELD_DATE: "Datum",
    FIELD_EAN: "EAN-code (barcode)",
    FIELD_IBAN: "IBAN (bankrekeningnummer)",
    FIELD_COMPANY: "Bedrijfsnaam",
    FIELD_VAT: "BTW-nummer",
    FIELD_INTEGER: "Geheel getal",
    FIELD_DECIMAL: "Decimaal getal",
    FIELD_BOOLEAN: "Ja/Nee (boolean)",
    FIELD_GENDER: "Geslacht",
    FIELD_AGE: "Leeftijd",
    FIELD_ID: "ID (oplopend nummer)",
    FIELD_UUID: "UUID",
    FIELD_URL: "URL/Website",
    FIELD_IP_ADDRESS: "IP-adres",
    FIELD_NATIONALITY: "Nationaliteit",
    FIELD_BIRTH_PLACE: "Geboorteplaats",
    FIELD_MARITAL_STATUS: "Burgerlijke staat",
    FIELD_NATIONAL_REGISTER: "Rijksregisternummer / BSN",
    FIELD_PASSPORT: "Paspoortnummer",
    FIELD_ID_CARD: "Identiteitskaartnummer",
    FIELD_MILITARY_RANK: "Militaire rang",
    FIELD_MILITARY_ID: "Militair ID / Stamnummer",
    FIELD_SERVICE_NUMBER: "Dienstnummer",
    FIELD_UNIT: "Eenheid",
    FIELD_DIVISION: "Divisie / Brigade",
    FIELD_BASE: "Kazerne / Basis",
    FIELD_ENLISTMENT_DATE: "Datum indiensttreding",
    FIELD_END_OF_SERVICE: "Datum uitdiensttreding",
    FIELD_DEPLOYMENT_STATUS: "Inzetstatus",
    FIELD_SECURITY_CLEARANCE: "Veiligheidsmachtiging",
    FIELD_MOS: "Beroepsspecialisatie (MOS)",
    FIELD_BLOOD_TYPE: "Bloedgroep",
    FIELD_DOG_TAG: "Dog tag / Identificatieplaatje",
    FIELD_EMERGENCY_CONTACT_NAME: "Noodcontact naam",
    FIELD_EMERGENCY_CONTACT_PHONE: "Noodcontact telefoon",
    FIELD_EMERGENCY_CONTACT_RELATION: "Noodcontact relatie",
    FIELD_PAY_GRADE: "Loonschaal",
    FIELD_YEARS_OF_SERVICE: "Dienstjaren",
    FIELD_MEDALS: "Medailles / Onderscheidingen",
    FIELD_FITNESS_SCORE: "Fitness score",
    FIELD_WEAPON_QUALIFICATION: "Wapenkwalificatie",
    FIELD_LANGUAGE_PROFICIENCY: "Taalvaardigheid",
    FIELD_DRIVER_LICENSE_MILITARY: "Militair rijbewijs",
    # SAP General
    FIELD_SAP_CLIENT: "SAP Mandant (MANDT)",
    FIELD_SAP_COMPANY_CODE: "SAP Bedrijfscode (BUKRS)",
    FIELD_SAP_PLANT: "SAP Werk (WERKS)",
    FIELD_SAP_DOCUMENT_NUMBER: "SAP Belegnummer",
    FIELD_SAP_FISCAL_YEAR: "SAP Boekjaar (GJAHR)",
    FIELD_SAP_POSTING_DATE: "SAP Boekingsdatum (BUDAT)",
    FIELD_SAP_CURRENCY: "SAP Valuta (WAERS)",
    FIELD_SAP_LANGUAGE_KEY: "SAP Taalsleutel (SPRAS)",
    # SAP MM
    FIELD_SAP_MATERIAL_NUMBER: "SAP Materiaalnummer (MATNR)",
    FIELD_SAP_MATERIAL_DESCRIPTION: "SAP Materiaalomschrijving (MAKTX)",
    FIELD_SAP_MATERIAL_GROUP: "SAP Materiaalgroep (MATKL)",
    FIELD_SAP_MATERIAL_TYPE: "SAP Materiaaltype (MTART)",
    FIELD_SAP_STORAGE_LOCATION: "SAP Opslaglocatie (LGORT)",
    FIELD_SAP_VENDOR_NUMBER: "SAP Leveranciersnummer (LIFNR)",
    FIELD_SAP_VENDOR_NAME: "SAP Leveranciersnaam",
    FIELD_SAP_PURCHASE_ORDER: "SAP Bestelbon (EBELN)",
    FIELD_SAP_PO_ITEM: "SAP Bestelbon positie (EBELP)",
    FIELD_SAP_PURCHASING_GROUP: "SAP Inkoopgroep (EKGRP)",
    FIELD_SAP_PURCHASING_ORG: "SAP Inkooporganisatie (EKORG)",
    FIELD_SAP_QUANTITY: "SAP Hoeveelheid (MENGE)",
    FIELD_SAP_UNIT_OF_MEASURE: "SAP Eenheid (MEINS)",
    FIELD_SAP_NET_PRICE: "SAP Nettoprijs (NETPR)",
    FIELD_SAP_GOODS_RECEIPT: "SAP Goederenontvangst (MBLNR)",
    FIELD_SAP_INVOICE_NUMBER: "SAP Factuurnummer",
    FIELD_SAP_MOVEMENT_TYPE: "SAP Bewegingssoort (BWART)",
    FIELD_SAP_BATCH_NUMBER: "SAP Batchnummer (CHARG)",
    FIELD_SAP_VALUATION_CLASS: "SAP Waarderingsklasse (BKLAS)",
    FIELD_SAP_MRP_TYPE: "SAP MRP-type (DISMM)",
    # SAP SD
    FIELD_SAP_CUSTOMER_NUMBER: "SAP Klantnummer (KUNNR)",
    FIELD_SAP_CUSTOMER_NAME: "SAP Klantnaam",
    FIELD_SAP_SALES_ORDER: "SAP Verkooporder (VBELN)",
    FIELD_SAP_SO_ITEM: "SAP Verkooporder positie (POSNR)",
    FIELD_SAP_SALES_ORG: "SAP Verkooporganisatie (VKORG)",
    FIELD_SAP_DISTRIBUTION_CHANNEL: "SAP Distributiekanaal (VTWEG)",
    FIELD_SAP_SALES_DIVISION: "SAP Verkoopdivisie (SPART)",
    FIELD_SAP_SHIPPING_POINT: "SAP Verzendpunt (VSTEL)",
    FIELD_SAP_DELIVERY_NUMBER: "SAP Leveringsnummer",
    FIELD_SAP_BILLING_DOCUMENT: "SAP Factuurdocument",
    FIELD_SAP_PRICING_CONDITION: "SAP Prijsconditie (KSCHL)",
    FIELD_SAP_INCOTERMS: "SAP Incoterms",
    FIELD_SAP_PAYMENT_TERMS: "SAP Betalingsconditie (ZTERM)",
    FIELD_SAP_CUSTOMER_GROUP: "SAP Klantengroep (KDGRP)",
    FIELD_SAP_SALES_DISTRICT: "SAP Verkoopdistrict (BZIRK)",
    # SAP FI
    FIELD_SAP_GL_ACCOUNT: "SAP Grootboekrekening (SAKNR)",
    FIELD_SAP_GL_ACCOUNT_DESC: "SAP Grootboek omschrijving",
    FIELD_SAP_COST_CENTER: "SAP Kostenplaats (KOSTL)",
    FIELD_SAP_PROFIT_CENTER: "SAP Winstcentrum (PRCTR)",
    FIELD_SAP_FI_DOCUMENT_TYPE: "SAP FI Documentsoort (BLART)",
    FIELD_SAP_DEBIT_CREDIT: "SAP Debet/Credit (SHKZG)",
    FIELD_SAP_AMOUNT: "SAP Bedrag (DMBTR)",
    FIELD_SAP_TAX_CODE: "SAP BTW-code (MWSKZ)",
    FIELD_SAP_CLEARING_DOCUMENT: "SAP Verrekeningsbeleg (AUGBL)",
    FIELD_SAP_BUSINESS_AREA: "SAP Bedrijfstak (GSBER)",
    # SAP CO
    FIELD_SAP_INTERNAL_ORDER: "SAP Interne order (AUFNR)",
    FIELD_SAP_COST_ELEMENT: "SAP Kostensoort (KSTAR)",
    FIELD_SAP_ACTIVITY_TYPE: "SAP Activiteitssoort (LSTAR)",
    FIELD_SAP_WBS_ELEMENT: "SAP WBS-element (POSID)",
    FIELD_SAP_CONTROLLING_AREA: "SAP Kostenrekeningschema (KOKRS)",
    # SAP HR
    FIELD_SAP_PERSONNEL_NUMBER: "SAP Personeelsnummer (PERNR)",
    FIELD_SAP_PERSONNEL_AREA: "SAP Personeelsgebied",
    FIELD_SAP_PERSONNEL_SUBAREA: "SAP Personeelsdeelgebied (BTRTL)",
    FIELD_SAP_EMPLOYEE_GROUP: "SAP Werknemersgroep (PERSG)",
    FIELD_SAP_EMPLOYEE_SUBGROUP: "SAP Werknemersdeelgroep (PERSK)",
    FIELD_SAP_ORG_UNIT: "SAP Organisatie-eenheid (ORGEH)",
    FIELD_SAP_POSITION: "SAP Positie (PLANS)",
    FIELD_SAP_JOB: "SAP Functie (STELL)",
    FIELD_SAP_PAYROLL_AREA: "SAP Salarisgebied (ABKRS)",
    FIELD_SAP_WAGE_TYPE: "SAP Loonsoort (LGART)",
    FIELD_SAP_INFOTYPE: "SAP Infotype (INFTY)",
    # SAP PP
    FIELD_SAP_PRODUCTION_ORDER: "SAP Productieorder",
    FIELD_SAP_BOM_NUMBER: "SAP Stuklijst (STLNR)",
    FIELD_SAP_ROUTING: "SAP Bewerkingsplan (PLNNR)",
    FIELD_SAP_WORK_CENTER: "SAP Werkplaats (ARBPL)",
    FIELD_SAP_PLANNED_ORDER: "SAP Planorder (PLNUM)",
    FIELD_SAP_PRODUCTION_VERSION: "SAP Productieversie (VERID)",
    # SAP PM
    FIELD_SAP_EQUIPMENT_NUMBER: "SAP Equipmentnummer (EQUNR)",
    FIELD_SAP_FUNCTIONAL_LOCATION: "SAP Technische plaats (TPLNR)",
    FIELD_SAP_MAINTENANCE_ORDER: "SAP Onderhoudsorder",
    FIELD_SAP_NOTIFICATION: "SAP Melding (QMNUM)",
    FIELD_SAP_MAINTENANCE_PLAN: "SAP Onderhoudsplan (WARPL)",
    FIELD_SAP_OBJECT_TYPE: "SAP Objecttype",
    # SAP QM
    FIELD_SAP_INSPECTION_LOT: "SAP Inspectielot",
    FIELD_SAP_INSPECTION_PLAN: "SAP Inspectieplan",
    FIELD_SAP_CATALOG_TYPE: "SAP Catalogustype",
    FIELD_SAP_USAGE_DECISION: "SAP Gebruiksbeslissing",
    # SAP WM
    FIELD_SAP_WAREHOUSE_NUMBER: "SAP Magazijnnummer (LGNUM)",
    FIELD_SAP_STORAGE_TYPE: "SAP Opslagtype (LGTYP)",
    FIELD_SAP_STORAGE_BIN: "SAP Opslagplaats (LGPLA)",
    FIELD_SAP_TRANSFER_ORDER: "SAP Transportopdracht (TANUM)",
    FIELD_SAP_HANDLING_UNIT: "SAP Handling Unit (HU)",
    # SAP SCM
    FIELD_SAP_SCM_LOCATION: "SAP SCM Locatie",
    FIELD_SAP_SCM_PRODUCT: "SAP SCM Product",
    FIELD_SAP_DEMAND_PLAN: "SAP Vraagplan",
    FIELD_SAP_TRANSPORT_LANE: "SAP Transportroute",
    FIELD_SAP_SUPPLY_SOURCE: "SAP Leveringsbron",
    FIELD_SAP_QUOTA_ARRANGEMENT: "SAP Quotaregeling",
    FIELD_SAP_SCHEDULING_AGREEMENT: "SAP Afleveringsplan (LPEIN)",
    FIELD_SAP_FORECAST_PROFILE: "SAP Prognoseprofiel",
    # SAP IS-U
    FIELD_SAP_ISU_CONTRACT_ACCOUNT: "SAP IS-U Contractrekening (VKONT)",
    FIELD_SAP_ISU_BUSINESS_PARTNER: "SAP IS-U Zakenpartner (GPART)",
    FIELD_SAP_ISU_CONNECTION_OBJECT: "SAP IS-U Aansluitobject (HAUS)",
    FIELD_SAP_ISU_PREMISE: "SAP IS-U Verblijf (VSTELLE)",
    FIELD_SAP_ISU_INSTALLATION: "SAP IS-U Installatie (ANLAGE)",
    FIELD_SAP_ISU_DEVICE: "SAP IS-U Toestel/Meter",
    FIELD_SAP_ISU_REGISTER: "SAP IS-U Teller/Register",
    FIELD_SAP_ISU_METER_READING: "SAP IS-U Meterstand",
    FIELD_SAP_ISU_RATE_CATEGORY: "SAP IS-U Tariefcategorie",
    FIELD_SAP_ISU_DIVISION_ISU: "SAP IS-U Divisie",
    FIELD_SAP_ISU_MOVE_IN_DATE: "SAP IS-U Intrekdatum",
    FIELD_SAP_ISU_MOVE_OUT_DATE: "SAP IS-U Uittrekdatum",
    FIELD_SAP_ISU_POD: "SAP IS-U Point of Delivery (EXT_UI)",
    FIELD_SAP_ISU_CONSUMPTION: "SAP IS-U Verbruik",
    # SAP PS
    FIELD_SAP_PROJECT_DEFINITION: "SAP Projectdefinitie (PSPID)",
    FIELD_SAP_NETWORK: "SAP Netwerk (NPLNR)",
    FIELD_SAP_NETWORK_ACTIVITY: "SAP Netwerkactiviteit (VORNR)",
    FIELD_SAP_MILESTONE: "SAP Mijlpaal",
    FIELD_UNKNOWN: "Onbekend - kies handmatig",
}


def detect_field_type_from_header(header: str) -> Optional[str]:
    """Detect field type based on column header name.

    Uses multiple strategies:
    1. Exact match on the full header
    2. Extract SAP technical code from parentheses (e.g. "MATNR" from "SAP Materiaalnummer (MATNR)")
    3. Try each word in the header individually
    4. Substring search for key terms within the header
    """
    clean = header.strip()

    # Strategy 1: Exact match on full header
    for pattern, field_type in HEADER_PATTERNS:
        if re.match(pattern, clean):
            return field_type

    # Strategy 2: Extract text between parentheses and try matching that
    # e.g. "SAP Materiaalnummer (MATNR)" -> try "MATNR"
    paren_match = re.search(r"\(([^)]+)\)", clean)
    if paren_match:
        extracted = paren_match.group(1).strip()
        for pattern, field_type in HEADER_PATTERNS:
            if re.match(pattern, extracted):
                return field_type

    # Strategy 3: Try individual words from the header
    # e.g. "SAP Materiaalnummer (MATNR)" -> try "SAP", "Materiaalnummer"
    # If the header looks like a SAP field, only match SAP-typed results
    is_sap_header = bool(re.search(r"(?i)\bsap\b|is[\s_-]?u", clean))
    words = re.split(r"[\s\(\)/,;]+", clean)
    for word in words:
        word = word.strip()
        if len(word) < 2:
            continue
        for pattern, field_type in HEADER_PATTERNS:
            if re.match(pattern, word):
                if is_sap_header and not field_type.startswith("sap_"):
                    continue
                return field_type

    # Strategy 4: Substring search - remove anchors and try contains match
    # This catches cases like "Noodcontact naam" matching "noodcontact[\s_-]?naam"
    for pattern, field_type in HEADER_PATTERNS:
        if is_sap_header and not field_type.startswith("sap_"):
            continue
        # Convert exact-match pattern to a contains pattern by removing ^ and $
        contains_pattern = pattern.replace("^(", "(?:").rstrip(")")
        if contains_pattern.endswith("$"):
            contains_pattern = contains_pattern[:-1]
        try:
            if re.search(contains_pattern, clean, re.IGNORECASE):
                return field_type
        except re.error:
            continue

    return None


def detect_field_type_from_data(values: list) -> Optional[str]:
    """Detect field type based on sample data values."""
    non_empty = [str(v).strip() for v in values if str(v).strip() and str(v).strip().lower() != "nan"]
    if not non_empty:
        return None

    # Check each pattern against the sample values
    type_scores: dict[str, int] = {}
    for value in non_empty[:50]:  # Check up to 50 samples
        for pattern, field_type in DATA_PATTERNS:
            if re.match(pattern, value):
                type_scores[field_type] = type_scores.get(field_type, 0) + 1
                break

    if not type_scores:
        # Check if all numeric
        try:
            [float(v) for v in non_empty[:50]]
            # Check if integers
            if all("." not in v for v in non_empty[:50]):
                return FIELD_INTEGER
            return FIELD_DECIMAL
        except (ValueError, TypeError):
            pass
        return None

    # Return the type with the highest match ratio (>50% of samples must match)
    best_type = max(type_scores, key=type_scores.get)
    if type_scores[best_type] / len(non_empty[:50]) > 0.5:
        return best_type
    return None


def detect_field_type(header: str, sample_values: list) -> tuple[str, float]:
    """
    Detect field type using both header and data analysis.
    Returns (field_type, confidence) where confidence is 0.0-1.0.
    """
    header_type = detect_field_type_from_header(header)
    data_type = detect_field_type_from_data(sample_values)

    if header_type and data_type:
        if header_type == data_type:
            return header_type, 1.0  # Both agree
        else:
            return header_type, 0.7  # Header takes priority but lower confidence

    if header_type:
        return header_type, 0.9  # Header match alone is quite reliable

    if data_type:
        return data_type, 0.6  # Data match alone is less reliable

    return FIELD_UNKNOWN, 0.0
