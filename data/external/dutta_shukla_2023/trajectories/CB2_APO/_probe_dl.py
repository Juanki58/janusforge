from __future__ import annotations
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
SHARE = "xl7tpf345rt8tikjaidfa8rm7gy2wrpj"
DEST = Path(r"C:\Users\juanc\projects\janusforge\data\external\dutta_shukla_2023\trajectories\CB2_APO")
DEST.mkdir(parents=True, exist_ok=True)
PROBE = DEST / "_probe"
PROBE.mkdir(exist_ok=True)

# Smallest known files from prior HTML probe
FILES = [
    (1046788274875, "mv_short_file", 121),
    (1046785195564, "list", 201),
]

def probe(fid: int, name: str, expected: int):
    url = f"https://uofi.app.box.com/index.php?rm=box_download_shared_file&shared_name={SHARE}&file_id=f_{fid}"
    out = PROBE / f"{name}.bin"
    req = Request(url, headers={
        "User-Agent": UA,
        "Referer": f"https://uofi.app.box.com/s/{SHARE}",
        "Accept": "*/*",
    })
    result = {"name": name, "file_id": fid, "expected": expected, "url": url}
    try:
        with urlopen(req, timeout=60) as r:
            data = r.read()
            out.write_bytes(data)
            head = data[:300]
            result.update({
                "status": r.status,
                "ctype": r.headers.get("Content-Type"),
                "bytes": len(data),
                "bandwidth": b"bandwidth" in head.lower() or b"error_message_bandwidth" in head,
                "html": b"<!DOCTYPE" in head or b"<html" in head.lower(),
                "head_ascii": head.decode("utf-8", "replace")[:200].replace("\n", " "),
            })
    except HTTPError as e:
        body = e.read(800)
        result.update({
            "status": e.code,
            "ctype": e.headers.get("Content-Type") if e.headers else None,
            "bytes": len(body),
            "bandwidth": b"bandwidth" in body.lower() or b"error_message_bandwidth" in body,
            "html": True,
            "head_ascii": body.decode("utf-8", "replace")[:250].replace("\n", " "),
        })
        out.write_bytes(body)
    except Exception as e:
        result.update({"status": 0, "error": f"{type(e).__name__}: {e}"})
    print(json.dumps(result, ensure_ascii=False))
    return result

results = [probe(*f) for f in FILES]
(PROBE / "probe_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
bw = any(r.get("bandwidth") for r in results)
ok = any(r.get("status") == 200 and not r.get("bandwidth") and not r.get("html") for r in results)
print("SUMMARY bandwidth_blocked=", bw, "any_ok=", ok)
