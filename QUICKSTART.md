# Akademik App - Quick Start Guide

## 🚀 Quick Setup (5 menit)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Application
```bash
python -m uvicorn main:app --reload
```

### 3. Test API
Buka browser: http://localhost:8000/docs

## 📋 Quick API Tests

### Test 1: Create Mahasiswa
```bash
curl -X POST "http://localhost:8000/api/mahasiswa" \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "John Doe",
    "email": "john@example.com",
    "no_telepon": "081234567890",
    "tanggal_lahir": "2000-01-01",
    "jenis_kelamin": "laki-laki",
    "program_studi": "teknik_informatika",
    "tahun_masuk": 2024
  }'
```

Response:
```json
{
  "nim": "2024-10-0001",
  "nama": "John Doe",
  "email": "john@example.com",
  "program_studi": "teknik_informatika",
  "tahun_masuk": 2024,
  "status": "aktif"
}
```

### Test 2: Create Mata Kuliah
```bash
curl -X POST "http://localhost:8000/api/mata-kuliah" \
  -H "Content-Type: application/json" \
  -d '{
    "kode": "IF201",
    "nama": "Data Structures",
    "sks": 3,
    "semester": 2,
    "program_studi": "teknik_informatika"
  }'
```

### Test 3: Create Enrollment
```bash
curl -X POST "http://localhost:8000/api/enrollment" \
  -H "Content-Type: application/json" \
  -d '{
    "nim": "2024-10-0001",
    "mata_kuliah_id": 1,
    "semester": 2,
    "tahun_akademik": "2024/2025"
  }'
```

### Test 4: Get List Mahasiswa
```bash
curl "http://localhost:8000/api/mahasiswa"
```

### Test 5: Update Nilai Mahasiswa
```bash
curl -X PUT "http://localhost:8000/api/enrollment/1" \
  -H "Content-Type: application/json" \
  -d '{
    "nilai": 85,
    "status": "selesai"
  }'
```

## 🧪 Run Tests
```bash
pytest -v
```

## 📖 Features Overview

### 1. ✅ OOP Class Diagram
- Mahasiswa class dengan methods (is_active, get_full_info)
- MataKuliah class dengan methods (get_info)
- Enrollment class dengan relationships
- Inheritance dari SQLAlchemy Base

### 2. ✅ REST API
- POST: Create resources
- GET: List dan detail
- PUT: Update resources
- DELETE: Delete resources

### 3. ✅ Validasi Input
- Email validation (format valid)
- Pydantic schemas
- Database constraints
- Value range checking

### 4. ✅ NIM Generator
- Format: TAHUN-KODE_PRODI-NOMOR_URUT
- Auto-increment per tahun per program studi
- Unique identifier
- Program studi codes (TI=10, SI=20, dll)

### 5. ✅ Database
- SQLite by default
- SQLAlchemy ORM
- Foreign key constraints
- Unique constraints
- Check constraints
- Cascade delete

### 6. ✅ Testing
- Unit tests (models, NIM generator)
- Integration tests (API endpoints)
- Database constraint tests
- 30+ test cases

## 📊 Database Schema

```sql
CREATE TABLE mahasiswa (
  nim VARCHAR(20) PRIMARY KEY,
  nama VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  no_telepon VARCHAR(15) NOT NULL,
  alamat TEXT,
  tanggal_lahir VARCHAR(10) NOT NULL,
  jenis_kelamin VARCHAR(20) NOT NULL,
  program_studi VARCHAR(50) NOT NULL,
  tahun_masuk INTEGER NOT NULL,
  status VARCHAR(50) DEFAULT 'aktif',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mata_kuliah (
  id INTEGER PRIMARY KEY,
  kode VARCHAR(20) UNIQUE NOT NULL,
  nama VARCHAR(100) NOT NULL,
  deskripsi TEXT,
  sks INTEGER NOT NULL CHECK(sks >= 1 AND sks <= 6),
  semester INTEGER NOT NULL CHECK(semester >= 1 AND semester <= 8),
  program_studi VARCHAR(50) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE enrollment (
  id INTEGER PRIMARY KEY,
  nim VARCHAR(20) NOT NULL,
  mata_kuliah_id INTEGER NOT NULL,
  nilai FLOAT CHECK(nilai IS NULL OR (nilai >= 0 AND nilai <= 100)),
  semester INTEGER NOT NULL,
  tahun_akademik VARCHAR(9) NOT NULL,
  status VARCHAR(50) DEFAULT 'terdaftar',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(nim) REFERENCES mahasiswa(nim) ON DELETE CASCADE,
  FOREIGN KEY(mata_kuliah_id) REFERENCES mata_kuliah(id) ON DELETE CASCADE,
  UNIQUE(nim, mata_kuliah_id, tahun_akademik)
);
```

## 🎓 Learning Outcomes

Setelah menggunakan aplikasi ini, Anda akan memahami:

1. **OOP Principles**
   - Class design dan inheritance
   - Encapsulation dengan properties
   - Method implementation

2. **Database Design**
   - Relationship modeling
   - Constraint implementation
   - Foreign key management

3. **REST API Development**
   - HTTP methods (CRUD)
   - Status codes
   - Error handling
   - Request validation

4. **Data Validation**
   - Input validation (Pydantic)
   - Database constraints
   - Business logic validation

5. **Testing**
   - Unit testing
   - Integration testing
   - Mocking database

## 🔗 Useful Links

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **Pydantic Docs**: https://docs.pydantic.dev
- **Pytest Docs**: https://docs.pytest.org

## 💡 Tips

1. **Debug Mode**: Set DEBUG=True di config untuk melihat SQL queries
2. **API Docs**: Gunakan Swagger UI (/docs) untuk testing
3. **Database Reset**: Delete akademik.db untuk reset database
4. **Database Browser**: Gunakan SQLite Browser untuk inspect database

---

Happy Learning! 🎉
