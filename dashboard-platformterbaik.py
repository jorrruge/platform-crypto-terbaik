import streamlit as st
import pandas as pd

# Bobot variabel (AHP)
weights = {
    'Kemudahan Penggunaan': 0.11,
    'Keamanan': 0.25,
    'Likuiditas': 0.06,
    'Biaya Transaksi': 0.39,
    'Reputasi Platform': 0.16,
    'Dukungan Pelanggan': 0.03
}

# Data rata-rata nilai setiap variabel dari masing-masing platform
average_data = {
    'Platform': ['Binance', 'Indodax', 'Tokocrypto'],
    'Kemudahan Penggunaan': [2.347345133, 3.205752212, 2.404867257],
    'Keamanan': [2.480825959, 3.200589971, 2.451327434],
    'Likuiditas': [2.466076696, 3.15339233, 2.460176991],
    'Biaya Transaksi': [2.412979351, 3.200589971, 2.510324484],
    'Reputasi Platform': [2.480825959, 3.230088496, 2.395280236],
    'Dukungan Pelanggan': [2.407079646, 3.200589971, 2.424778761]
}

# Hasil SAW
saw_data = {
    'Platform': ['Binance', 'Indodax', 'Tokocrypto'],
    'Nilai SAW': [0.760722069, 1.0, 0.768069649],
    'Peringkat': [3, 1, 2]
}

# Hasil TOPSIS (Nilai terbaik dan terburuk)
topsis_best = {
    'Variabel': ['Kemudahan Penggunaan', 'Keamanan', 'Likuiditas', 'Biaya Transaksi', 'Reputasi Platform', 'Dukungan Pelanggan'],
    'Nilai Terbaik': [0.074833926, 0.169034549, 0.040267113, 0.263925478, 0.109379365, 0.020509599],
    'Platform Terbaik': ['Indodax', 'Indodax', 'Indodax', 'Indodax', 'Indodax', 'Indodax']
}

topsis_worst = {
    'Variabel': ['Kemudahan Penggunaan', 'Keamanan', 'Likuiditas', 'Biaya Transaksi', 'Reputasi Platform', 'Dukungan Pelanggan'],
    'Nilai Terburuk': [0.05479558, 0.129463328, 0.031415128, 0.198977918, 0.081110543, 0.015424731],
    'Platform Terburuk': ['Binance', 'Tokocrypto', 'Tokocrypto', 'Binance', 'Tokocrypto', 'Binance']
}

# Menghitung skor berbobot dari rata-rata nilai
def calculate_weighted_scores(data, weights):
    df = pd.DataFrame(data)
    for column in weights.keys():
        df[column] = df[column] * weights[column]
    df['Total Score'] = df[list(weights.keys())].sum(axis=1)
    return df

def display_dashboard():
    st.title("Dashboard Pemilihan Platform Exchange Cryptocurrency")

    # Tampilan utama: hasil SAW
    st.subheader("Peringkat Platform Berdasarkan SAW")
    saw_df = pd.DataFrame(saw_data)
    st.table(saw_df)

    # Tampilan hasil TOPSIS
    st.subheader("Nilai Terbaik dan Terburuk pada Masing-masing Variabel (TOPSIS)")
    topsis_best_df = pd.DataFrame(topsis_best)
    topsis_worst_df = pd.DataFrame(topsis_worst)

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Nilai Terbaik**")
        st.table(topsis_best_df)
    with col2:
        st.write("**Nilai Terburuk**")
        st.table(topsis_worst_df)

    # User memilih variabel
    st.subheader("Peringkat Berdasarkan Variabel yang Dipilih")
    selected_variable = st.selectbox("Pilih Variabel Penilaian:", list(weights.keys()))

    # Menampilkan peringkat berdasarkan variabel
    weighted_scores = calculate_weighted_scores(average_data, weights)
    sorted_scores = weighted_scores.sort_values(by=selected_variable, ascending=False)

    st.write(f"Peringkat Berdasarkan Variabel: {selected_variable}")
    st.table(sorted_scores[['Platform', selected_variable]])

# Menampilkan dashboard
display_dashboard()
