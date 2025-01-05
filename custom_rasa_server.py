from rasa.core.run import serve_application
from sanic_cors import CORS

if __name__ == "__main__":
    # Jalankan server aplikasi Rasa
    app = serve_application()  # Fungsi bawaan Rasa untuk menjalankan server
    
    # Pastikan aplikasi bukan None
    if app is not None:
        CORS(app)  # Tambahkan middleware CORS
        app.run(host="0.0.0.0", port=5005)
    else:
        print("Gagal memulai server Rasa. Periksa konfigurasi.")
