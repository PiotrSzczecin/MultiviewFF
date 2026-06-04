# MultiviewFF
Lekki system multiviewerów IPTV/HLS oparty o FFmpeg + Python, przeznaczony do monitoringu kanałów telewizyjnych w środowisku MCR/NOC.  Projekt umożliwia generowanie wielu ścian monitorujących (multiview) z kanałów HLS/IPTV z minimalnym zużyciem CPU, działających lokalnie lub zdalnie przez przeglądarkę WWW.

WYMAGANIA

1. Python

Zainstaluj Python 3.10 lub nowszy.

Podczas instalacji zaznacz:

Add Python to PATH

2. FFmpeg

Pobierz FFmpeg:

https://ffmpeg.org/download.html

Domyślna ścieżka FFmpeg:

C:\ffmpeg\bin\ffmpeg.exe

Jeśli masz FFmpeg gdzie indziej, popraw w config.json:

"ffmpeg_path": "C:\\ffmpeg\\bin\\ffmpeg.exe"
FONTCONFIG WARNING

Jeśli pojawi się ostrzeżenie o fontach, ale obraz działa — można je zignorować.

Skrypt używa fontu:

C:\Windows\Fonts\arial.ttf
OPTYMALIZACJA CPU

Jeśli komputer nie wyrabia:

w config.json zmień:

"fps": 5

Można również:

obniżyć bitrate,
zmniejszyć rozdzielczość kafelków,
użyć NVENC / QSV.

URUCHOMIENIE
1. Rozpakuj paczkę

Np. do:

D:\MWE_Multiview

2. Uruchom generator multiview
start_mosaic.bat

albo:

python mosaic.py

3. W drugim oknie uruchom serwer WWW
start_server.bat

albo:

python -m http.server 8080

4. Otwórz podgląd
MV1
http://localhost:8081/player.html


VLC

Alternatywnie można otworzyć bezpośredni HLS w VLC:

MV1
http://localhost:8081/hls/index.m3u8



KONFIGURACJA
Nazwa walla

W config.json:

"wall": {
  "title": "MWE Multiview 1 (ogólne)",
  "header_height": 60
}
Lista kanałów

Kanały znajdują się w:

"channels": []

Przykład:

{
  "name": "AntenaHD",
  "url": "https://example.com/index.m3u8"
}
AUDIO METERS

Każdy stream audio może być przetwarzany przez filtr FFmpeg:

showvolume

i renderowany jako pasek audio na dole kafelka.

BRAK AUDIO METERA

Możliwe przyczyny:

kanał nie ma audio,
kanał ma nietypowy układ audio,
FFmpeg nie zdążył poprawnie zainicjować streamu,
audio codec jest niestandardowy.
