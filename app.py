import streamlit as st
import pandas as pd
import io

st.title("Converter Format Absensi")

uploaded_file = st.file_uploader("Upload file base.xls / base.xlsx", type=["xls", "xlsx"])

if uploaded_file:
    try:
        file_bytes = uploaded_file.read()

        # Coba baca sebagai xlsx dulu
        try:
            df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
        except:
            # Kalau gagal, coba sebagai xls lama
            df = pd.read_excel(io.BytesIO(file_bytes), engine="xlrd")

        st.subheader("Preview Data Asli")
        st.dataframe(df.head())

        # ---- PROSES KONVERSI ----
        df["Tgl/Waktu"] = pd.to_datetime(df["Tgl/Waktu"], dayfirst=True, errors="coerce")

        df["Tanggal"] = df["Tgl/Waktu"].dt.strftime("%d/%m/%Y")
        df["Jam"] = df["Tgl/Waktu"].dt.strftime("%H:%M:%S")
        df["Tgl/Waktu"] = df["Tgl/Waktu"].dt.strftime("%d/%m/%Y %H:%M:%S")

        final_df = df[["No.ID", "Tgl/Waktu", "Tanggal", "Jam"]]

        st.subheader("Preview Hasil Konversi")
        st.dataframe(final_df.head())

        csv = final_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download absen.csv",
            csv,
            "absen.csv",
            "text/csv"
        )

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
