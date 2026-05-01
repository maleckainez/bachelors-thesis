import subprocess, re
from pathlib import Path

VIDEO_DIR = Path("/Volumes/Sandisk_usb/od 6 do 14")
OUTPUT_FILE = Path("/Volumes/Sandisk_usb/od 6 do 14/16_min_video.mp4")
LIST_FILE = Path("/Volumes/Sandisk_usb/od 6 do 14/video_list.txt")
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv"}
MAX_VIDEOS = 8 

def natural_key(path: Path):
    """
    Natural sorting key function for file paths. Splits the filename into parts of digits and non-digits.
    For example, "video10.mp4" will be split into ["video", 10, ".mp4"], allowing for correct numerical sorting.
    """
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", path.name)
    ]

files = sorted(
    [
        p for p in VIDEO_DIR.iterdir()
        if p.suffix.lower() in VIDEO_EXTENSIONS and p.resolve() != OUTPUT_FILE.resolve()
    ],
    key=natural_key
)

if MAX_VIDEOS is not None:
    if MAX_VIDEOS <= 0:
        raise ValueError("MAX_VIDEOS must be greater than 0 or None.")
    files = files[:MAX_VIDEOS]

if not files:
    raise FileNotFoundError("No video files found in the specified directory.")

with LIST_FILE.open("w", encoding="utf-8") as f:
    for file in files:
        path = file.resolve().as_posix()
        f.write(f"file '{path}'\n")
        

cmd = [
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", str(LIST_FILE),
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    str(OUTPUT_FILE)
]

subprocess.run(cmd, check=True)

print(f"Concatenated {len(files)} file(s) into: {OUTPUT_FILE}")