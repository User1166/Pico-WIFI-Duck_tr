import wifi
import socketpool
import time
from adafruit_httpserver import Server, Request, JSONResponse, POST, Response
from duck import exe

# Wi-Fi AP (Access Point) ayarları
ssid = "FATİHH"
password = "12345678"

# Wi-Fi erişim noktası başlatma fonksiyonu
def start_access_point():
    try:
        print("Wi-Fi kapatılıyor...")
        wifi.radio.stop_station()  # Önce kapat
        time.sleep(2)  # Bekleme süresi ekle
        print(f"Wi-Fi erişim noktası başlatılıyor: {ssid}")
        wifi.radio.start_ap(ssid, password)
        time.sleep(1)  # IP atanmasını bekle
        print("Wi-Fi erişim noktası oluşturuldu!")
        print("IP Adresi:", wifi.radio.ipv4_address)
    except Exception as e:
        print(f"Hata: {e}. Wi-Fi erişim noktası oluşturulamadı.")

# Server ve socketpool ayarları
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

# Ana sayfa (HTML döndürme)
@server.route("/")
def base(request: Request):
    try:
        with open("index.html", "r") as file:
            html_content = file.read()
        headers = {"Content-Type": "text/html"}
        return Response(request, html_content, headers=headers)
    except Exception as e:
        print(f"Error loading index.html: {e}")
        return Response(request, "Error loading page", status=500)

# API endpoint (POST isteği işleme)
@server.route("/api", POST, append_slash=True)
def api(request: Request):
    try:
        if request.method == POST:
            req = request.json()
            payload = req["content"]
            payload = payload.splitlines()  # Her satırı ayır
            exe(payload)  # Payload'u çalıştır
            return JSONResponse(request, {"message": "Done"})
    except Exception as e:
        print(f"Error processing API request: {e}")
        return JSONResponse(request, {"error": "Failed to process request"}, status=500)

# Server'ı başlat
def start_server():
    try:
        print("Starting server on 192.168.4.1:80")
        server.serve_forever('192.168.4.1', 80)  # IP ve port
    except Exception as e:
        print(f"Error starting server: {e}")

# Ana fonksiyon
def main():
    # Wi-Fi erişim noktasını başlat
    start_access_point()

    # Eğer IP alınmamışsa hata mesajı göster
    if wifi.radio.ipv4_address is None:
        print("⚠️  HATA: Wi-Fi erişim noktası oluşmadı!")
    
    # Server'ı başlat
    start_server()

# Başlatma
if __name__ == "__main__":
    main()
