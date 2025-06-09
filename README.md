"# uas-ml" 

## How to run
1. Run `pip install -r requirements.txt`
2. Run `uvicorn app.main:app`

## Instruksi Frontend

Pastikan semua integrasi frontend dilakukan dengan pendekatan modern berbasis fetch API, bukan form HTML klasik.

1. Semua form HTML seperti login, register, preferences, dll, harus dikendalikan menggunakan `fetch()` di JavaScript, bukan dengan form submission `<form action="..." method="POST">`.

2. Data yang dikirim ke backend harus dalam format `application/json`. Jangan gunakan `application/x-www-form-urlencoded`.

Contoh implementasi:
```javascript
fetch("/auth/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ email, password })
})