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
    jarak = 0
    hasil = 0
    biaya = 0
    status = ""
    kategori = ""
    
    v_awal = request.form.get('km_awal', '')
    v_akhir = request.form.get('km_akhir', '')
    v_liter = request.form.get('liter', '')
    v_harga = request.form.get('harga_bbm', '')

    try:
        if not v_awal or not v_akhir or not v_liter or not v_harga:
            status = "⚠️ Harap isi semua kolom!"
            kategori = "error"
            raise ValueError("Input Kosong")

        awal = float(v_awal)
        akhir = float(v_akhir)
        liter = float(v_liter)
        harga = float(v_harga)

        if akhir <= awal:
            status = "❌ KM Akhir harus lebih besar dari KM Awal!"
            kategori = "error"
        elif liter <= 0:
            status = "❌ Liter bensin tidak boleh 0!"
            kategori = "error"
        else:
            jarak = akhir - awal
            hasil = jarak / liter
            biaya = liter * harga

            if hasil > 100:
                status = "❌ Data tidak realistis (Cek input)"
                kategori = "error"
            elif hasil < 10:
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
        if not status: 
            status = "❌ Gunakan angka yang valid!"
            kategori = "error"

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