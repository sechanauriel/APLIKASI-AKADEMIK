# API Examples dengan Python & cURL

## 🐍 Python Examples

### Setup
```python
import requests
import json

BASE_URL = "http://localhost:8000"
```

### 1. Create Mahasiswa
```python
def create_mahasiswa():
    """Membuat mahasiswa baru dengan NIM auto-generate"""
    payload = {
        "nama": "Putri Nurhaliza",
        "email": "putri@example.com",
        "no_telepon": "081234567890",
        "alamat": "Bandung, Jawa Barat",
        "tanggal_lahir": "2000-05-15",
        "jenis_kelamin": "perempuan",
        "program_studi": "teknik_informatika",
        "tahun_masuk": 2024,
        "status": "aktif"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/mahasiswa",
        json=payload
    )
    
    if response.status_code == 201:
        mahasiswa = response.json()
        print(f"✅ Mahasiswa created: {mahasiswa['nim']}")
        return mahasiswa
    else:
        print(f"❌ Error: {response.json()}")
        return None

# Usage
mahasiswa = create_mahasiswa()
# ✅ Mahasiswa created: 2024-10-0001
```

### 2. List Mahasiswa
```python
def list_mahasiswa(program_studi=None, status=None):
    """Get list mahasiswa dengan filter optional"""
    params = {
        "skip": 0,
        "limit": 10
    }
    
    if program_studi:
        params["program_studi"] = program_studi
    if status:
        params["status"] = status
    
    response = requests.get(
        f"{BASE_URL}/api/mahasiswa",
        params=params
    )
    
    if response.status_code == 200:
        mahasiswa_list = response.json()
        print(f"✅ Found {len(mahasiswa_list)} mahasiswa:")
        for mhs in mahasiswa_list:
            print(f"  - {mhs['nim']}: {mhs['nama']} ({mhs['program_studi']})")
        return mahasiswa_list
    else:
        print(f"❌ Error: {response.json()}")
        return None

# Usage
list_mahasiswa(program_studi="teknik_informatika")
```

### 3. Get Mahasiswa Detail
```python
def get_mahasiswa(nim):
    """Get detail mahasiswa berdasarkan NIM"""
    response = requests.get(
        f"{BASE_URL}/api/mahasiswa/{nim}"
    )
    
    if response.status_code == 200:
        mahasiswa = response.json()
        print(f"✅ Mahasiswa Detail:")
        print(f"  NIM: {mahasiswa['nim']}")
        print(f"  Nama: {mahasiswa['nama']}")
        print(f"  Email: {mahasiswa['email']}")
        print(f"  Program Studi: {mahasiswa['program_studi']}")
        print(f"  Tahun Masuk: {mahasiswa['tahun_masuk']}")
        print(f"  Status: {mahasiswa['status']}")
        return mahasiswa
    else:
        print(f"❌ Error: {response.json()}")
        return None

# Usage
get_mahasiswa("2024-10-0001")
```

### 4. Update Mahasiswa
```python
def update_mahasiswa(nim, **kwargs):
    """Update mahasiswa fields"""
    response = requests.put(
        f"{BASE_URL}/api/mahasiswa/{nim}",
        json=kwargs
    )
    
    if response.status_code == 200:
        mahasiswa = response.json()
        print(f"✅ Mahasiswa updated:")
        print(json.dumps(mahasiswa, indent=2))
        return mahasiswa
    else:
        print(f"❌ Error: {response.json()}")
        return None

# Usage
update_mahasiswa("2024-10-0001", 
                nama="Putri Nurhaliza Updated",
                status="tidak_aktif")
```

### 5. Create Mata Kuliah
```python
def create_mata_kuliah():
    """Membuat mata kuliah baru"""
    payload = {
        "kode": "IF301",
        "nama": "Database Systems",
        "deskripsi": "Mempelajari sistem basis data relasional",
        "sks": 3,
        "semester": 3,
        "program_studi": "teknik_informatika"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/mata-kuliah",
        json=payload
    )
    
    if response.status_code == 201:
        mk = response.json()
        print(f"✅ Mata Kuliah created: {mk['kode']} ({mk['id']})")
        return mk
    else:
        print(f"❌ Error: {response.json()}")
        return None

# Usage
mata_kuliah = create_mata_kuliah()
```

### 6. Create Enrollment
```python
def create_enrollment(nim, mata_kuliah_id):
    """Register mahasiswa ke mata kuliah"""
    payload = {
        "nim": nim,
        "mata_kuliah_id": mata_kuliah_id,
        "semester": 3,
        "tahun_akademik": "2024/2025",
        "status": "terdaftar"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/enrollment",
        json=payload
    )
    
    if response.status_code == 201:
        enrollment = response.json()
        print(f"✅ Enrollment created: {enrollment['id']}")
        return enrollment
    else:
        print(f"❌ Error: {response.json()}")
        return None

# Usage
enrollment = create_enrollment("2024-10-0001", 1)
```

### 7. Update Enrollment (Input Nilai)
```python
def input_nilai(enrollment_id, nilai):
    """Input nilai mahasiswa ke enrollment"""
    payload = {
        "nilai": nilai,
        "status": "selesai"
    }
    
    response = requests.put(
        f"{BASE_URL}/api/enrollment/{enrollment_id}",
        json=payload
    )
    
    if response.status_code == 200:
        enrollment = response.json()
        print(f"✅ Nilai updated: {enrollment['nilai']}")
        return enrollment
    else:
        print(f"❌ Error: {response.json()}")
        return None

# Usage
input_nilai(1, 85.5)
```

