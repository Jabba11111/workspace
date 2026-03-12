"""
Test data generators for each detected field type.
Uses Faker for realistic data generation with European locale support.
"""

import random
import string
from datetime import date, timedelta
from typing import Optional

from faker import Faker

from .pattern_analyzer import PatternAnalyzer
from .field_detector import (
    FIELD_FIRST_NAME, FIELD_LAST_NAME, FIELD_FULL_NAME, FIELD_EMAIL,
    FIELD_PHONE, FIELD_STREET, FIELD_HOUSE_NUMBER, FIELD_POSTCODE, FIELD_CITY,
    FIELD_COUNTRY, FIELD_DATE_OF_BIRTH, FIELD_DATE, FIELD_EAN, FIELD_IBAN,
    FIELD_COMPANY, FIELD_VAT, FIELD_INTEGER, FIELD_DECIMAL, FIELD_BOOLEAN,
    FIELD_GENDER, FIELD_AGE, FIELD_ID, FIELD_UUID, FIELD_URL, FIELD_IP_ADDRESS,
    FIELD_NATIONALITY, FIELD_BIRTH_PLACE, FIELD_MARITAL_STATUS,
    FIELD_NATIONAL_REGISTER, FIELD_PASSPORT, FIELD_ID_CARD,
    FIELD_MILITARY_RANK, FIELD_MILITARY_ID, FIELD_SERVICE_NUMBER,
    FIELD_UNIT, FIELD_DIVISION, FIELD_BASE, FIELD_ENLISTMENT_DATE,
    FIELD_END_OF_SERVICE, FIELD_DEPLOYMENT_STATUS, FIELD_SECURITY_CLEARANCE,
    FIELD_MOS, FIELD_BLOOD_TYPE, FIELD_DOG_TAG,
    FIELD_EMERGENCY_CONTACT_NAME, FIELD_EMERGENCY_CONTACT_PHONE,
    FIELD_EMERGENCY_CONTACT_RELATION, FIELD_PAY_GRADE, FIELD_YEARS_OF_SERVICE,
    FIELD_MEDALS, FIELD_FITNESS_SCORE, FIELD_WEAPON_QUALIFICATION,
    FIELD_LANGUAGE_PROFICIENCY, FIELD_DRIVER_LICENSE_MILITARY,
    # SAP
    FIELD_SAP_CLIENT, FIELD_SAP_COMPANY_CODE, FIELD_SAP_PLANT,
    FIELD_SAP_DOCUMENT_NUMBER, FIELD_SAP_FISCAL_YEAR, FIELD_SAP_POSTING_DATE,
    FIELD_SAP_CURRENCY, FIELD_SAP_LANGUAGE_KEY,
    FIELD_SAP_MATERIAL_NUMBER, FIELD_SAP_MATERIAL_DESCRIPTION,
    FIELD_SAP_MATERIAL_GROUP, FIELD_SAP_MATERIAL_TYPE,
    FIELD_SAP_STORAGE_LOCATION, FIELD_SAP_VENDOR_NUMBER, FIELD_SAP_VENDOR_NAME,
    FIELD_SAP_PURCHASE_ORDER, FIELD_SAP_PO_ITEM, FIELD_SAP_PURCHASING_GROUP,
    FIELD_SAP_PURCHASING_ORG, FIELD_SAP_QUANTITY, FIELD_SAP_UNIT_OF_MEASURE,
    FIELD_SAP_NET_PRICE, FIELD_SAP_GOODS_RECEIPT, FIELD_SAP_INVOICE_NUMBER,
    FIELD_SAP_MOVEMENT_TYPE, FIELD_SAP_BATCH_NUMBER, FIELD_SAP_VALUATION_CLASS,
    FIELD_SAP_MRP_TYPE,
    FIELD_SAP_CUSTOMER_NUMBER, FIELD_SAP_CUSTOMER_NAME, FIELD_SAP_SALES_ORDER,
    FIELD_SAP_SO_ITEM, FIELD_SAP_SALES_ORG, FIELD_SAP_DISTRIBUTION_CHANNEL,
    FIELD_SAP_SALES_DIVISION, FIELD_SAP_SHIPPING_POINT,
    FIELD_SAP_DELIVERY_NUMBER, FIELD_SAP_BILLING_DOCUMENT,
    FIELD_SAP_PRICING_CONDITION, FIELD_SAP_INCOTERMS, FIELD_SAP_PAYMENT_TERMS,
    FIELD_SAP_CUSTOMER_GROUP, FIELD_SAP_SALES_DISTRICT,
    FIELD_SAP_GL_ACCOUNT, FIELD_SAP_GL_ACCOUNT_DESC, FIELD_SAP_COST_CENTER,
    FIELD_SAP_PROFIT_CENTER, FIELD_SAP_FI_DOCUMENT_TYPE, FIELD_SAP_DEBIT_CREDIT,
    FIELD_SAP_AMOUNT, FIELD_SAP_TAX_CODE, FIELD_SAP_CLEARING_DOCUMENT,
    FIELD_SAP_BUSINESS_AREA,
    FIELD_SAP_INTERNAL_ORDER, FIELD_SAP_COST_ELEMENT, FIELD_SAP_ACTIVITY_TYPE,
    FIELD_SAP_WBS_ELEMENT, FIELD_SAP_CONTROLLING_AREA,
    FIELD_SAP_PERSONNEL_NUMBER, FIELD_SAP_PERSONNEL_AREA,
    FIELD_SAP_PERSONNEL_SUBAREA, FIELD_SAP_EMPLOYEE_GROUP,
    FIELD_SAP_EMPLOYEE_SUBGROUP, FIELD_SAP_ORG_UNIT, FIELD_SAP_POSITION,
    FIELD_SAP_JOB, FIELD_SAP_PAYROLL_AREA, FIELD_SAP_WAGE_TYPE,
    FIELD_SAP_INFOTYPE,
    FIELD_SAP_PRODUCTION_ORDER, FIELD_SAP_BOM_NUMBER, FIELD_SAP_ROUTING,
    FIELD_SAP_WORK_CENTER, FIELD_SAP_PLANNED_ORDER, FIELD_SAP_PRODUCTION_VERSION,
    FIELD_SAP_EQUIPMENT_NUMBER, FIELD_SAP_FUNCTIONAL_LOCATION,
    FIELD_SAP_MAINTENANCE_ORDER, FIELD_SAP_NOTIFICATION,
    FIELD_SAP_MAINTENANCE_PLAN, FIELD_SAP_OBJECT_TYPE,
    FIELD_SAP_INSPECTION_LOT, FIELD_SAP_INSPECTION_PLAN,
    FIELD_SAP_CATALOG_TYPE, FIELD_SAP_USAGE_DECISION,
    FIELD_SAP_WAREHOUSE_NUMBER, FIELD_SAP_STORAGE_TYPE, FIELD_SAP_STORAGE_BIN,
    FIELD_SAP_TRANSFER_ORDER, FIELD_SAP_HANDLING_UNIT,
    FIELD_SAP_SCM_LOCATION, FIELD_SAP_SCM_PRODUCT, FIELD_SAP_DEMAND_PLAN,
    FIELD_SAP_TRANSPORT_LANE, FIELD_SAP_SUPPLY_SOURCE,
    FIELD_SAP_QUOTA_ARRANGEMENT, FIELD_SAP_SCHEDULING_AGREEMENT,
    FIELD_SAP_FORECAST_PROFILE,
    FIELD_SAP_ISU_CONTRACT_ACCOUNT, FIELD_SAP_ISU_BUSINESS_PARTNER,
    FIELD_SAP_ISU_CONNECTION_OBJECT, FIELD_SAP_ISU_PREMISE,
    FIELD_SAP_ISU_INSTALLATION, FIELD_SAP_ISU_DEVICE, FIELD_SAP_ISU_REGISTER,
    FIELD_SAP_ISU_METER_READING, FIELD_SAP_ISU_RATE_CATEGORY,
    FIELD_SAP_ISU_DIVISION_ISU, FIELD_SAP_ISU_MOVE_IN_DATE,
    FIELD_SAP_ISU_MOVE_OUT_DATE, FIELD_SAP_ISU_POD, FIELD_SAP_ISU_CONSUMPTION,
    FIELD_SAP_PROJECT_DEFINITION, FIELD_SAP_NETWORK, FIELD_SAP_NETWORK_ACTIVITY,
    FIELD_SAP_MILESTONE,
    FIELD_SAMPLE_BASED, FIELD_UNKNOWN,
)

# Supported European locales
LOCALE_MAP = {
    "België (NL)": "nl_BE",
    "België (FR)": "fr_BE",
    "Nederland": "nl_NL",
    "Duitsland": "de_DE",
    "Frankrijk": "fr_FR",
    "Luxemburg": "fr_FR",
    "Spanje": "es_ES",
    "Italië": "it_IT",
    "Portugal": "pt_PT",
    "Oostenrijk": "de_AT",
    "Verenigd Koninkrijk": "en_GB",
    "Ierland": "en_IE",
    "Zwitserland (DE)": "de_CH",
    "Zwitserland (FR)": "fr_CH",
    "Zweden": "sv_SE",
    "Noorwegen": "no_NO",
    "Denemarken": "da_DK",
    "Finland": "fi_FI",
    "Polen": "pl_PL",
    "Tsjechië": "cs_CZ",
}

