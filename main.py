from datetime import datetime
# DATA BANDARA
bandara = {
    1: "Soekarno-Hatta (CGK)",
    2: "Juanda (SUB)",
    3: "Ngurah Rai (DPS)",
    4: "Kualanamu (KNO)",
    5: "Hasanuddin (UPG)",
    6: "Minangkabau (PDG)",
    7: "Ahmad Yani (SRG)",
    8: "Adisucipto (JOG)",
    9: "Halim Perdanakusuma (HLP)",
    10: "Sultan Mahmud Badaruddin II (PLM)",
    11: "Sultan Syarif Kasim II (PKU)",
    12: "Supadio (PNK)"
}


# DATA MASTER

akun = {}
rute_pesawat = {}       
pesanan = {}            
riwayat = {}            
id_terakhir = 0

login_loket = ("loket123", "loket1234")
login_admin = ("admin123", "admin1234")


# INPUT HELPER

def input_nonempty(p):
    while True:
        v = input(p).strip()
        if v == "":
            print("Input tidak boleh kosong!\n")
        else:
            return v

def input_angka(p):
    while True:
        v = input_nonempty(p)
        if not v.isdigit():
            print("Input harus angka!\n")
        else:
            return int(v)

def input_jadwal(p):
    while True:
        t = input_nonempty(p)
        try:
            dt = datetime.strptime(t, "%Y-%m-%d %H:%M")
            if dt < datetime.now():
                print("Tidak boleh memilih waktu yang sudah lewat!\n")
                continue
            return t
        except:
            print("Format salah! Gunakan YYYY-MM-DD HH:MM\n")


# CLEAN EXPIRED ROUTE & TICKET

def bersihkan_kadaluarsa():
    now = datetime.now()
    to_del = []

    for key, data in rute_pesawat.items():
        dt = datetime.strptime(data["jadwal"], "%Y-%m-%d %H:%M")
        if dt < now:
            to_del.append(key)

    for key in to_del:
        # pindahkan semua pesanan ke riwayat expired
        for uid, tk in pesanan.items():
            for id_t, info in list(tk.items()):
                if info["kode_rute"] == key:
                    info["status"] = "expired"
                    riwayat.setdefault(uid, {})[id_t] = info
                    del pesanan[uid][id_t]

        del rute_pesawat[key]


# ADMIN MENU

def tampil_bandara():
    print("\n===== DAFTAR BANDARA =====")
    for i, b in bandara.items():
        print(f"{i}. {b}")
    print()

def admin_tambah_rute():
    print("\n===== TAMBAH RUTE =====")
    kode = input_nonempty("Masukkan kode rute baru: ").upper()

    if kode in rute_pesawat:
        print("Kode rute sudah ada!\n")
        return

    tampil_bandara()
    asal = input_angka("Pilih nomor bandara keberangkatan: ")
    if asal not in bandara:
        print("Bandara tidak valid!\n")
        return

    tampil_bandara()
    tujuan = input_angka("Pilih nomor bandara tujuan: ")
    if tujuan not in bandara:
        print("Bandara tidak valid!\n")
        return

    jadwal = input_jadwal("Masukkan jadwal (YYYY-MM-DD HH:MM): ")
    harga = input_angka("Masukkan harga tiket: ")

    # kursi total 140
    kursi = {i: "O" for i in range(1, 141)}

    rute_pesawat[kode] = {
        "asal": bandara[asal],
        "tujuan": bandara[tujuan],
        "jadwal": jadwal,
        "harga": harga,
        "kursi": kursi
    }

    print("Rute berhasil ditambahkan!\n")

def admin_tampil_rute():
    bersihkan_kadaluarsa()
    print("\n===== SEMUA RUTE =====")
    if not rute_pesawat:
        print("Belum ada rute.\n")
        return

    for kode, r in rute_pesawat.items():
        print("------------------------")
        print(f"Kode Rute   : {kode}")
        print(f"Asal        : {r['asal']}")
        print(f"Tujuan      : {r['tujuan']}")
        print(f"Jadwal      : {r['jadwal']}")
        print(f"Harga       : {r['harga']}")
        print("------------------------")

