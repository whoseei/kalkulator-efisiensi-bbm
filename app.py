from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', hasil=None, biaya=None, jarak=None, status="", kategori="")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/hitung', methods=['POST'])
def hitung():
    # 1. Inisialisasi variabel default agar tidak error
    jarak = 0
    hasil = 0
    biaya = 0
    status = ""
    kategori = ""
    
    # Ambil data mentah untuk dikembalikan ke form (v_awal, dll)
    v_awal = request.form.get('km_awal', '')
    v_akhir = request.form.get('km_akhir', '')
    v_liter = request.form.get('liter', '')
    v_harga = request.form.get('harga_bbm', '')

    try:
        # 2. Cek apakah ada input yang kosong sama sekali
        if not v_awal or not v_akhir or not v_liter or not v_harga:
            status = "⚠️ Harap isi semua kolom!"
            kategori = "error"
            raise ValueError("Input Kosong") # Lempar ke except

        # 3. Konversi ke angka
        awal = float(v_awal)
        akhir = float(v_akhir)
        liter = float(v_liter)
        harga = float(v_harga)

        # 4. Validasi Logika Angka
        if akhir <= awal:
            status = "❌ KM Akhir harus lebih besar dari KM Awal!"
            kategori = "error"
        elif liter <= 0:
            status = "❌ Liter bensin tidak boleh 0!"
            kategori = "error"
        else:
            # 5. Rumus perhitungan
            jarak = akhir - awal
            hasil = jarak / liter
            biaya = liter * harga
            
            # 6. Logika Level Efisiensi
            if hasil > 100:
                status = "❌ Data tidak realistis (Cek input)"
                kategori = "error"
            elif hasil < 10: # Standar boros banget
                status = "❌ Sangat Boros"
                kategori = "sangat-boros"
            elif hasil < 15:
                status = "⚠️ Boros"
                kategori = "boros"
            elif hasil < 20:
                status = "🟡 Normal"
                kategori = "normal"
            elif hasil < 30:
                status = "✅ Irit"
                kategori = "irit"
            else:
                status = "🚀 Sangat Irit (Luar Biasa!)"
                kategori = "sangat-irit"

    except ValueError:
        # Jika input bukan angka atau kosong, status sudah diatur di atas
        if not status: 
            status = "❌ Gunakan angka yang valid!"
            kategori = "error"

    # 7. SATU return untuk semua kondisi
    return render_template('home.html', 
                           jarak=jarak, 
                           hasil=round(hasil, 2), 
                           biaya=biaya,
                           status=status,
                           kategori=kategori,
                           v_awal=v_awal,
                           v_akhir=v_akhir,
                           v_liter=v_liter,
                           v_harga=v_harga)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)