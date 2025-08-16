import os, time, json, socket, asyncio
import psutil
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

PORT  = int(os.getenv("AGENT_PORT", "8765"))
TOKEN = os.getenv("AGENT_TOKEN", "change-me")  # set your own strong token!

app = FastAPI(title="LAN System Monitor")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def metrics_snapshot() -> dict:
    vm = psutil.virtual_memory()
    disk = psutil.disk_usage(os.getenv("SYSTEMDRIVE", "C:\\"))
    net = psutil.net_io_counters()
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_used_mb": round(vm.used / (1024*1024), 1),
        "ram_total_mb": round(vm.total / (1024*1024), 1),
        "disk_used_gb": round(disk.used / (1024**3), 2),
        "disk_total_gb": round(disk.total / (1024**3), 2),
        "process_count": len(psutil.pids()),
        "net_bytes_sent": net.bytes_sent,
        "net_bytes_recv": net.bytes_recv,
        "timestamp": time.time(),
    }

@app.get("/")
async def home(_: Request):
    ip = get_ip()
    html = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>LAN System Monitor</title>
<style>
  :root {{ --bg:#0b1220; --card:#141c2f; --fg:#fff; }}
  body {{ margin:0; padding:24px; font-family:system-ui,Segoe UI,Roboto,Arial; background:var(--bg); color:var(--fg); }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; }}
  .card {{ background:var(--card); border-radius:16px; padding:18px; box-shadow:0 6px 20px rgba(0,0,0,.3); }}
  .kv {{ font-size:13px; opacity:.8; margin-bottom:6px; }}
  .val {{ font-size:32px; line-height:1.1; word-break:break-word; }}
  .status {{ margin:8px 0 18px; opacity:.9; }}
  .hint {{ font-size:12px; opacity:.7; }}
  input {{ padding:6px 10px; border-radius:10px; border:none; outline:none; }}
  button {{ padding:6px 12px; border-radius:10px; border:none; cursor:pointer; }}
</style>
</head>
<body>
  <h1>LAN System Monitor</h1>
  <div class="hint">Open on another laptop: <b>http://{ip}:{PORT}</b></div>
  <div class="hint">Token is required (set via AGENT_TOKEN env var).</div>

  <div class="status" id="status">Connecting…</div>
  <div style="margin:6px 0 14px;">
    <input id="token" placeholder="enter token" />
    <button onclick="saveToken()">Save token</button>
  </div>

  <div class="grid">
    <div class="card"><div class="kv">CPU %</div><div class="val" id="cpu">–</div></div>
    <div class="card"><div class="kv">RAM Used / Total (MB)</div><div class="val" id="ram">–</div></div>
    <div class="card"><div class="kv">Disk Used / Total (GB)</div><div class="val" id="disk">–</div></div>
    <div class="card"><div class="kv">Processes</div><div class="val" id="procs">–</div></div>
    <div class="card"><div class="kv">Network bytes (sent / recv)</div><div class="val" id="net">–</div></div>
    <div class="card"><div class="kv">Last update</div><div class="val" id="ts">–</div></div>
  </div>

<script>
  function saveToken(){{ 
    localStorage.setItem("agent_token", document.getElementById("token").value.trim()); 
    location.reload(); 
  }}

  const PORT = {PORT};
  const token = localStorage.getItem("agent_token") || "";
  document.getElementById("token").value = token;

  const scheme = location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(`${{scheme}}://${{location.hostname}}:${{PORT}}/ws?token=${{encodeURIComponent(token)}}`);

  const set = (id,v)=>document.getElementById(id).textContent=v;

  ws.onopen   = () => document.getElementById("status").textContent = "Connected";
  ws.onclose  = () => document.getElementById("status").textContent = "Disconnected";
  ws.onerror  = () => document.getElementById("status").textContent = "Error (check token/port/firewall)";

  ws.onmessage = (e) => {{
    const d = JSON.parse(e.data);
    set("cpu", (d.cpu_percent ?? 0).toFixed(1));
    set("ram", `${{d.ram_used_mb}} / ${{d.ram_total_mb}}`);
    set("disk", `${{d.disk_used_gb}} / ${{d.disk_total_gb}}`);
    set("procs", d.process_count);
    set("net", `${{d.net_bytes_sent}} / ${{d.net_bytes_recv}}`);
    set("ts", new Date(d.timestamp*1000).toLocaleTimeString());
  }};
</script>
</body></html>"""
    return HTMLResponse(html)

@app.get("/metrics")
async def metrics(token: str):
    if token != TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return JSONResponse(metrics_snapshot())

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    token = ws.query_params.get("token")
    if token != TOKEN:
        await ws.close(code=4401)
        return
    await ws.accept()
    try:
        while True:
            await ws.send_text(json.dumps(metrics_snapshot()))
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    ip = get_ip()
    print(f"Agent URL:   http://{ip}:{PORT}")
    print(f"Auth token:  {TOKEN!r}")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        log_level="warning",
        log_config=None   
    )
