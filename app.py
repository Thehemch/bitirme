from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'gizli_anahtar'  # Flash mesaj ve session için

# MySQL bağlantısı
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bitirme"
    )
    print("✅ MySQL bağlantısı başarılı!")
except mysql.connector.Error as err:
    print("❌ MySQL bağlantı hatası:", err)

# 📌 Anasayfa — sadece oturum açan görebilir
@app.route('/')
def index():
    if "kullanici_adi" not in session:
        return redirect(url_for("giris"))
    return render_template('index.html')

# 📌 Giriş Sayfası
@app.route("/giris", methods=["GET", "POST"])
def giris():
    if request.method == "POST":
        kullanici_adi = request.form["kullanici_adi"]
        sifre = request.form["sifre"]

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bitirme"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kullanici WHERE kullanici_adi = %s AND sifre = %s", (kullanici_adi, sifre))
        kullanici = cursor.fetchone()
        conn.close()

        if kullanici:
            session["kullanici_adi"] = kullanici_adi
            return redirect(url_for("index"))
        else:
            flash("Kullanıcı adı veya şifre hatalı!")
            return redirect(url_for("giris"))

    return render_template("giris.html")

# 📌 Kayıt Sayfası
@app.route("/kayit", methods=["GET", "POST"])
def kayit():
    if request.method == "POST":
        kullanici_adi = request.form["kullanici_adi"]
        sifre = request.form["sifre"]

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bitirme"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO kullanici (kullanici_adi, sifre) VALUES (%s, %s)", (kullanici_adi, sifre))
        conn.commit()
        conn.close()

        flash("Kayıt başarılı! Giriş yapabilirsiniz.")
        return redirect(url_for("giris"))

    return render_template("kayit.html")

# 📌 Çıkış
@app.route("/cikis")
def cikis():
    session.pop("kullanici_adi", None)
    flash("Çıkış yapıldı.")
    return redirect(url_for("giris"))

# 🔧 Diğer sayfalar (giriş kontrolü yoksa doğrudan çalışır)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/zeytinyagi_dashboard')
def zeytinyagi_dashboard():
    return render_template('zeytinyagi_dashboard.html')

@app.route('/tahmin')
def tahmin():
    return render_template('tahmin.html')

@app.route("/yag_tahminleme")
def yag_tahminleme():
    return render_template("yag_tahminleme.html")

@app.route("/akilli_harita")
def akilli_harita():
    return render_template("akilli_harita.html")

@app.route("/rapor")
def rapor():
    return render_template("rapor.html")

# 📊 Stored procedure ile dashboard verileri
@app.route('/get_dashboard_data', methods=['POST'])
def get_dashboard_data():
    data = request.get_json()
    procedure_name = data.get('procedure')

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bitirme"
        )
        cursor = conn.cursor()
        cursor.callproc(procedure_name)
        result_list = []
        for result in cursor.stored_results():
            result_list = result.fetchall()
        return jsonify(result_list)
    except Exception as e:
        import traceback
        traceback.print_exc()
        app.logger.error("Hata oluştu: %s", e)
        return jsonify([])
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

@app.route('/get_info_data', methods=['POST'])
def get_info_data():
    data = request.get_json()
    procedure_name = data.get('procedure')

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bitirme"
        )
        cursor = conn.cursor()
        cursor.callproc(procedure_name)
        result_list = []
        for result in cursor.stored_results():
            result_list = result.fetchall()
        if result_list and len(result_list[0]) > 0:
            return jsonify(result_list[0])
        else:
            return jsonify(None)
    except Exception as e:
        import traceback
        traceback.print_exc()
        app.logger.error("Hata oluştu: %s", e)
        return jsonify(None)
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

# Uygulama başlat
if __name__ == '__main__':
    app.run(debug=True)
