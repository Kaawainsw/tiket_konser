# app.py
import streamlit as st
from datetime import datetime

# =========================
# CLASS NODE
# =========================
class Node:
    def __init__(self, plat, jenis):
        self.plat = plat
        self.jenis = jenis
        self.jam_masuk = datetime.now()
        self.next = None


# =========================
# CLASS LINKED LIST
# =========================
class ParkingLinkedList:
    def __init__(self):
        self.head = None

    # tambah kendaraan
    def tambah_kendaraan(self, plat, jenis):
        kendaraan_baru = Node(plat, jenis)

        if self.head is None:
            self.head = kendaraan_baru
        else:
            current = self.head

            while current.next:
                current = current.next

            current.next = kendaraan_baru

    # tampilkan kendaraan
    def tampilkan_kendaraan(self):
        data = []

        current = self.head

        while current:
            data.append({
                "Plat Nomor": current.plat,
                "Jenis": current.jenis,
                "Jam Masuk": current.jam_masuk.strftime("%H:%M:%S")
            })

            current = current.next

        return data

    # kendaraan keluar
    def keluar_kendaraan(self, plat):
        current = self.head
        previous = None

        while current:

            if current.plat == plat:

                # hitung durasi parkir
                sekarang = datetime.now()
                durasi = sekarang - current.jam_masuk

                jam = max(1, durasi.seconds // 3600)

                # tarif parkir
                if current.jenis == "Mobil":
                    tarif = 5000
                else:
                    tarif = 2000

                total_bayar = jam * tarif

                # hapus node
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next

                return {
                    "plat": current.plat,
                    "jenis": current.jenis,
                    "durasi": jam,
                    "total": total_bayar
                }

            previous = current
            current = current.next

        return None


# =========================
# STREAMLIT
# =========================

st.set_page_config(
    page_title="Sistem Parkir",
    layout="wide"
)

st.title("🚗 Sistem Parkir Kampus")

# session state
if "parkir" not in st.session_state:
    st.session_state.parkir = ParkingLinkedList()

if "total_pemasukan" not in st.session_state:
    st.session_state.total_pemasukan = 0


# =========================
# FORM TAMBAH KENDARAAN
# =========================

st.subheader("➕ Tambah Kendaraan")

col1, col2 = st.columns(2)

with col1:
    plat = st.text_input("Plat Nomor")

with col2:
    jenis = st.selectbox(
        "Jenis Kendaraan",
        ["Mobil", "Motor"]
    )

if st.button("Tambah Kendaraan"):

    if plat != "":

        st.session_state.parkir.tambah_kendaraan(
            plat,
            jenis
        )

        st.success("Kendaraan berhasil masuk!")

    else:
        st.warning("Plat nomor wajib diisi")


# =========================
# TAMPILKAN DATA PARKIR
# =========================

st.subheader("📋 Daftar Kendaraan Parkir")

data_parkir = st.session_state.parkir.tampilkan_kendaraan()

if data_parkir:
    st.table(data_parkir)
else:
    st.info("Belum ada kendaraan parkir")


# =========================
# KENDARAAN KELUAR
# =========================

st.subheader("🚪 Kendaraan Keluar")

daftar_plat = [
    kendaraan["Plat Nomor"]
    for kendaraan in data_parkir
]

if daftar_plat:

    plat_keluar = st.selectbox(
        "Pilih Kendaraan",
        daftar_plat
    )

    if st.button("Hitung Biaya & Keluar"):

        hasil = st.session_state.parkir.keluar_kendaraan(
            plat_keluar
        )

        if hasil:

            st.session_state.total_pemasukan += hasil["total"]

            st.success("Kendaraan keluar berhasil!")

            st.write("### 💰 Detail Pembayaran")
            st.write(f"Plat Nomor : {hasil['plat']}")
            st.write(f"Jenis : {hasil['jenis']}")
            st.write(f"Durasi : {hasil['durasi']} jam")
            st.write(f"Total Bayar : Rp {hasil['total']:,}")

else:
    st.info("Tidak ada kendaraan")


# =========================
# STATISTIK
# =========================

st.sidebar.title("📊 Statistik")

st.sidebar.metric(
    "Jumlah Kendaraan",
    len(data_parkir)
)

st.sidebar.metric(
    "Total Pemasukan",
    f"Rp {st.session_state.total_pemasukan:,}"
)