# Country codes for IBAN/VAT generation
COUNTRY_CODES = {
    "nl_BE": "BE", "fr_BE": "BE", "nl_NL": "NL", "de_DE": "DE",
    "fr_FR": "FR", "es_ES": "ES", "it_IT": "IT", "pt_PT": "PT",
    "de_AT": "AT", "en_GB": "GB", "en_IE": "IE", "de_CH": "CH",
    "fr_CH": "CH", "sv_SE": "SE", "no_NO": "NO", "da_DK": "DK",
    "fi_FI": "FI", "pl_PL": "PL", "cs_CZ": "CZ",
}


def calculate_ean13_check_digit(digits_12: str) -> str:
    """Calculate the EAN-13 check digit according to GS1 rules."""
    total = 0
    for i, d in enumerate(digits_12):
        weight = 1 if i % 2 == 0 else 3
        total += int(d) * weight
    check = (10 - (total % 10)) % 10
    return str(check)


def generate_ean13() -> str:
    """Generate a valid EAN-13 barcode."""
    # Use common European prefixes (540-549 Belgium, 870-879 Netherlands, etc.)
    prefixes = ["540", "541", "870", "871", "400", "300", "800", "843"]
    prefix = random.choice(prefixes)
    rest = "".join([str(random.randint(0, 9)) for _ in range(9)])
    digits_12 = prefix + rest
    return digits_12 + calculate_ean13_check_digit(digits_12)


# Belgian/NATO military ranks
MILITARY_RANKS = {
    "BE": [
        # Soldaten
        "Soldaat", "Eerste Soldaat", "Korporaal", "Eerste Korporaal",
        # Onderofficieren
        "Sergeant", "Eerste Sergeant", "Eerste Sergeant-Majoor",
        "Adjudant", "Adjudant-Chef", "Adjudant-Majoor",
        # Officieren
        "Onderluitenant", "Luitenant", "Kapitein",
        "Majoor", "Luitenant-Kolonel", "Kolonel",
        # Generaals
        "Brigadegeneraal", "Generaal-Majoor", "Luitenant-Generaal", "Generaal",
    ],
    "NL": [
        "Soldaat", "Soldaat der eerste klasse", "Korporaal", "Korporaal der eerste klasse",
        "Sergeant", "Sergeant der eerste klasse", "Sergeant-majoor",
        "Adjudant-onderofficier", "Adjudant",
        "Tweede Luitenant", "Eerste Luitenant", "Kapitein",
        "Majoor", "Luitenant-Kolonel", "Kolonel",
        "Brigadegeneraal", "Generaal-majoor", "Luitenant-generaal", "Generaal",
    ],
    "DEFAULT": [
        "Private", "Private First Class", "Corporal", "Sergeant",
        "Staff Sergeant", "Sergeant First Class", "Master Sergeant",
        "Second Lieutenant", "First Lieutenant", "Captain",
        "Major", "Lieutenant Colonel", "Colonel",
        "Brigadier General", "Major General", "Lieutenant General", "General",
    ],
}

BELGIAN_UNITS = [
    "1ste Bataljon Jagers te Voet", "2de Bataljon Jagers te Voet",
    "3de Bataljon Parachutisten", "1ste Bataljon Grenadiers",
    "12de Linie - Prins Leopold", "13de Linie",
    "1ste Regiment Gidsen", "2de Regiment Lansiers",
    "4de Regiment Genie", "11de Bataljon Genie",
    "Bataljon ISTAR", "Eenheid Speciale Operaties",
    "1ste Bataljon Artillerie", "3de Bataljon Artillerie",
    "Kwartier Majoor Housiau", "Signal Battalion",
    "Medisch Interventiecentrum", "Logistiek Bataljon",
    "Luchtmachtbasis Kleine-Brogel", "Luchtmachtbasis Florennes",
    "Marinecomponent Zeebrugge", "Mine Counter Measures",
    "Cyber Command", "Inlichtingen- en Veiligheidsgroep",
]

BELGIAN_BASES = [
    "Kwartier Koning Albert I - Brussel",
    "Kwartier Koningin Elisabeth - Evere",
    "Kamp Beverlo - Leopoldsburg",
    "Kazerne Generaal Baron Jacques - Marche-en-Famenne",
    "Kwartier Majoor Housiau - Marche-en-Famenne",
    "Luchtmachtbasis Kleine-Brogel",
    "Luchtmachtbasis Florennes",
    "Marinebasis Zeebrugge",
    "Kwartier Sergeant De Bruyne - Neder-over-Heembeek",
    "Kamp Lagland - Arlon",
    "Kwartier Rucquoy - Tournai",
    "Kwartier Platteau - Peutie",
    "Kwartier Lombardsijde",
    "Kwartier Ieper",
    "Kwartier Berlaar",
]

MILITARY_MOS = [
    "Infanterist", "Artillerist", "Genieofficier", "Cavalerieofficier",
    "Luchtmachtpiloot", "Helikopterpiloot", "Navigator",
    "Verpleegkundige", "Paracommando", "EOD-specialist",
    "Communicatiespecialist", "Logistiek medewerker", "Wapeningenieur",
    "IT-specialist Cyber", "Inlichtingenanalist", "Meteoroloog",
    "Mechanieker luchtvaartuigen", "Duiker-ontmijner",
    "Brandbestrijding", "Militaire politie", "Muzikant",
    "Kok", "Chauffeur zware voertuigen", "Administratief medewerker",
]

SECURITY_CLEARANCES = [
    "Geen", "Vertrouwelijk", "Geheim", "Zeer Geheim", "Cosmic Top Secret (NATO)",
]

DEPLOYMENT_STATUSES = [
    "Beschikbaar", "Ingezet - Binnenland", "Ingezet - Buitenland",
    "In opleiding", "Verlof", "Medisch onbeschikbaar",
    "Reserve", "Stand-by", "Pensioen",
]

BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

PAY_GRADES = [
    "BV1", "BV2", "BV3", "BV4",  # Beroepsvrijwilliger
    "BOO1", "BOO2", "BOO3", "BOO4", "BOO5",  # Beroepsonderofficier
    "BOF1", "BOF2", "BOF3", "BOF4", "BOF5", "BOF6",  # Beroepsofficier
    "HO1", "HO2", "HO3", "HO4",  # Hogere officier
]

MEDALS_LIST = [
    "Militair Ereteken", "Herinneringsmedaille Buitenlandse Operaties",
    "Kruis van Ridder in de Leopoldsorde", "Medaille NATO Meritorious Service",
    "Burgerlijk Kruis 1ste Klasse", "Operatiemedaille ISAF",
    "Operatiemedaille UNIFIL", "Operatiemedaille EUTM",
    "Medaille Militaire Verdienste", "Militair Kruis 2de Klasse",
    "Herinneringsmedaille Humanitaire Operaties",
    "NATO Medal - Non Article 5",
]

WEAPON_QUALIFICATIONS = [
    "FN SCAR-L - Scherpschutter", "FN SCAR-L - Standaard",
    "FN MAG - Gekwalificeerd", "FN Minimi - Gekwalificeerd",
    "FN Five-seveN - Standaard", "FN P90 - Standaard",
    "M72 LAW - Gekwalificeerd", "Carl Gustaf - Gekwalificeerd",
    "Niet gekwalificeerd",
]

MILITARY_DRIVER_LICENSES = [
    "B - Licht voertuig", "C - Vrachtwagen", "CE - Vrachtwagen + aanhanger",
    "D - Bus / Troepenvervoer", "Rupsbandvoertuig - Piranha",
    "Rupsbandvoertuig - Pandur", "Rupsbandvoertuig - Dingo",
    "Niet van toepassing",
]

NATIONALITIES = [
    "Belgisch", "Nederlands", "Duits", "Frans", "Luxemburgs",
    "Brits", "Spaans", "Italiaans", "Portugees", "Pools",
    "Zwitsers", "Zweeds", "Noors", "Deens", "Fins",
    "Oostenrijks", "Iers", "Tsjechisch", "Grieks", "Roemeens",
]

MARITAL_STATUSES = [
    "Ongehuwd", "Gehuwd", "Wettelijk samenwonend",
    "Gescheiden", "Weduwe/Weduwnaar",
]

EMERGENCY_RELATIONS = [
    "Echtgeno(o)t(e)", "Partner", "Vader", "Moeder",
    "Broer", "Zus", "Zoon", "Dochter", "Vriend(in)",
]


# --- SAP Reference Data ---

