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

    def _gen_unknown(self) -> str:
        return self.fake.word()
