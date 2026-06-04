
import json, math, subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG = json.loads((BASE_DIR / "config.json").read_text(encoding="utf-8"))

def esc(t):
    return t.replace("\\","\\\\").replace(":","\\:").replace("'","\\'")

ffmpeg = CONFIG["ffmpeg_path"]
channels = CONFIG["channels"]
cols = CONFIG["layout"]["columns"]

video_w = CONFIG["layout"]["video_width"]
video_h = CONFIG["layout"]["video_height"]
header_h = CONFIG["layout"]["channel_header_height"]
meter_h = CONFIG["layout"]["audio_meter_height"]
fps = CONFIG["layout"]["fps"]

wall_title = CONFIG["wall"]["title"]
wall_header_h = CONFIG["wall"]["header_height"]

rows = math.ceil(len(channels)/cols)

tile_w = video_w
tile_h = header_h + video_h + meter_h

wall_w = tile_w * cols
wall_h = tile_h * rows + wall_header_h

font = "C\\:/Windows/Fonts/arial.ttf"

parts = []

for i,ch in enumerate(channels):

    name = esc(ch["name"])

    parts.append(
        f"color=c=0x111111:s={tile_w}x{header_h}:r={fps},"
        f"drawtext=fontfile='{font}':text='{name}':x=12:y=(h-th)/2:fontsize=22:fontcolor=white"
        f"[h{i}]"
    )

    parts.append(
        f"[{i}:v]"
        f"fps={fps},"
        f"scale={video_w}:{video_h}:force_original_aspect_ratio=decrease,"
        f"pad={video_w}:{video_h}:(ow-iw)/2:(oh-ih)/2,"
        f"setsar=1"
        f"[v{i}]"
    )

    parts.append(
        f"[{i}:a]"
        f"aformat=channel_layouts=stereo,"
        f"showvolume=w={tile_w}:h={meter_h}:r={fps}:b=4:dm=1:ds=log,"
        f"scale={tile_w}:{meter_h}"
        f"[m{i}]"
    )

    parts.append(f"[h{i}][v{i}][m{i}]vstack=inputs=3[t{i}]")

total = rows * cols

for i in range(len(channels), total):
    parts.append(
        f"color=c=black:s={tile_w}x{tile_h}:r={fps},"
        f"drawbox=x=0:y=0:w=iw:h={header_h}:color=0x111111:t=fill,"
        f"drawtext=fontfile='{font}':text='EMPTY':x=12:y=8:fontsize=22:fontcolor=gray"
        f"[t{i}]"
    )

row_labels = []
for r in range(rows):
    inputs = "".join(f"[t{r*cols+c}]" for c in range(cols))
    lbl = f"row{r}"
    row_labels.append(lbl)
    parts.append(f"{inputs}hstack=inputs={cols}[{lbl}]")

if len(row_labels) == 1:
    parts.append(f"[{row_labels[0]}]copy[grid]")
else:
    stack = "".join(f"[{x}]" for x in row_labels)
    parts.append(f"{stack}vstack=inputs={len(row_labels)}[grid]")

parts.append(
    f"color=c=black:s={wall_w}x{wall_h}:r={fps},"
    f"drawbox=x=0:y={wall_header_h-2}:w=iw:h=2:color=white@0.3:t=fill,"
    f"drawtext=fontfile='{font}':text='{esc(wall_title)}':x=20:y=14:fontsize=30:fontcolor=white,"
    f"drawtext=fontfile='{font}':text='%{{localtime\\:%Y-%m-%d %H\\\\\\:%M\\\\\\:%S}}':x=w-tw-20:y=14:fontsize=28:fontcolor=white"
    f"[bg]"
)

parts.append(f"[bg][grid]overlay=x=0:y={wall_header_h}[outv]")

fc = ";".join(parts)

cmd = [ffmpeg, "-hide_banner", "-loglevel", "info"]

for ch in channels:
    cmd += [
        "-thread_queue_size","1024",
        "-reconnect","1",
        "-reconnect_streamed","1",
        "-reconnect_delay_max","5",
        "-i", ch["url"]
    ]

hls = BASE_DIR / "hls"
hls.mkdir(exist_ok=True)

cmd += [
    "-filter_complex", fc,
    "-map","[outv]",
    "-an",
    "-c:v","libx264",
    "-preset","veryfast",
    "-tune","zerolatency",
    "-b:v","6500k",
    "-g", str(fps*2),
    "-f","hls",
    "-hls_time","2",
    "-hls_list_size","6",
    "-hls_flags","delete_segments+append_list",
    "-hls_segment_filename", str(hls / "seg_%05d.ts"),
    str(hls / "index.m3u8")
]

subprocess.run(cmd)