SAP_COMPANY_CODES = ["1000", "1100", "1200", "2000", "2100", "3000", "3100", "4000"]
SAP_PLANTS = [
    "1000", "1100", "1200", "1300", "2000", "2100", "2200",
    "3000", "3100", "4000", "4100", "5000",
]
SAP_STORAGE_LOCATIONS = [
    "0001", "0002", "0003", "0010", "0020", "0100", "0200",
    "1000", "1100", "2000", "3000", "9999",
]
SAP_MATERIAL_TYPES = [
    ("ROH", "Grondstof"), ("HALB", "Halffabricaat"), ("FERT", "Eindproduct"),
    ("HIBE", "Bedrijfsmiddel"), ("VERP", "Verpakking"), ("DIEN", "Dienst"),
    ("NLAG", "Niet-voorraad"), ("ERSA", "Reserveonderdeel"), ("UNBW", "Onbewerkt"),
]
SAP_MATERIAL_GROUPS = [
    ("001", "Grondstoffen"), ("002", "Hulpstoffen"), ("003", "Verpakkingsmateriaal"),
    ("004", "Handelsartikelen"), ("005", "Kantoormiddelen"), ("006", "Technisch materiaal"),
    ("007", "Elektronica"), ("008", "Reserveonderdelen"), ("009", "Brandstof"),
    ("010", "Textiel"), ("011", "Voeding"), ("012", "Chemicaliën"),
]
SAP_PURCHASING_GROUPS = [
    ("001", "Inkoop Algemeen"), ("002", "Inkoop Technisch"), ("003", "Inkoop IT"),
    ("004", "Inkoop Diensten"), ("005", "Inkoop Logistiek"),
]
SAP_PURCHASING_ORGS = ["1000", "2000", "3000", "4000"]
SAP_UNITS_OF_MEASURE = [
    "ST", "KG", "L", "M", "M2", "M3", "PCE", "PAL", "ROL", "SET", "TO", "KM", "H",
]
SAP_MOVEMENT_TYPES = [
    ("101", "Goederenontvangst PO"), ("102", "Retour GR PO"),
    ("201", "Verbruik kostenplaats"), ("202", "Retour verbruik"),
    ("261", "Verbruik productieorder"), ("262", "Retour verbruik PO"),
    ("301", "Overplaatsing werk-werk"), ("311", "Overplaatsing locatie"),
    ("501", "Goederenontvangst zonder PO"), ("561", "Initiële opname"),
    ("601", "Goederenuitgifte levering"), ("602", "Retour goederenuitgifte"),
    ("651", "Afschrijving"), ("901", "GR blokkeervoorraad"),
]
SAP_MRP_TYPES = [
    ("PD", "MRP"), ("VB", "Verbruiksgestuurd"), ("VV", "Handmatig"),
    ("ND", "Geen planning"), ("V1", "Automatisch herbestelpunt"),
]
SAP_VALUATION_CLASSES = ["3000", "3001", "3100", "7900", "7920", "3010", "3020"]

SAP_SALES_ORGS = ["1000", "1100", "2000", "2100", "3000"]
SAP_DISTRIBUTION_CHANNELS = [
    ("10", "Directe verkoop"), ("20", "Groothandel"), ("30", "Detailhandel"),
    ("40", "E-commerce"), ("50", "Overheid"),
]
SAP_SALES_DIVISIONS = [
    ("01", "Producten"), ("02", "Diensten"), ("03", "Reserveonderdelen"),
    ("04", "Consulting"), ("10", "Militair materieel"),
]
SAP_SHIPPING_POINTS = [
    ("0001", "Verzendpunt Antwerpen"), ("0002", "Verzendpunt Brussel"),
    ("0003", "Verzendpunt Luik"), ("0004", "Verzendpunt Gent"),
]
SAP_PRICING_CONDITIONS = [
    "PR00", "PR01", "K004", "K005", "K007", "KA00", "KF00",
    "MWST", "RA00", "RA01", "RB00", "ZK05", "ZR00",
]
SAP_INCOTERMS = [
    "EXW", "FCA", "CPT", "CIP", "DAP", "DPU", "DDP", "FAS", "FOB", "CFR", "CIF",
]
SAP_PAYMENT_TERMS = [
    ("ZB01", "Netto 14 dagen"), ("ZB02", "Netto 30 dagen"),
    ("ZB03", "Netto 60 dagen"), ("ZB04", "2% 10d, netto 30d"),
    ("ZB05", "Vooruitbetaling"), ("ZB06", "Netto 45 dagen"),
]
SAP_CUSTOMER_GROUPS = [
    ("01", "Industrie"), ("02", "Handel"), ("03", "Overheid"),
    ("04", "Particulier"), ("05", "Non-profit"), ("06", "Defensie"),
]

SAP_GL_ACCOUNTS = [
    ("100000", "Kas"), ("110000", "Bank"), ("113100", "Bankrekening EUR"),
    ("140000", "Vorderingen op klanten"), ("160000", "Voorraden grondstoffen"),
    ("200000", "Crediteuren"), ("210000", "BTW te betalen"),
    ("300000", "Kapitaal"), ("400000", "Opbrengsten verkoop"),
    ("410000", "Opbrengsten diensten"), ("500000", "Grondstofkosten"),
    ("510000", "Loonkosten"), ("520000", "Afschrijvingskosten"),
    ("530000", "Energiekosten"), ("600000", "Overige kosten"),
    ("610000", "Huurkosten"), ("620000", "Verzekeringskosten"),
    ("700000", "Financiële opbrengsten"), ("800000", "Uitzonderlijke kosten"),
]
SAP_FI_DOC_TYPES = [
    ("SA", "Grootboekdocument"), ("KR", "Leveranciersfactuur"),
    ("KG", "Leverancierscreditnota"), ("DR", "Klantfactuur"),
    ("DG", "Klantcreditnota"), ("AB", "Boekhoudkundig document"),
    ("DA", "Klantdocument"), ("KA", "Leveranciersdocument"),
]
SAP_TAX_CODES = [
    ("V0", "0% BTW binnenland"), ("V1", "6% BTW"), ("V2", "12% BTW"),
    ("V3", "21% BTW"), ("VX", "BTW intracommunautair"),
    ("V4", "0% Export"), ("V5", "21% BTW verlegging"),
]

SAP_COST_CENTERS = [
    ("1000", "Directie"), ("1100", "HR"), ("1200", "Finance"),
    ("1300", "IT"), ("2000", "Productie"), ("2100", "Kwaliteit"),
    ("2200", "Logistiek"), ("3000", "Verkoop"), ("3100", "Marketing"),
    ("4000", "R&D"), ("4100", "Engineering"), ("5000", "Onderhoud"),
]
SAP_ACTIVITY_TYPES = [
    ("1410", "Machineuren"), ("1420", "Manuren"),
    ("1430", "Reparatie-uren"), ("1440", "Setup-uren"),
]

SAP_EMPLOYEE_GROUPS = [
    ("1", "Actief"), ("2", "Gepensioneerd"), ("3", "Tijdelijk"),
    ("4", "Extern"), ("5", "Stagiair"),
]
SAP_EMPLOYEE_SUBGROUPS = [
    ("01", "Voltijds onbepaalde duur"), ("02", "Deeltijds onbepaalde duur"),
    ("03", "Voltijds bepaalde duur"), ("04", "Deeltijds bepaalde duur"),
    ("05", "Interimkracht"), ("06", "Freelancer"),
]
SAP_POSITIONS = [
    ("50000001", "Manager Afdeling"), ("50000002", "Teamleider"),
    ("50000003", "Senior Specialist"), ("50000004", "Specialist"),
    ("50000005", "Junior Medewerker"), ("50000006", "Administratief bediende"),
    ("50000007", "Projectleider"), ("50000008", "Analist"),
]
SAP_JOBS = [
    ("50000001", "Manager"), ("50000002", "Ingenieur"), ("50000003", "Technicus"),
    ("50000004", "Administratief"), ("50000005", "Consultant"),
    ("50000006", "Analist"), ("50000007", "Operator"),
]
SAP_PAYROLL_AREAS = [
    ("B1", "Maandelijks bedienden"), ("B2", "Maandelijks arbeiders"),
    ("W1", "Tweewekelijks"), ("01", "Standaard"),
]
SAP_WAGE_TYPES = [
    ("1000", "Basisloon"), ("1100", "Overwerkvergoeding"),
    ("1200", "Nachtpremie"), ("1300", "Weekendpremie"),
    ("1400", "Gevarentoelage"), ("1500", "Maaltijdcheques"),
    ("2000", "Eindejaarspremie"), ("2100", "Vakantiegeld"),
    ("3000", "Kilometervergoeding"), ("3100", "Verplaatsingsvergoeding"),
]
SAP_INFOTYPES = [
    ("0000", "Maatregelen"), ("0001", "Organisatorische toewijzing"),
    ("0002", "Persoonlijke gegevens"), ("0006", "Adressen"),
    ("0007", "Geplande werktijd"), ("0008", "Basisbetalingen"),
    ("0009", "Bankgegevens"), ("0014", "Periodieke betalingen/inhoudingen"),
    ("0015", "Aanvullende betalingen"), ("0021", "Familie/personen"),
    ("0105", "Communicatie"), ("2001", "Afwezigheden"),
    ("2002", "Aanwezigheden"), ("2006", "Afwezigheidsquota"),
]