def admin_edit_rute():
    admin_tampil_rute()
    kode = input_nonempty("Masukkan kode rute yang ingin diedit: ").upper()

    if kode not in rute_pesawat:
        print("Rute tidak ditemukan!\n")
        return

    data = rute_pesawat[kode]

    print("Tekan ENTER untuk tidak mengubah data")

    # asal
    tampil_bandara()
    asal = input("Bandara asal baru (kosong = tdk diubah): ").strip()
    if asal.isdigit() and int(asal) in bandara:
        data["asal"] = bandara[int(asal)]

    # tujuan
    tampil_bandara()
    tujuan = input("Bandara tujuan baru (kosong = tdk diubah): ").strip()
    if tujuan.isdigit() and int(tujuan) in bandara:
        data["tujuan"] = bandara[int(tujuan)]

    # jadwal
    jadwal_baru = input("Jadwal baru (YYYY-MM-DD HH:MM): ").strip()
    if jadwal_baru:
        try:
            dt = datetime.strptime(jadwal_baru, "%Y-%m-%d %H:%M")
            if dt > datetime.now():
                data["jadwal"] = jadwal_baru
        except:
            print("Format jadwal salah, tidak diubah.")

    # harga
    harga_baru = input("Harga baru: ").strip()
    if harga_baru.isdigit():
        data["harga"] = int(harga_baru)

    print("Rute berhasil diperbarui!\n")

def admin_hapus_rute():
    admin_tampil_rute()
    kode = input_nonempty("Masukkan kode rute yang akan dihapus: ").upper()

    if kode not in rute_pesawat:
        print("Rute tidak ditemukan!\n")
        return

    del rute_pesawat[kode]
    print("Rute berhasil dihapus!\n")

def menu_admin():
    while True:
        bersihkan_kadaluarsa()
        print("\n===== MENU ADMIN =====")
        print("1. Tambah Rute")
        print("2. Tampilkan Rute")
        print("3. Edit Rute")
        print("4. Hapus Rute")
        print("5. Kembali")

        p = input_nonempty("Pilih: ")

        if p == "1":
            admin_tambah_rute()
        elif p == "2":
            admin_tampil_rute()
        elif p == "3":
            admin_edit_rute()
        elif p == "4":
            admin_hapus_rute()
        elif p == "5":
            break
        else:
            print("Pilihan salah!\n")


# USER SYSTEM

def buat_akun():
    global id_terakhir

    print("\n===== BUAT AKUN =====")
    nama = input_nonempty("Nama lengkap: ")

    while True:
        email = input_nonempty("Email: ").lower()
        if "@" not in email:
            print("Email tidak valid!")
            continue
        if email in akun:
            print("Email sudah digunakan!")
            continue
        break

    while True:
        pw = input_nonempty("Password (min 8): ")
        if len(pw) < 8:
            print("Minimal 8 karakter!\n")
        else:
            break

    telepon = input_nonempty("Telepon: ")

    id_terakhir += 1
    akun[email] = {
        "id": id_terakhir,
        "nama": nama,
        "password": pw,
        "telepon": telepon
    }

    print("Akun berhasil dibuat!\n")

def login():
    print("\n===== LOGIN =====")
    email = input_nonempty("Email: ").lower()

    if email not in akun:
        print("Email tidak terdaftar!\n")
        return None

    pw = input_nonempty("Password: ")

    if pw == akun[email]["password"]:
        print(f"Selamat datang {akun[email]['nama']}!\n")
        return email
    else:
        print("Password salah!\n")
        return None


# USER: TICKET MENU

def tampil_rute_user():
    bersihkan_kadaluarsa()
    print("\n===== RUTE TERSEDIA =====")
    if not rute_pesawat:
        print("Belum ada rute.\n")
        return

    for kode, r in rute_pesawat.items():
        print("------------------------")
        print(f"Kode Rute  : {kode}")
        print(f"Asal       : {r['asal']}")
        print(f"Tujuan     : {r['tujuan']}")
        print(f"Jadwal     : {r['jadwal']}")
        print(f"Harga      : {r['harga']}")
        print("------------------------")

def tampil_kursi(kursi):
    print("\n===== KURSI TERSEDIA =====")
    for i in range(1, 141):
        status = kursi[i]
        print(f"{i}:{status}", end="  ")
        if i % 10 == 0:
            print()
    print()

def pesan_tiket(id_user):
    bersihkan_kadaluarsa()
    if not rute_pesawat:
        print("Belum ada rute tersedia.\n")
        return

    tampil_rute_user()
    kode = input_nonempty("Masukkan kode rute: ").upper()

    if kode not in rute_pesawat:
        print("Rute tidak ditemukan!")
        return

    r = rute_pesawat[kode]
    kursi = r["kursi"]

    tampil_kursi(kursi)

    # pilih kursi
    while True:
        pilih = input_nonempty("Pilih nomor kursi: ")
        if not pilih.isdigit():
            print("Harus angka!")
            continue

        pilih = int(pilih)
        if pilih < 1 or pilih > 140:
            print("Kursi tidak tersedia!")
            continue

        if kursi[pilih] == "X":
            print("Kursi sudah digunakan!")
            continue

        break

    kursi[pilih] = "X"

    tiket_id = f"T{len(pesanan.get(id_user, {})) + 1}"

    data = {
        "kode_rute": kode,
        "kursi": pilih,
        "harga": r["harga"],
        "asal": r["asal"],
        "tujuan": r["tujuan"],
        "jadwal": r["jadwal"],
        "status": "active"
    }

    pesanan.setdefault(id_user, {})[tiket_id] = data

    print(f"Tiket berhasil dipesan! ID Tiket: {tiket_id}\n")

