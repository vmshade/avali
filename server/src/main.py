import asyncio
import json
import re
import subprocess
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from .validate import validate_download_input, extract_video_id

app = FastAPI(title="avali")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

RATE_LIMIT: dict[str, list[float]] = {}
RATE_WINDOW = 5.0
RATE_MAX = 5


def rate_limit(ip: str) -> None:
    now = time.time()
    timestamps = RATE_LIMIT.get(ip, [])
    timestamps = [t for t in timestamps if now - t < RATE_WINDOW]
    if len(timestamps) >= RATE_MAX:
        raise HTTPException(status_code=429, detail="slow down a little!!!")
    timestamps.append(now)
    RATE_LIMIT[ip] = timestamps


class DownloadRequest(BaseModel):
    url: str
    format: str = "video+audio"
    quality: int | None = None
    container: str = "mp4"


def sanitize_filename(name: str) -> str:
    return re.sub(r'[^\w\s.-]', "", name).strip() or "video"


def get_video_title(video_id: str) -> str | None:
    try:
        result = subprocess.run(
            ["yt-dlp", "--print", "title", f"https://www.youtube.com/watch?v={video_id}"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return None


VIDEO_MIME = {
    "mp4": "video/mp4",
    "webm": "video/webm",
    "mkv": "video/x-matroska",
}
AUDIO_MIME = {
    "mp4": "audio/mp4",
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "flac": "audio/flac",
}


def get_format_args(fmt: str, quality: int | None = None, container: str = "mp4") -> list[str]:
    if fmt == "audio":
        if container in ("mp3", "wav", "flac"):
            return ["-f", "bestaudio", "--extract-audio", "--audio-format", container]
        return ["-f", "bestaudio[ext=m4a]/bestaudio"]

    if container == "mkv":
        if quality:
            return [
                "-f",
                f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best",
                "--merge-output-format", "mkv",
            ]
        return ["-f", "bestvideo+bestaudio", "--merge-output-format", "mkv"]

    vext = container
    aext = "m4a" if container == "mp4" else "webm"

    if fmt == "video+audio":
        if quality:
            return ["-f", f"bestvideo[height<={quality}][ext={vext}]+bestaudio[ext={aext}]/best[height<={quality}][ext={vext}]/best"]
        return ["-f", f"bestvideo[ext={vext}]+bestaudio[ext={aext}]/best[ext={vext}]/best"]

    if fmt == "video":
        if quality:
            return ["-f", f"bestvideo[height<={quality}][ext={vext}]+bestaudio[ext={aext}]/best[height<={quality}][ext={vext}]/best"]
        return ["-f", f"bestvideo[ext={vext}]+bestaudio[ext={aext}]/best[ext={vext}]/best"]

    return ["-f", "best[ext=mp4]/best"]


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/qualities")
async def get_qualities(url: str, request: Request):
    ip = request.client.host if request.client else "unknown"
    rate_limit(ip)

    err = validate_download_input(url, "video+audio")
    if err:
        raise HTTPException(status_code=400, detail=err)

    vid = extract_video_id(url)
    loop = asyncio.get_running_loop()

    def run():
        proc = subprocess.Popen(
            ["yt-dlp", "--dump-json", "--no-warnings",
             f"https://www.youtube.com/watch?v={vid}"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        try:
            stdout, stderr = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            raise TimeoutError("ytdlp timed out")
        return proc.returncode, stdout, stderr

    try:
        returncode, stdout, stderr = await loop.run_in_executor(None, run)
    except TimeoutError as e:
        raise HTTPException(status_code=500, detail=str(e))

    if returncode != 0:
        err_text = stderr.decode("utf-8", errors="replace").strip()
        raise HTTPException(status_code=500, detail=err_text or "failed to fetch formats")

    data = json.loads(stdout)
    formats = data.get("formats", [])

    heights = sorted(set(
        f["height"] for f in formats
        if f.get("vcodec") and f["vcodec"] != "none" and f.get("height")
    ), reverse=True)

    if not heights:
        raise HTTPException(status_code=500, detail="no video formats found")

    return {"qualities": heights}


@app.post("/api/metadata")
async def get_metadata(req: DownloadRequest, request: Request):
    ip = request.client.host if request.client else "unknown"
    rate_limit(ip)

    err = validate_download_input(req.url, req.format)
    if err:
        raise HTTPException(status_code=400, detail=err)

    vid = extract_video_id(req.url)
    fmt = req.format
    fmt_args = get_format_args(fmt, req.quality, req.container)

    loop = asyncio.get_running_loop()

    def run():
        proc = subprocess.Popen(
            ["yt-dlp", *fmt_args, "--dump-json", "--no-warnings",
             f"https://www.youtube.com/watch?v={vid}"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        try:
            stdout, stderr = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            raise TimeoutError("yt-dlp timed out")
        return proc.returncode, stdout, stderr

    try:
        returncode, stdout, stderr = await loop.run_in_executor(None, run)
    except TimeoutError as e:
        raise HTTPException(status_code=500, detail=str(e))

    if returncode != 0:
        err_text = stderr.decode("utf-8", errors="replace").strip()
        raise HTTPException(status_code=500, detail=err_text or "failed to get metadata")

    data = json.loads(stdout)

    total_size = 0
    requested = data.get("requested_formats")
    if requested:
        for f in requested:
            size = f.get("filesize") or f.get("filesize_approx") or 0
            total_size += size
    else:
        total_size = data.get("filesize") or data.get("filesize_approx") or 0

    title = data.get("title", "") or ""

    return {
        "size": total_size if total_size > 0 else None,
        "title": title,
    }


@app.post("/api/download")
async def download(req: DownloadRequest, request: Request):
    ip = request.client.host if request.client else "unknown"
    rate_limit(ip)

    err = validate_download_input(req.url, req.format)
    if err:
        raise HTTPException(status_code=400, detail=err)

    vid = extract_video_id(req.url)
    fmt = req.format
    fmt_args = get_format_args(fmt, req.quality, req.container)

    title = get_video_title(vid)
    safe_name = sanitize_filename(title or vid)

    loop = asyncio.get_running_loop()

    def start_proc():
        return subprocess.Popen(
            ["yt-dlp", *fmt_args, "-o", "-", "--no-warnings", "--quiet",
             f"https://www.youtube.com/watch?v={vid}"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )

    proc = await loop.run_in_executor(None, start_proc)

    def read_first_chunk():
        return proc.stdout.read(65536)

    try:
        first_chunk = await asyncio.wait_for(
            loop.run_in_executor(None, read_first_chunk), timeout=10.0,
        )
    except asyncio.TimeoutError:
        await loop.run_in_executor(None, proc.kill)
        await loop.run_in_executor(None, proc.wait)
        raise HTTPException(status_code=500, detail="ytdlp timed out")

    if not first_chunk:
        await loop.run_in_executor(None, proc.wait)
        raise HTTPException(status_code=500, detail="ytdlp produced no output")

    container = req.container
    if fmt == "audio":
        ext = container if container != "mp4" else "m4a"
        mime = AUDIO_MIME.get(container, "audio/mp4")
    else:
        ext = container
        mime = VIDEO_MIME.get(container, "video/mp4")

    async def stream():
        yield first_chunk
        while True:
            chunk = await loop.run_in_executor(None, lambda: proc.stdout.read(65536))
            if not chunk:
                break
            yield chunk
        await loop.run_in_executor(None, proc.wait)

    return StreamingResponse(
        stream(),
        media_type=mime,
        headers={
            "Content-Disposition": f'attachment; filename="{safe_name}.{ext}"',
            "X-Content-Type-Options": "nosniff",
        },
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
