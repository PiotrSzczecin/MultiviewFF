# MultiviewFF
Lekki system multiviewerów IPTV/HLS oparty o FFmpeg + Python, przeznaczony do monitoringu kanałów telewizyjnych w środowisku MCR/NOC.  Projekt umożliwia generowanie wielu ścian monitorujących (multiview) z kanałów HLS/IPTV z minimalnym zużyciem CPU, działających lokalnie lub zdalnie przez przeglądarkę WWW.

WYMAGANIA

1. Python
2. FFmpeg

Domyślna ścieżka FFmpeg:

C:\ffmpeg\bin\ffmpeg.exe

Jeśli masz FFmpeg gdzie indziej, popraw w config.json:

"ffmpeg_path": "C:\\ffmpeg\\bin\\ffmpeg.exe"

Fontconfig warning

Jeśli pojawi się ostrzeżenie o fontach, ale obraz działa — można zignorować.
Skrypt wskazuje font:

C:\Windows\Fonts\arial.ttf

Jeśli komputer nie wyrabia, w config.json zmień:

"fps": 5

URUCHOMIENIE

1. Rozpakuj paczkę np. do:

2. Uruchom:
start_mosaic.bat

albo:
python mosaic.py

3. W drugim oknie uruchom:
start_server.bat

albo:
python -m http.server 8080

4. Otwórz:
http://localhost:8081/player.html


Alternatywnie VLC:
http://localhost:8081/hls/index.m3u8

KONFIGURACJA

Nazwa walla jest w config.json:

"wall": {
  "title": "MWE Multiview 1 (ogólne)",
  "header_height": 60
}

Kanały są w sekcji:

"channels": []

CO ROBI AUDIO METER

Każdy stream audio jest przetwarzany przez filtr FFmpeg:

showvolume

i nakładany jako pasek video na dolną część kafelka.

Brak audio metera na którymś kanale

Możliwe, że kanał:
- nie ma audio,
- ma nietypowy układ audio,
- FFmpeg nie zdążył go poprawnie zainicjować.
