# 🚀 Workflow CI – Eksperimen SML  
**Alya Shandy Aurora**

Folder ini berisi seluruh konfigurasi **Continuous Integration (CI)** berbasis **MLflow + GitHub Actions**, yang digunakan untuk:

- Tracking eksperimen model ML  
- Menyimpan model otomatis ke artifact store  
- Membangun image Docker otomatis dari model terbaru  
- Push image tersebut ke Docker Hub  

Workflow ini memastikan pipeline model berjalan otomatis setiap ada perubahan pada repository.

---

## 📂 Struktur Folder

```
Workflow_CI/
├── MLProject/                      # Config MLflow project
│   ├── conda.yaml                  # Environment MLProject
│   ├── dataset_preprocessing/
│   ├── modelling.py                # Script training
│   └── MLProject                   # File konfigurasi MLflow project
├── .github/
│   └── workflows/
│       └── mlflow_ci.yml           # GitHub Actions CI workflow
└── README.md                       # Dokumentasi workflow CI (file ini)
```

---

# ⚙️ 1. Cara Kerja Workflow CI

Workflow CI berjalan otomatis ketika:

- Ada **push ke branch main**
- Ada **Pull Request**
- Atau dijalankan **manual dispatch**

Workflow melakukan **4 tahap utama**:

---

## 🧪 1) Menjalankan MLflow Project

Training dijalankan otomatis menggunakan:

```bash
mlflow run MLProject -P alpha=0.5 -P l1_ratio=0.1
```

Model akan tersimpan di:

```
mlruns/0/<RUN_ID>/artifacts/model/
```

---

## 🧱 2) Mengambil RUN ID Terbaru

```bash
LAST_RUN_ID=$(ls -t MLProject/mlruns/0 | head -n 1)
```

Sehingga Docker **selalu dibuat dari model terbaru**.

---

## 🐳 3) Build Docker Image dari Model

```bash
mlflow models build-docker \
    -m MLProject/mlruns/0/$LAST_RUN_ID/artifacts/model \
    -n ${{ secrets.DOCKERHUB_USERNAME }}/msml-california:latest
```

---

## 📤 4) Push Image ke Docker Hub

Login otomatis:

```bash
echo "${{ secrets.DOCKERHUB_TOKEN }}" | docker login \
    -u "${{ secrets.DOCKERHUB_USERNAME }}" --password-stdin
```

Push image:

```bash
docker push ${{ secrets.DOCKERHUB_USERNAME }}/msml-california:latest
```

---

# 🔑 2. Secret GitHub yang Wajib Ada

Tambahkan melalui:

**GitHub → Settings → Secrets → Actions**

| Secret | Isi |
|--------|-----|
| `DOCKERHUB_USERNAME` | Username Docker Hub |
| `DOCKERHUB_TOKEN` | Token Docker Hub (bukan password) |
| `WORKFLOW_CI_TOKEN` | Personal Access Token GitHub |

---

# 🧪 3. Menjalankan Workflow Secara Manual

Masuk ke:

```
GitHub → Actions → mlflow_ci → Run workflow
```

Pilih branch **main**, lalu klik **Run Workflow**.

---

# 📦 4. Build & Serve Docker Secara Lokal

Jika ingin menjalankan Docker hasil CI:

```bash
docker pull <username>/msml-california:latest
docker run -p 5001:8080 <username>/msml-california:latest
```

Akses endpoint inferensi:

👉 http://localhost:5001/invocations

---

# 🔍 5. Catatan Penting

- MLflow Project harus dapat dijalankan lokal tanpa error  
- Pastikan `conda.yaml` lengkap  
- Folder **mlruns/** tidak wajib di-push  
- Struktur MLProject harus sesuai standar MLflow  

---

# ✔️ 6. Status Submission

Workflow CI ini *sudah memenuhi seluruh kriteria*:

✔️ Training otomatis  
✔️ Tracking eksperimen MLflow  
✔️ Build Docker otomatis  
✔️ Push image ke Docker Hub  
✔️ Menggunakan MLProject  

---

# 📞 Kontak

Reviewer dapat menjalankan pipeline melalui tab **Actions** di GitHub.

---

