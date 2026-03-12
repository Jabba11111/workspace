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
    (r"(?i)^(id|identifier|nummer|number)$", FIELD_ID),
    (r"(?i)^(uuid|guid)$", FIELD_UUID),
    (r"(?i)^(url|website|link|site|webpage)$", FIELD_URL),
    (r"(?i)^(ip|ip[\s_-]?address|ip[\s_-]?adres)$", FIELD_IP_ADDRESS),

    # Personal extended
    (r"(?i)^(nationaliteit|nationality|nationalit[eé])$", FIELD_NATIONALITY),
    (r"(?i)^(geboorteplaats|birth[\s_-]?place|lieu[\s_-]?de[\s_-]?naissance|geburtsort)$", FIELD_BIRTH_PLACE),
    (r"(?i)^(burgerlijke[\s_-]?staat|marital[\s_-]?status|[eé]tat[\s_-]?civil|familienstand)$", FIELD_MARITAL_STATUS),
    (r"(?i)^(rijksregisternummer|national[\s_-]?register|rrn|bsn|niss|num[eé]ro[\s_-]?national)$", FIELD_NATIONAL_REGISTER),
    (r"(?i)^(paspoort|passport|paspoortnummer|passport[\s_-]?number|num[eé]ro[\s_-]?de[\s_-]?passeport)$", FIELD_PASSPORT),
    (r"(?i)^(identiteitskaart|id[\s_-]?card|id[\s_-]?kaart[\s_-]?nummer|carte[\s_-]?d[\s_-]?identit[eé]|personalausweis)$", FIELD_ID_CARD),

    # Military / Defense HR
    (r"(?i)^(rang|rank|grade|militaire[\s_-]?rang|dienstgraad)$", FIELD_MILITARY_RANK),
    (r"(?i)^(militair[\s_-]?id|military[\s_-]?id|stamnummer)$", FIELD_MILITARY_ID),
    (r"(?i)^(dienstnummer|service[\s_-]?number|matricule)$", FIELD_SERVICE_NUMBER),
    (r"(?i)^(eenheid|unit|unit[eé])$", FIELD_UNIT),
    (r"(?i)^(divisie|division|brigade|regiment)$", FIELD_DIVISION),
    (r"(?i)^(kazerne|basis|base|camp|garnizoen|garrison)$", FIELD_BASE),
    (r"(?i)^(datum[\s_-]?indienst|enlistment[\s_-]?date|date[\s_-]?d[\s_-]?enr[oô]lement|indiensttreding)$", FIELD_ENLISTMENT_DATE),
    (r"(?i)^(einde[\s_-]?dienst|end[\s_-]?of[\s_-]?service|uitdiensttreding)$", FIELD_END_OF_SERVICE),
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
    FIELD_UNKNOWN: "Onbekend - kies handmatig",
}


def detect_field_type_from_header(header: str) -> Optional[str]:
    """Detect field type based on column header name."""
    clean = header.strip()
    for pattern, field_type in HEADER_PATTERNS:
        if re.match(pattern, clean):
            return field_type
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
