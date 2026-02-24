import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

FILE_NAME = "database_sbu.xlsx"

# Buat file jika belum ada
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "Tahun",
        "Nama Paket",
        "OPD",
        "Nilai HPS",
        "Metode",
        "SBU",
        "Penyedia"
    ])
    df.to_excel(FILE_NAME, index=False)

# Simpan Data
def simpan_data():
    data = {
        "Tahun": entry_tahun.get(),
        "Nama Paket": entry_paket.get(),
        "OPD": entry_opd.get(),
        "Nilai HPS": entry_hps.get(),
        "Metode": entry_metode.get(),
        "SBU": entry_sbu.get(),
        "Penyedia": entry_penyedia.get()
    }

    df = pd.read_excel(FILE_NAME)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(FILE_NAME, index=False)

    messagebox.showinfo("Sukses", "Data berhasil disimpan!")
    kosongkan_form()

# Cari + Rekomendasi SBU
def cari_data():
    keyword = entry_cari.get().lower()
    df = pd.read_excel(FILE_NAME)

    hasil = df[df["Nama Paket"].astype(str).str.lower().str.contains(keyword, na=False)]

    text_hasil.delete(1.0, tk.END)

    if hasil.empty:
        text_hasil.insert(tk.END, "Data tidak ditemukan.\n")
    else:
        text_hasil.insert(tk.END, f"Ditemukan {len(hasil)} histori paket\n\n")

        for index, row in hasil.iterrows():
            text_hasil.insert(tk.END, 
                f"Tahun: {row['Tahun']}\n"
                f"Nama Paket: {row['Nama Paket']}\n"
                f"SBU: {row['SBU']}\n"
                f"{'-'*40}\n"
            )

        # Rekomendasi SBU terbanyak
        rekomendasi = hasil["SBU"].value_counts().idxmax()
        text_hasil.insert(tk.END, f"\nREKOMENDASI SBU: {rekomendasi} (paling sering digunakan)\n")

# Hapus Data berdasarkan Nama Paket
def hapus_data():
    keyword = entry_cari.get().lower()
    df = pd.read_excel(FILE_NAME)

    df_baru = df[~df["Nama Paket"].astype(str).str.lower().str.contains(keyword, na=False)]
    df_baru.to_excel(FILE_NAME, index=False)

    messagebox.showinfo("Info", "Data yang sesuai keyword telah dihapus.")

# Kosongkan Form
def kosongkan_form():
    entry_tahun.delete(0, tk.END)
    entry_paket.delete(0, tk.END)
    entry_opd.delete(0, tk.END)
    entry_hps.delete(0, tk.END)
    entry_metode.delete(0, tk.END)
    entry_sbu.delete(0, tk.END)
    entry_penyedia.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("Database Historis SBU - Versi Profesional")
root.geometry("750x650")

tk.Label(root, text="DATABASE HISTORIS SBU", font=("Arial", 16, "bold")).pack(pady=10)

frame_input = tk.Frame(root)
frame_input.pack()

labels = ["Tahun", "Nama Paket", "OPD", "Nilai HPS", "Metode", "SBU", "Penyedia"]
entries = []

for label in labels:
    tk.Label(frame_input, text=label).pack()
    entry = tk.Entry(frame_input, width=50)
    entry.pack()
    entries.append(entry)

entry_tahun, entry_paket, entry_opd, entry_hps, entry_metode, entry_sbu, entry_penyedia = entries

tk.Button(root, text="Simpan Data", command=simpan_data, bg="green", fg="white").pack(pady=10)

tk.Label(root, text="CARI & ANALISIS HISTORI PAKET", font=("Arial", 12, "bold")).pack(pady=10)

entry_cari = tk.Entry(root, width=50)
entry_cari.pack()

tk.Button(root, text="Cari + Rekomendasi SBU", command=cari_data, bg="blue", fg="white").pack(pady=5)
tk.Button(root, text="Hapus Data Sesuai Keyword", command=hapus_data, bg="red", fg="white").pack(pady=5)

text_hasil = tk.Text(root, height=18, width=90)
text_hasil.pack(pady=10)

root.mainloop()