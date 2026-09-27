# loan-risk-scoring

Loan risk scoring script - Capstone Milestone 3 (RevoU x BINUS).

Proyek ini menghitung skor risiko kredit (0-100) untuk setiap pengajuan pinjaman
berdasarkan data pemohon, lalu memberikan kategori risiko dan penjelasan singkat
dalam bahasa Indonesia layaknya seorang credit analyst. **Seluruh data pada
`test_applications.csv` bersifat fiktif** dan hanya digunakan untuk keperluan
demo/latihan.

Perhitungan skor pada `score_applications.py` **identik dengan logika di node
"Risk Score" pada workflow n8n**, sehingga hasilnya bisa dijadikan acuan
pembanding antara implementasi Python dan n8n.

## Aturan Scoring

Skor dasar dan penambahan poin:

- `(1 - EXT_SOURCE_2) x 40` sebagai skor dasar. Jika `EXT_SOURCE_2` kosong,
  gunakan nilai default 0.5 dan beri `data_flag`:
  "EXT_SOURCE_2 kosong - wajib review manual".
- Rasio `AMT_CREDIT / AMT_INCOME_TOTAL`:
  - `> 5` → tambah 15 poin
  - `> 3` → tambah 8 poin
- `NAME_HOUSING_TYPE` = "Rented apartment" atau "With parents" → tambah 15 poin.
- `NAME_EDUCATION_TYPE` = "Lower secondary" → tambah 10 poin.
- `REGION_RATING_CLIENT`:
  - `3` → tambah 10 poin
  - `2` → tambah 5 poin
- `YEARS_EMPLOYED < 1` → tambah 10 poin.
- `EXT_SOURCE_2 < 0.3` dan status tempat tinggal menyewa/dengan orang tua →
  tambah 10 poin.
- Skor dibulatkan dan dibatasi maksimal 100.

Kategori risiko:

- **High**: skor > 70
- **Medium**: skor 40-70
- **Low**: skor < 40

`needs_review` bernilai `True` jika skor > 70 **atau** `EXT_SOURCE_2` kosong.

## Cara Menjalankan

```bash
python score_applications.py
```

Script akan membaca `test_applications.csv` dan menghasilkan
`scored_applications.csv`.

## File Output

- **`scored_applications.csv`** — hasil scoring per aplikasi dengan kolom:
  `app_id`, `risk_score`, `risk_category`, `credit_to_income`, `data_flag`,
  `needs_review`, `explanation`.
- **`insert_scores.sql`** — script T-SQL (Microsoft SQL Server) berisi
  `CREATE TABLE` dan `INSERT` untuk memuat hasil scoring ke tabel
  `dbo.loan_risk_scores`.
