# app.py

import streamlit as st


# =========================
# CLASS NODE
# =========================
class Node:
    def __init__(self, nama, kategori, jumlah):
        self.nama = nama
        self.kategori = kategori
        self.jumlah = jumlah
        self.next = None


# =========================
# CLASS LINKED LIST
# =========================
class TicketLinkedList:
    def __init__(self):
        self.head = None

    # tambah pembeli
    def tambah_pembeli(self, nama, kategori, jumlah):

        pembeli_baru = Node(
            nama,
            kategori,
            jumlah
        )

        if self.head is None:
            self.head = pembeli_baru

        else:
            current = self.head

            while current.next:
                current = current.next

            current.next = pembeli_baru

    # tampilkan data
    def tampilkan_pembeli(self):

        data = []

        current = self.head

        while current:

            # harga tiket
            if current.kategori == "VIP":
                harga = 500000
            else:
                harga = 250000

            total = harga * current.jumlah

            data.append({
                "Nama": current.nama,
                "Kategori": current.kategori,
                "Jumlah Tiket": current.jumlah,
                "Total Harga": f"Rp {total:,}"
            })

            current = current.next

        return data

    # hapus pembeli
    def hapus_pembeli(self, nama):

        current = self.head
        previous = None

        while current:

            if current.nama == nama:

                if previous is None:
                    self.head = current.next

                else:
                    previous.next = current.next

                return True

            previous = current
            current = current.next

        return False

    # hitung total tiket
    def total_tiket(self):

        total = 0

        current = self.head

        while current:
            total += current.jumlah
            current = current.next

        return total


# =========================
# STREAMLIT
# =========================

st.set_page_config(
    page_title="Sistem Tiket Konser",
    layout="wide"
)

st.title("🎫 Sistem Pemesanan Tiket Konser")

# session state
if "tiket" not in st.session_state:
    st.session_state.tiket = TicketLinkedList()

TOTAL_TIKET = 100

# =========================
# FORM INPUT
# =========================

st.subheader("📝 Pesan Tiket")

col1, col2, col3 = st.columns(3)

with col1:
    nama = st.text_input("Nama Pembeli")

with col2:
    kategori = st.selectbox(
        "Kategori Tiket",
        ["VIP", "Festival"]
    )

with col3:
    jumlah = st.number_input(
        "Jumlah Tiket",
        min_value=1,
        step=1
    )

# tombol tambah
if st.button("Pesan Tiket"):

    tiket_terjual = st.session_state.tiket.total_tiket()

    if tiket_terjual + jumlah > TOTAL_TIKET:

        st.error("Tiket tidak mencukupi!")

    elif nama == "":

        st.warning("Nama wajib diisi!")

    else:

        st.session_state.tiket.tambah_pembeli(
            nama,
            kategori,
            jumlah
        )

        st.success("Tiket berhasil dipesan!")


# =========================
# TABEL PEMBELI
# =========================

st.subheader("📋 Daftar Pembeli")

data = st.session_state.tiket.tampilkan_pembeli()

if data:
    st.table(data)

else:
    st.info("Belum ada pembeli")


# =========================
# BATALKAN TIKET
# =========================

st.subheader("❌ Batalkan Tiket")

daftar_nama = [
    pembeli["Nama"]
    for pembeli in data
]

if daftar_nama:

    nama_hapus = st.selectbox(
        "Pilih Pembeli",
        daftar_nama
    )

    if st.button("Batalkan Tiket"):

        hasil = st.session_state.tiket.hapus_pembeli(
            nama_hapus
        )

        if hasil:
            st.success("Tiket berhasil dibatalkan!")

        else:
            st.error("Data tidak ditemukan")

else:
    st.info("Tidak ada data pembeli")


# =========================
# STATISTIK
# =========================

tiket_terjual = st.session_state.tiket.total_tiket()
tiket_sisa = TOTAL_TIKET - tiket_terjual

st.sidebar.title("📊 Statistik")

st.sidebar.metric(
    "Tiket Terjual",
    tiket_terjual
)

st.sidebar.metric(
    "Tiket Tersisa",
    tiket_sisa
)

# status tiket
if tiket_sisa == 0:
    st.sidebar.error("SOLD OUT")

else:
    st.sidebar.success("Tiket Tersedia")
