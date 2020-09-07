# SIX Automated Presence

> Buat kelas onlen.

# Pendahuluan

Buat absen di SIX ITB. CRON not included, klo mo fork silahkan saja. Masih testing sekarang.

# Prerequisites

Punya Python. Kalo gapunya ya gabisa.

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

4. Kalo dah masuk, tinggal jalanin scriptnya.

```bash
python main.py
```

# Note

Script ini tidak termasuk CRON/scheduling. Kalo ada yang mau improve silahkan fork buat kepentingan bersama.
