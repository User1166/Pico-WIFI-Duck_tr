# Pico WiFi Duck - Raspberry Pi Pico W

![Raspberry Pi Pico W](https://cdn.mos.cms.futurecdn.net/Xmn9ztSwKavDfzgX6x3g4g.jpg)

## Overview

Pico WiFi Duck is a project that enables the emulation of a USB Rubber Ducky over Wi-Fi using the Raspberry Pi Pico W. This functionality allows for remote control and automation of target systems, making it a versatile tool for penetration testing and security assessments. This project is inspired by the [WIFI DUCK](https://github.com/spacehuhntech/wifiduck) project by [spacehuhn](https://github.com/SpacehuhnTech).

## Features

- Emulates USB Rubber Ducky functionality over Wi-Fi.
- Remote scripting and automation capabilities.
- Requires only one Microcontroller.
- Based on the [pico-ducky](https://github.com/dbisu/pico-ducky) project.
- Cost-effective, approximately $6 (40dt).

## Getting Started

### Prerequisites

- Raspberry Pi Pico W.
- Micro-USB Cable.
- Basic Knowledge.

### Installation

1. **Install CircuitPython:**

   -Download .uf2 file from this repo
   - Plug the device into a USB port while holding the boot button. It will show up as a removable media device named RPI-RP2.
   - Copy the downloaded (".uf2") file to the root of the Pico (RPI-RP2). The device will reboot and after a second or so, it will reconnect as CIRCUITPY.

2. **Install Pico Wifi Duck Files on the Pico:**
    -Download this repo as zip and copy the lib file to the root folder of your pico
   - While plugging in your Pico, copy and paste the files that you unzip onto the "CIRCUITPY" drive.
   

### Usage

1. Connect your Raspberry Pi Pico W to the target system using a good-quality USB cable.

2. Connect to the WiFi network created by the Pico; it's called **"Pico-ducky"**, and its password is **"12345678"**.
3. You can change the name and the password of the wifi duck by changing code.py file

   ![WIFI CONNECTION](https://gcdnb.pbrd.co/images/Nm86ZhwCuXth.jpg?o=1)

4. Open your browser and navigate to [192.168.4.1](http://192.168.4.1).

   ![Webpage](https://gcdnb.pbrd.co/images/Qrj5szwW56B3.jpg?o=1)

5. Write your script in the textarea and click on "RUN" .

### Note
THİS İS NOT ORİGİNAL PİCO WIFI DUCK, ONLY TURKİSH LAYOUT AND CİRCUİTPY 9.2.3 VERSİON OF THE CODE 
