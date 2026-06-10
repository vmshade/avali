import re
from urllib.parse import urlparse, parse_qs

YOUTUBE_URL_RE = re.compile(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/")
YOUTUBE_VIDEO_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{11}$")

ALLOWED_FORMATS = ["video", "video+audio", "audio"]


def is_youtube_url(url: str) -> bool:
    return bool(YOUTUBE_URL_RE.match(url))


def extract_video_id(url: str) -> str | None:
    try:
        parsed = urlparse(url if url.startswith("http") else f"https://{url}")
        if parsed.hostname == "youtu.be":
            return parsed.path.lstrip("/").split("/")[0] or None
        if parsed.hostname and parsed.hostname.endswith("youtube.com"):
            qs = parse_qs(parsed.query)
            return qs.get("v", [None])[0]
        return None
    except Exception:
        return None


def is_valid_video_id(vid: str | None) -> bool:
    return vid is not None and bool(YOUTUBE_VIDEO_ID_RE.match(vid))


def validate_download_input(url: str, fmt: str) -> str | None:
    if not url or not url.strip():
        return "url is required!"
    if fmt not in ALLOWED_FORMATS:
        return f"format must be one of these: {', '.join(ALLOWED_FORMATS)}"
    url = url.strip()
    if not is_youtube_url(url):
        return "url must be a youtube link!"
    vid = extract_video_id(url)
    if not is_valid_video_id(vid):
        return "url does not contain a valid video ID!"
    return None
