from flask import Flask, render_template, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL bağlantısı
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # şifre varsa yaz
        database="bitirme"
    )
    print("✅ MySQL bağlantısı başarılı!")
except mysql.connector.Error as err:
    print("❌ MySQL bağlantı hatası:", err)


# Anasayfa
@app.route('/')
def index():
    return render_template('index.html')

# Dashboard sayfası
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/zeytinyagi_dashboard')
def zeytinyagi_dashboard():
    return render_template('zeytinyagi_dashboard.html')

@app.route('/tahmin')
def tahmin():
    return render_template('tahmin.html')

@app.route("/tahmin")
def zeytin_tahmin():
    return render_template("tahmin.html")

@app.route("/yag_tahminleme")
def yag_tahminleme():
    return render_template("yag_tahminleme.html")

@app.route("/akilli_harita")
def akilli_harita():
    return render_template("akilli_harita.html")

@app.route("/rapor")
def rapor():
    return render_template("rapor.html")


# Dashboard grafik verilerini çekmek için API
@app.route('/get_dashboard_data', methods=['POST'])
def get_dashboard_data():
    data = request.get_json()
    procedure_name = data.get('procedure')

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bitirme"
        )
        cursor = db.cursor()
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
            db.close()
        except:
            pass


# Info-line kutuları için verileri çekmek (örneğin artış oranları)
@app.route('/get_info_data', methods=['POST'])
def get_info_data():
    data = request.get_json()
    procedure_name = data.get('procedure')

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bitirme"
        )
        cursor = db.cursor()
        cursor.callproc(procedure_name)
        result_list = []
        for result in cursor.stored_results():
            result_list = result.fetchall()
        # Tek değer döndüreceğiz
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
            db.close()
        except:
            pass


# Uygulama başlatma
if __name__ == '__main__':
    app.run(debug=True)