def tiket_user(id_user):
    bersihkan_kadaluarsa()
    print("\n===== TIKET AKTIF =====")
    data = pesanan.get(id_user, {})

    if not data:
        print("Tidak ada tiket aktif.\n")
    else:
        for t, d in data.items():
            print("------------------------")
            print(f"ID Tiket   : {t}")
            print(f"Rute       : {d['asal']} → {d['tujuan']}")
            print(f"Jadwal     : {d['jadwal']}")
            print(f"Kursi      : {d['kursi']}")
            print(f"Harga      : {d['harga']}")
            print("------------------------")

def riwayat_user(id_user):
    print("\n===== RIWAYAT PEMESANAN =====")
    data = riwayat.get(id_user, {})

    if not data:
        print("Belum ada riwayat.\n")
        return

    for t, d in data.items():
        print("------------------------")
        print(f"ID Tiket   : {t}")
        print(f"Status     : {d['status']}")
        print(f"Rute       : {d['asal']} → {d['tujuan']}")
        print(f"Jadwal     : {d['jadwal']}")
        print(f"Kursi      : {d['kursi']}")
        print("------------------------")

def user_menu(email):
    id_user = akun[email]["id"]

    while True:
        bersihkan_kadaluarsa()
        print("\n===== MENU USER =====")
        print("1. Tampilkan Rute")
        print("2. Pesan Tiket")
        print("3. Tiket Aktif")
        print("4. Riwayat Pemesanan")
        print("5. Logout")

        p = input_nonempty("Pilih: ")

        if p == "1":
            tampil_rute_user()
        elif p == "2":
            pesan_tiket(id_user)
        elif p == "3":
            tiket_user(id_user)
        elif p == "4":
            riwayat_user(id_user)
        elif p == "5":
            break
        else:
            print("Pilihan salah!\n")


# LOKET
def loket_proses():
    print("\n===== GUNAKAN TIKET =====")
    kode = input_nonempty("Masukkan ID tiket: ").upper()

    ditemukan = False

    # cari tiket di semua user
    for uid, tk in pesanan.items():
        if kode in tk:
            ditemukan = True
            data = tk[kode]

            # tampilkan detail tiket
            print("\n===== DATA TIKET =====")
            print(f"ID Tiket   : {kode}")
            print(f"User ID    : {uid}")
            print(f"Rute       : {data['asal']} → {data['tujuan']}")
            print(f"Jadwal     : {data['jadwal']}")
            print(f"Kursi      : {data['kursi']}")
            print(f"Harga      : {data['harga']}")
            print("======================")

            # konfirmasi
            while True:
                konfirmasi = input("Gunakan tiket ini? (Y/N): ").strip().upper()
                if konfirmasi in ["Y", "N"]:
                    break
                print("Input harus Y atau N!")

            if konfirmasi == "Y":
                data["status"] = "used"
                riwayat.setdefault(uid, {})[kode] = data
                del tk[kode]
                print("Tiket berhasil digunakan!\n")
            else:
                print("Penggunaan tiket dibatalkan.\n")

            return

    if not ditemukan:
        print("Tiket tidak ditemukan!\n")

def loket_menu():
    while True:
        print("\n===== MENU LOKET =====")
        print("1. Gunakan Tiket")
        print("2. Logout")

        p = input_nonempty("Pilih: ")

        if p == "1":
            loket_proses()
        elif p == "2":
            break
        else:
            print("Pilihan salah!\n")


# MAIN MENU

while True:
    bersihkan_kadaluarsa()
    print("\n===== APLIKASI TIKET PESAWAT =====")
    print("1. Admin")
    print("2. User")
    print("3. Loket")
    print("4. Keluar")

    p = input_nonempty("Pilih menu: ")

    if p == "1":
        u = input_nonempty("Username admin: ")
        pw = input_nonempty("Password: ")
        if (u, pw) == login_admin:
            menu_admin()
        else:
            print("Login gagal!\n")

    elif p == "2":
        print("\n1. Login\n2. Daftar")
        op = input_nonempty("Pilih: ")

        if op == "1":
            email = login()
            if email:
                user_menu(email)
        elif op == "2":
            buat_akun()

    elif p == "3":
        u = input_nonempty("Username loket: ")
        pw = input_nonempty("Password: ")
        if (u, pw) == login_loket:
            loket_menu()
        else:
            print("Login gagal!\n")

    elif p == "4":
        print("Keluar program...")
        break

    else:
        print("Pilihan salah!\n")
