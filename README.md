# Testdata Generator

Een Streamlit applicatie waarmee je testdata kunt genereren op basis van een CSV of Excel bestand.

## Features

- **Upload CSV/Excel** - Sleep of upload een bestand met de gewenste kolomstructuur
- **Automatische veldherkenning** - Kolommen worden automatisch geanalyseerd op basis van naam en data
- **Handmatige aanpassing** - Pas veldtypes aan waar de automatische detectie onzeker is
- **Europese ondersteuning** - Correcte adressen, postcodes, telefoonnummers voor 15+ Europese landen
- **Geldige EAN-codes** - EAN-13 barcodes met correcte checkdigit
- **Geldige IBAN nummers** - Per land correcte IBAN formaten
- **Download** - Exporteer als CSV, Excel of JSON

## Ondersteunde veldtypes

| Categorie | Velden |
|-----------|--------|
| Persoon | Voornaam, Achternaam, Volledige naam, Geslacht, Leeftijd, Geboortedatum |
| Contact | E-mail, Telefoon |
| Adres | Straat, Huisnummer, Postcode, Stad/Gemeente, Land |
| Zakelijk | Bedrijfsnaam, BTW-nummer, IBAN, EAN-code |
| Technisch | ID, UUID, URL, IP-adres |
| Overig | Datum, Geheel getal, Decimaal getal, Boolean |

## Installatie

```bash
pip install -r requirements.txt
```

## Gebruik

```bash
streamlit run app.py
```

## Ondersteunde landen

België, Nederland, Duitsland, Frankrijk, Luxemburg, Spanje, Italië, Portugal, Oostenrijk, Verenigd Koninkrijk, Ierland, Zwitserland, Zweden, Noorwegen, Denemarken, Finland, Polen, Tsjechië
