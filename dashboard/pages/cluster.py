import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# Data Preparation
hour_df = pd.read_csv("dashboard/hour.csv")
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Membuat cluster suhu menjadi 3 kategori
temp_cluster = pd.cut(hour_df["temp"], [0, 0.33, 0.67, 1], labels=["Low", "Mid", "High"])

# Membuat cluster kelembapan menjadi 3 kategori
hum_cluster = pd.cut(hour_df["hum"], [0, 0.33, 0.67, 1], labels=["Low", "Mid", "High"])

# Membuat cluster jumlah penyewaan menjadi 2 kategori
temp_cnt = pd.cut(hour_df["cnt"], [0, hour_df["cnt"].mean(), hour_df["cnt"].max()], labels=["Low", "High"])

cluster_df = pd.concat([temp_cluster, hum_cluster, temp_cnt], axis=1)
cluster_df.columns = ["temperature", "humidity", "rent"]
cluster_df.head()

# Dashboard Title
st.set_page_config(page_title="Bike Sharing Dashboard")

# Sidebar
with st.sidebar:
    st.title("Bike Sharing Dataset Analysis Dashboard")
    st.page_link("dashboard.py", label="Beranda", icon="🏠")
    st.page_link("pages/cluster.py", label="Analisis Lanjutan", icon="📊")
    st.page_link("pages/about.py", label="Tentang", icon="ℹ️")

st.title("Analisis Lanjutan Clustering")
st.write("Pembuatan cluster dilakukan menggunakan teknik binning dari method cut pada library pandas.")
st.markdown(
    "- Pembentukan cluster tingkat penyewaan sepeda dibagi ke dalam 2 kelompok, yaitu cluster rendah dan Tinggi. Batas yang digunakan adalah rata-rata jumlah penyewaan.\n\n"
    "- Pembuatan cluster suhu dan kelembapan dibagi ke dalam 3 kelompok, yaitu rendah, sedang, dan tinggi. Batas yang digunakan adalah 0,33 dan 0,67."
)

with st.container():
    st.write("Tingkat Penyewaan Sepeda")
    fig, ax = plt.subplots()

    ax.pie(cluster_df["rent"].value_counts(), labels=["Rendah", "Tinggi"], autopct="%1.1f%%", colors=["#FFB433", "#0A5EB0"])

    st.pyplot(fig)
    with st.expander("Penjelasan"):
        st.markdown(
            "- Berdasarkan cluster yang dibuat, tingkat penyewaan sepeda dari tahun 2011 hingga 2012 sebagian besar termasuk kategori low atau di bawah rata-rata. Hal ini menjadi masukan bagi perusahaan untuk dapat mengambil kebijakan agar dapat menarik lebih banyak pelanggan."
        )

col11, col12 = st.columns(2)

with col11:
    st.write("Tingkat Penyewaan Sepeda Berdasarkan Suhu")
    fig, ax = plt.subplots()

    # Kelompokkan tingkat penyewaan berdasarkan suhu
    rent_temp = cluster_df.groupby("temperature")["rent"].value_counts().unstack()

    # Plot
    ax.bar(rent_temp.index, rent_temp["Low"], label="Rendah", color="#FFB433")
    ax.bar(rent_temp.index, rent_temp["High"], bottom=rent_temp["Low"], label="Tinggi", color="#0A5EB0")
    ax.set_xticks(rent_temp["Low"].index, ["Rendah", "Sedang", "Tinggi"])
    ax.set_xlabel("Cluster Suhu")
    ax.legend(title="Tingkat Penyewaan", loc="upper left")
    st.pyplot(fig)

with col12:
    st.write("Tingkat Penyewaan Sepeda Berdasarkan Kelembapan")
    fig, ax = plt.subplots()

    # Kelompokkan tingkat penyewaan berdasarkan kelembapan
    rent_hum = cluster_df.groupby("humidity")["rent"].value_counts().unstack()

    # Plot
    ax.bar(rent_hum.index, rent_hum["Low"], label="Rendah", color="#FFB433")
    ax.bar(rent_hum.index, rent_hum["High"], bottom=rent_hum["Low"], label="Tinggi", color="#0A5EB0")
    ax.set_xticks(rent_hum["Low"].index, ["Rendah", "Sedang", "Tinggi"])
    ax.set_xlabel("Cluster Kelembapan")
    ax.legend(title="Tingkat Penyewaan", loc="upper left")
    st.pyplot(fig)