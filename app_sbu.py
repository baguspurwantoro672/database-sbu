import streamlit as st
import pandas as pd
import os

FILE_DB = "database_sbu.xlsx"

st.set_page_config(page_title="Database Historis SBU", layout="centered")

st.title("📊 Database Historis SBU")
st.write("Pencarian SBU Berdasarkan Nama Paket & Wilayah")

if not os.path.exists(FILE_DB):
    df = pd.DataFrame(columns=["Provinsi", "Kab/Kota", "Nama Paket", "Tahun", "SBU"])
    df.to_excel(FILE_DB, index=False)

df = pd.read_excel(FILE_DB)

menu = st.sidebar.selectbox("Menu", ["Tambah Data", "Cari Paket"])

if menu == "Tambah Data":
    st.subheader("Tambah Data Paket")

    provinsi = st.text_input("Provinsi")
    kabkota = st.text_input("Kabupaten/Kota")
    nama = st.text_input("Nama Paket")
    tahun = st.text_input("Tahun")
    sbu = st.text_input("SBU")

    if st.button("Simpan"):
        data_baru = pd.DataFrame([[provinsi, kabkota, nama, tahun, sbu]],
                                 columns=["Provinsi", "Kab/Kota", "Nama Paket", "Tahun", "SBU"])

        df2 = pd.concat([df, data_baru], ignore_index=True)
        df2.to_excel(FILE_DB, index=False)

        st.success("Data berhasil disimpan!")

elif menu == "Cari Paket":
    st.subheader("Cari Historis SBU")

    keyword = st.text_input("Masukkan Nama Paket")

    if keyword:
        hasil = df[df["Nama Paket"].str.contains(keyword, case=False, na=False)]

        if hasil.empty:
            st.warning("Data tidak ditemukan.")
        else:
            for index, row in hasil.iterrows():
                st.write(
                    f"- {row['SBU']} ({row['Tahun']} - {row['Kab/Kota']}, {row['Provinsi']})"
                )
