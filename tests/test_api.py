"""Tests untuk API endpoints"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from main import app
from app.models import (
    Mahasiswa, MataKuliah, Enrollment,
    StatusMahasiswa, JenisKelamin, StatusEnrollment
)

# Setup test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_akademik.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override get_db untuk testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestRootEndpoints:
    """Test root endpoints"""
    
    def test_root(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Selamat datang di Aplikasi Akademik"
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "OK"


class TestMahasiswaEndpoints:
    """Test Mahasiswa endpoints"""
    
    def test_create_mahasiswa(self, db):
        """Test create mahasiswa"""
        payload = {
            "nama": "John Doe",
            "email": "john@example.com",
            "no_telepon": "081234567890",
            "alamat": "Jl. Test No. 1",
            "tanggal_lahir": "2000-01-01",
            "jenis_kelamin": "laki-laki",
            "program_studi": "teknik_informatika",
            "tahun_masuk": 2024
        }
        
        response = client.post("/api/mahasiswa", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["nama"] == "John Doe"
        assert data["nim"] == "2024-10-0001"
    
    def test_create_mahasiswa_invalid_email(self, db):
        """Test create mahasiswa dengan email invalid"""
        payload = {
            "nama": "John Doe",
            "email": "invalid-email",  # Invalid email
            "no_telepon": "081234567890",
            "tanggal_lahir": "2000-01-01",
            "jenis_kelamin": "laki-laki",
            "program_studi": "teknik_informatika",
            "tahun_masuk": 2024
        }
        
        response = client.post("/api/mahasiswa", json=payload)
        assert response.status_code == 422
    
    def test_create_mahasiswa_duplicate_email(self, db):
        """Test create mahasiswa dengan email yang sudah ada"""
        payload = {
            "nama": "John Doe",
            "email": "john@example.com",
            "no_telepon": "081234567890",
            "tanggal_lahir": "2000-01-01",
            "jenis_kelamin": "laki-laki",
            "program_studi": "teknik_informatika",
            "tahun_masuk": 2024
        }
        
        # Create first mahasiswa
        response1 = client.post("/api/mahasiswa", json=payload)
        assert response1.status_code == 201
        
        # Try to create with same email
        response2 = client.post("/api/mahasiswa", json=payload)
        assert response2.status_code == 400
        assert "sudah terdaftar" in response2.json()["detail"]
    
    def test_get_mahasiswa_list(self, db):
        """Test get mahasiswa list"""
        payload = {
            "nama": "John Doe",
            "email": "john@example.com",
            "no_telepon": "081234567890",
            "tanggal_lahir": "2000-01-01",
            "jenis_kelamin": "laki-laki",
            "program_studi": "teknik_informatika",
            "tahun_masuk": 2024
        }
        
        client.post("/api/mahasiswa", json=payload)
        
        response = client.get("/api/mahasiswa")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["nama"] == "John Doe"
    
    def test_get_mahasiswa_detail(self, db):
        """Test get mahasiswa detail"""
        payload = {
            "nama": "John Doe",
            "email": "john@example.com",
            "no_telepon": "081234567890",
            "tanggal_lahir": "2000-01-01",
            "jenis_kelamin": "laki-laki",
            "program_studi": "teknik_informatika",
            "tahun_masuk": 2024
        }
        
        create_response = client.post("/api/mahasiswa", json=payload)
        nim = create_response.json()["nim"]
        
        response = client.get(f"/api/mahasiswa/{nim}")
        assert response.status_code == 200
        assert response.json()["nim"] == nim
    
    def test_get_mahasiswa_not_found(self, db):
        """Test get mahasiswa yang tidak ada"""
        response = client.get("/api/mahasiswa/0000-00-0000")
        assert response.status_code == 404
    
    def test_update_mahasiswa(self, db):
        """Test update mahasiswa"""
        payload = {
            "nama": "John Doe",
            "email": "john@example.com",
            "no_telepon": "081234567890",
            "tanggal_lahir": "2000-01-01",
            "jenis_kelamin": "laki-laki",
            "program_studi": "teknik_informatika",
            "tahun_masuk": 2024
        }
        
        create_response = client.post("/api/mahasiswa", json=payload)
        nim = create_response.json()["nim"]
        
        update_payload = {"nama": "Jane Doe"}
        response = client.put(f"/api/mahasiswa/{nim}", json=update_payload)
        
        assert response.status_code == 200
        assert response.json()["nama"] == "Jane Doe"
    
    def test_delete_mahasiswa(self, db):
        """Test delete mahasiswa"""
        payload = {
            "nama": "John Doe",
            "email": "john@example.com",
            "no_telepon": "081234567890",
            "tanggal_lahir": "2000-01-01",
            "jenis_kelamin": "laki-laki",
            "program_studi": "teknik_informatika",
            "tahun_masuk": 2024
        }
        
        create_response = client.post("/api/mahasiswa", json=payload)
        nim = create_response.json()["nim"]
        
        response = client.delete(f"/api/mahasiswa/{nim}")
        assert response.status_code == 204


class TestMataKuliahEndpoints:
    """Test MataKuliah endpoints"""
    
    def test_create_mata_kuliah(self, db):
        """Test create mata kuliah"""
        payload = {
            "kode": "IF201",
            "nama": "Data Structures",
            "deskripsi": "Belajar struktur data",
            "sks": 3,
            "semester": 2,
            "program_studi": "teknik_informatika"
        }
        
        response = client.post("/api/mata-kuliah", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["kode"] == "IF201"
        assert data["nama"] == "Data Structures"
    
    def test_get_mata_kuliah_list(self, db):
        """Test get mata kuliah list"""
        payload = {
            "kode": "IF201",
            "nama": "Data Structures",
            "sks": 3,
            "semester": 2,
            "program_studi": "teknik_informatika"
        }
        
        client.post("/api/mata-kuliah", json=payload)
        
        response = client.get("/api/mata-kuliah")
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestEnrollmentEndpoints:
    """Test Enrollment endpoints"""
    
    def test_create_enrollment(self, db):
        """Test create enrollment"""
        # Create mahasiswa
        mhs_payload = {
            "nama": "John Doe",
            "email": "john@example.com",
            "no_telepon": "081234567890",
            "tanggal_lahir": "2000-01-01",
            "jenis_kelamin": "laki-laki",
            "program_studi": "teknik_informatika",
            "tahun_masuk": 2024
        }
        mhs_response = client.post("/api/mahasiswa", json=mhs_payload)
        nim = mhs_response.json()["nim"]
        
        # Create mata kuliah
        mk_payload = {
            "kode": "IF201",
            "nama": "Data Structures",
            "sks": 3,
            "semester": 2,
            "program_studi": "teknik_informatika"
        }
        mk_response = client.post("/api/mata-kuliah", json=mk_payload)
        mata_kuliah_id = mk_response.json()["id"]
        
        # Create enrollment
        enroll_payload = {
            "nim": nim,
            "mata_kuliah_id": mata_kuliah_id,
            "nilai": 85,
            "semester": 2,
            "tahun_akademik": "2024/2025"
        }
        response = client.post("/api/enrollment", json=enroll_payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nim"] == nim
        assert data["nilai"] == 85
