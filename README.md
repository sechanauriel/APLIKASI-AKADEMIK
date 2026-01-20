# Aplikasi Akademik - REST API dengan FastAPI

Aplikasi akademik sederhana yang mengimplementasikan konsep OOP, REST API, dan database constraints dengan pembelajaran tujuan:

- ✅ Implementasi class diagram ke kode OOP
- ✅ Membangun REST API dengan FastAPI
- ✅ Validasi input dengan constraint database
- ✅ Generate identifier unik (NIM) dengan format institusional
- ✅ Testing dengan pytest

## 🏗️ Arsitektur Aplikasi

### Class Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Mahasiswa                               │
├─────────────────────────────────────────────────────────────────┤
│ PK: nim (YYYY-KK-NNNN)                                           │
│ - nama: str (100)                                                │
│ - email: str (unique)                                            │
│ - no_telepon: str                                                │
│ - alamat: str                                                    │
│ - tanggal_lahir: date                                            │
│ - jenis_kelamin: enum                                            │
│ - program_studi: str                                             │
│ - tahun_masuk: int (2000-2100)                                   │
│ - status: enum (aktif, tidak_aktif, lulus, keluar)              │
├─────────────────────────────────────────────────────────────────┤
│ + get_full_info() -> dict                                        │
│ + is_active() -> bool                                            │
└─────────────────────────────────────────────────────────────────┘
         │
         │ (1:N relationship)
         │ cascading delete
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Enrollment                               │
├─────────────────────────────────────────────────────────────────┤
│ PK: id                                                           │
│ FK: nim (Mahasiswa)                                              │
│ FK: mata_kuliah_id (MataKuliah)                                  │
│ - nilai: float (0-100, nullable)                                 │
│ - semester: int (1-8)                                            │
│ - tahun_akademik: str (YYYY/YYYY)                                │
│ - status: enum (terdaftar, mengambil, selesai, batal)            │
│ UQ: (nim, mata_kuliah_id, tahun_akademik)                        │
├─────────────────────────────────────────────────────────────────┤
└─────────────────────────────────────────────────────────────────┘
         │
         │ (N:1 relationship)
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       MataKuliah                                │
├─────────────────────────────────────────────────────────────────┤
│ PK: id                                                           │
│ - kode: str (unique)                                             │
│ - nama: str (100)                                                │
│ - deskripsi: str                                                 │
│ - sks: int (1-6)                                                 │
│ - semester: int (1-8)                                            │
│ - program_studi: str                                             │
├─────────────────────────────────────────────────────────────────┤
│ + get_info() -> dict                                             │
└─────────────────────────────────────────────────────────────────┘
```

### Struktur Folder

```
akademik_app/
├── app/
│   ├── __init__.py
│   ├── config.py              # Konfigurasi aplikasi
│   ├── database.py            # Database setup dan session
│   ├── models.py              # SQLAlchemy ORM models
│   ├── schemas.py             # Pydantic validation schemas
│   ├── nim_generator.py       # NIM generator utility
│   └── routes/
│       ├── __init__.py
│       ├── mahasiswa.py       # Mahasiswa endpoints
│       ├── mata_kuliah.py     # MataKuliah endpoints
│       └── enrollment.py      # Enrollment endpoints
├── tests/
│   ├── __init__.py
│   ├── test_models.py         # Model tests
│   ├── test_nim_generator.py  # NIM generator tests
│   └── test_api.py            # API endpoint tests
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── pytest.ini                 # Pytest configuration
└── .env                       # Environment variables (optional)
```

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.10+
- pip

### 2. Clone/Setup Project
```bash
cd akademik_app
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
# Development mode dengan auto-reload
python -m uvicorn main:app --reload

# Production mode
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Aplikasi akan berjalan di: `http://localhost:8000`

### 5. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📋 API Endpoints

### 1. Mahasiswa Endpoints

#### Create Mahasiswa (Auto-generate NIM)
```http
POST /api/mahasiswa
Content-Type: application/json

{
  "nama": "John Doe",
  "email": "john@example.com",
  "no_telepon": "081234567890",
  "alamat": "Jl. Test No. 1",
  "tanggal_lahir": "2000-01-01",
  "jenis_kelamin": "laki-laki",
  "program_studi": "teknik_informatika",
  "tahun_masuk": 2024,
  "status": "aktif"
}

Response: 201 Created
{
  "nim": "2024-10-0001",
  "nama": "John Doe",
  "email": "john@example.com",
  "program_studi": "teknik_informatika",
  "tahun_masuk": 2024,
  "status": "aktif",
  "created_at": "2024-01-20T10:30:00",
  "updated_at": "2024-01-20T10:30:00"
}
```

