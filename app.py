"""
Testdata Generator - Streamlit Application

Upload a CSV or Excel file, automatically detect field types,
adjust as needed, and generate realistic test data.
"""

import io
import pandas as pd
import streamlit as st

from testdata_generator.field_detector import (
    detect_field_type,
    FIELD_LABELS,
    FIELD_UNKNOWN,
)
from testdata_generator.generators import TestDataGenerator, LOCALE_MAP


# --- Page config ---
st.set_page_config(
    page_title="Testdata Generator",
    page_icon="🧪",
    layout="wide",
)

st.title("Testdata Generator")
st.markdown(
    "Upload een CSV of Excel bestand, controleer de herkende veldtypes, "
    "en genereer realistische testdata."
)


# --- Session state initialization ---
if "detected_fields" not in st.session_state:
    st.session_state.detected_fields = {}
if "uploaded_df" not in st.session_state:
    st.session_state.uploaded_df = None
if "generated_df" not in st.session_state:
    st.session_state.generated_df = None


# --- Sidebar settings ---
st.sidebar.header("Instellingen")

selected_locale_label = st.sidebar.selectbox(
    "Land / Regio",
    options=list(LOCALE_MAP.keys()),
    index=0,
    help="Kies het land voor het genereren van adressen, telefoonnummers, etc.",
)
locale = LOCALE_MAP[selected_locale_label]

num_rows = st.sidebar.number_input(
    "Aantal rijen te genereren",
    min_value=1,
    max_value=100000,
    value=100,
    step=10,
)


# --- File upload ---
st.header("1. Bestand uploaden")
uploaded_file = st.file_uploader(
    "Kies een CSV of Excel bestand",
    type=["csv", "xlsx", "xls"],
    help="Upload een bestand met de kolomstructuur die je wilt gebruiken voor testdata.",
)

if uploaded_file is not None:
    # Read the file
    try:
        if uploaded_file.name.endswith(".csv"):
            # Try common separators
            content = uploaded_file.read().decode("utf-8", errors="replace")
            uploaded_file.seek(0)
            for sep in [",", ";", "\t", "|"]:
                try:
                    df = pd.read_csv(io.StringIO(content), sep=sep, nrows=100)
                    if len(df.columns) > 1:
                        break
                except Exception:
                    continue
            else:
                df = pd.read_csv(io.StringIO(content), nrows=100)
        else:
            df = pd.read_excel(uploaded_file, nrows=100)

        st.session_state.uploaded_df = df

        st.success(
            f"Bestand geladen: **{len(df.columns)}** kolommen, "
            f"**{len(df)}** voorbeeld-rijen gevonden."
        )

        # Show preview
        with st.expander("Voorbeeld van het bronbestand", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)

    except Exception as e:
        st.error(f"Fout bij het lezen van het bestand: {e}")
        st.stop()


