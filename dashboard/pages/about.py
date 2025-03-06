import streamlit as st

# Dashboard Title
st.set_page_config(page_title="Bike Sharing Dashboard")

# Sidebar
with st.sidebar:
    st.title("Bike Sharing Dataset Analysis Dashboard")
    st.page_link("dashboard.py", label="Beranda", icon="🏠")
    st.page_link("pages/cluster.py", label="Analisis Lanjutan", icon="📊")
    st.page_link("pages/about.py", label="Tentang", icon="ℹ️")

st.title("Informasi Dataset")
st.write("Proses penyewaan sepeda bersama sangat berkorelasi dengan lingkungan dan kondisi musiman. Misalnya, kondisi cuaca, curah hujan, hari dalam seminggu, musim, jam dalam sehari, dll. dapat memengaruhi perilaku penyewaan. Kumpulan data inti terkait dengan catatan historis dua tahun yang sesuai dengan tahun 2011 dan 2012 dari sistem Capital Bikeshare, Washington D.C., AS yang tersedia untuk umum di http://capitalbikeshare.com/system-data. Kami menggabungkan data berdasarkan dua jam dan harian, lalu mengekstrak dan menambahkan informasi cuaca dan musiman yang sesuai. Informasi cuaca diekstrak dari http://www.freemeteo.com.")
st.subheader("Daftar Pustaka")
st.write("Fanaee-T, Hadi, and Gama, Joao, \"Event labeling combining ensemble detectors and background knowledge\", Progress in Artificial Intelligence (2013): pp. 1-15, Springer Berlin Heidelberg, doi:10.1007/s13748-013-0040-3.")