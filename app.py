# app.py

import streamlit as st
from PIL import Image

# =========================
# CONFIG PAGE
# =========================

st.set_page_config(
    page_title="TXT Concert Ticket",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.stApp {
    background-color: #dff4ff;
}

h1 {
    text-align: center;
    color: #003366;
    font-size: 45px;
}

h3 {
    color: #003366;
}

.kotak {
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-weight: bold;
    margin-bottom: 10px;
    font-size: 18px;
}

.vip {
    background-color: #6fd6a8;
    color: black;
}

.blue {
    background-color: #69b6ff;
}

.pink {
    background-color: #ff9db2;
    color: black;
}

.sold {
    background-color: gray;
}

.stat-box {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LINKED LIST
# =========================

class Node:
    def __init__(self, nama, kategori, jumlah):
        self.nama = nama
        self.kategori = kategori
        self.jumlah = jumlah
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # tambah data
    def tambah(self, nama, kategori, jumlah):

        node_baru = Node(
            nama,
            kategori,
            jumlah
        )

        if self.head is None:
            self.head = node_baru

        else:

            current = self.head

            while current.next:
                current = current.next

            current.next = node_baru

    # tampil data
    def tampilkan(self):

        data = []

        current = self.head

        while current:

            harga = harga_tiket[current.kategori]
            total = harga * current.jumlah

            data.append({
                "Nama": current.nama,
                "Kategori": current.kategori,
                "Jumlah": current.jumlah,
                "Total": f"Rp {total:,}"
            })

            current = current.next

        return data

    # hitung tiket per kategori
    def hitung_tiket(self, kategori):

        total = 0

        current = self.head

        while current:

            if current.kategori == kategori:
                total += current.jumlah

            current = current.next

        return total


# =========================
# SESSION STATE
# =========================

if "konser" not in st.session_state:
    st.session_state.konser = LinkedList()

# =========================
# DATA TIKET
# =========================

kuota_tiket = {
    "VIP A": 50,
    "VIP B": 50,
    "BLUE A": 50,
    "BLUE B": 50,
    "PINK A": 50,
    "PINK B": 50
}

harga_tiket = {
    "VIP A": 3000000,
    "VIP B": 3000000,
    "BLUE A": 2500000,
    "BLUE B": 2500000,
    "PINK A": 1500000,
    "PINK B": 1500000
}

# =========================
# TITLE
# =========================

st.title("🎫 TXT CONCERT TICKET SYSTEM")

st.write("### Tomorrow X Together World Tour")

# =========================
# GAMBAR DENAH
# =========================

gambar = Image.open("txt_concert.png")

st.image(
    gambar,
    use_container_width=True
)

# =========================
# BOOKING FORM
# =========================

st.write("---")
st.subheader("📝 Booking Tiket")

col1, col2, col3 = st.columns(3)

with col1:
    nama = st.text_input("Nama Pembeli")

with col2:

    kategori = st.selectbox(
        "Kategori Tiket",
        list(kuota_tiket.keys())
    )

with col3:

    jumlah = st.number_input(
        "Jumlah Tiket",
        min_value=1,
        step=1
    )

# =========================
# SISA TIKET
# =========================

terjual = st.session_state.konser.hitung_tiket(
    kategori
)

sisa = kuota_tiket[kategori] - terjual

st.info(f"Sisa tiket {kategori}: {sisa}")

# =========================
# BUTTON PESAN
# =========================

if st.button("🎟 Pesan Tiket"):

    if nama == "":

        st.warning("Nama wajib diisi!")

    elif jumlah > sisa:

        st.error("Kuota tiket tidak mencukupi!")

    else:

        st.session_state.konser.tambah(
            nama,
            kategori,
            jumlah
        )

        st.success("Tiket berhasil dipesan!")

# =========================
# TAMPIL DATA PEMBELI
# =========================

st.write("---")
st.subheader("📋 Daftar Pembeli")

data = st.session_state.konser.tampilkan()

if data:
    st.table(data)

else:
    st.info("Belum ada pembeli")

# =========================
# STATISTIK
# =========================

st.write("---")
st.subheader("📊 Statistik Tiket")

col1, col2, col3 = st.columns(3)

kategori_list = list(kuota_tiket.keys())

for index, kategori in enumerate(kategori_list):

    terjual = st.session_state.konser.hitung_tiket(
        kategori
    )

    sisa = kuota_tiket[kategori] - terjual

    if "VIP" in kategori:
        kelas = "vip"

    elif "BLUE" in kategori:
        kelas = "blue"

    else:
        kelas = "pink"

    html = f"""
    <div class="kotak {kelas}">
        {kategori}<br>
        Terjual: {terjual}<br>
        Sisa: {sisa}
    </div>
    """

    if index % 3 == 0:
        with col1:
            st.markdown(html, unsafe_allow_html=True)

    elif index % 3 == 1:
        with col2:
            st.markdown(html, unsafe_allow_html=True)

    else:
        with col3:
            st.markdown(html, unsafe_allow_html=True)

# =========================
# SOLD OUT CHECK
# =========================

semua_habis = True

for kategori in kuota_tiket:

    terjual = st.session_state.konser.hitung_tiket(
        kategori
    )

    sisa = kuota_tiket[kategori] - terjual

    if sisa > 0:
        semua_habis = False

if semua_habis:

    st.error("🚫 SEMUA TIKET SOLD OUT")

else:

    st.success("✅ Tiket Masih Tersedia")
