# 🎓 Chatbot Bimbingan Akademik Universitas Bengkulu

**Chatbot Bimbingan Akademik Universitas Bengkulu** adalah aplikasi berbasis web yang dirancang untuk membantu mahasiswa dalam mendapatkan informasi akademik secara cepat, mudah, dan interaktif.  
Melalui sistem ini, mahasiswa dapat menanyakan berbagai hal terkait peraturan akademik, skripsi, cuti kuliah, nilai, hingga tata cara administrasi kampus tanpa harus datang langsung ke bagian akademik.

Proyek ini dikembangkan sebagai langkah awal menuju **otomatisasi layanan bimbingan akademik digital** di Universitas Bengkulu, dengan tujuan meningkatkan efisiensi komunikasi dan mempercepat penyampaian informasi kepada mahasiswa.

---

## 🎯 Tujuan Proyek

- Memberikan **layanan bimbingan akademik otomatis** yang responsif dan informatif bagi mahasiswa Universitas Bengkulu.  
- Mengurangi beban administrasi dosen atau petugas akademik dengan **otomatisasi jawaban terhadap pertanyaan berulang**.  
- Meningkatkan pengalaman mahasiswa dalam mengakses informasi akademik secara digital, cepat, dan terintegrasi.  
- Menjadi **proyek pengembangan chatbot berbasis AI sederhana** untuk penerapan di lingkungan kampus.

---

## 💬 Contoh Pertanyaan Chatbot

| Kategori | Contoh Pertanyaan | Contoh Jawaban |
|-----------|------------------|----------------|
| 📚 Akademik Umum | “Kapan waktu pengisian KRS?” | “Pengisian KRS biasanya dibuka setiap awal semester sesuai kalender akademik.” |
| 🎓 Skripsi | “Berapa batas waktu pengerjaan skripsi?” | “Batas waktu pengerjaan skripsi maksimal 2 semester setelah seminar proposal.” |
| 🕓 Cuti Kuliah | “Bagaimana cara mengajukan cuti kuliah?” | “Mahasiswa dapat mengajukan cuti kuliah melalui portal akademik dengan surat persetujuan dari dosen wali.” |
| 🏛️ Peraturan Kampus | “Berapa IPK minimal untuk bisa skripsi?” | “IPK minimal untuk mengajukan skripsi adalah 2.75 sesuai dengan peraturan akademik UNIB.” |

---

## 🚀 Fitur Utama

- 💬 **Chatbot Interaktif**  
  Menjawab pertanyaan mahasiswa terkait akademik secara otomatis dan cepat.

- 🧠 **Basis Pengetahuan (Knowledge Base)**  
  Menyimpan kumpulan pertanyaan dan jawaban seputar peraturan akademik yang dapat diperbarui oleh admin.

- 🧩 **Manajemen Data Chatbot**  
  Admin dapat menambah, mengubah, atau menghapus dataset pertanyaan–jawaban melalui dashboard yang interaktif.

- 🎨 **Dashboard Admin Modern**  
  Dilengkapi tabel dinamis, modal form input data, dan sistem notifikasi dengan tampilan clean dan responsif.

- 🌙 **Mode Terang & Gelap (Dark Mode)**  
  Tampilan dapat diubah antara mode terang dan gelap, dan preferensi mode tersimpan otomatis di browser.

- 📁 **Upload & Retrain Dataset**  
  Admin dapat memperbarui data chatbot dengan mengunggah file baru untuk retraining model AI-nya.

- 🔐 **Autentikasi Admin (opsional)**  
  Fitur login untuk membatasi akses pengelolaan data chatbot hanya untuk pengguna tertentu.

---

## 🧩 Teknologi yang Digunakan

### 💻 **Frontend**
- HTML5  
- CSS3 (dengan desain modern, responsif, dan dark mode)
- JavaScript (interaktivitas dan integrasi AJAX)

### ⚙️ **Backend**
- Python (Framework **Flask**)  
- Flask-Restful untuk API  
- Joblib untuk model penyimpanan AI  
- Pandas & NLTK untuk pengolahan teks

### 🗃️ **Database**
- SQLite / MySQL (tergantung konfigurasi)

### 📚 **Library Utama**
- `flask`  
- `flask_sqlalchemy`  
- `pandas`  
- `scikit-learn`  
- `nltk`  
- `joblib`

---

## 🗂️ Struktur Folder

```
chatbot-bimbingan-akademik/
│
├── app.py                  # File utama backend Flask
├── static/                 # File CSS, JS, dan aset frontend
├── templates/              # File HTML untuk dashboard dan chatbot
├── dataset/                # Dataset pertanyaan-jawaban chatbot
├── model/                  # File model hasil training
├── requirements.txt        # Dependensi proyek
└── README.md               # Dokumentasi proyek
```

---

## ⚙️ Cara Menjalankan Proyek

1. **Clone Repository**
   ```bash
   git clone https://github.com/username/chatbot-bimbingan-akademik.git
   cd chatbot-bimbingan-akademik
   ```

2. **Instal Dependensi**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Aplikasi**
   ```bash
   python app.py
   ```

4. **Akses di Browser**
   ```
   http://localhost:5000
   ```

---

## 🧠 Tentang Proyek

Proyek ini merupakan hasil pengembangan sistem **Chatbot Akademik Universitas Bengkulu** yang mengintegrasikan AI sederhana dengan antarmuka berbasis web.  
Sistem ini memungkinkan mahasiswa untuk memperoleh bimbingan akademik secara mandiri, sedangkan admin dapat memperbarui data chatbot dengan mudah melalui dashboard.

Dengan fitur dark mode, desain modern, dan kemampuan update dataset, proyek ini menjadi contoh penerapan teknologi AI sederhana yang bermanfaat di dunia pendidikan.

---

## 👨‍💻 Pengembang

Dikembangkan oleh **[njwnabilah](https://github.com/njwnabilah)**  
Universitas Bengkulu  
Sebagai proyek inovatif untuk sistem bimbingan akademik digital berbasis chatbot.
