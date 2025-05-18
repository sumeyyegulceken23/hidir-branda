from flask import Flask, render_template, redirect, url_for, flash, request, Response
from flask_login import LoginManager
from models import db, User, Hizmet, GaleriGorsel, Galeri, Proje, SSS,Urun
from admin_routes import admin_bp
import os

app = Flask(__name__)

# --- DOSYA ve VERİTABANI AYARLARI ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'gizli_anahtar'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'site.db')
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')   # 🔥 DOĞRU YOL BURASI
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB maksimum yükleme limiti
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Eğer uploads klasörü yoksa otomatik oluştur
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# --- VERİTABANI BAĞLANTISI ---
db.init_app(app)

# --- GİRİŞ YÖNETİMİ ---
login_manager = LoginManager()
login_manager.login_view = 'admin.admin_login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ADMIN ROUTE KAYDI ---
app.register_blueprint(admin_bp)

# --- ANA SAYFA ROUTELARI ---
@app.route("/")
def index():
    hizmetler = Hizmet.query.all()
    galeri_gorseller = GaleriGorsel.query.all()
    return render_template("index.html", hizmetler=hizmetler, galeri_gorseller=galeri_gorseller)

@app.route("/hakkimizda")
def hakkimizda():
    return render_template("hakkimizda.html")

@app.route("/projeler")
def projeler():
    projeler = Proje.query.all()
    return render_template("projeler.html", projeler=projeler)

@app.route("/galeri")
def galeri():
    galeriler = Galeri.query.all()
    return render_template("galeri.html", galeriler=galeriler)

@app.route("/sss")
def sss():
    sorular = SSS.query.all()
    return render_template("sss.html", sorular=sorular)

@app.route("/iletisim")
def iletisim():
    return render_template("iletisim.html")

# --- ÜRÜN DETAY SAYFALARI ---
@app.route("/urunler/tente")
def urun_tente():
    return render_template("urun_tente.html")

@app.route("/urunler/semsiye")
def urun_semsiye():
    return render_template("urun_semsiye.html")

@app.route("/urunler/kisbahcesi")
def urun_kisbahcesi():
    return render_template("urun_kisbahcesi.html")

@app.route("/urunler/pergola")
def urun_pergola():
    return render_template("urun_pergola.html")

@app.route("/urunler/arac")
def urun_arac():
    return render_template("urun_arac.html")

from models import Urun  # varsa üstte zaten, yoksa ekle

@app.route("/urunler/<slug>")
def urun_detay(slug):
    urun = Urun.query.filter_by(slug=slug).first_or_404()
    return render_template("urun_detay.html", urun=urun)

from flask import Response
from models import Urun

@app.route("/sitemap.xml")
def sitemap():
    urunler = Urun.query.all()
    urls = [
        {"loc": url_for("index", _external=True)},
        {"loc": url_for("hakkimizda", _external=True)},
        {"loc": url_for("projeler", _external=True)},
        {"loc": url_for("galeri", _external=True)},
        {"loc": url_for("iletisim", _external=True)},
        {"loc": url_for("sss", _external=True)},
    ]

    for urun in urunler:
        urls.append({
            "loc": url_for("urun_detay", slug=urun.slug, _external=True)
        })

    xml = render_template("sitemap_template.xml", urls=urls)
    return Response(xml, mimetype="application/xml")




@app.context_processor
def urunleri_getir():
    urunler = Urun.query.order_by(Urun.baslik).all()
    return dict(urunler=urunler)


# --- UYGULAMA BAŞLAT ---
if __name__ == "__main__":
    app.run(debug=True)
