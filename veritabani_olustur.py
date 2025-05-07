from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import os

print("→ Veritabanı oluşturuluyor...")

# Instance klasörü yoksa oluştur
os.makedirs("instance", exist_ok=True)

with app.app_context():
    db.create_all()
    print("✅ Tablolar oluşturuldu.")
    admin = User(username="admin", password_hash=generate_password_hash("12345"))
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin kullanıcısı eklendi.")
