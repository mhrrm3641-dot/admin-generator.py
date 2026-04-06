from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
from datetime import datetime

app = FastAPI(title="Sohbet Aktivasyon API")

# Veritabanı yolu (Admin paneliyle aynı yeri görmeli)
db_path = os.path.join(os.path.dirname(__file__), '../data/vouchers.db')

# Kullanıcı Kayıt Modeli
class RegisterRequest(BaseModel):
    username: str
    password: str
    activation_code: str

@app.get("/")
def read_root():
    return {"status": "Sistem Aktif", "message": "Sohbet API Hazır"}

@app.post("/register")
def register_user(req: RegisterRequest):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Kodun geçerliliğini kontrol et
    cursor.execute("SELECT id, is_used FROM vouchers WHERE code = ?", (req.activation_code,))
    voucher = cursor.fetchone()

    if not voucher:
        conn.close()
        raise HTTPException(status_code=400, detail="Geçersiz aktivasyon kodu!")
    
    if voucher[1] == 1:
        conn.close()
        raise HTTPException(status_code=400, detail="Bu kod daha önce kullanılmış!")

    # 2. Kullanıcıyı oluştur (Burada gerçek projede şifre hash'lenmelidir)
    try:
        # Önce users tablosu yoksa oluşturalım (Hata almamak için)
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
        
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (req.username, req.password))
        
        # 3. Kodu "Kullanıldı" olarak işaretle
        cursor.execute("""
            UPDATE vouchers 
            SET is_used = 1, used_at = ? 
            WHERE code = ?
        """, (datetime.now(), req.activation_code))
        
        conn.commit()
        return {"message": "Kayıt başarılı! Sohbete giriş yapabilirsiniz."}
        
    except sqlite3.IntegrityError:
        return {"error": "Bu kullanıcı adı zaten alınmış."}
    finally:
        conn.close()

# Sunucuyu çalıştırmak için terminale: uvicorn main:app --reload