# --- Field type detection and configuration ---
if st.session_state.uploaded_df is not None:
    df = st.session_state.uploaded_df
    st.header("2. Veldtypes controleren en aanpassen")

    st.markdown(
        "Hieronder zie je de automatisch herkende veldtypes. "
        "Pas aan waar nodig. Velden gemarkeerd met een lage betrouwbaarheid "
        "verdienen extra aandacht."
    )

    # All available field type options, grouped by category for easier navigation
    FIELD_CATEGORIES = {
        "Persoon": ["first_name", "last_name", "full_name", "gender", "age",
                     "date_of_birth", "birth_place", "nationality", "marital_status"],
        "Identificatie": ["id", "uuid", "national_register", "passport", "id_card"],
        "Contact": ["email", "phone", "street", "house_number", "postcode",
                     "city", "country"],
        "Noodcontact": ["emergency_contact_name", "emergency_contact_phone",
                        "emergency_contact_relation"],
        "Zakelijk": ["company", "vat_number", "iban", "ean"],
        "Technisch": ["url", "ip_address", "date", "integer", "decimal", "boolean"],
        "Militair": ["military_rank", "military_id", "service_number", "unit",
                      "division", "base", "enlistment_date", "end_of_service",
                      "deployment_status", "security_clearance", "mos", "blood_type",
                      "dog_tag", "pay_grade", "years_of_service", "medals",
                      "fitness_score", "weapon_qualification", "language_proficiency",
                      "driver_license_military"],
    }
    # Build categorized labels: "Categorie > Label"
    field_type_options = []
    field_type_labels = []
    categorized_types = set()
    for cat_name, type_keys in FIELD_CATEGORIES.items():
        for ft in type_keys:
            if ft in FIELD_LABELS:
                field_type_options.append(ft)
                field_type_labels.append(f"{cat_name} > {FIELD_LABELS[ft]}")
                categorized_types.add(ft)
    # Add all SAP types grouped by module prefix
    for ft, label in FIELD_LABELS.items():
        if ft.startswith("sap_") and ft not in categorized_types:
            field_type_options.append(ft)
            field_type_labels.append(label)  # Already prefixed with "SAP ..."
            categorized_types.add(ft)
    # Add any remaining (including unknown)
    for ft, label in FIELD_LABELS.items():
        if ft not in categorized_types:
            field_type_options.append(ft)
            field_type_labels.append(label)
            categorized_types.add(ft)

    # Detect field types for each column
    cols_per_row = 3
    columns_list = list(df.columns)

    for row_start in range(0, len(columns_list), cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx, col_name in enumerate(columns_list[row_start:row_start + cols_per_row]):
            with cols[col_idx]:
                sample_values = df[col_name].dropna().head(50).tolist()
                detected_type, confidence = detect_field_type(str(col_name), sample_values)

                # Confidence indicator
                if confidence >= 0.9:
                    conf_indicator = "🟢"
                    conf_text = "Hoog"
                elif confidence >= 0.6:
                    conf_indicator = "🟡"
                    conf_text = "Gemiddeld"
                else:
                    conf_indicator = "🔴"
                    conf_text = "Laag - controleer!"

                # Show sample values
                sample_str = ", ".join([str(v) for v in sample_values[:3]])
                if len(sample_str) > 60:
                    sample_str = sample_str[:60] + "..."

                st.markdown(f"**{col_name}** {conf_indicator} _{conf_text}_")
                if sample_str:
                    st.caption(f"Voorbeeld: {sample_str}")

                # Selectbox for field type
                default_index = field_type_options.index(detected_type)
                selected_label = st.selectbox(
                    f"Type voor '{col_name}'",
                    options=field_type_labels,
                    index=default_index,
                    key=f"field_type_{col_name}",
                    label_visibility="collapsed",
                )
                selected_type = field_type_options[field_type_labels.index(selected_label)]
                st.session_state.detected_fields[col_name] = selected_type

    # --- Show warnings for unknown fields ---
    unknown_fields = [
        col for col, ft in st.session_state.detected_fields.items()
        if ft == FIELD_UNKNOWN
    ]
    if unknown_fields:
        st.warning(
            f"De volgende kolommen konden niet automatisch herkend worden en "
            f"vereisen handmatige selectie: **{', '.join(unknown_fields)}**"
        )

    # --- Generate button ---
    st.header("3. Testdata genereren")

    col1, col2 = st.columns([1, 3])
    with col1:
        generate_btn = st.button(
            "Genereer testdata",
            type="primary",
            use_container_width=True,
        )

    if generate_btn:
        if not st.session_state.detected_fields:
            st.error("Geen velden geconfigureerd. Upload eerst een bestand.")
        else:
            with st.spinner(f"{num_rows} rijen genereren..."):
                generator = TestDataGenerator(locale=locale)
                rows = generator.generate_rows(
                    st.session_state.detected_fields, num_rows
                )
                generated_df = pd.DataFrame(rows)
                st.session_state.generated_df = generated_df

            st.success(f"{num_rows} rijen testdata gegenereerd!")

    # --- Display and download generated data ---
    if st.session_state.generated_df is not None:
        generated_df = st.session_state.generated_df

        st.subheader("Voorbeeld gegenereerde data")
        st.dataframe(generated_df.head(20), use_container_width=True)

        st.subheader("4. Downloaden")

        col_dl1, col_dl2, col_dl3 = st.columns(3)

        with col_dl1:
            csv_data = generated_df.to_csv(index=False, sep=";").encode("utf-8")
            st.download_button(
                label="Download als CSV",
                data=csv_data,
                file_name="testdata.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with col_dl2:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                generated_df.to_excel(writer, index=False, sheet_name="Testdata")
            st.download_button(
                label="Download als Excel",
                data=buffer.getvalue(),
                file_name="testdata.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        with col_dl3:
            json_data = generated_df.to_json(orient="records", force_ascii=False).encode("utf-8")
            st.download_button(
                label="Download als JSON",
                data=json_data,
                file_name="testdata.json",
                mime="application/json",
                use_container_width=True,
            )


# --- Empty state ---
if st.session_state.uploaded_df is None:
    st.info(
        "Upload een CSV of Excel bestand om te beginnen. "
        "De kolommen worden automatisch geanalyseerd en je kunt de "
        "veldtypes aanpassen voordat je testdata genereert."
    )

    st.markdown("### Ondersteunde veldtypes")
    col1, col2, col3 = st.columns(3)
    types_list = list(FIELD_LABELS.items())
    third = len(types_list) // 3

    for col, start in zip([col1, col2, col3], [0, third, third * 2]):
        with col:
            for _, label in types_list[start:start + third]:
                st.markdown(f"- {label}")
