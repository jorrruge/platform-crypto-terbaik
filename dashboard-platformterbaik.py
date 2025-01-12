import streamlit as st
import pandas as pd
import altair as alt

# Data bobot
bobot = {
    "Kemudahan Penggunaan": 0.11,
    "Keamanan": 0.25,
    "Likuiditas": 0.06,
    "Biaya Transaksi": 0.39,
    "Reputasi Platform": 0.16,
    "Dukungan Pelanggan": 0.03,
}

# Data nilai rata-rata
nilai_rata_rata = {
    "Platform": ["Binance", "Indodax", "Tokocrypto"],
    "Kemudahan Penggunaan": [2.347345133, 3.205752212, 2.404867257],
    "Keamanan": [2.480825959, 3.200589971, 2.451327434],
    "Likuiditas": [2.466076696, 3.15339233, 2.460176991],
    "Biaya Transaksi": [2.412979351, 3.200589971, 2.510324484],
    "Reputasi Platform": [2.480825959, 3.230088496, 2.395280236],
    "Dukungan Pelanggan": [2.407079646, 3.200589971, 2.424778761],
}

# Convert data to DataFrame
nilai_df = pd.DataFrame(nilai_rata_rata)

# Data SAW
saw_data = {
    "Platform": ["Binance", "Indodax", "Tokocrypto"],
    "Nilai SAW": [0.760722069, 1, 0.768069649],
    "Peringkat": [3, 1, 2],
}

# Data TOPSIS
topsis_data = {
    "Variabel": [
        "Kemudahan Penggunaan", "Keamanan", "Likuiditas", "Biaya Transaksi", 
        "Reputasi Platform", "Dukungan Pelanggan"
    ],
    "Solusi Ideal Positif": [
        0.074833926, 0.169034549, 0.040267113, 0.263925478, 0.109379365, 0.020509599
    ],
    "Platform Terbaik": ["Indodax"] * 6,
    "Solusi Ideal Negatif": [
        0.05479558, 0.129463328, 0.031415128, 0.198977918, 0.081110543, 0.015424731
    ],
    "Platform Terburuk": ["Binance", "Tokocrypto", "Tokocrypto", "Binance", "Tokocrypto", "Binance"],
}

# Convert data to DataFrame
saw_df = pd.DataFrame(saw_data)
saw_df.index += 1  # Adjust index to start from 1

topsis_df = pd.DataFrame(topsis_data)

# Streamlit UI
st.title("Platform Exchange Cryptocurrency Terbaik")
st.write("Hai! Saya Jorge Michael Bryan, mahasiswa Universitas Brawijaya. Berikut analisis platform exchange cryptocurrency berdasarkan beberapa variabel.")

# Halaman Utama
st.subheader("Perbandingan Keseluruhan Variabel")
# Melting dataframe untuk menampilkan semua variabel dalam satu grafik
nilai_melted = nilai_df.melt(id_vars="Platform", var_name="Variabel", value_name="Nilai")

# Altair chart for combined variables
combined_chart = (
    alt.Chart(nilai_melted)
    .mark_line(point=True)
    .encode(
        x=alt.X("Variabel:N", sort=list(bobot.keys())),
        y=alt.Y("Nilai:Q"),
        color=alt.Color("Platform:N", scale=alt.Scale(scheme="category10")),
        tooltip=["Platform", "Variabel", "Nilai"]
    )
    .properties(
        title="Perbandingan Nilai Antar Platform Berdasarkan Semua Variabel",
        width=700,
        height=400
    )
)
st.altair_chart(combined_chart, use_container_width=True)

# Sidebar Menu
menu = st.sidebar.selectbox("Pilih Variabel", ["Platform Terbaik"] + list(bobot.keys()))

if menu == "Platform Terbaik":
    st.subheader("Peringkat Platform Terbaik Berdasarkan SAW")
    st.dataframe(saw_df)  # Menampilkan tabel dengan nomor urut mulai dari 1
    # Grafik SAW
    saw_chart = (
        alt.Chart(saw_df)
        .mark_bar()
        .encode(
            x=alt.X("Platform", sort=["Binance", "Indodax", "Tokocrypto"]),
            y=alt.Y("Nilai SAW"),
            color=alt.Color("Platform", scale=alt.Scale(scheme="category10")),
            tooltip=["Platform", "Nilai SAW", "Peringkat"]
        )
        .properties(
            title="Grafik Peringkat Berdasarkan SAW",
            width=600,
            height=400
        )
    )
    st.altair_chart(saw_chart, use_container_width=True)
else:
    st.subheader(f"Perbandingan Berdasarkan Variabel: {menu}")
    comparison_df = nilai_df[["Platform", menu]]
    
    # Grafik variabel tertentu
    variable_chart = (
        alt.Chart(comparison_df)
        .mark_bar()
        .encode(
            x=alt.X("Platform", sort=["Binance", "Indodax", "Tokocrypto"]),
            y=alt.Y(menu, title=f"Nilai {menu}"),
            color=alt.Color("Platform", scale=alt.Scale(scheme="category10")),
            tooltip=["Platform", menu]
        )
        .properties(
            title=f"Grafik {menu} Antar Platform",
            width=600,
            height=400
        )
    )
    st.altair_chart(variable_chart, use_container_width=True)
