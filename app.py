import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# --- MAPPING KODE KE LABEL ---
# Data ini ditranskripsi dari deskripsi dataset untuk membuat dropdown yang user-friendly

marital_status_map = {1: "Single", 2: "Married", 3: "Widower", 4: "Divorced", 5: "Facto Union", 6: "Legally Separated"}
attendance_map = {1: "Daytime", 0: "Evening"}
binary_map = {1: "Yes", 0: "No"}
gender_map = {1: "Male", 0: "Female"}

application_mode_map = {
    1: "1st phase - general contingent", 2: "Ordinance No. 612/93", 5: "1st phase - special contingent (Azores Island)",
    7: "Holders of other higher courses", 10: "Ordinance No. 854-B/99", 15: "International student (bachelor)",
    16: "1st phase - special contingent (Madeira Island)", 17: "2nd phase - general contingent", 18: "3rd phase - general contingent",
    26: "Ordinance No. 533-A/99, item b2) (Different Plan)", 27: "Ordinance No. 533-A/99, item b3 (Other Institution)",
    39: "Over 23 years old", 42: "Transfer", 43: "Change of course", 44: "Technological specialization diploma holders",
    51: "Change of institution/course", 53: "Short cycle diploma holders", 57: "Change of institution/course (International)"
}

course_map = {
    33: "Biofuel Production Technologies", 171: "Animation and Multimedia Design", 8014: "Social Service (evening attendance)",
    9003: "Agronomy", 9070: "Communication Design", 9085: "Veterinary Nursing", 9119: "Informatics Engineering",
    9130: "Equinculture", 9147: "Management", 9238: "Social Service", 9254: "Tourism", 9500: "Nursing",
    9556: "Oral Hygiene", 9670: "Advertising and Marketing Management", 9773: "Journalism and Communication",
    9853: "Basic Education", 9991: "Management (evening attendance)"
}

qualification_map = {
    1: "Secondary education", 2: "Higher education - bachelor's degree", 3: "Higher education - degree",
    4: "Higher education - master's", 5: "Higher education - doctorate", 6: "Frequency of higher education",
    9: "12th year of schooling - not completed", 10: "11th year of schooling - not completed",
    12: "Other - 11th year of schooling", 14: "10th year of schooling", 15: "10th year of schooling - not completed",
    19: "Basic education 3rd cycle (9th/10th/11th year) or equiv.", 38: "Basic education 2nd cycle (6th/7th/8th year) or equiv.",
    39: "Technological specialization course", 40: "Higher education - degree (1st cycle)",
    42: "Professional higher technical course", 43: "Higher education - master (2nd cycle)"
}

# Mapping untuk pekerjaan (dipersingkat untuk kejelasan)
occupation_map = {
    0: "Student", 1: "Management/Executive", 2: "Intellectual/Scientific Specialist",
    3: "Intermediate Technician/Professional", 4: "Administrative Staff", 5: "Personal Services/Security/Sales",
    6: "Agriculture/Fishery Skilled Worker", 7: "Industry/Construction Skilled Worker",
    8: "Machine Operator/Assembly Worker", 9: "Unskilled Worker", 10: "Armed Forces", 90: "Other", 99: "N/A"
}
# Anda dapat menambahkan sisa kode pekerjaan yang lebih detail ke dictionary ini jika diperlukan


# --- FUNGSI UTAMA APLIKASI ---

@st.cache_resource
def load_artifacts():
    """Memuat model, scaler, dan artefak lainnya dengan penanganan error."""
    try:
        model = joblib.load(os.path.join('model', 'student_status_classifier.joblib'))
        scaler = joblib.load(os.path.join('model', 'scaler_status.joblib'))
        trained_columns = joblib.load(os.path.join('model', 'trained_columns_status.joblib'))
        target_mapping = joblib.load(os.path.join('model', 'target_mapping_status.joblib'))
        inverse_target_mapping = {v: k for k, v in target_mapping.items()}
        return model, scaler, trained_columns, inverse_target_mapping
    except FileNotFoundError:
        st.error("❌ **Error:** File model atau artefak pendukung tidak ditemukan.")
        st.info("Pastikan semua file (`student_status_classifier.joblib`, `scaler_status.joblib`, dll.) ada di dalam direktori 'model/'.")
        st.stop()

