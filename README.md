# 🦆 Pico WiFi Duck

A powerful WiFi-controlled BadUSB tool built on **Raspberry Pi Pico W** with CircuitPython.  
It combines a **Ducky Script interpreter**, **jiggler**, **system information stealer**, **FTP file transfer**, and a **remote file explorer** — all accessible through a sleek web interface.

![Pico W](https://img.shields.io/badge/Raspberry%20Pi-Pico%20W-green)
![CircuitPython](https://img.shields.io/badge/CircuitPython-9.2.3-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## ✨ Features

- 🌐 **Web-Based Control Panel** – Access all functions via `http://192.168.4.1` after connecting to the Pico's WiFi AP.
- 🦆 **Ducky Script Interpreter** – Execute Rubber Ducky payloads with Turkish keyboard layout support.
- 🎮 **Jiggler** – Trigger random mouse and/or keyboard movements via web buttons or hardware pins (GP5/GP6).
- 📊 **System Info Stealer** – Gather WiFi passwords, OS details, CPU, RAM, GPU, IP/MAC, ARP table, and user accounts.
- 📁 **Remote File Explorer** – Browse directories on the target PC and upload selected files to an FTP server.
- 📸 **Screenshot Capture** – Take screenshots and send them directly to FTP.
- 👤 **Account Management** – Create new user accounts, grant admin privileges, and enable RDP.
- ⚡ **Quick Commands** – Clipboard injection, message boxes, volume control, monitor off, and website launcher.
- 🔌 **Hardware Trigger** – GP5 (Mouse Jiggler) and GP6 (Mouse+Keyboard Jiggler) pins for physical activation.
- 🧩 **Modular Design** – Easy to extend with your own Ducky Scripts or PowerShell commands.

---

## 📦 Hardware Requirements

- **Raspberry Pi Pico W** (WiFi support required)
- Micro USB cable (power + data)
- Optional: Jumper wires / buttons for GP5/GP6 triggers

---

## 🚀 Installation

### 1. Install CircuitPython (At project files)
- Hold the **BOOTSEL** button while connecting the Pico to your computer.
- Drag the `.uf2` file onto the **RPI-RP2** drive.

### 2. Copy Required Libraries
Place the following libraries inside the **`lib/`** folder on the **CIRCUITPY** drive: (also in project files)
- `adafruit_hid`
- `adafruit_httpserver`
- `keyboard_layout_win_tr.mpy` (Turkish keyboard layout)
- `keycode_win_tr.mpy` (Turkish keycodes)

> 📁 You can find these libraries in the [Adafruit CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle).

### 3. Upload Project Files
Copy these files to the root of the **CIRCUITPY** drive:
- `code.py`
- `boot.py`
- `duck.py`
- `index.html`

### 4. Connect & Access
- The Pico W will create a WiFi access point:
  - **SSID:** `FATİHH`
  - **Password:** `12345678`
- Connect your phone/PC to this network.
- Open a browser and go to **`http://192.168.4.1`**
-You can change it from code.py
---

## 🕹️ Usage

### Web Interface
The UI is divided into three panels:

| Panel | Description |
|-------|-------------|
| 🦆 **Ducky Script** | Write or load a payload and press **RUN** to execute. |
| 🎮 **Jiggler & Quick Commands** | Activate jigglers or run stealthy commands (message box, clipboard, volume, etc.) |
| 📁 **FTP & File Explorer** | Configure FTP, browse remote PC files, upload selected items, and collect system info. |

### Hardware Triggers
| Pin | Action |
|-----|--------|
| **GP5 → GND** | Mouse jiggler runs while connected |
| **GP6 → GND** | Mouse + Keyboard jiggler runs while connected |

> 💡 Use a jumper wire or a button to easily trigger these actions.

### FTP Configuration
1. Set up an FTP server (e.g., FileZilla Server).
2. Enter the server IP, username, password, and target folder in the **FTP Settings** menu.
3. Save the configuration – it persists in your browser's local storage.

---

## 📂 File Structure
CIRCUITPY/
├── boot.py # USB drive mode control (GP2)
├── code.py # Main web server and logic
├── duck.py # Ducky Script parser & HID execution
├── index.html # Web control panel
└── lib/ # Required CircuitPython libraries

text

---

## ⚙️ Customization

### Change WiFi Credentials
Edit `code.py`:
```python
SSID = "YOUR_SSID"
PASSWORD = "YOUR_PASSWORD"
Modify Hardware Pins
In code.py, adjust:

python
gp5 = digitalio.DigitalInOut(board.GP5)   # Mouse trigger
gp6 = digitalio.DigitalInOut(board.GP6)   # Mouse+Keyboard trigger
Add New Ducky Scripts
Edit the loadScript() function in index.html to include your own payload templates.

⚠️ Disclaimer
This project is intended for educational purposes and authorized security testing only.
Misuse of this tool on systems you do not own or have explicit permission to test is illegal and strictly discouraged. The author assumes no responsibility for any unauthorized or malicious use.

🤝 Credits
Turkish keyboard layout support based on Narsty's keycode_win_tr

Inspired by the classic WiFi Duck projects and Pico-Ducky.(https://github.com/majdsassi/Pico-WIFI-Duck)



