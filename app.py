# app.py

import streamlit as st

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

/* BOX AREA */
.area {
    padding: 35px;
    border-radius: 20px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin: 10px;
}

/* WARNA AREA */
.vip {
    background-color: #8ef0c1;
    color: black;
}

.blue {
    background-color: #7fc8ff;
    color: black;
}

.pink {
    background-color: #ffb3c7;
    color: black;
}

/* STAGE */
.stage {
    background-color: black;
    color: white;
    text-align: center;
    padding: 25px;
    border-radius: 15px;
    font-size: 35px;
    font-weight: bold;
    margin-bottom: 30px;
}

/* BOX STATISTIK */
.stat-box {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-weight: bold;
    margin-bottom: 15px;
    font-size: 20px;
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

    # TAMBAH DATA
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

    # TAMPIL DATA
    def tampilkan(self):

        data = []

        current = self.head

        while current:

            harga = harga_tiket[current.kategori]

            total = harga * current.jumlah

            data.append({
                "Nama": current.nama,
                "Kategori": current.kategori,
                "Jumlah Tiket": current.jumlah,
                "Total Harga": f"Rp {total:,}"
            })

            current = current.next

        return data

    # HITUNG TIKET
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
# DENAH KONSER
# =========================

st.write("---")

st.subheader("🎤 Denah Konser")

# STAGE
st.markdown("""
<div class="stage">
STAGE
</div>
""", unsafe_allow_html=True)

# VIP
col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    <div class="area vip">
    VIP A
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="area vip">
    VIP B
    </div>
    """, unsafe_allow_html=True)

# BLUE
col3, col4 = st.columns(2)

with col3:

    st.markdown("""
    <div class="area blue">
    BLUE A
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown("""
    <div class="area blue">
    BLUE B
    </div>
    """, unsafe_allow_html=True)

# PINK
col5, col6 = st.columns(2)

with col5:

    st.markdown("""
    <div class="area pink">
    PINK A
    </div>
    """, unsafe_allow_html=True)

with col6:

    st.markdown("""
    <div class="area pink">
    PINK B
    </div>
    """, unsafe_allow_html=True)

# =========================
# FORM BOOKING
# =========================

st.write("---")

st.subheader("📝 Booking Tiket")

col7, col8, col9 = st.columns(3)

with col7:

    nama = st.text_input(
        "Nama Pembeli"
    )

with col8:

    kategori = st.selectbox(
        "Kategori Tiket",
        list(kuota_tiket.keys())
    )

with col9:

    jumlah = st.number_input(
        "Jumlah Tiket",
        min_value=1,
        step=1
    )

# =========================
# CEK SISA TIKET
# =========================

terjual = st.session_state.konser.hitung_tiket(
    kategori
)

sisa = kuota_tiket[kategori] - terjual

st.info(
    f"Sisa tiket {kategori}: {sisa}"
)

# =========================
# BUTTON PESAN
# =========================

if st.button("🎟 Pesan Tiket"):

    if nama == "":

        st.warning(
            "Nama wajib diisi!"
        )

    elif jumlah > sisa:

        st.error(
            "Kuota tiket tidak mencukupi!"
        )

    else:

        st.session_state.konser.tambah(
            nama,
            kategori,
            jumlah
        )

        st.success(
            "Tiket berhasil dipesan!"
        )

# =========================
# DATA PEMBELI
# =========================

st.write("---")

st.subheader("📋 Daftar Pembeli")

data = st.session_state.konser.tampilkan()

if data:

    st.table(data)

else:

    st.info(
        "Belum ada pembeli"
    )
# =========================
# UPDATE DATA
# =========================

st.write("---")

st.subheader("✏ Update Tiket")

daftar_nama = [
    pembeli["Nama"]
    for pembeli in data
]

if daftar_nama:

    nama_update = st.selectbox(
        "Pilih Pembeli",
        daftar_nama
    )

    kategori_baru = st.selectbox(
        "Kategori Baru",
        list(kuota_tiket.keys())
    )

    jumlah_baru = st.number_input(
        "Jumlah Baru",
        min_value=1,
        step=1,
        key="update_jumlah"
    )

    if st.button("Update Tiket"):

        current = st.session_state.konser.head

        while current:

            if current.nama == nama_update:

                current.kategori = kategori_baru
                current.jumlah = jumlah_baru

                st.success(
                    "Data berhasil diupdate!"
                )

                break

            current = current.next

# =========================
# DELETE DATA
# =========================

st.write("---")

st.subheader("🗑 Batalkan Tiket")

if daftar_nama:

    nama_hapus = st.selectbox(
        "Pilih Nama",
        daftar_nama,
        key="hapus"
    )

    if st.button("Hapus Tiket"):

        current = st.session_state.konser.head
        previous = None

        while current:

            if current.nama == nama_hapus:

                if previous is None:

                    st.session_state.konser.head = current.next

                else:

                    previous.next = current.next

                st.success(
                    "Tiket berhasil dibatalkan!"
                )

                break

            previous = current
            current = current.next
            
# =========================
# STATISTIK
# =========================

st.write("---")

st.subheader("📊 Statistik Tiket")

col10, col11, col12 = st.columns(3)

kategori_list = list(
    kuota_tiket.keys()
)

for index, kategori in enumerate(kategori_list):

    terjual = st.session_state.konser.hitung_tiket(
        kategori
    )

    sisa = kuota_tiket[kategori] - terjual

    if "VIP" in kategori:

        warna = "#6fd6a8"

    elif "BLUE" in kategori:

        warna = "#69b6ff"

    else:

        warna = "#ff9db2"

    html = f"""
    <div class="stat-box"
    style="background-color:{warna}; color:black;">
        {kategori}<br><br>
        Terjual : {terjual}<br>
        Sisa : {sisa}
    </div>
    """

    if index % 3 == 0:

        with col10:
            st.markdown(
                html,
                unsafe_allow_html=True
            )

    elif index % 3 == 1:

        with col11:
            st.markdown(
                html,
                unsafe_allow_html=True
            )

    else:

        with col12:
            st.markdown(
                html,
                unsafe_allow_html=True
            )

# =========================
# SOLD OUT
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

    st.error(
        "🚫 SEMUA TIKET SOLD OUT"
    )

else:

    st.success(
        "✅ Tiket Masih Tersedia"
    )