def create_input_form():
    """Membuat form input data mahasiswa yang user-friendly."""
    with st.form("student_input_form"):
        st.header("👤 Data Diri & Akademik Mahasiswa")
        
        col1, col2 = st.columns(2)
        with col1:
            marital_status = st.selectbox("Status Pernikahan", options=list(marital_status_map.keys()), format_func=lambda x: marital_status_map[x])
            gender = st.selectbox("Jenis Kelamin", options=list(gender_map.keys()), format_func=lambda x: gender_map[x])
            age_at_enrollment = st.number_input("Usia Saat Pendaftaran", min_value=17, max_value=70, value=20, step=1, help="Usia mahasiswa ketika mendaftar.")
            daytime_attendance = st.selectbox("Waktu Kuliah", options=list(attendance_map.keys()), format_func=lambda x: attendance_map[x])
        with col2:
            scholarship_holder = st.selectbox("Penerima Beasiswa", options=list(binary_map.keys()), format_func=lambda x: binary_map[x])
            debtor = st.selectbox("Memiliki Hutang", options=list(binary_map.keys()), format_func=lambda x: binary_map[x])
            tuition_fees_up_to_date = st.selectbox("Biaya Kuliah Lunas", options=list(binary_map.keys()), format_func=lambda x: binary_map[x])
            international = st.selectbox("Mahasiswa Internasional", options=list(binary_map.keys()), format_func=lambda x: binary_map[x])

        st.divider()
        st.header("📝 Latar Belakang Pendaftaran & Pendidikan")
        
        col3, col4 = st.columns(2)
        with col3:
            application_mode = st.selectbox("Jalur Pendaftaran", options=list(application_mode_map.keys()), format_func=lambda x: application_mode_map[x])
            course = st.selectbox("Jurusan yang Dipilih", options=list(course_map.keys()), format_func=lambda x: course_map[x])
            previous_qualification = st.selectbox("Pendidikan Terakhir", options=list(qualification_map.keys()), format_func=lambda x: qualification_map[x])
            admission_grade = st.number_input("Nilai Penerimaan", min_value=0.0, max_value=200.0, value=125.0, help="Rentang nilai: 0 - 200.")
            application_order = st.number_input("Urutan Pilihan Jurusan", min_value=0, max_value=9, value=1, help="Urutan prioritas saat mendaftar (0=pilihan pertama).")
        with col4:
            mothers_occupation = st.selectbox("Pekerjaan Ibu", options=list(occupation_map.keys()), format_func=lambda x: occupation_map[x])
            fathers_occupation = st.selectbox("Pekerjaan Ayah", options=list(occupation_map.keys()), format_func=lambda x: occupation_map[x])
            previous_qualification_grade = st.number_input("Nilai Pendidikan Terakhir", min_value=0.0, max_value=200.0, value=120.0, help="Rentang nilai: 0 - 200.")
            displaced = st.selectbox("Mahasiswa Pindahan", options=list(binary_map.keys()), format_func=lambda x: binary_map[x])
            educational_special_needs = st.selectbox("Kebutuhan Pendidikan Khusus", options=list(binary_map.keys()), format_func=lambda x: binary_map[x])

        st.divider()
        st.header("📚 Performa Akademik (Semester 1 & 2)")

        col5, col6 = st.columns(2)
        with col5:
            st.markdown("**Semester 1**")
            cu_1st_sem_approved = st.number_input("SKS Lulus Sem 1", min_value=0, step=1, value=5, help="Jumlah SKS yang berhasil lulus di semester 1.")
            cu_1st_sem_grade = st.number_input("Rata-rata Nilai Sem 1", min_value=0.0, max_value=20.0, value=12.5, help="Rentang nilai: 0 - 20.")
            cu_1st_sem_enrolled = st.number_input("SKS Didaftar Sem 1", min_value=0, step=1, value=6, help="Jumlah SKS yang diambil di semester 1.")
        with col6:
            st.markdown("**Semester 2**")
            cu_2nd_sem_approved = st.number_input("SKS Lulus Sem 2", min_value=0, step=1, value=5, help="Jumlah SKS yang berhasil lulus di semester 2.")
            cu_2nd_sem_grade = st.number_input("Rata-rata Nilai Sem 2", min_value=0.0, max_value=20.0, value=12.5, help="Rentang nilai: 0 - 20.")
            cu_2nd_sem_enrolled = st.number_input("SKS Didaftar Sem 2", min_value=0, step=1, value=6, help="Jumlah SKS yang diambil di semester 2.")

        # Input yang kurang kritikal atau terlalu banyak, bisa menggunakan nilai default atau disembunyikan
        # Di sini kita tetap memasukkannya dengan nilai default agar struktur data lengkap
        data = {
            'Marital_status': marital_status, 'Application_mode': application_mode, 'Application_order': application_order,
            'Course': course, 'Daytime_evening_attendance': daytime_attendance, 'Previous_qualification': previous_qualification,
            'Previous_qualification_grade': previous_qualification_grade, 'Nacionality': 1, # Default
            'Mothers_qualification': qualification_map.keys().__iter__().__next__(), # Default
            'Fathers_qualification': qualification_map.keys().__iter__().__next__(), # Default
            'Mothers_occupation': mothers_occupation, 'Fathers_occupation': fathers_occupation, 'Admission_grade': admission_grade,
            'Displaced': displaced, 'Educational_special_needs': educational_special_needs, 'Debtor': debtor,
            'Tuition_fees_up_to_date': tuition_fees_up_to_date, 'Gender': gender, 'Scholarship_holder': scholarship_holder,
            'Age_at_enrollment': age_at_enrollment, 'International': international,
            'Curricular_units_1st_sem_credited': 0, 'Curricular_units_1st_sem_enrolled': cu_1st_sem_enrolled,
            'Curricular_units_1st_sem_evaluations': cu_1st_sem_enrolled, 'Curricular_units_1st_sem_approved': cu_1st_sem_approved,
            'Curricular_units_1st_sem_grade': cu_1st_sem_grade, 'Curricular_units_1st_sem_without_evaluations': 0,
            'Curricular_units_2nd_sem_credited': 0, 'Curricular_units_2nd_sem_enrolled': cu_2nd_sem_enrolled,
            'Curricular_units_2nd_sem_evaluations': cu_2nd_sem_enrolled, 'Curricular_units_2nd_sem_approved': cu_2nd_sem_approved,
            'Curricular_units_2nd_sem_grade': cu_2nd_sem_grade, 'Curricular_units_2nd_sem_without_evaluations': 0,
            'Unemployment_rate': 12.0, 'Inflation_rate': 1.0, 'GDP': 0.0
        }
        
        submitted = st.form_submit_button("🚀 Prediksi Status Mahasiswa")
        
        if submitted:
            return pd.DataFrame(data, index=[0])
    return None


