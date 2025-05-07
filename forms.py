from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SelectField,HiddenField
from wtforms.validators import DataRequired, Optional
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


# Hizmet Alanı Formu
class HizmetForm(FlaskForm):
    ad = StringField('Hizmet Adı', validators=[DataRequired()])
    ikon = StringField('Bootstrap İkon Kodu', validators=[DataRequired()])
    aciklama = TextAreaField('Açıklama', validators=[Optional()])

# Galeri (Anasayfa veya Genel)
class GaleriForm(FlaskForm):
    baslik = StringField("Başlık", validators=[DataRequired()])
    gorsel = FileField("Görsel", validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], "Sadece görsel dosyaları!")
    ])

class GenelGaleriForm(FlaskForm):
    gorsel = FileField("Görsel", validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], "Sadece görsel dosyaları!")
    ])

# Proje
class ProjeForm(FlaskForm):
    baslik = StringField('Proje Başlığı', validators=[Optional()])
    gorsel_yolu = FileField('Görsel Yükle', validators=[DataRequired()])

# Proje Tanıtım Videosu
class ProjeVideoForm(FlaskForm):
    tanitim_baslik = StringField('Tanıtım Başlığı', validators=[Optional()])
    tanitim_aciklama = TextAreaField('Tanıtım Metni', validators=[Optional()])
    video_url = StringField('Video URL', validators=[Optional()])

# Ürün Bilgileri
class UrunForm(FlaskForm):
    slug = StringField('Slug (URL Adresi)', validators=[DataRequired()])
    baslik = StringField('Ürün Başlığı', validators=[DataRequired()])
    aciklama = TextAreaField('Ürün Açıklaması', validators=[Optional()])
    avantajlar = TextAreaField('Avantajlar (her satır ayrı madde)', validators=[Optional()])
    kullanim_alanlari = TextAreaField('Kullanım Alanları (her satır ayrı madde)', validators=[Optional()])
    gorsel = FileField('Kapak Görseli', validators=[Optional()])

# Ürün Galeri
class UrunGaleriForm(FlaskForm):
    urun_id = HiddenField('Ürün')   # Burası değişiyor!
    gorsel = FileField('Galeri Görseli', validators=[DataRequired()])

# Hakkımızda
class HakkimizdaForm(FlaskForm):
    metin = TextAreaField('Hakkımızda Metni', validators=[DataRequired()])

# Sık Sorulan Sorular
class SSSForm(FlaskForm):
    soru = StringField('Soru', validators=[DataRequired()])
    cevap = TextAreaField('Cevap', validators=[DataRequired()])


class ProjeForm(FlaskForm):
    baslik = StringField("Proje Başlığı", validators=[DataRequired()])
    gorsel = FileField("Proje Görseli", validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], "Sadece resim dosyaları yükleyebilirsiniz.")])


class SSSForm(FlaskForm):
    soru = StringField('Soru', validators=[DataRequired()])
    cevap = TextAreaField('Cevap', validators=[DataRequired()])

