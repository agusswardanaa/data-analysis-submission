import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Data Preparation
day_df = pd.read_csv("dashboard/day.csv")
hour_df = pd.read_csv("dashboard/hour.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Dashboard Title
st.set_page_config(page_title="Bike Sharing Dashboard")

# Sidebar
with st.sidebar:
    st.title("Bike Sharing Dataset Analysis Dashboard")
    st.page_link("dashboard.py", label="Beranda", icon="🏠")
    st.page_link("pages/cluster.py", label="Analisis Lanjutan", icon="📊")
    st.page_link("pages/about.py", label="Tentang", icon="ℹ️")

col11, col12 = st.columns(2)

with col11:
    mean_daily = day_df["cnt"].mean()
    st.metric("Rata-Rata Penyewaan Sepeda per Jam", f"{mean_daily:.2f}")

with col12:
    mean_hourly = hour_df["cnt"].mean()
    st.metric("Rata-Rata Penyewaan Sepeda per Jam", f"{mean_hourly:.2f}")

st.title("Visualisasi Data")

col21, col22 = st.columns(2)

with col21:
    st.write("Jumlah Penyewaan Sepeda per Bulan")
    # Agregasi penyewaan secara bulanan
    monthly_avg = hour_df.groupby(by="mnth").agg({
        "cnt": "sum"
    })

    # Ambil 3 bulan dengan jumlah penyewaan tertinggi
    top_3_months = monthly_avg["cnt"].nlargest(3).index
    colors = ["#0A5EB0" if i in top_3_months else "#BCCCDC" for i in monthly_avg.index]

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.bar(monthly_avg.index, monthly_avg["cnt"], color=colors)
    ax.set_xlabel("Bulan")
    st.pyplot(fig)

with col22:
    st.write("Jumlah Penyewaan Sepeda per Jam")
    # Agregasi data per jam
    hourly_avg = hour_df.groupby(by="hr").agg({
        "cnt": "sum"
    })

    # Plot data
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.plot(hourly_avg.index, hourly_avg["cnt"], color="#0A5EB0")
    ax.set_xlabel("Jam")
    st.pyplot(fig)

with st.container():
    st.write("Hubungan Kondisi Cuaca dengan Penyewaan Sepeda")
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))

    ax[0].scatter(hour_df["temp"], hour_df["cnt"], color="#0A5EB0")
    ax[0].set_title("Scatter Plot Jumlah Penyewaan Sepeda dengan Suhu")
    ax[0].set_xlabel("Suhu")
    ax[0].set_ylabel("Jumlah Penyewaan Sepeda")

    ax[1].scatter(hour_df["windspeed"], hour_df["cnt"], color="#FFB433")
    ax[1].set_title("Scatter Plot Jumlah Penyewaan Sepeda dengan Kecepatan Angin")
    ax[1].set_xlabel("Kecepatan Angin")
    ax[1].set_ylabel("Jumlah Penyewaan Sepeda")

    st.pyplot(fig)
    with st.expander("Penjelasan"):
        st.markdown(
            "- Jumlah penyewaan sepeda dan suhu terlihat berhubungan secara positif. Hal ini ditandai ketika suhu makin tinggi, jumlah penyewaan sepeda juga semakin tinggi. Pelanggan akan menyewa sepeda ketika suhu panas dibandingkan suhu dingin.\n\n"
            "- Jumlah penyewaan sepeda dan kecepatan angin terlihat memiliki hubungan negatif. Hal ini dilihat ketika semakin rendah kecepatan angin, jumlah penyewaan sepeda semakin tinggi. Perusahaan dapat memberikan potongan harga kepada pelanggan ketika kecepatan angin sedang rendah untuk menarik lebih banyak pelanggan."
        )

with st.container():
    st.write("Jumlah Penyewaan Sepeda Setiap Hari Berdasarkan Status Keanggotaan Pelanggan")
    fig, ax = plt.subplots()

    # Kelompokkan penyewaan berdasarkan hari dan status keanggotaan pelanggan
    sum_hour_weekday = hour_df.groupby("weekday")[["casual", "registered"]].sum()

    # Plot
    ax.bar(sum_hour_weekday.index, sum_hour_weekday["casual"], label="Casual", color="#FFB433")
    ax.bar(sum_hour_weekday.index, sum_hour_weekday["registered"], bottom=sum_hour_weekday["casual"], label="Registered", color="#0A5EB0")
    ax.set_xticks(sum_hour_weekday.index, ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"])
    ax.legend(title="Status Keanggotaan", loc="upper left")

    st.pyplot(fig)
    with st.expander("Penjelasan"):
        st.markdown(
            "- Pelanggan yang sudah terdaftar menjadi anggota melakukan lebih banyak transaksi dibandingkan pengguna biasa. Oleh karena itu, perusahaan dapat menghadirkan promosi bagi pengguna yang terdaftar untuk menggaet lebih banyak pelanggan."
        )

with st.container():
    st.write("Jumlah Penyewaan Sepeda per Hari")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(day_df["dteday"], day_df["cnt"])

    st.pyplot(fig)
    with st.expander("Penjelasan"):
        st.markdown(
            "- Secara umum, penyewaan sepeda memiliki tren meningkat dari tahun 2011 hingga 2012.\n\n"
            "- Akan tetapi, jumlah penyewaan sepeda selalu menyentuh titik tertinggi pada pertengahan tahun.\n\n"
            "- Jumlah penyewaan sepeda selalu mengalami penurunan menjelang akhir tahun.\n\n"
            "- Perusahaan dapat menambahkan fasilitas jas hujan atau sejenisnya agar pelanggan dapat menyewa sepeda pada akhir tahun dan memberikan diskon saat pertengahan tahun untuk menarik lebih banyak konsumen."
        )