# --- MAIN APP LAYOUT ---

st.set_page_config(page_title="Prediksi Status Mahasiswa", layout="wide")
st.title("🎓 Prediksi Status Kelulusan Mahasiswa")
st.markdown("Aplikasi ini membantu **Jaya Jaya Institut** untuk mendeteksi secara dini mahasiswa yang berpotensi **Dropout**.")

# Memuat artefak
model, scaler, trained_columns, inverse_target_mapping = load_artifacts()

# Membuat form input
input_df = create_input_form()

if input_df is not None:
    st.divider()
    st.header("📈 Hasil Prediksi")
    
    # Prapemrosesan data input
    try:
        input_df_reordered = input_df[trained_columns]
        input_df_scaled = scaler.transform(input_df_reordered)
        
        # Prediksi probabilitas
        prediction_proba = model.predict_proba(input_df_scaled)
        
        # Menyiapkan data untuk ditampilkan
        proba_df = pd.DataFrame({
            'Status': [inverse_target_mapping[i] for i in range(len(inverse_target_mapping))],
            'Probabilitas (%)': prediction_proba[0] * 100
        }).set_index('Status')
        
        st.write("Berikut adalah persentase probabilitas untuk setiap status:")
        
        # Tampilkan dalam bentuk bar chart
        st.bar_chart(proba_df, y='Probabilitas (%)')
        
        # Tampilkan detail dalam tabel
        st.dataframe(proba_df.style.format("{:.2f}%", subset=['Probabilitas (%)']))
        
        # Memberikan insight berdasarkan probabilitas tertinggi
        highest_proba_status = proba_df['Probabilitas (%)'].idxmax()
        if highest_proba_status == "Dropout":
            st.error(f"⚠️ **Perhatian Khusus:** Mahasiswa ini memiliki probabilitas tertinggi untuk **Dropout** ({proba_df.loc[highest_proba_status, 'Probabilitas (%)']:.2f}%).", icon="🚨")
        elif highest_proba_status == "Graduate":
            st.success(f"✅ **Prospek Baik:** Mahasiswa ini memiliki probabilitas tertinggi untuk **Lulus** ({proba_df.loc[highest_proba_status, 'Probabilitas (%)']:.2f}%).", icon="🎓")
        else: # Enrolled
            st.info(f"ℹ️ **Informasi:** Mahasiswa ini kemungkinan besar akan tetap **Terdaftar/Aktif** ({proba_df.loc[highest_proba_status, 'Probabilitas (%)']:.2f}%).", icon="📚")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {e}")

st.caption("Dibuat untuk Jaya Jaya Institut | Versi 1.1")