#### List Mahasiswa
```http
GET /api/mahasiswa?skip=0&limit=10&program_studi=teknik_informatika&status=aktif
```

#### Get Mahasiswa Detail
```http
GET /api/mahasiswa/{nim}
```

#### Update Mahasiswa
```http
PUT /api/mahasiswa/{nim}
{
  "nama": "Jane Doe",
  "status": "tidak_aktif"
}
```

#### Delete Mahasiswa
```http
DELETE /api/mahasiswa/{nim}
```

### 2. Mata Kuliah Endpoints

#### Create Mata Kuliah
```http
POST /api/mata-kuliah
{
  "kode": "IF201",
  "nama": "Data Structures",
  "deskripsi": "Belajar struktur data",
  "sks": 3,
  "semester": 2,
  "program_studi": "teknik_informatika"
}
```

#### List Mata Kuliah
```http
GET /api/mata-kuliah?program_studi=teknik_informatika&semester=2
```

#### Get Mata Kuliah Detail
```http
GET /api/mata-kuliah/{id}
```

#### Update Mata Kuliah
```http
PUT /api/mata-kuliah/{id}
{
  "nama": "Data Structures & Algorithms"
}
```

#### Delete Mata Kuliah
```http
DELETE /api/mata-kuliah/{id}
```

### 3. Enrollment Endpoints

#### Create Enrollment
```http
POST /api/enrollment
{
  "nim": "2024-10-0001",
  "mata_kuliah_id": 1,
  "nilai": null,
  "semester": 2,
  "tahun_akademik": "2024/2025",
  "status": "terdaftar"
}
```

#### List Enrollment
```http
GET /api/enrollment?nim=2024-10-0001&tahun_akademik=2024/2025
```

#### Get Enrollment Detail
```http
GET /api/enrollment/{id}
```

#### Update Enrollment (Grade)
```http
PUT /api/enrollment/{id}
{
  "nilai": 85,
  "status": "selesai"
}
```

#### Delete Enrollment
```http
DELETE /api/enrollment/{id}
```

#### Get Transkrip Mahasiswa
```http
GET /api/enrollment/mahasiswa/{nim}/transkrip
```

## 🔐 Validasi & Constraints

### Database Constraints

1. **Mahasiswa Table**
   - `nim`: Primary Key, unique, not null
   - `email`: Unique, not null
   - `tahun_masuk`: CHECK (tahun_masuk >= 2000 AND tahun_masuk <= 2100)
   - Indexes: email, program_studi, tahun_masuk

2. **MataKuliah Table**
   - `kode`: Unique, not null
   - `sks`: CHECK (sks >= 1 AND sks <= 6)
   - `semester`: CHECK (semester >= 1 AND semester <= 8)
   - Indexes: kode, program_studi, semester

3. **Enrollment Table**
   - `nilai`: CHECK (nilai IS NULL OR (nilai >= 0 AND nilai <= 100))
   - `semester`: CHECK (semester >= 1 AND semester <= 8)
   - `(nim, mata_kuliah_id, tahun_akademik)`: Unique constraint
   - Foreign keys: nim (CASCADE), mata_kuliah_id (CASCADE)

### Input Validation (Pydantic)

- **Email**: Valid email format (EmailStr)
- **Nama**: Min 3 karakter, tidak boleh hanya angka
- **No Telepon**: 10-15 karakter
- **Tanggal Lahir**: Format YYYY-MM-DD
- **Tahun Akademik**: Format YYYY/YYYY
- **Nilai**: 0-100 (float)
- **SKS**: 1-6
- **Semester**: 1-8

## 🆔 NIM Generator

### Format Institusional
```
NIM = TAHUN-KODE_PRODI-NOMOR_URUT
Contoh: 2024-10-0001

- 2024: Tahun masuk
- 10:   Kode program studi
- 0001: Nomor urut (auto-increment per tahun per prodi)
```

### Program Studi Codes
```
teknik_informatika:      10
sistem_informasi:        20
ilmu_komputer:           30
rekayasa_perangkat_lunak: 40
cybersecurity:           50
```

### Usage
```python
from app.nim_generator import NIMGenerator, generate_unique_nim

# Generate NIM otomatis
nim = generate_unique_nim(db, "teknik_informatika", 2024)
# Result: "2024-10-0001" (atau nomor urut berikutnya)

# Validasi format NIM
is_valid = NIMGenerator.validate_nim_format("2024-10-0001")  # True

# Parse NIM
info = NIMGenerator.parse_nim("2024-10-0001")
# Result: {
#   "tahun_masuk": 2024,
#   "kode_prodi": "10",
#   "nomor_urut": 1
# }
```

## 🧪 Testing

### Run All Tests
```bash
pytest

# Dengan verbose output
pytest -v

# Dengan coverage report
pytest --cov=app tests/
```