### 8. Get Transkrip Mahasiswa
```python
def get_transkrip(nim):
    """Get transkrip lengkap mahasiswa"""
    response = requests.get(
        f"{BASE_URL}/api/enrollment/mahasiswa/{nim}/transkrip"
    )
    
    if response.status_code == 200:
        transkrip = response.json()
        print(f"✅ Transkrip {nim}:")
        print(f"{'Tahun':<12} {'Semester':<10} {'Mata Kuliah':<15} {'Nilai':<8} {'Status':<15}")
        print("-" * 60)
        
        total_nilai = 0
        count = 0
        
        for enrollment in transkrip:
            print(f"{enrollment['tahun_akademik']:<12} {enrollment['semester']:<10} "
                  f"{enrollment['mata_kuliah_id']:<15} "
                  f"{enrollment['nilai'] or '-':<8} {enrollment['status']:<15}")
            
            if enrollment['nilai'] is not None:
                total_nilai += enrollment['nilai']
                count += 1
        
        if count > 0:
            rata_rata = total_nilai / count
            print(f"\nRata-rata: {rata_rata:.2f}")
        
        return transkrip
    else:
        print(f"❌ Error: {response.json()}")
        return None

# Usage
get_transkrip("2024-10-0001")
```

### 9. Delete Enrollment
```python
def delete_enrollment(enrollment_id):
    """Delete enrollment"""
    response = requests.delete(
        f"{BASE_URL}/api/enrollment/{enrollment_id}"
    )
    
    if response.status_code == 204:
        print(f"✅ Enrollment {enrollment_id} deleted")
        return True
    else:
        print(f"❌ Error: {response.json()}")
        return False

# Usage
delete_enrollment(1)
```

### 10. Delete Mahasiswa
```python
def delete_mahasiswa(nim):
    """Delete mahasiswa dan semua enrollmentnya"""
    response = requests.delete(
        f"{BASE_URL}/api/mahasiswa/{nim}"
    )
    
    if response.status_code == 204:
        print(f"✅ Mahasiswa {nim} deleted")
        return True
    else:
        print(f"❌ Error: {response.json()}")
        return False

# Usage
delete_mahasiswa("2024-10-0001")
```

## 🔧 cURL Examples

### 1. Create Mahasiswa
```bash
curl -X POST "http://localhost:8000/api/mahasiswa" \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "Putri Nurhaliza",
    "email": "putri@example.com",
    "no_telepon": "081234567890",
    "tanggal_lahir": "2000-05-15",
    "jenis_kelamin": "perempuan",
    "program_studi": "teknik_informatika",
    "tahun_masuk": 2024
  }' | jq
```

### 2. List Mahasiswa
```bash
curl "http://localhost:8000/api/mahasiswa?skip=0&limit=10" | jq
```

### 3. Get Detail Mahasiswa
```bash
curl "http://localhost:8000/api/mahasiswa/2024-10-0001" | jq
```

### 4. Update Mahasiswa
```bash
curl -X PUT "http://localhost:8000/api/mahasiswa/2024-10-0001" \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "Putri Nurhaliza Updated",
    "status": "tidak_aktif"
  }' | jq
```

### 5. Create Mata Kuliah
```bash
curl -X POST "http://localhost:8000/api/mata-kuliah" \
  -H "Content-Type: application/json" \
  -d '{
    "kode": "IF301",
    "nama": "Database Systems",
    "sks": 3,
    "semester": 3,
    "program_studi": "teknik_informatika"
  }' | jq
```

### 6. List Mata Kuliah
```bash
curl "http://localhost:8000/api/mata-kuliah?program_studi=teknik_informatika" | jq
```

### 7. Create Enrollment
```bash
curl -X POST "http://localhost:8000/api/enrollment" \
  -H "Content-Type: application/json" \
  -d '{
    "nim": "2024-10-0001",
    "mata_kuliah_id": 1,
    "semester": 3,
    "tahun_akademik": "2024/2025"
  }' | jq
```

### 8. Update Nilai (Enrollment)
```bash
curl -X PUT "http://localhost:8000/api/enrollment/1" \
  -H "Content-Type: application/json" \
  -d '{
    "nilai": 85,
    "status": "selesai"
  }' | jq
```

### 9. Get Transkrip
```bash
curl "http://localhost:8000/api/enrollment/mahasiswa/2024-10-0001/transkrip" | jq
```

### 10. Delete Enrollment
```bash
curl -X DELETE "http://localhost:8000/api/enrollment/1"
```

### 11. Delete Mahasiswa
```bash
curl -X DELETE "http://localhost:8000/api/mahasiswa/2024-10-0001"
```

## 📊 Batch Operations

### Create Multiple Mahasiswa
```python
def create_batch_mahasiswa(count=5):
    """Create multiple mahasiswa"""
    for i in range(1, count + 1):
        payload = {
            "nama": f"Mahasiswa {i}",
            "email": f"mahasiswa{i}@example.com",
            "no_telepon": f"0812345678{i:02d}",
            "tanggal_lahir": "2000-01-01",
            "jenis_kelamin": "laki-laki" if i % 2 == 0 else "perempuan",
            "program_studi": "teknik_informatika",
            "tahun_masuk": 2024
        }
        
        response = requests.post(f"{BASE_URL}/api/mahasiswa", json=payload)
        if response.status_code == 201:
            mahasiswa = response.json()
            print(f"✅ Created: {mahasiswa['nim']} - {mahasiswa['nama']}")

# Usage
create_batch_mahasiswa(5)
```

---

**Tips:**
- Gunakan `jq` untuk pretty-print JSON (install: `brew install jq` / `apt install jq`)
- Test di Swagger UI dulu: http://localhost:8000/docs
- Ganti host/port sesuai environment
