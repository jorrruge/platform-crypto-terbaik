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

# Convert data to DataFrame
saw_df = pd.DataFrame(saw_data)
saw_df.index += 1  # Adjust index to start from 1

# Generate tabel "Alternatif Terbaik/Terendah"
best_worst_df = pd.DataFrame({
    "No": list(range(1, len(bobot) + 1)),
    "Variabel": list(bobot.keys()),
    "Alternatif Terbaik pada Variabel Ini": nilai_df.set_index("Platform").idxmax().tolist(),
    "Alternatif Terendah pada Variabel Ini": nilai_df.set_index("Platform").idxmin().tolist(),
})

# Menghapus kolom index default dari Pandas (hilangkan kolom tidak terpakai seperti "0, 1, 2...")
best_worst_df.reset_index(drop=True, inplace=True)

# Streamlit UI
st.title("Platform Exchange Cryptocurrency Terbaik")
st.write("Hai! Saya Jorge Michael Bryan, mahasiswa Universitas Brawijaya. Berikut analisis platform exchange cryptocurrency berdasarkan beberapa variabel.")

# Sidebar Menu
menu = st.sidebar.selectbox("Pilih Variabel", ["Platform Terbaik"] + list(bobot.keys()))

if menu == "Platform Terbaik":
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
            color=alt.Color(
                "Platform:N",
                scale=alt.Scale(
                    domain=["Binance", "Indodax", "Tokocrypto"],
                    range=["#FF7F0E", "#1F77B4", "#2CA02C"]  # Menukar warna Binance dengan Indodax
                )
            ),
            tooltip=["Platform", "Variabel", "Nilai"]
        )
        .properties(
            title="Perbandingan Nilai Antar Platform Berdasarkan Semua Variabel",
            width=700,
            height=400
        )
    )
    st.altair_chart(combined_chart, use_container_width=True)
    
    st.subheader("Peringkat Platform Terbaik")
    # Grafik SAW
    saw_chart = (
        alt.Chart(saw_df)
        .mark_bar()
        .encode(
            x=alt.X("Platform", sort=["Binance", "Indodax", "Tokocrypto"]),
            y=alt.Y("Nilai SAW"),
            color=alt.Color(
                "Platform:N",
                scale=alt.Scale(
                    domain=["Binance", "Indodax", "Tokocrypto"],
                    range=["#FF7F0E", "#1F77B4", "#2CA02C"]  # Menukar warna Binance dengan Indodax
                )
            ),
            tooltip=["Platform", "Nilai SAW", "Peringkat"]
        )
        .properties(
            title="Grafik Peringkat",
            width=600,
            height=400
        )
    )
    st.altair_chart(saw_chart, use_container_width=True)
    
    # Menampilkan tabel SAW
    st.dataframe(saw_df)  # Tabel SAW di bawah grafik
    
    st.subheader("Alternatif Terbaik dan Terendah pada Setiap Variabel")
    # Menampilkan tabel alternatif terbaik dan terendah
    st.table(best_worst_df)

else:
    st.subheader(f"Perbandingan Berdasarkan Variabel: {menu}")
    
    # Membuat kolom "Nilai" berdasarkan nilai rata-rata
    comparison_df = nilai_df[["Platform", menu]].copy()
    comparison_df.rename(columns={menu: "Nilai"}, inplace=True)
    comparison_df.index += 1  # Adjust index to start from 1
    
    # Grafik variabel tertentu
    variable_chart = (
        alt.Chart(comparison_df)
        .mark_bar()
        .encode(
            x=alt.X("Platform", sort=["Binance", "Indodax", "Tokocrypto"]),
            y=alt.Y("Nilai", title=f"Nilai {menu}"),
            color=alt.Color(
                "Platform:N",
                scale=alt.Scale(
                    domain=["Binance", "Indodax", "Tokocrypto"],
                    range=["#FF7F0E", "#1F77B4", "#2CA02C"]  # Menukar warna Binance dengan Indodax
                )
            ),
            tooltip=["Platform", "Nilai"]
        )
        .properties(
            title=f"Grafik {menu} Antar Platform",
            width=600,
            height=400
        )
    )
    st.altair_chart(variable_chart, use_container_width=True)
    
    # Menampilkan tabel di bawah grafik
    st.table(comparison_df)
