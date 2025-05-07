from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Hizmet, GaleriGorsel, Proje, SSS, Galeri,Urun,UrunGaleri
from forms import HizmetForm, GaleriForm, GenelGaleriForm, ProjeForm, SSSForm,UrunForm,UrunGaleriForm

import os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# --- Giriş Formu ---
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Kullanıcı Adı", validators=[DataRequired()])
    password = PasswordField("Şifre", validators=[DataRequired()])

# --- Giriş Sayfası ---
@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("Başarıyla giriş yaptınız.", "success")
            return redirect(url_for("admin.panel"))
        else:
            flash("Kullanıcı adı veya şifre yanlış!", "danger")
    return render_template("admin/login.html", form=form)

# --- Çıkış ---
@admin_bp.route("/logout")
@login_required
def admin_logout():
    logout_user()
    flash("Çıkış yapıldı.", "info")
    return redirect(url_for("admin.admin_login"))

# --- Panel ---
@admin_bp.route("/")
@login_required
def panel():
    return render_template("admin/panel.html")

# --- Hizmetler ---
@admin_bp.route("/hizmetler")
@login_required
def hizmetler():
    hizmetler = Hizmet.query.all()
    return render_template("admin/hizmetler.html", hizmetler=hizmetler)

@admin_bp.route("/hizmetler/ekle", methods=["GET", "POST"])
@login_required
def hizmet_ekle():
    form = HizmetForm()
    if form.validate_on_submit():
        yeni = Hizmet(ad=form.ad.data, ikon=form.ikon.data, aciklama=form.aciklama.data)
        db.session.add(yeni)
        db.session.commit()
        flash("Hizmet eklendi.", "success")
        return redirect(url_for("admin.hizmetler"))
    return render_template("admin/hizmet_form.html", form=form, baslik="Yeni Hizmet")

@admin_bp.route("/hizmetler/sil/<int:id>")
@login_required
def hizmet_sil(id):
    hizmet = Hizmet.query.get_or_404(id)
    db.session.delete(hizmet)
    db.session.commit()
    flash("Hizmet silindi.", "danger")
    return redirect(url_for("admin.hizmetler"))

# --- Anasayfa Galerisi (GaleriGorsel) ---
@admin_bp.route("/galeri")
@login_required
def galeri():
    gorseller = GaleriGorsel.query.all()
    return render_template("admin/galeri.html", gorseller=gorseller)

@admin_bp.route("/galeri/ekle", methods=["GET", "POST"])
@login_required
def galeri_ekle():
    form = GaleriForm()
    if form.validate_on_submit():
        dosya = form.gorsel.data
        if dosya:
            filename = secure_filename(dosya.filename)
            yol = os.path.join(current_app.root_path, "static", "uploads", filename)
            dosya.save(yol)
            gorsel_yolu = f"uploads/{filename}"
            yeni = GaleriGorsel(baslik=form.baslik.data, gorsel_yolu=gorsel_yolu)
            db.session.add(yeni)
            db.session.commit()
            flash("Görsel eklendi.", "success")
            return redirect(url_for("admin.galeri"))
    return render_template("admin/galeri_form.html", form=form, baslik="Yeni Görsel Ekle")

@admin_bp.route("/galeri/sil/<int:id>")
@login_required
def galeri_sil(id):
    gorsel = GaleriGorsel.query.get_or_404(id)
    try:
        gorsel_path = os.path.join(current_app.root_path, "static", gorsel.gorsel_yolu)
        if os.path.exists(gorsel_path):
            os.remove(gorsel_path)
    except Exception as e:
        flash(f"Görsel silinemedi: {e}", "warning")
    db.session.delete(gorsel)
    db.session.commit()
    flash("Görsel silindi.", "danger")
    return redirect(url_for("admin.galeri"))

@admin_bp.route("/galeri/guncelle/<int:id>", methods=["GET", "POST"])
@login_required
def galeri_guncelle(id):
    gorsel = GaleriGorsel.query.get_or_404(id)
    form = GaleriForm(obj=gorsel)

    if form.validate_on_submit():
        gorsel.baslik = form.baslik.data

        if form.gorsel.data:
            dosya = form.gorsel.data
            filename = secure_filename(dosya.filename)
            yol = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            dosya.save(yol)
            gorsel.gorsel_yolu = f"uploads/{filename}"

        db.session.commit()
        flash("Galeri görseli güncellendi.", "success")
        return redirect(url_for("admin.galeri"))

    return render_template("admin/galeri_form.html", form=form, baslik="Galeri Görseli Güncelle")


# --- Projeler ---
@admin_bp.route("/projeler")
@login_required
def projeler():
    projeler = Proje.query.all()
    return render_template("admin/projeler.html", projeler=projeler)

