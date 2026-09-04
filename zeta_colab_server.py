"""ZetaForge Colab server bootstrap.

Run this in a Google Colab GPU runtime. It installs nothing by itself; the
notebook is the recommended one-click path. This script is useful when a
single Python cell/file is preferred.
"""
import getpass
import os
import subprocess
import time
from pathlib import Path

import requests
from pyngrok import conf, ngrok

RESERVED_DOMAIN = os.getenv("ZETAFORGE_NGROK_DOMAIN", "paralegal-pampers-chevron.ngrok-free.dev")
LOCAL_PORT = int(os.getenv("ZETAFORGE_PORT", "5001"))
MODEL_PATH = os.getenv("ZETAFORGE_MODEL", "/content/Llama-3.1-8B-Stheno-v3.4-Q4_K_M.gguf")
CONTEXT_SIZE = int(os.getenv("ZETAFORGE_CONTEXT", "8192"))
GPU_LAYERS = int(os.getenv("ZETAFORGE_GPU_LAYERS", "33"))


def get_ngrok_token():
    token = ""
    try:
        from google.colab import userdata
        token = userdata.get("NGROK_AUTHTOKEN") or ""
    except Exception:
        pass
    token = token or os.getenv("NGROK_AUTHTOKEN", "")
    if not token:
        token = getpass.getpass("Ngrok Authtoken (not echoed): ")
    if not token.strip():
        raise RuntimeError("No Ngrok Authtoken supplied.")
    return token.strip()


def main():
    token = get_ngrok_token()
    conf.get_default().auth_token = token
    try:
        ngrok.kill()
    except Exception:
        pass
    subprocess.run(["pkill", "-9", "ngrok"], stderr=subprocess.DEVNULL, check=False)

    cmd = ["./koboldcpp", "--model", MODEL_PATH, "--port", str(LOCAL_PORT),
           "--gpulayers", str(GPU_LAYERS), "--contextsize", str(CONTEXT_SIZE),
           "--flashattention", "--smartcontext"]
    log = open("/content/koboldcpp.log", "a", buffering=1)
    proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)

    local_models = f"http://127.0.0.1:{LOCAL_PORT}/v1/models"
    for _ in range(90):
        if proc.poll() is not None:
            raise RuntimeError(Path("/content/koboldcpp.log").read_text(errors="replace")[-4000:])
        try:
            if requests.get(local_models, timeout=2).ok:
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        raise TimeoutError("KoboldCpp did not become ready within 90 seconds.")

    try:
        tunnel = ngrok.connect(LOCAL_PORT, domain=RESERVED_DOMAIN)
    except Exception:
        tunnel = ngrok.connect(LOCAL_PORT, domain=RESERVED_DOMAIN, pooling_enabled=True)

    base = tunnel.public_url.rstrip("/") + "/v1"
    headers = {"Content-Type": "application/json", "ngrok-skip-browser-warning": "true"}
    models = requests.get(base + "/models", headers=headers, timeout=15)
    models.raise_for_status()
    model_id = (models.json().get("data") or [{}])[0].get("id") or "Llama-3.1-8B-Stheno-v3.4"
    test = requests.post(base + "/chat/completions", headers=headers, json={
        "model": model_id,
        "messages": [{"role": "user", "content": "Reply with exactly: ZetaForge connection OK"}],
        "temperature": 0,
        "max_tokens": 12,
        "stream": False,
    }, timeout=90)
    test.raise_for_status()
    reply = ((test.json().get("choices") or [{}])[0].get("message") or {}).get("content", "").strip()

    print("=" * 72)
    print("ZetaForge Colab server is ready")
    print("API:", base)
    print("Model:", model_id)
    print("Verification:", reply)
    print("Keep this process alive while using ZetaForge.")
    print("=" * 72)
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
