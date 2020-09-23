# SIX Automated Presence

> Buat kelas onlen.

# Pendahuluan

![Working proof](./proof.gif)

Buat absen di SIX ITB. CRON not included, silakan fork untuk kepentingan bersama.

# Prerequisites

- Punya Python. Kalo gapunya ya gabisa.
- Untuk Selenium harus disetup sendiri; cari driver browser yang sesuai. Dalam code ini saya menggunakan [geckodriver](https://github.com/mozilla/geckodriver/releases) untuk Firefox. Ikutin petunjuk yang ada, masukin ke _*PATH*_.

_Note_: As per 23/09/2020, setup Selenium sudah bisa diabaikan bila menggunakan modul absensi berbasiskan HTTP Request. (`presence_by_request.py`)

# Setup

1. Jalanin di cmd/terminal untuk setup venv:

```bash
python -m venv venv
```

2. Masuk ke venv:

Untuk Windows:

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

Untuk Linux-based System:

```
./venv/scripts/activate
pip install -r requirements.txt
```

3. Bikin file `credentials.json`, ada contohnya.

4. Jalankan code ini.

```bash
python main.py
```

# Contributing

Jika hendak contribute, silahkan submit Pull Request, nanti akan direview. (Mungkin) akan butuh beberapa hal seperti:

- CRON support (script jalan di background tiap suatu interval)
- Multithread support (melakukan absensi beberapa orang sekaligus)
