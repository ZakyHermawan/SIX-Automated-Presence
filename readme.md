# SIX Automated Presence

> Buat kelas onlen.

# Pendahuluan

![Working proof](./proof.gif)

Buat absen di SIX ITB. CRON not included, silakan fork untuk kepentingan bersama.

# Prerequisites

- Punya Python. Kalo gapunya ya gabisa.
- Untuk Selenium harus disetup sendiri; cari driver browser yang sesuai. Dalam code ini saya menggunakan [geckodriver](https://github.com/mozilla/geckodriver/releases) untuk Firefox. Ikutin petunjuk yang ada, masukin ke _*PATH*_.

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

4. Kalo dah masuk, tinggal jalanin scriptnya. Di repo bakal ditaroh di mode headless biar ga muncul browsernya kaya di gif.

```bash
python main.py
```
