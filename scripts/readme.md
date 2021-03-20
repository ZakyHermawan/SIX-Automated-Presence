# CRON

## Windows:

1. Buat virtual environment dengan nama venv
2. Aktifkan virtual environment
3. ```pip install six-presence```
4. jalankan cron.bat


Catatan:
Terkadang task yang sudah diberikan tidak dijalankan oleh windows karena komputer tidak terhubung dengan sumber tegangan AC. 
Untuk menangani hal ini kita bisa mengubah pengaturannya (windows search > Task Scheduler Library > Double click pada AutoLoginSIX > Conditions  lalu matikan centang untuk "*start the task only if the computer is on AC power*" pada bagian Power)

Referensi: [Membuat task scheduler pada Windwos](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks)
