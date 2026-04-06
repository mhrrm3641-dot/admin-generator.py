import sqlite3
import secrets
import string
import os
from datetime import datetime

# Veritabanı yolu ayarı
db_path = os.path.join(os.path.dirname(__file__), '../data/vouchers.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

def init_db():
    """Veritabanını ve tabloyu hazırlar."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vouchers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            is_used BOOLEAN DEFAULT 0,
            assigned_user_id TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            used_at DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def generate_codes(count=50):
    """Yeni ve güvenli aktivasyon kodları üretir."""
    # Okunabilirliği zorlaştıran karakterleri (0, O, I, L) çıkardık
    alphabet = "".join(c for c in string.ascii_uppercase + string.digits if c not in "0OIL")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    new_vouchers = []
    for _ in range(count):
        # 12 haneli rastgele kod oluştur ve formatla (ABCD-EFGH-JKLM)
        raw_code = ''.join(secrets.choice(alphabet) for _ in range(12))
        formatted_code = '-'.join([raw_code[i:i+4] for i in range(0, 12, 4)])
        
        try:
            cursor.execute("INSERT INTO vouchers (code) VALUES (?)", (formatted_code,))
            new_vouchers.append(formatted_code)
        except sqlite3.IntegrityError:
            continue
            
    conn.commit()
    conn.close()
    print(f"✅ {len(new_vouchers)} adet yeni kod başarıyla üretildi.")
    return new_vouchers

def export_for_sale():
    """Henüz kullanılmamış kodları satış dosyasına döker."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM vouchers WHERE is_used = 0")
    codes = cursor.fetchall()
    
    filename = "satis_bekleyen_kodlar.txt"
    with open(filename, "w") as f:
        for c in codes:
            f.write(f"{c[0]}\n")
    
    conn.close()
    print(f"📂 {len(codes)} adet kod '{filename}' dosyasına yazıldı. Bunları satış platformuna yükleyebilirsin.")

if __name__ == "__main__":
    init_db()
    # Önce kod üret (İstediğin sayıyı buraya yazabilirsin)
    generate_codes(20)
    # Sonra hepsini dışa aktar
    export_for_sale()
