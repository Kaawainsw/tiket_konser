# app.py

import streamlit as st

# =========================
# SETTING PAGE
# =========================

st.set_page_config(
    page_title="Tiket Konser",
    layout="wide"
)

# =========================
# CSS CUSTOM
# =========================

st.markdown("""
<style>

.stApp {
    background-color: #cfefff;
}

h1 {
    text-align: center;
    color: #003366;
}

.kotak-seat {
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-weight: bold;
    margin: 5px;
}

.vip {
    background-color: #ff4b4b;
}

.festival {
    background-color: #4b7bff;
}

.booked {
    background-color: gray;
}

.panggung {
    background-color: black;
    color: white;
    text-align: center;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 30px;
    font-size: 25px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LINKED LIST
# =========================

class Node:
    def __init__(self, nama, seat):
        self.nama = nama
        self.seat = seat
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, nama, seat):

        node_baru = Node(nama, seat)

        if self.head is None:
            self.head = node_baru

        else:
            current = self.head

            while current.next:
                current = current.next

            current.next = node_baru

    def cek_seat(self, seat):

        current = self.head

        while current:

            if current.seat == seat:
                return True

            current = current.next

        return False

    def tampilkan(self):

        data = []

        current = self.head

        while current:

            data.append({
                "Nama": current.nama,
                "Seat": current.seat
            })

            current = current.next

        return data


# =========================
# SESSION STATE
# =========================

if "konser" not in st.session_state:
    st.session_state.konser = LinkedList()

# =========================
# JUDUL
# =========================

st.title("🎫 SISTEM TIKET KONSER")

# =========================
# PANGGUNG
# =========================

st.markdown("""
<div class="panggung">
🎤 PANGGUNG
</div>
""", unsafe_allow_html=True)

# =========================
# TAMPILAN SEAT
# =========================

seat_list = [
    ["VIP-1", "VIP-2", "VIP-3", "VIP-4"],
    ["FES-1", "FES-2", "FES-3", "FES-4"],
    ["FES-5", "FES-6", "FES-7", "FES-8"]
]

st.subheader("🪑 Denah Seat")

for baris in seat_list:

    cols = st.columns(4)

    for i, seat in enumerate(baris):

        if st.session_state.konser.cek_seat(seat):

            cols[i].markdown(
                f"""
                <div class="kotak-seat booked">
                {seat}<br>BOOKED
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            if "VIP" in seat:
                kelas = "vip"
            else:
                kelas = "festival"

            cols[i].markdown(
                f"""
                <div class="kotak-seat {kelas}">
                {seat}
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================
# FORM BOOKING
# =========================

st.subheader("📝 Booking Tiket")

nama = st.text_input("Nama")

seat_pilih = st.selectbox(
    "Pilih Seat",
    [
        seat
        for row in seat_list
        for seat in row
        if not st.session_state.konser.cek_seat(seat)
    ]
)

if st.button("Pesan Tiket"):

    if nama == "":

        st.warning("Nama wajib diisi!")

    else:

        st.session_state.konser.tambah(
            nama,
            seat_pilih
        )

        st.success("Tiket berhasil dipesan!")

# =========================
# DATA PEMBELI
# =========================

st.subheader("📋 Daftar Pembeli")

data = st.session_state.konser.tampilkan()

if data:
    st.table(data)

else:
    st.info("Belum ada pembeli")

# =========================
# SIDEBAR
# =========================

total_seat = 12
terjual = len(data)
sisa = total_seat - terjual

st.sidebar.title("📊 Statistik")

st.sidebar.metric(
    "Seat Terjual",
    terjual
)

st.sidebar.metric(
    "Seat Tersisa",
    sisa
)

if sisa == 0:
    st.sidebar.error("SOLD OUT")

else:
    st.sidebar.success("Tiket Tersedia")
