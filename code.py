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

# duck.py'den tuşları al
try:
    from duck import duckyCommands
    safe_keys = []
    for key in duckyCommands.values():
        if isinstance(key, int) and key >= Keycode.A and key <= Keycode.Z:
            safe_keys.append(key)
    # ENTER ve CAPSLOCK ekle
    safe_keys.extend([Keycode.ENTER, Keycode.CAPS_LOCK])
    print(f"✅ {len(safe_keys)} tuş yüklendi (ENTER, CAPSLOCK dahil)")
except:
    safe_keys = [Keycode.A, Keycode.B, Keycode.C, Keycode.ENTER, Keycode.CAPS_LOCK]
    print("⚠️ Varsayılan tuşlar kullanılıyor")

ssid = "FATİHH"
password = "12345678"

# Pinler
gp5 = digitalio.DigitalInOut(board.GP5)
gp6 = digitalio.DigitalInOut(board.GP6)
gp5.pull = digitalio.Pull.UP
gp6.pull = digitalio.Pull.UP

# HID
mouse = Mouse(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)

jiggler_running = False

def mouse_jiggle():
    global jiggler_running
    jiggler_running = True
    print("🖱️ Mouse jiggle başladı")
    while jiggler_running and not gp5.value:
        mouse.move(random.randint(-100, 100), random.randint(-100, 100))
        time.sleep(0.1)
        server.poll()
    jiggler_running = False
    print("🖱️ Mouse jiggle bitti")

def combined_jiggle():
    global jiggler_running
    jiggler_running = True
    print("🖱️⌨️ Mouse + Klavye başladı")
    while jiggler_running and not gp6.value:
        if random.random() < 0.5:
            mouse.move(random.randint(-100, 100), random.randint(-100, 100))
        else:
            key = random.choice(safe_keys)
            kbd.press(key)
            time.sleep(0.05)
            kbd.release_all()
        time.sleep(0.1)
        server.poll()
    jiggler_running = False
    print("🖱️⌨️ Mouse + Klavye bitti")

# WiFi AP
wifi.radio.start_ap(ssid, password)
print(f"📡 WiFi: {ssid} | IP: {wifi.radio.ipv4_address}")

# Server
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=False)

@server.route("/")
def base(request: Request):
    with open("index.html", "r") as f:
        return Response(request, f.read(), headers={"Content-Type": "text/html"})

@server.route("/api", POST)
def api(request: Request):
    return JSONResponse(request, {"message": "OK"})

@server.route("/jiggle/mouse", POST)
def api_mouse(request: Request):
    global jiggler_running
    if not jiggler_running:
        jiggler_running = True
        print("🌐 Web: Mouse jiggle başladı")
        for _ in range(50):
            if not jiggler_running:
                break
            mouse.move(random.randint(-100, 100), random.randint(-100, 100))
            time.sleep(0.1)
        jiggler_running = False
        print("🌐 Web: Mouse jiggle bitti")
    return JSONResponse(request, {"status": "ok"})

@server.route("/jiggle/combined", POST)
def api_combined(request: Request):
    global jiggler_running
    if not jiggler_running:
        jiggler_running = True
        print("🌐 Web: Mouse + Klavye başladı")
        for _ in range(50):
            if not jiggler_running:
                break
            if random.random() < 0.5:
                mouse.move(random.randint(-100, 100), random.randint(-100, 100))
            else:
                key = random.choice(safe_keys)
                kbd.press(key)
                time.sleep(0.05)
                kbd.release_all()
            time.sleep(0.1)
        jiggler_running = False
        print("🌐 Web: Mouse + Klavye bitti")
    return JSONResponse(request, {"status": "ok"})

@server.route("/jiggle/stop", POST)
def api_stop(request: Request):
    global jiggler_running
    jiggler_running = False
    print("⏹️ Jiggler durduruldu")
    return JSONResponse(request, {"status": "stopped"})

# Ana döngü
print("🔍 Pin kontrolü başladı")
server.start('192.168.4.1', 80)

while True:
    server.poll()

    if not gp5.value and not jiggler_running:
        print("🔵 GP5 tetiklendi -> Mouse")
        mouse_jiggle()
    elif not gp6.value and not jiggler_running:
        print("🟢 GP6 tetiklendi -> Mouse + Klavye")
        combined_jiggle()

    time.sleep(0.1)