### Test Coverage

Tests mencakup:

1. **test_nim_generator.py**
   - NIM format validation
   - NIM generation dengan uniqueness
   - Program studi code mapping
   - NIM parsing

2. **test_models.py**
   - Model creation
   - Unique constraints (email, kode)
   - Value constraints (SKS, semester, nilai)
   - Relationship testing

3. **test_api.py**
   - CRUD operations
   - Input validation
   - Error handling
   - Duplicate prevention
   - Edge cases

### Example Test Run
```
tests/test_nim_generator.py::TestNIMGenerator::test_generate_nim_first_mahasiswa PASSED
tests/test_models.py::TestMahasiswaModel::test_create_mahasiswa PASSED
tests/test_api.py::TestMahasiswaEndpoints::test_create_mahasiswa PASSED
...
======================== 30 passed in 2.34s ========================
```

## 📝 Usage Examples

### Contoh 1: Create Mahasiswa Baru
```python
import requests

response = requests.post(
    "http://localhost:8000/api/mahasiswa",
    json={
        "nama": "Putri Nurhaliza",
        "email": "putri@example.com",
        "no_telepon": "081234567890",
        "tanggal_lahir": "2000-05-15",
        "jenis_kelamin": "perempuan",
        "program_studi": "teknik_informatika",
        "tahun_masuk": 2024
    }
)

mahasiswa = response.json()
print(f"NIM: {mahasiswa['nim']}")
print(f"Nama: {mahasiswa['nama']}")
```

### Contoh 2: Register Mata Kuliah & Enrollment
```python
# Create mata kuliah
mk_response = requests.post(
    "http://localhost:8000/api/mata-kuliah",
    json={
        "kode": "IF301",
        "nama": "Database Systems",
        "sks": 3,
        "semester": 3,
        "program_studi": "teknik_informatika"
    }
)
mk_id = mk_response.json()["id"]

# Create enrollment
enroll_response = requests.post(
    "http://localhost:8000/api/enrollment",
    json={
        "nim": "2024-10-0001",
        "mata_kuliah_id": mk_id,
        "semester": 3,
        "tahun_akademik": "2024/2025"
    }
)
```

### Contoh 3: Get Transkrip Mahasiswa
```python
response = requests.get(
    "http://localhost:8000/api/enrollment/mahasiswa/2024-10-0001/transkrip"
)

transkrip = response.json()
for enrollment in transkrip:
    print(f"Mata Kuliah: {enrollment['mata_kuliah_id']}")
    print(f"Nilai: {enrollment['nilai']}")
    print(f"Tahun Akademik: {enrollment['tahun_akademik']}")
```

## 🔧 Konfigurasi

### Environment Variables (.env)
```bash
DATABASE_URL=sqlite:///./akademik.db
SQLALCHEMY_ECHO=False
DEBUG=True
```

### Production Settings
Ubah di `app/config.py`:
```python
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/akademik_db"
    SQLALCHEMY_ECHO: bool = False
    DEBUG: bool = False
```

## 📚 Pembelajaran Key Concepts

### 1. OOP Implementation
- **Classes**: Mahasiswa, MataKuliah, Enrollment
- **Inheritance**: Pydantic models, SQLAlchemy Base
- **Encapsulation**: Private methods, property decorators
- **Relationships**: One-to-Many (Mahasiswa-Enrollment)

### 2. Database Design
- **Normalization**: 3NF structure
- **Constraints**: Check, Unique, Foreign Key, Primary Key
- **Indexes**: Performance optimization
- **Cascading Delete**: Data integrity

### 3. REST API Design
- **HTTP Methods**: POST (create), GET (read), PUT (update), DELETE (delete)
- **Status Codes**: 201, 204, 400, 404, 422
- **Error Handling**: Validation, duplicate prevention
- **Relationships**: Nested resources

### 4. Input Validation
- **Pydantic**: Schema validation
- **Database Constraints**: Value range checks
- **Business Logic**: Duplicate prevention, foreign key validation

### 5. Testing
- **Unit Tests**: Individual components
- **Integration Tests**: API endpoints
- **Database Tests**: Constraints and relationships
- **Fixtures**: Test database isolation

## 🎯 Future Enhancements

- [ ] Authentication & Authorization (JWT)
- [ ] Pagination optimization
- [ ] Caching (Redis)
- [ ] Async database queries
- [ ] Email notifications
- [ ] Transcript PDF generation
- [ ] GPA calculation
- [ ] Schedule management
- [ ] Admin dashboard
- [ ] Mobile API

## 📞 Support

Untuk pertanyaan atau issues, silakan buat issue di repository.

## 📄 License

MIT License

---

**Created with ❤️ for Learning OOP & REST API Development**