@admin_bp.route("/projeler/ekle", methods=["GET", "POST"])
@login_required
def proje_ekle():
    form = ProjeForm()
    if form.validate_on_submit():
        dosya = form.gorsel.data
        if dosya:
            filename = secure_filename(dosya.filename)
            yol = os.path.join(current_app.root_path, "static", "uploads", filename)
            dosya.save(yol)
            gorsel_yolu = f"uploads/{filename}"
            yeni = Proje(baslik=form.baslik.data, gorsel_yolu=gorsel_yolu)
            db.session.add(yeni)
            db.session.commit()
            flash("Proje eklendi.", "success")
            return redirect(url_for("admin.projeler"))
    return render_template("admin/proje_form.html", form=form, baslik="Yeni Proje Ekle")

@admin_bp.route("/projeler/sil/<int:id>")
@login_required
def proje_sil(id):
    proje = Proje.query.get_or_404(id)
    try:
        proje_path = os.path.join(current_app.root_path, "static", proje.gorsel_yolu)
        if os.path.exists(proje_path):
            os.remove(proje_path)
    except Exception as e:
        flash(f"Proje görseli silinemedi: {e}", "warning")
    db.session.delete(proje)
    db.session.commit()
    flash("Proje silindi.", "danger")
    return redirect(url_for("admin.projeler"))

# --- GENEL GALERİ (Galeri) ---
@admin_bp.route("/galeri-genel")
@login_required
def galeri_genel():
    galeriler = Galeri.query.all()
    return render_template("admin/galeri_genel.html", galeriler=galeriler)

@admin_bp.route("/galeri-genel/ekle", methods=["GET", "POST"])
@login_required
def galeri_genel_ekle():
    form = GenelGaleriForm()
    if form.validate_on_submit():
        dosya = form.gorsel.data
        if dosya:
            filename = secure_filename(dosya.filename)
            yol = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            dosya.save(yol)
            gorsel_yolu = f"uploads/{filename}"
            yeni = Galeri(gorsel_yolu=gorsel_yolu)
            db.session.add(yeni)
            db.session.commit()
            flash("Genel galeriye görsel eklendi.", "success")
            return redirect(url_for("admin.galeri_genel"))
    return render_template("admin/galeri_genel_form.html", form=form, baslik="Yeni Genel Galeri Görseli")

@admin_bp.route("/galeri-genel/sil/<int:id>")
@login_required
def galeri_genel_sil(id):
    gorsel = Galeri.query.get_or_404(id)
    try:
        gorsel_path = os.path.join(current_app.root_path, "static", gorsel.gorsel_yolu)
        if os.path.exists(gorsel_path):
            os.remove(gorsel_path)
    except Exception as e:
        flash(f"Dosya silinirken hata oluştu: {e}", "warning")
    db.session.delete(gorsel)
    db.session.commit()
    flash("Galeri görseli silindi.", "danger")
    return redirect(url_for("admin.galeri_genel"))

# --- SSS ---
@admin_bp.route("/sss")
@login_required
def sss_listesi():
    sorular = SSS.query.all()
    return render_template("admin/sss.html", sorular=sorular)


@admin_bp.route("/sss/ekle", methods=["GET", "POST"])
@login_required
def sss_ekle():
    form = SSSForm()
    if form.validate_on_submit():
        yeni = SSS(
            soru=form.soru.data,
            cevap=form.cevap.data
        )
        db.session.add(yeni)
        db.session.commit()
        flash("Soru başarıyla eklendi.", "success")
        return redirect(url_for("admin.sss_listesi"))
    return render_template("admin/sss_form.html", form=form, baslik="Yeni Soru Ekle")

@admin_bp.route("/sss/sil/<int:id>")
@login_required
def sss_sil(id):
    soru = SSS.query.get_or_404(id)
    db.session.delete(soru)
    db.session.commit()
    flash("Soru silindi.", "danger")
    return redirect(url_for("admin.sss_listesi"))

@admin_bp.route("/sss/guncelle/<int:id>", methods=["GET", "POST"])
@login_required
def sss_guncelle(id):
    soru = SSS.query.get_or_404(id)
    form = SSSForm(obj=soru)
    if form.validate_on_submit():
        soru.soru = form.soru.data
        soru.cevap = form.cevap.data
        db.session.commit()
        flash("Soru güncellendi.", "success")
        return redirect(url_for("admin.sss_listesi"))
    return render_template("admin/sss_form.html", form=form, baslik="SSS Güncelle")



# --- ÜRÜNLER --- (admin için)
@admin_bp.route("/urunler")
@login_required
def urunler():
    urunler = Urun.query.all()
    return render_template("admin/urunler.html", urunler=urunler)

