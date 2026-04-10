import storage
import board
import digitalio
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Pin konfigürasyonu
gp1 = digitalio.DigitalInOut(board.GP1)
gp2 = digitalio.DigitalInOut(board.GP2)

# GP1'i çıkış ve LOW yap
gp1.switch_to_output(value=False)

# GP2'yi pull-up ile giriş yap
gp2.pull = digitalio.Pull.UP
gp2.switch_to_input()

# Bağlantı kontrolü (GP2 LOW ise bağlı)
if not gp2.value:
    storage.enable_usb_drive()
    for i in range(5):
        led.value = True
        time.sleep(0.5)
        led.value = False
        time.sleep(0.5)
else:
    storage.disable_usb_drive()
    led.value = True
    time.sleep(3)
    led.value = False

# Pinleri temizle
gp1.deinit()
gp2.deinit()