SAP_WORK_CENTERS = [
    ("MC-01", "CNC Freesmachine 1"), ("MC-02", "CNC Draaibank 2"),
    ("AS-01", "Assemblagelijn 1"), ("AS-02", "Assemblagelijn 2"),
    ("WD-01", "Laslijn 1"), ("PK-01", "Verpakkingslijn 1"),
    ("QC-01", "Kwaliteitscontrole 1"), ("MT-01", "Onderhoudswerkplaats"),
]

SAP_EQUIPMENT_TYPES = [
    ("M", "Machine"), ("V", "Voertuig"), ("E", "Elektrisch"),
    ("I", "Instrument"), ("P", "Pomp"), ("K", "Ketel"),
]

SAP_OBJECT_TYPES = [
    ("EQKT", "Equipment"), ("IFLO", "Functionele locatie"),
    ("EQUI", "Equipment technisch"), ("IFLOT", "Technische plaats"),
]

SAP_QM_CATALOG_TYPES = [
    ("1", "Foutsoorten"), ("2", "Foutoorzaken"), ("3", "Maatregelen"),
    ("5", "Activiteiten"), ("9", "Kenmerken"),
]
SAP_QM_USAGE_DECISIONS = [
    ("A", "Aanvaard"), ("R", "Afgekeurd"),
    ("A1", "Aanvaard met beperkingen"), ("A2", "Aanvaard na herbewerking"),
]

SAP_ISU_RATE_CATEGORIES = [
    ("E1", "Elektriciteit dag"), ("E2", "Elektriciteit nacht"),
    ("G1", "Aardgas normaal"), ("G2", "Aardgas sociaal"),
    ("W1", "Water huishoudelijk"), ("W2", "Water industrieel"),
]
SAP_ISU_DIVISIONS = [
    ("01", "Elektriciteit"), ("02", "Aardgas"), ("03", "Water"),
    ("04", "Warmte"), ("05", "Telecommunicatie"),
]

SAP_CURRENCIES = ["EUR", "USD", "GBP", "CHF", "SEK", "NOK", "DKK", "PLN", "CZK"]
SAP_LANGUAGE_KEYS = ["NL", "FR", "DE", "EN", "ES", "IT", "PT"]

SAP_MILESTONES = [
    "Projectstart", "Ontwerp goedgekeurd", "Prototype gereed",
    "Testfase compleet", "Go-live", "Projectafsluiting",
    "Fase 1 compleet", "Fase 2 compleet", "UAT gereed", "Overdracht",
]


def generate_valid_vat(country_code: str) -> str:
    """Generate a plausible VAT number for the given country."""
    formats = {
        "BE": lambda: f"BE0{random.randint(100000000, 999999999)}",
        "NL": lambda: f"NL{random.randint(100000000, 999999999)}B{random.randint(1, 99):02d}",
        "DE": lambda: f"DE{random.randint(100000000, 999999999)}",
        "FR": lambda: f"FR{''.join(random.choices(string.ascii_uppercase + string.digits, k=2))}{random.randint(100000000, 999999999)}",
        "LU": lambda: f"LU{random.randint(10000000, 99999999)}",
        "AT": lambda: f"ATU{random.randint(10000000, 99999999)}",
        "ES": lambda: f"ES{random.choice(string.ascii_uppercase)}{random.randint(10000000, 99999999)}",
        "IT": lambda: f"IT{random.randint(10000000000, 99999999999)}",
        "GB": lambda: f"GB{random.randint(100000000, 999999999)}",
    }
    generator = formats.get(country_code, lambda: f"{country_code}{random.randint(100000000, 999999999)}")
    return generator()