@admin_bp.route("/urunler/ekle", methods=["GET", "POST"])
@login_required
def urun_ekle():
    form = UrunForm()
    if form.validate_on_submit():
        dosya = form.gorsel.data
        gorsel_yolu = None
        if dosya:
            filename = secure_filename(dosya.filename)
            yol = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            dosya.save(yol)
            gorsel_yolu = f"uploads/{filename}"

        yeni = Urun(
            slug=form.slug.data,
            baslik=form.baslik.data,
            aciklama=form.aciklama.data,
            avantajlar=form.avantajlar.data,
            kullanim_alanlari=form.kullanim_alanlari.data,
            gorsel=gorsel_yolu
        )
        db.session.add(yeni)
        db.session.commit()
        flash("Ürün eklendi.", "success")
        return redirect(url_for("admin.urunler"))
    return render_template("admin/urun_form.html", form=form, baslik="Yeni Ürün Ekle")

@admin_bp.route("/urunler/sil/<int:id>")
@login_required
def urun_sil(id):
    urun = Urun.query.get_or_404(id)
    try:
        # görsel dosyasını da sil
        gorsel_path = os.path.join(current_app.root_path, "static", urun.gorsel)
        if os.path.exists(gorsel_path):
            os.remove(gorsel_path)
    except Exception as e:
        flash(f"Görsel silinemedi: {e}", "warning")

    db.session.delete(urun)
    db.session.commit()
    flash("Ürün silindi.", "danger")
    return redirect(url_for("admin.urunler"))

@admin_bp.route("/urunler/guncelle/<int:id>", methods=["GET", "POST"])
@login_required
def urun_guncelle(id):
    urun = Urun.query.get_or_404(id)
    form = UrunForm(obj=urun)

    if form.validate_on_submit():
        urun.slug = form.slug.data
        urun.baslik = form.baslik.data
        urun.aciklama = form.aciklama.data
        urun.avantajlar = form.avantajlar.data
        urun.kullanim_alanlari = form.kullanim_alanlari.data

        if form.gorsel.data:
            dosya = form.gorsel.data
            filename = secure_filename(dosya.filename)
            yol = os.path.join(current_app.root_path, "static", "uploads", filename)
            dosya.save(yol)
            urun.gorsel = f"uploads/{filename}"

        db.session.commit()
        flash("Ürün başarıyla güncellendi.", "success")
        return redirect(url_for("admin.urunler"))

    return render_template("admin/urun_form.html", form=form, baslik="Ürün Güncelle")




@admin_bp.route("/urunler/<int:urun_id>/galeri", methods=["GET", "POST"])
@login_required
def urun_galeri(urun_id):
    urun = Urun.query.get_or_404(urun_id)
    form = UrunGaleriForm()
    form.urun_id.data = urun.id  # gizli input gibi

    if form.validate_on_submit():
        dosya = form.gorsel.data
        if dosya:
            filename = secure_filename(dosya.filename)
            yol = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            dosya.save(yol)
            gorsel_yolu = f"uploads/{filename}"
            yeni = UrunGaleri(urun_id=urun.id, gorsel=gorsel_yolu)
            db.session.add(yeni)
            db.session.commit()
            flash("Galeri görseli eklendi.", "success")
            return redirect(url_for("admin.urun_galeri", urun_id=urun.id))

    galeriler = UrunGaleri.query.filter_by(urun_id=urun.id).all()
    return render_template("admin/urun_galeri.html", urun=urun, galeriler=galeriler, form=form)


# --- ÜRÜN GALERİ (UrunGaleri) ---



# Ürün Galeri Fotoğrafı Ekle
@admin_bp.route("/urun-galeri/ekle/<int:urun_id>", methods=["GET", "POST"])
@login_required
def urun_galeri_ekle(urun_id):
    form = UrunGaleriForm()
    urun = Urun.query.get_or_404(urun_id)

    if form.validate_on_submit():
        dosya = form.gorsel.data
        if dosya:
            filename = secure_filename(dosya.filename)
            yol = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            dosya.save(yol)
            gorsel_yolu = f"uploads/{filename}"

            yeni_gorsel = UrunGaleri(urun_id=urun.id, gorsel=gorsel_yolu)
            db.session.add(yeni_gorsel)
            db.session.commit()
            flash("Galeri fotoğrafı başarıyla eklendi.", "success")
            return redirect(url_for('admin.urun_galeri', urun_id=urun.id))

    return render_template("admin/urun_galeri_ekle.html", form=form, urun=urun)

# Ürün Galeri Fotoğrafı Sil
@admin_bp.route("/urun-galeri/sil/<int:id>")
@login_required
def urun_galeri_sil(id):
    gorsel = UrunGaleri.query.get_or_404(id)
    urun_id = gorsel.urun_id

    try:
        gorsel_path = os.path.join(current_app.root_path, "static", gorsel.gorsel)
        if os.path.exists(gorsel_path):
            os.remove(gorsel_path)
    except Exception as e:
        flash(f"Fotoğraf silinirken hata oluştu: {e}", "warning")

    db.session.delete(gorsel)
    db.session.commit()
    flash("Fotoğraf silindi.", "danger")
    return redirect(url_for('admin.urun_galeri', urun_id=urun_id))