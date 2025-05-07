from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

# Hizmet Alanları (Anasayfa)
class Hizmet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    ikon = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.Text)

# Anasayfa Galerisi
class GaleriGorsel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100))
    gorsel_yolu = db.Column(db.String(200), nullable=False)

# Projeler Sayfası
class Proje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100))
    gorsel_yolu = db.Column(db.String(200), nullable=False)

class ProjeVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tanitim_baslik = db.Column(db.String(100))
    tanitim_aciklama = db.Column(db.Text)
    video_url = db.Column(db.String(300))

# Genel Galeri
class Galeri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gorsel_yolu = db.Column(db.String(200), nullable=False)

# Ürün Detay Sayfaları
class Urun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    baslik = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.Text)
    avantajlar = db.Column(db.Text)  # \n ile ayrılabilir
    kullanim_alanlari = db.Column(db.Text)  # \n ile ayrılabilir
    gorsel = db.Column(db.String(200))

class UrunGaleri(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    urun_id = db.Column(db.Integer, db.ForeignKey('urun.id'), nullable=False)
    gorsel = db.Column(db.String(200), nullable=False)
    urun = db.relationship('Urun', backref='galeriler')

# Hakkımızda Sayfası
class Hakkimizda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metin = db.Column(db.Text)

# Sık Sorulan Sorular
class SSS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    soru = db.Column(db.String(200), nullable=False)
    cevap = db.Column(db.Text, nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)





