@echo off
echo Memeriksa CRON...
setlocal EnableDelayedExpansion
schtasks /query /TN "AutoLoginSIX" >NUL 2>&1
IF %errorlevel% NEQ 0 (
    SET "ACRON=n"
    SET /P "ACRON=CRON belum diaktifkan. Aktifkan CRON (Y/[n])? "
    IF !ACRON!==Y (		
		SET "INTERVAL=60"
		SET /P "INTERVAL=Masukkan interval dalam menit (default 60): "
        echo Mengaktifkan CRON...

        schtasks /CREATE /SC minute /mo !INTERVAL! /tn AutoLoginSIX /tr "%~dp0run.bat"
        schtasks /RUN /tn AutoLoginSIX
        echo Berhasil mengaktifkan CRON!
    ) ELSE (
        echo Tidak mengaktifkan CRON, program berakhir
    )
) ELSE (
    SET /P "DCRON=CRON sudah aktif. Hapus CRON (Y/[n])? "
    IF !DCRON!==Y (
        echo Menghapus CRON...
        schtasks /DELETE /tn AutoLoginSIX /f
        echo Berhasil menghapus CRON!
    ) ELSE (
        echo Tidak menghapus CRON, program berakhir
    )
)
endlocal