class TestDataGenerator:
    """Generates test data for detected field types."""

    def __init__(self, locale: str = "nl_BE"):
        self.locale = locale
        self.fake = Faker(locale)
        Faker.seed(None)  # Random seed each time
        self._id_counter = 0
        self._country_code = COUNTRY_CODES.get(locale, "BE")

    def generate_value(self, field_type: str, row_index: int = 0) -> str:
        """Generate a single value for the given field type."""
        generators = {
            FIELD_FIRST_NAME: self._gen_first_name,
            FIELD_LAST_NAME: self._gen_last_name,
            FIELD_FULL_NAME: self._gen_full_name,
            FIELD_EMAIL: self._gen_email,
            FIELD_PHONE: self._gen_phone,
            FIELD_STREET: self._gen_street,
            FIELD_HOUSE_NUMBER: self._gen_house_number,
            FIELD_POSTCODE: self._gen_postcode,
            FIELD_CITY: self._gen_city,
            FIELD_COUNTRY: self._gen_country,
            FIELD_DATE_OF_BIRTH: self._gen_date_of_birth,
            FIELD_DATE: self._gen_date,
            FIELD_EAN: self._gen_ean,
            FIELD_IBAN: self._gen_iban,
            FIELD_COMPANY: self._gen_company,
            FIELD_VAT: self._gen_vat,
            FIELD_INTEGER: self._gen_integer,
            FIELD_DECIMAL: self._gen_decimal,
            FIELD_BOOLEAN: self._gen_boolean,
            FIELD_GENDER: self._gen_gender,
            FIELD_AGE: self._gen_age,
            FIELD_ID: lambda: self._gen_id(row_index),
            FIELD_UUID: self._gen_uuid,
            FIELD_URL: self._gen_url,
            FIELD_IP_ADDRESS: self._gen_ip,
            FIELD_NATIONALITY: self._gen_nationality,
            FIELD_BIRTH_PLACE: self._gen_birth_place,
            FIELD_MARITAL_STATUS: self._gen_marital_status,
            FIELD_NATIONAL_REGISTER: self._gen_national_register,
            FIELD_PASSPORT: self._gen_passport,
            FIELD_ID_CARD: self._gen_id_card,
            FIELD_MILITARY_RANK: self._gen_military_rank,
            FIELD_MILITARY_ID: self._gen_military_id,
            FIELD_SERVICE_NUMBER: self._gen_service_number,
            FIELD_UNIT: self._gen_unit,
            FIELD_DIVISION: self._gen_division,
            FIELD_BASE: self._gen_base,
            FIELD_ENLISTMENT_DATE: self._gen_enlistment_date,
            FIELD_END_OF_SERVICE: self._gen_end_of_service,
            FIELD_DEPLOYMENT_STATUS: self._gen_deployment_status,
            FIELD_SECURITY_CLEARANCE: self._gen_security_clearance,
            FIELD_MOS: self._gen_mos,
            FIELD_BLOOD_TYPE: self._gen_blood_type,
            FIELD_DOG_TAG: self._gen_dog_tag,
            FIELD_EMERGENCY_CONTACT_NAME: self._gen_emergency_contact_name,
            FIELD_EMERGENCY_CONTACT_PHONE: self._gen_emergency_contact_phone,
            FIELD_EMERGENCY_CONTACT_RELATION: self._gen_emergency_contact_relation,
            FIELD_PAY_GRADE: self._gen_pay_grade,
            FIELD_YEARS_OF_SERVICE: self._gen_years_of_service,
            FIELD_MEDALS: self._gen_medals,
            FIELD_FITNESS_SCORE: self._gen_fitness_score,
            FIELD_WEAPON_QUALIFICATION: self._gen_weapon_qualification,
            FIELD_LANGUAGE_PROFICIENCY: self._gen_language_proficiency,
            FIELD_DRIVER_LICENSE_MILITARY: self._gen_driver_license_military,
            # SAP General
            FIELD_SAP_CLIENT: self._gen_sap_client,
            FIELD_SAP_COMPANY_CODE: self._gen_sap_company_code,
            FIELD_SAP_PLANT: self._gen_sap_plant,
            FIELD_SAP_DOCUMENT_NUMBER: self._gen_sap_document_number,
            FIELD_SAP_FISCAL_YEAR: self._gen_sap_fiscal_year,
            FIELD_SAP_POSTING_DATE: self._gen_sap_posting_date,
            FIELD_SAP_CURRENCY: self._gen_sap_currency,
            FIELD_SAP_LANGUAGE_KEY: self._gen_sap_language_key,
            # SAP MM
            FIELD_SAP_MATERIAL_NUMBER: self._gen_sap_material_number,
            FIELD_SAP_MATERIAL_DESCRIPTION: self._gen_sap_material_description,
            FIELD_SAP_MATERIAL_GROUP: self._gen_sap_material_group,
            FIELD_SAP_MATERIAL_TYPE: self._gen_sap_material_type,
            FIELD_SAP_STORAGE_LOCATION: self._gen_sap_storage_location,
            FIELD_SAP_VENDOR_NUMBER: self._gen_sap_vendor_number,
            FIELD_SAP_VENDOR_NAME: self._gen_sap_vendor_name,
            FIELD_SAP_PURCHASE_ORDER: self._gen_sap_purchase_order,
            FIELD_SAP_PO_ITEM: self._gen_sap_po_item,
            FIELD_SAP_PURCHASING_GROUP: self._gen_sap_purchasing_group,
            FIELD_SAP_PURCHASING_ORG: self._gen_sap_purchasing_org,
            FIELD_SAP_QUANTITY: self._gen_sap_quantity,
            FIELD_SAP_UNIT_OF_MEASURE: self._gen_sap_unit_of_measure,
            FIELD_SAP_NET_PRICE: self._gen_sap_net_price,
            FIELD_SAP_GOODS_RECEIPT: self._gen_sap_goods_receipt,
            FIELD_SAP_INVOICE_NUMBER: self._gen_sap_invoice_number,
            FIELD_SAP_MOVEMENT_TYPE: self._gen_sap_movement_type,
            FIELD_SAP_BATCH_NUMBER: self._gen_sap_batch_number,
            FIELD_SAP_VALUATION_CLASS: self._gen_sap_valuation_class,
            FIELD_SAP_MRP_TYPE: self._gen_sap_mrp_type,
            # SAP SD
            FIELD_SAP_CUSTOMER_NUMBER: self._gen_sap_customer_number,
            FIELD_SAP_CUSTOMER_NAME: self._gen_sap_customer_name,
            FIELD_SAP_SALES_ORDER: self._gen_sap_sales_order,
            FIELD_SAP_SO_ITEM: self._gen_sap_so_item,
            FIELD_SAP_SALES_ORG: self._gen_sap_sales_org,
            FIELD_SAP_DISTRIBUTION_CHANNEL: self._gen_sap_distribution_channel,
            FIELD_SAP_SALES_DIVISION: self._gen_sap_sales_division,
            FIELD_SAP_SHIPPING_POINT: self._gen_sap_shipping_point,
            FIELD_SAP_DELIVERY_NUMBER: self._gen_sap_delivery_number,
            FIELD_SAP_BILLING_DOCUMENT: self._gen_sap_billing_document,
            FIELD_SAP_PRICING_CONDITION: self._gen_sap_pricing_condition,
            FIELD_SAP_INCOTERMS: self._gen_sap_incoterms,
            FIELD_SAP_PAYMENT_TERMS: self._gen_sap_payment_terms,
            FIELD_SAP_CUSTOMER_GROUP: self._gen_sap_customer_group,
            FIELD_SAP_SALES_DISTRICT: self._gen_sap_sales_district,
            # SAP FI
            FIELD_SAP_GL_ACCOUNT: self._gen_sap_gl_account,
            FIELD_SAP_GL_ACCOUNT_DESC: self._gen_sap_gl_account_desc,
            FIELD_SAP_COST_CENTER: self._gen_sap_cost_center,
            FIELD_SAP_PROFIT_CENTER: self._gen_sap_profit_center,
            FIELD_SAP_FI_DOCUMENT_TYPE: self._gen_sap_fi_document_type,
            FIELD_SAP_DEBIT_CREDIT: self._gen_sap_debit_credit,
            FIELD_SAP_AMOUNT: self._gen_sap_amount,
            FIELD_SAP_TAX_CODE: self._gen_sap_tax_code,
            FIELD_SAP_CLEARING_DOCUMENT: self._gen_sap_clearing_document,
            FIELD_SAP_BUSINESS_AREA: self._gen_sap_business_area,
            # SAP CO
            FIELD_SAP_INTERNAL_ORDER: self._gen_sap_internal_order,
            FIELD_SAP_COST_ELEMENT: self._gen_sap_cost_element,
            FIELD_SAP_ACTIVITY_TYPE: self._gen_sap_activity_type,
            FIELD_SAP_WBS_ELEMENT: self._gen_sap_wbs_element,
            FIELD_SAP_CONTROLLING_AREA: self._gen_sap_controlling_area,
            # SAP HR
            FIELD_SAP_PERSONNEL_NUMBER: self._gen_sap_personnel_number,
            FIELD_SAP_PERSONNEL_AREA: self._gen_sap_personnel_area,
            FIELD_SAP_PERSONNEL_SUBAREA: self._gen_sap_personnel_subarea,
            FIELD_SAP_EMPLOYEE_GROUP: self._gen_sap_employee_group,
            FIELD_SAP_EMPLOYEE_SUBGROUP: self._gen_sap_employee_subgroup,
            FIELD_SAP_ORG_UNIT: self._gen_sap_org_unit,
            FIELD_SAP_POSITION: self._gen_sap_position,
            FIELD_SAP_JOB: self._gen_sap_job,
            FIELD_SAP_PAYROLL_AREA: self._gen_sap_payroll_area,
            FIELD_SAP_WAGE_TYPE: self._gen_sap_wage_type,
            FIELD_SAP_INFOTYPE: self._gen_sap_infotype,
            # SAP PP
            FIELD_SAP_PRODUCTION_ORDER: self._gen_sap_production_order,
            FIELD_SAP_BOM_NUMBER: self._gen_sap_bom_number,
            FIELD_SAP_ROUTING: self._gen_sap_routing,
            FIELD_SAP_WORK_CENTER: self._gen_sap_work_center,
            FIELD_SAP_PLANNED_ORDER: self._gen_sap_planned_order,
            FIELD_SAP_PRODUCTION_VERSION: self._gen_sap_production_version,
            # SAP PM
            FIELD_SAP_EQUIPMENT_NUMBER: self._gen_sap_equipment_number,
            FIELD_SAP_FUNCTIONAL_LOCATION: self._gen_sap_functional_location,
            FIELD_SAP_MAINTENANCE_ORDER: self._gen_sap_maintenance_order,
            FIELD_SAP_NOTIFICATION: self._gen_sap_notification,
            FIELD_SAP_MAINTENANCE_PLAN: self._gen_sap_maintenance_plan,
            FIELD_SAP_OBJECT_TYPE: self._gen_sap_object_type,
            # SAP QM
            FIELD_SAP_INSPECTION_LOT: self._gen_sap_inspection_lot,
            FIELD_SAP_INSPECTION_PLAN: self._gen_sap_inspection_plan,
            FIELD_SAP_CATALOG_TYPE: self._gen_sap_catalog_type,
            FIELD_SAP_USAGE_DECISION: self._gen_sap_usage_decision,
            # SAP WM
            FIELD_SAP_WAREHOUSE_NUMBER: self._gen_sap_warehouse_number,
            FIELD_SAP_STORAGE_TYPE: self._gen_sap_storage_type,
            FIELD_SAP_STORAGE_BIN: self._gen_sap_storage_bin,
            FIELD_SAP_TRANSFER_ORDER: self._gen_sap_transfer_order,
            FIELD_SAP_HANDLING_UNIT: self._gen_sap_handling_unit,
            # SAP SCM
            FIELD_SAP_SCM_LOCATION: self._gen_sap_scm_location,
            FIELD_SAP_SCM_PRODUCT: self._gen_sap_scm_product,
            FIELD_SAP_DEMAND_PLAN: self._gen_sap_demand_plan,
            FIELD_SAP_TRANSPORT_LANE: self._gen_sap_transport_lane,
            FIELD_SAP_SUPPLY_SOURCE: self._gen_sap_supply_source,
            FIELD_SAP_QUOTA_ARRANGEMENT: self._gen_sap_quota_arrangement,
            FIELD_SAP_SCHEDULING_AGREEMENT: self._gen_sap_scheduling_agreement,
            FIELD_SAP_FORECAST_PROFILE: self._gen_sap_forecast_profile,
            # SAP IS-U
            FIELD_SAP_ISU_CONTRACT_ACCOUNT: self._gen_sap_isu_contract_account,
            FIELD_SAP_ISU_BUSINESS_PARTNER: self._gen_sap_isu_business_partner,
            FIELD_SAP_ISU_CONNECTION_OBJECT: self._gen_sap_isu_connection_object,
            FIELD_SAP_ISU_PREMISE: self._gen_sap_isu_premise,
            FIELD_SAP_ISU_INSTALLATION: self._gen_sap_isu_installation,
            FIELD_SAP_ISU_DEVICE: self._gen_sap_isu_device,
            FIELD_SAP_ISU_REGISTER: self._gen_sap_isu_register,
            FIELD_SAP_ISU_METER_READING: self._gen_sap_isu_meter_reading,
            FIELD_SAP_ISU_RATE_CATEGORY: self._gen_sap_isu_rate_category,
            FIELD_SAP_ISU_DIVISION_ISU: self._gen_sap_isu_division,
            FIELD_SAP_ISU_MOVE_IN_DATE: self._gen_sap_isu_move_in_date,
            FIELD_SAP_ISU_MOVE_OUT_DATE: self._gen_sap_isu_move_out_date,
            FIELD_SAP_ISU_POD: self._gen_sap_isu_pod,
            FIELD_SAP_ISU_CONSUMPTION: self._gen_sap_isu_consumption,
            # SAP PS
            FIELD_SAP_PROJECT_DEFINITION: self._gen_sap_project_definition,
            FIELD_SAP_NETWORK: self._gen_sap_network,
            FIELD_SAP_NETWORK_ACTIVITY: self._gen_sap_network_activity,
            FIELD_SAP_MILESTONE: self._gen_sap_milestone,
            FIELD_SAMPLE_BASED: self._gen_unknown,
            FIELD_UNKNOWN: self._gen_unknown,
        }
        gen = generators.get(field_type, self._gen_unknown)
        return str(gen())

    def generate_rows(
        self,
        field_config: dict[str, str],
        num_rows: int,
        sample_data: Optional[dict[str, list]] = None,
    ) -> list[dict]:
        """
        Generate multiple rows of test data.
        field_config: {column_name: field_type}
        sample_data: {column_name: [sample_values]} - used for sample_based fields
        """
        # Pre-build PatternAnalyzers for sample-based fields
        analyzers: dict[str, PatternAnalyzer] = {}
        if sample_data:
            for col_name, field_type in field_config.items():
                if field_type == FIELD_SAMPLE_BASED and col_name in sample_data:
                    analyzers[col_name] = PatternAnalyzer(sample_data[col_name])

        rows = []
        self._id_counter = 0
        for i in range(num_rows):
            row = {}
            for col_name, field_type in field_config.items():
                if field_type == FIELD_SAMPLE_BASED and col_name in analyzers:
                    row[col_name] = analyzers[col_name].generate()
                else:
                    row[col_name] = self.generate_value(field_type, i)
            rows.append(row)
        return rows

    # --- Individual generators ---

    def _gen_first_name(self) -> str:
        return self.fake.first_name()

    def _gen_last_name(self) -> str:
        return self.fake.last_name()

    def _gen_full_name(self) -> str:
        return self.fake.name()

    def _gen_email(self) -> str:
        return self.fake.email()

    def _gen_phone(self) -> str:
        return self.fake.phone_number()

    def _gen_street(self) -> str:
        return self.fake.street_name()

    def _gen_house_number(self) -> str:
        num = random.randint(1, 250)
        if random.random() < 0.1:
            num = f"{num}{random.choice(['A', 'B', 'C', ' bus 1', ' bus 2'])}"
        return str(num)

    def _gen_postcode(self) -> str:
        return self.fake.postcode()

    def _gen_city(self) -> str:
        return self.fake.city()

    def _gen_country(self) -> str:
        return self.fake.country()

    def _gen_date_of_birth(self) -> str:
        start = date(1950, 1, 1)
        end = date(2005, 12, 31)
        delta = end - start
        random_date = start + timedelta(days=random.randint(0, delta.days))
        return random_date.strftime("%d/%m/%Y")

    def _gen_date(self) -> str:
        start = date(2020, 1, 1)
        end = date.today()
        delta = end - start
        random_date = start + timedelta(days=random.randint(0, delta.days))
        return random_date.strftime("%d/%m/%Y")

    def _gen_ean(self) -> str:
        return generate_ean13()

    def _gen_iban(self) -> str:
        return self.fake.iban()

    def _gen_company(self) -> str:
        return self.fake.company()

    def _gen_vat(self) -> str:
        return generate_valid_vat(self._country_code)

    def _gen_integer(self) -> str:
        return str(random.randint(0, 10000))

    def _gen_decimal(self) -> str:
        return f"{random.uniform(0, 10000):.2f}"

    def _gen_boolean(self) -> str:
        return random.choice(["Ja", "Nee"])

    def _gen_gender(self) -> str:
        return random.choice(["M", "V"])

    def _gen_age(self) -> str:
        return str(random.randint(18, 90))

    def _gen_id(self, row_index: int) -> str:
        self._id_counter = row_index + 1
        return str(self._id_counter)

    def _gen_uuid(self) -> str:
        return self.fake.uuid4()

    def _gen_url(self) -> str:
        return self.fake.url()

    def _gen_ip(self) -> str:
        return self.fake.ipv4()

    def _gen_nationality(self) -> str:
        return random.choice(NATIONALITIES)

    def _gen_birth_place(self) -> str:
        return self.fake.city()

    def _gen_marital_status(self) -> str:
        return random.choice(MARITAL_STATUSES)

    def _gen_national_register(self) -> str:
        # Belgian RRN format: YY.MM.DD-XXX.CC
        year = random.randint(50, 99) if random.random() < 0.5 else random.randint(0, 5)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        seq = random.randint(1, 997)
        base = f"{year:02d}{month:02d}{day:02d}{seq:03d}"
        # For people born after 2000, prefix with 2
        if year < 10:
            check_base = int(f"2{base}")
        else:
            check_base = int(base)
        check = 97 - (check_base % 97)
        return f"{year:02d}.{month:02d}.{day:02d}-{seq:03d}.{check:02d}"

    def _gen_passport(self) -> str:
        # Belgian passport: 2 letters + 7 digits
        letters = "".join(random.choices(string.ascii_uppercase, k=2))
        digits = "".join(random.choices(string.digits, k=7))
        return f"{letters}{digits}"

    def _gen_id_card(self) -> str:
        # Belgian eID: 12 digits (XXX-XXXXXXX-XX)
        p1 = random.randint(100, 999)
        p2 = random.randint(1000000, 9999999)
        p3 = random.randint(10, 99)
        return f"{p1}-{p2}-{p3}"

    def _gen_military_rank(self) -> str:
        ranks = MILITARY_RANKS.get(self._country_code, MILITARY_RANKS["DEFAULT"])
        return random.choice(ranks)

    def _gen_military_id(self) -> str:
        # Format: MXXXXXX
        return f"M{random.randint(100000, 999999)}"

    def _gen_service_number(self) -> str:
        # Format: XX-XXXXXX
        return f"{random.randint(10, 99)}-{random.randint(100000, 999999)}"

    def _gen_unit(self) -> str:
        return random.choice(BELGIAN_UNITS)

    def _gen_division(self) -> str:
        divisions = [
            "Landcomponent", "Luchtcomponent", "Marinecomponent",
            "Medische Component", "Licht Brigade",
            "Middelzware Brigade", "ISTAR-groep",
            "Special Operations Regiment",
        ]
        return random.choice(divisions)

    def _gen_base(self) -> str:
        return random.choice(BELGIAN_BASES)

    def _gen_enlistment_date(self) -> str:
        start = date(1985, 1, 1)
        end = date(2024, 12, 31)
        delta = end - start
        random_date = start + timedelta(days=random.randint(0, delta.days))
        return random_date.strftime("%d/%m/%Y")

    def _gen_end_of_service(self) -> str:
        # Some are still active (empty), some have an end date
        if random.random() < 0.3:
            return ""  # Still active
        start = date(2000, 1, 1)
        end = date(2026, 12, 31)
        delta = end - start
        random_date = start + timedelta(days=random.randint(0, delta.days))
        return random_date.strftime("%d/%m/%Y")

    def _gen_deployment_status(self) -> str:
        return random.choice(DEPLOYMENT_STATUSES)

    def _gen_security_clearance(self) -> str:
        return random.choice(SECURITY_CLEARANCES)

    def _gen_mos(self) -> str:
        return random.choice(MILITARY_MOS)

    def _gen_blood_type(self) -> str:
        return random.choice(BLOOD_TYPES)

    def _gen_dog_tag(self) -> str:
        last = self.fake.last_name().upper()
        first = self.fake.first_name()[0].upper()
        mid = random.choice(string.ascii_uppercase)
        blood = random.choice(BLOOD_TYPES)
        svc = f"{random.randint(10, 99)}-{random.randint(100000, 999999)}"
        return f"{last} {first}.{mid}. / {svc} / {blood}"

    def _gen_emergency_contact_name(self) -> str:
        return self.fake.name()

    def _gen_emergency_contact_phone(self) -> str:
        return self.fake.phone_number()

    def _gen_emergency_contact_relation(self) -> str:
        return random.choice(EMERGENCY_RELATIONS)

    def _gen_pay_grade(self) -> str:
        return random.choice(PAY_GRADES)

    def _gen_years_of_service(self) -> str:
        return str(random.randint(0, 40))

    def _gen_medals(self) -> str:
        count = random.randint(0, 3)
        if count == 0:
            return "Geen"
        return "; ".join(random.sample(MEDALS_LIST, count))

    def _gen_fitness_score(self) -> str:
        score = random.randint(40, 100)
        if score >= 80:
            label = "Uitstekend"
        elif score >= 65:
            label = "Goed"
        elif score >= 50:
            label = "Voldoende"
        else:
            label = "Onvoldoende"
        return f"{score}/100 ({label})"

    def _gen_weapon_qualification(self) -> str:
        return random.choice(WEAPON_QUALIFICATIONS)

    def _gen_language_proficiency(self) -> str:
        languages = {
            "Nederlands": random.choice(["A1", "A2", "B1", "B2", "C1", "C2", "Moedertaal"]),
            "Frans": random.choice(["A1", "A2", "B1", "B2", "C1", "C2", "Moedertaal"]),
            "Engels": random.choice(["A1", "A2", "B1", "B2", "C1", "C2"]),
            "Duits": random.choice(["A1", "A2", "B1", "B2", "C1"]),
        }
        # Pick 2-4 languages
        selected = random.sample(list(languages.items()), random.randint(2, 4))
        return "; ".join(f"{lang}: {level}" for lang, level in selected)

    def _gen_driver_license_military(self) -> str:
        return random.choice(MILITARY_DRIVER_LICENSES)

    # --- SAP Generators ---

    def _gen_sap_client(self) -> str:
        return random.choice(["100", "200", "300", "400", "800", "900"])

    def _gen_sap_company_code(self) -> str:
        return random.choice(SAP_COMPANY_CODES)

    def _gen_sap_plant(self) -> str:
        return random.choice(SAP_PLANTS)

    def _gen_sap_document_number(self) -> str:
        return f"{random.randint(100000000, 999999999):010d}"

    def _gen_sap_fiscal_year(self) -> str:
        return str(random.randint(2020, 2026))

    def _gen_sap_posting_date(self) -> str:
        start = date(2023, 1, 1)
        end = date.today()
        delta = end - start
        d = start + timedelta(days=random.randint(0, delta.days))
        return d.strftime("%d.%m.%Y")

    def _gen_sap_currency(self) -> str:
        return random.choice(SAP_CURRENCIES)

    def _gen_sap_language_key(self) -> str:
        return random.choice(SAP_LANGUAGE_KEYS)

    # SAP MM
    def _gen_sap_material_number(self) -> str:
        prefix = random.choice(["MAT", "ROH", "FRT", "HLB", "ERS"])
        return f"{prefix}-{random.randint(100000, 999999)}"

    def _gen_sap_material_description(self) -> str:
        adjectives = ["Standaard", "Premium", "Industrieel", "Technisch", "Speciaal"]
        nouns = [
            "Bout M8x40", "Moer M10", "Lager 6205", "Kabel 3x2.5mm",
            "Pomp onderdeel", "Filter element", "Afdichtring", "Pakking",
            "Smeermiddel", "Reinigingsmiddel", "Beschermkap", "Sensor",
            "Klep DN50", "Buis 100mm", "Plaat 2mm staal", "Profiel HEA200",
        ]
        return f"{random.choice(adjectives)} {random.choice(nouns)}"

    def _gen_sap_material_group(self) -> str:
        code, desc = random.choice(SAP_MATERIAL_GROUPS)
        return f"{code} - {desc}"

    def _gen_sap_material_type(self) -> str:
        code, desc = random.choice(SAP_MATERIAL_TYPES)
        return f"{code} - {desc}"

    def _gen_sap_storage_location(self) -> str:
        return random.choice(SAP_STORAGE_LOCATIONS)

    def _gen_sap_vendor_number(self) -> str:
        return f"{random.randint(100000, 999999):010d}"

    def _gen_sap_vendor_name(self) -> str:
        return self.fake.company()

    def _gen_sap_purchase_order(self) -> str:
        return f"45{random.randint(10000000, 99999999)}"

    def _gen_sap_po_item(self) -> str:
        return f"{random.randint(1, 20) * 10:05d}"

    def _gen_sap_purchasing_group(self) -> str:
        code, desc = random.choice(SAP_PURCHASING_GROUPS)
        return f"{code} - {desc}"

    def _gen_sap_purchasing_org(self) -> str:
        return random.choice(SAP_PURCHASING_ORGS)

    def _gen_sap_quantity(self) -> str:
        return f"{random.uniform(1, 5000):.2f}"

    def _gen_sap_unit_of_measure(self) -> str:
        return random.choice(SAP_UNITS_OF_MEASURE)

    def _gen_sap_net_price(self) -> str:
        return f"{random.uniform(0.50, 50000):.2f}"

    def _gen_sap_goods_receipt(self) -> str:
        return f"50{random.randint(10000000, 99999999)}"

    def _gen_sap_invoice_number(self) -> str:
        return f"51{random.randint(10000000, 99999999)}"

    def _gen_sap_movement_type(self) -> str:
        code, desc = random.choice(SAP_MOVEMENT_TYPES)
        return f"{code} - {desc}"

    def _gen_sap_batch_number(self) -> str:
        year = random.randint(2023, 2026)
        seq = random.randint(1, 9999)
        return f"B{year}{seq:04d}"

    def _gen_sap_valuation_class(self) -> str:
        return random.choice(SAP_VALUATION_CLASSES)

    def _gen_sap_mrp_type(self) -> str:
        code, desc = random.choice(SAP_MRP_TYPES)
        return f"{code} - {desc}"

    # SAP SD
    def _gen_sap_customer_number(self) -> str:
        return f"{random.randint(100000, 999999):010d}"

    def _gen_sap_customer_name(self) -> str:
        return self.fake.company()

    def _gen_sap_sales_order(self) -> str:
        return f"{random.randint(100000000, 999999999):010d}"

    def _gen_sap_so_item(self) -> str:
        return f"{random.randint(1, 30) * 10:06d}"

    def _gen_sap_sales_org(self) -> str:
        return random.choice(SAP_SALES_ORGS)

    def _gen_sap_distribution_channel(self) -> str:
        code, desc = random.choice(SAP_DISTRIBUTION_CHANNELS)
        return f"{code} - {desc}"

    def _gen_sap_sales_division(self) -> str:
        code, desc = random.choice(SAP_SALES_DIVISIONS)
        return f"{code} - {desc}"

    def _gen_sap_shipping_point(self) -> str:
        code, desc = random.choice(SAP_SHIPPING_POINTS)
        return f"{code} - {desc}"

    def _gen_sap_delivery_number(self) -> str:
        return f"80{random.randint(10000000, 99999999)}"

    def _gen_sap_billing_document(self) -> str:
        return f"90{random.randint(10000000, 99999999)}"

    def _gen_sap_pricing_condition(self) -> str:
        return random.choice(SAP_PRICING_CONDITIONS)

    def _gen_sap_incoterms(self) -> str:
        return random.choice(SAP_INCOTERMS)

    def _gen_sap_payment_terms(self) -> str:
        code, desc = random.choice(SAP_PAYMENT_TERMS)
        return f"{code} - {desc}"

    def _gen_sap_customer_group(self) -> str:
        code, desc = random.choice(SAP_CUSTOMER_GROUPS)
        return f"{code} - {desc}"

    def _gen_sap_sales_district(self) -> str:
        districts = [
            ("BE01", "Vlaanderen"), ("BE02", "Wallonië"), ("BE03", "Brussel"),
            ("NL01", "Randstad"), ("NL02", "Zuid"), ("DE01", "West"),
        ]
        code, desc = random.choice(districts)
        return f"{code} - {desc}"

    # SAP FI
    def _gen_sap_gl_account(self) -> str:
        code, _ = random.choice(SAP_GL_ACCOUNTS)
        return code

    def _gen_sap_gl_account_desc(self) -> str:
        _, desc = random.choice(SAP_GL_ACCOUNTS)
        return desc

    def _gen_sap_cost_center(self) -> str:
        code, desc = random.choice(SAP_COST_CENTERS)
        return f"{code} - {desc}"

    def _gen_sap_profit_center(self) -> str:
        return f"PC{random.randint(1000, 9999)}"

    def _gen_sap_fi_document_type(self) -> str:
        code, desc = random.choice(SAP_FI_DOC_TYPES)
        return f"{code} - {desc}"

    def _gen_sap_debit_credit(self) -> str:
        return random.choice(["S - Debet", "H - Credit"])

    def _gen_sap_amount(self) -> str:
        return f"{random.uniform(10, 500000):.2f}"

    def _gen_sap_tax_code(self) -> str:
        code, desc = random.choice(SAP_TAX_CODES)
        return f"{code} - {desc}"

    def _gen_sap_clearing_document(self) -> str:
        if random.random() < 0.3:
            return ""
        return f"{random.randint(100000000, 999999999):010d}"

    def _gen_sap_business_area(self) -> str:
        areas = [("1000", "Operations"), ("2000", "Support"), ("3000", "Defensie")]
        code, desc = random.choice(areas)
        return f"{code} - {desc}"

    # SAP CO
    def _gen_sap_internal_order(self) -> str:
        return f"{random.randint(800000, 899999)}"

    def _gen_sap_cost_element(self) -> str:
        elements = [
            ("400000", "Materiaalkosten"), ("410000", "Externe diensten"),
            ("420000", "Loonkosten"), ("430000", "Afschrijvingen"),
            ("440000", "Overige kosten"),
        ]
        code, desc = random.choice(elements)
        return f"{code} - {desc}"

    def _gen_sap_activity_type(self) -> str:
        code, desc = random.choice(SAP_ACTIVITY_TYPES)
        return f"{code} - {desc}"

    def _gen_sap_wbs_element(self) -> str:
        project = f"P-{random.randint(1000, 9999)}"
        phase = random.randint(1, 5)
        task = random.randint(1, 10)
        return f"{project}.{phase}.{task:02d}"

    def _gen_sap_controlling_area(self) -> str:
        return random.choice(["1000", "2000"])

    # SAP HR
    def _gen_sap_personnel_number(self) -> str:
        return f"{random.randint(10000, 99999):08d}"

    def _gen_sap_personnel_area(self) -> str:
        areas = [
            ("BE10", "België Brussel"), ("BE20", "België Antwerpen"),
            ("BE30", "België Luik"), ("NL10", "Nederland"),
        ]
        code, desc = random.choice(areas)
        return f"{code} - {desc}"

    def _gen_sap_personnel_subarea(self) -> str:
        subareas = [
            ("0001", "Hoofdkantoor"), ("0002", "Filiaal"),
            ("0003", "Magazijn"), ("0004", "Productie"),
        ]
        code, desc = random.choice(subareas)
        return f"{code} - {desc}"

    def _gen_sap_employee_group(self) -> str:
        code, desc = random.choice(SAP_EMPLOYEE_GROUPS)
        return f"{code} - {desc}"

    def _gen_sap_employee_subgroup(self) -> str:
        code, desc = random.choice(SAP_EMPLOYEE_SUBGROUPS)
        return f"{code} - {desc}"

    def _gen_sap_org_unit(self) -> str:
        return f"{random.randint(50000000, 59999999)}"

    def _gen_sap_position(self) -> str:
        code, desc = random.choice(SAP_POSITIONS)
        return f"{code} - {desc}"

    def _gen_sap_job(self) -> str:
        code, desc = random.choice(SAP_JOBS)
        return f"{code} - {desc}"

    def _gen_sap_payroll_area(self) -> str:
        code, desc = random.choice(SAP_PAYROLL_AREAS)
        return f"{code} - {desc}"

    def _gen_sap_wage_type(self) -> str:
        code, desc = random.choice(SAP_WAGE_TYPES)
        return f"{code} - {desc}"

    def _gen_sap_infotype(self) -> str:
        code, desc = random.choice(SAP_INFOTYPES)
        return f"{code} - {desc}"

    # SAP PP
    def _gen_sap_production_order(self) -> str:
        return f"60{random.randint(10000000, 99999999)}"

    def _gen_sap_bom_number(self) -> str:
        return f"{random.randint(10000000, 99999999):08d}"

    def _gen_sap_routing(self) -> str:
        return f"{random.randint(1000000, 9999999):08d}"

    def _gen_sap_work_center(self) -> str:
        code, desc = random.choice(SAP_WORK_CENTERS)
        return f"{code} - {desc}"

    def _gen_sap_planned_order(self) -> str:
        return f"{random.randint(10000000, 99999999):010d}"

    def _gen_sap_production_version(self) -> str:
        return f"{random.randint(1, 5):04d}"

    # SAP PM
    def _gen_sap_equipment_number(self) -> str:
        return f"{random.randint(10000000, 99999999):010d}"

    def _gen_sap_functional_location(self) -> str:
        site = random.choice(["BRU", "ANT", "LIE", "GNT"])
        building = random.randint(1, 10)
        floor = random.randint(0, 5)
        room = random.randint(1, 50)
        return f"{site}-{building:02d}-{floor:02d}-{room:03d}"

    def _gen_sap_maintenance_order(self) -> str:
        return f"40{random.randint(10000000, 99999999)}"

    def _gen_sap_notification(self) -> str:
        return f"10{random.randint(10000000, 99999999)}"

    def _gen_sap_maintenance_plan(self) -> str:
        return f"MP{random.randint(100000, 999999)}"

    def _gen_sap_object_type(self) -> str:
        code, desc = random.choice(SAP_OBJECT_TYPES)
        return f"{code} - {desc}"

    # SAP QM
    def _gen_sap_inspection_lot(self) -> str:
        return f"{random.randint(100000000, 999999999):012d}"

    def _gen_sap_inspection_plan(self) -> str:
        return f"IP-{random.randint(10000, 99999)}"

    def _gen_sap_catalog_type(self) -> str:
        code, desc = random.choice(SAP_QM_CATALOG_TYPES)
        return f"{code} - {desc}"

    def _gen_sap_usage_decision(self) -> str:
        code, desc = random.choice(SAP_QM_USAGE_DECISIONS)
        return f"{code} - {desc}"

    # SAP WM
    def _gen_sap_warehouse_number(self) -> str:
        return random.choice(["100", "200", "300", "400", "500"])

    def _gen_sap_storage_type(self) -> str:
        types = [
            ("001", "Hoogbouwmagazijn"), ("002", "Vloeropslagplaats"),
            ("003", "Stellingopslag"), ("004", "Koelmagazijn"),
            ("005", "Buitenopslag"), ("010", "Goederenontvangst"),
            ("020", "Goederenuitgifte"),
        ]
        code, desc = random.choice(types)
        return f"{code} - {desc}"

    def _gen_sap_storage_bin(self) -> str:
        row = random.choice(string.ascii_uppercase[:8])
        rack = random.randint(1, 50)
        level = random.randint(1, 6)
        return f"{row}-{rack:02d}-{level:02d}"

    def _gen_sap_transfer_order(self) -> str:
        return f"{random.randint(100000, 999999):010d}"

    def _gen_sap_handling_unit(self) -> str:
        return f"HU{random.randint(10000000, 99999999)}"

    # SAP SCM
    def _gen_sap_scm_location(self) -> str:
        locations = [
            "LOC_BRU_01", "LOC_ANT_01", "LOC_LIE_01", "LOC_GNT_01",
            "LOC_AMS_01", "LOC_ROT_01", "DC_BRU_01", "DC_ANT_01",
        ]
        return random.choice(locations)

    def _gen_sap_scm_product(self) -> str:
        return f"SCM-{random.randint(100000, 999999)}"

    def _gen_sap_demand_plan(self) -> str:
        return f"DP-{random.randint(2024, 2026)}-{random.randint(1, 12):02d}"

    def _gen_sap_transport_lane(self) -> str:
        origins = ["BRU", "ANT", "LIE", "AMS", "ROT", "FRA"]
        dests = ["BRU", "ANT", "LIE", "AMS", "ROT", "FRA", "PAR", "LON"]
        o, d = random.sample(origins + dests, 2)
        return f"{o} -> {d}"

    def _gen_sap_supply_source(self) -> str:
        vendor = f"{random.randint(100000, 999999):010d}"
        return f"Vendor {vendor}"

    def _gen_sap_quota_arrangement(self) -> str:
        return f"QA-{random.randint(1000, 9999)}"

    def _gen_sap_scheduling_agreement(self) -> str:
        return f"55{random.randint(10000000, 99999999)}"

    def _gen_sap_forecast_profile(self) -> str:
        profiles = ["FP01", "FP02", "FP03", "FSTD", "FMAN", "FAUTO"]
        return random.choice(profiles)

    # SAP IS-U
    def _gen_sap_isu_contract_account(self) -> str:
        return f"{random.randint(100000000000, 999999999999)}"

    def _gen_sap_isu_business_partner(self) -> str:
        return f"{random.randint(1000000000, 9999999999)}"

    def _gen_sap_isu_connection_object(self) -> str:
        return f"CO-{random.randint(100000, 999999)}"

    def _gen_sap_isu_premise(self) -> str:
        return f"PR-{random.randint(100000, 999999)}"

    def _gen_sap_isu_installation(self) -> str:
        return f"IN-{random.randint(1000000, 9999999)}"

    def _gen_sap_isu_device(self) -> str:
        brands = ["LAN", "SAG", "ITR", "ISK", "KAM"]
        brand = random.choice(brands)
        return f"{brand}-{random.randint(10000000, 99999999)}"

    def _gen_sap_isu_register(self) -> str:
        return f"REG-{random.randint(1, 4):03d}"

    def _gen_sap_isu_meter_reading(self) -> str:
        return f"{random.randint(1000, 99999):.1f}"

    def _gen_sap_isu_rate_category(self) -> str:
        code, desc = random.choice(SAP_ISU_RATE_CATEGORIES)
        return f"{code} - {desc}"

    def _gen_sap_isu_division(self) -> str:
        code, desc = random.choice(SAP_ISU_DIVISIONS)
        return f"{code} - {desc}"

    def _gen_sap_isu_move_in_date(self) -> str:
        start = date(2015, 1, 1)
        end = date(2025, 12, 31)
        delta = end - start
        d = start + timedelta(days=random.randint(0, delta.days))
        return d.strftime("%d.%m.%Y")

    def _gen_sap_isu_move_out_date(self) -> str:
        if random.random() < 0.4:
            return ""
        start = date(2018, 1, 1)
        end = date(2026, 6, 30)
        delta = end - start
        d = start + timedelta(days=random.randint(0, delta.days))
        return d.strftime("%d.%m.%Y")

    def _gen_sap_isu_pod(self) -> str:
        # Point of Delivery - EAN-achtig 18-digit
        return f"54{random.randint(10**15, 10**16 - 1)}"

    def _gen_sap_isu_consumption(self) -> str:
        return f"{random.randint(500, 50000)} kWh"

    # SAP PS
    def _gen_sap_project_definition(self) -> str:
        prefixes = ["PRJ", "DEF", "MIL", "INF", "IT"]
        return f"{random.choice(prefixes)}-{random.randint(1000, 9999)}"

    def _gen_sap_network(self) -> str:
        return f"NW-{random.randint(100000, 999999)}"

    def _gen_sap_network_activity(self) -> str:
        return f"{random.randint(1, 50) * 10:04d}"

    def _gen_sap_milestone(self) -> str:
        return random.choice(SAP_MILESTONES)

    def _gen_unknown(self) -> str:
        return self.fake.word()
