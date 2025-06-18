# 🎓 Proyek Akhir: Deteksi Dini Mahasiswa Dropout untuk Jaya Jaya Institut

## 💼 Business Understanding

### 📌 Latar Belakang Bisnis
Jaya Jaya Institut adalah institusi pendidikan tinggi yang berdiri sejak tahun 2000 dan memiliki reputasi sangat baik. Namun, institut menghadapi tantangan serius berupa tingginya angka mahasiswa *dropout*, yang berdampak pada citra institusi, efisiensi sumber daya, dan keberlanjutan finansial.

### ❓ Permasalahan Bisnis
Bagaimana cara membangun sistem yang dapat mengidentifikasi mahasiswa berisiko *dropout* secara akurat dan proaktif berdasarkan data yang tersedia?

### 📦 Cakupan Proyek
1. **Analisis Data Eksploratif (EDA)**  
2. **Pengembangan Model Machine Learning**  
3. **Pembuatan Dashboard Bisnis (Looker Studio)**  
4. **Prototipe Aplikasi Web (Streamlit)**

---

## 📊 Business Dashboard

**🛠️ Tools:** Looker Studio  
**🔗 Link Dashboard:** [Klik di sini](https://lookerstudio.google.com/reporting/f976dbc6-632c-42b3-a89b-13936367d25c)

### ✨ Fitur Utama:
- **KPI Utama:** Total Mahasiswa, Jumlah Lulus, Dropout, dan Tingkat Dropout (%)
- **Filter Interaktif:** Berdasarkan Jurusan, Jenis Kelamin, Status Beasiswa, dan Status Pembayaran
- **Analisis Risiko:** Perbandingan tingkat dropout antar jurusan dan dampak status keuangan serta performa akademik
- **Tabel Detail:** Data tabular untuk analisis mendalam per segmen

---

## 🤖 Sistem Machine Learning

### 📥 Dataset
- **Nama:** Students Performance Dataset  
- **Sumber:** Dicoding Academy  
- **Link:** [Lihat Dataset](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/data.csv)

### 🧪 Setup Environment

**🧰 requirements.txt:**
```
pandas
numpy
scikit-learn
joblib
streamlit
imbalanced-learn
matplotlib
seaborn
```

**🛠️ Cara Setup:**

<details>
<summary><strong>Opsi 1: venv (Rekomendasi)</strong></summary>

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
.env\Scriptsctivate   # Windows
pip install -r requirements.txt
```
</details>

<details>
<summary><strong>Opsi 2: conda</strong></summary>

```bash
conda create --name proyek_akhir python=3.9
conda activate proyek_akhir
pip install -r requirements.txt
```
</details>

---

## 🧪 Menjalankan Prototipe Aplikasi

### 💻 Akses Lokal:
```bash
streamlit run app.py
```

### 🌐 Akses Online:
🔗 [https://lulus-atau-tidak.streamlit.app/](https://lulus-atau-tidak.streamlit.app/)

---

## ✅ Kesimpulan

1. **Performa Akademik Awal = Indikator Kunci:**  
   Jumlah SKS lulus dan rata-rata nilai semester awal sangat berpengaruh terhadap kemungkinan *dropout*.

2. **Faktor Keuangan:**  
   Mahasiswa dengan pembayaran UKT tidak lancar memiliki risiko *dropout* lebih tinggi.

3. **Model Akurat & Andal:**  
   `RandomForestClassifier` terbukti efektif setelah penanganan overfitting dan imbalance data.

4. **Dashboard Efektif:**  
   Visualisasi data memudahkan pengambilan keputusan strategis bagi manajemen.

---

## 📌 Rekomendasi Action Items

- 🔔 **Sistem Peringatan Dini (Early Warning System):**  
  Gunakan prototipe untuk identifikasi dini mahasiswa berisiko setelah semester 1 dan 2.

- 🎓 **Bimbingan Akademik Proaktif:**  
  Bentuk tim pendamping untuk mahasiswa dengan performa akademik rendah.

- 💰 **Bantuan Finansial Fleksibel:**  
  Berikan solusi seperti cicilan, konseling keuangan, atau info beasiswa bagi mahasiswa dengan masalah UKT.

- 🧭 **Evaluasi Kurikulum Jurusan Risiko Tinggi:**  
  Tinjau jurusan dengan tingkat *dropout* tinggi melalui data dari dashboard.

- 🧩 **Promosi Keterlibatan Mahasiswa:**  
  Dorong partisipasi dalam kegiatan kampus dan komunitas untuk meningkatkan motivasi dan retensi.
