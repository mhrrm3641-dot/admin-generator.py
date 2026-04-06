async function kayitOl() {
    // Formdaki verileri alalım
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const activation_code = document.getElementById('activation_code').value;
    const messageDiv = document.getElementById('message');

    // Basit bir boşluk kontrolü
    if (!username || !password || !activation_code) {
        messageDiv.innerText = "Lütfen tüm alanları doldurun!";
        messageDiv.style.color = "red";
        return;
    }

    try {
        // API'ye istek gönderiyoruz
        const response = await fetch('http://localhost:8000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
                activation_code: activation_code
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Başarılıysa kullanıcıyı bilgilendir veya yönlendir
            messageDiv.innerText = "✅ " + data.message;
            messageDiv.style.color = "green";
            // İleride buraya: window.location.href = "/chat"; eklenebilir
        } else {
            // Hata varsa (Geçersiz kod vb.)
            messageDiv.innerText = "❌ " + (data.detail || data.error);
            messageDiv.style.color = "red";
        }
    } catch (error) {
        messageDiv.innerText = "Sunucuya bağlanılamadı!";
        messageDiv.style.color = "red";
    }
}
