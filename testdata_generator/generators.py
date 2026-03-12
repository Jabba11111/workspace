"""
Test data generators for each detected field type.
Uses Faker for realistic data generation with European locale support.
"""

import random
import string
from datetime import date, timedelta
from typing import Optional

from faker import Faker

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
    FIELD_UNKNOWN,
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
            FIELD_UNKNOWN: self._gen_unknown,
        }
        gen = generators.get(field_type, self._gen_unknown)
        return str(gen())

    def generate_rows(self, field_config: dict[str, str], num_rows: int) -> list[dict]:
        """
        Generate multiple rows of test data.
        field_config: {column_name: field_type}
        """
        rows = []
        self._id_counter = 0
        for i in range(num_rows):
            row = {}
            for col_name, field_type in field_config.items():
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

    def _gen_unknown(self) -> str:
        return self.fake.word()
