"""Tests untuk Models"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
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


@pytest.fixture
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)


class TestMahasiswaModel:
    """Test class untuk Mahasiswa model"""
    
    def test_create_mahasiswa(self, db):
        """Test membuat mahasiswa baru"""
        mahasiswa = Mahasiswa(
            nim="2024-10-0001",
            nama="John Doe",
            email="john@example.com",
            no_telepon="081234567890",
            alamat="Jl. Test No. 1",
            tanggal_lahir="2000-01-01",
            jenis_kelamin=JenisKelamin.LAKI_LAKI,
            program_studi="teknik_informatika",
            tahun_masuk=2024,
            status=StatusMahasiswa.AKTIF
        )
        db.add(mahasiswa)
        db.commit()
        
        assert mahasiswa.nim == "2024-10-0001"
        assert mahasiswa.nama == "John Doe"
        assert mahasiswa.is_active() is True
    
    def test_mahasiswa_unique_email(self, db):
        """Test email harus unik"""
        mahasiswa1 = Mahasiswa(
            nim="2024-10-0001",
            nama="John Doe",
            email="john@example.com",
            no_telepon="081234567890",
            tanggal_lahir="2000-01-01",
            jenis_kelamin=JenisKelamin.LAKI_LAKI,
            program_studi="teknik_informatika",
            tahun_masuk=2024
        )
        db.add(mahasiswa1)
        db.commit()
        
        mahasiswa2 = Mahasiswa(
            nim="2024-10-0002",
            nama="Jane Doe",
            email="john@example.com",  # Email duplikat
            no_telepon="081234567891",
            tanggal_lahir="2000-01-02",
            jenis_kelamin=JenisKelamin.PEREMPUAN,
            program_studi="teknik_informatika",
            tahun_masuk=2024
        )
        db.add(mahasiswa2)
        
        with pytest.raises(Exception):
            db.commit()
    
    def test_mahasiswa_get_full_info(self, db):
        """Test method get_full_info"""
        mahasiswa = Mahasiswa(
            nim="2024-10-0001",
            nama="John Doe",
            email="john@example.com",
            no_telepon="081234567890",
            tanggal_lahir="2000-01-01",
            jenis_kelamin=JenisKelamin.LAKI_LAKI,
            program_studi="teknik_informatika",
            tahun_masuk=2024
        )
        db.add(mahasiswa)
        db.commit()
        
        info = mahasiswa.get_full_info()
        assert info["nim"] == "2024-10-0001"
        assert info["nama"] == "John Doe"
        assert info["program_studi"] == "teknik_informatika"


class TestMataKuliahModel:
    """Test class untuk MataKuliah model"""
    
    def test_create_mata_kuliah(self, db):
        """Test membuat mata kuliah baru"""
        mata_kuliah = MataKuliah(
            kode="IF201",
            nama="Data Structures",
            deskripsi="Belajar struktur data",
            sks=3,
            semester=2,
            program_studi="teknik_informatika"
        )
        db.add(mata_kuliah)
        db.commit()
        
        assert mata_kuliah.kode == "IF201"
        assert mata_kuliah.nama == "Data Structures"
        assert mata_kuliah.sks == 3
    
    def test_mata_kuliah_unique_kode(self, db):
        """Test kode mata kuliah harus unik"""
        mk1 = MataKuliah(
            kode="IF201",
            nama="Data Structures",
            sks=3,
            semester=2,
            program_studi="teknik_informatika"
        )
        db.add(mk1)
        db.commit()
        
        mk2 = MataKuliah(
            kode="IF201",  # Kode duplikat
            nama="Other Course",
            sks=3,
            semester=3,
            program_studi="teknik_informatika"
        )
        db.add(mk2)
        
        with pytest.raises(Exception):
            db.commit()
    
    def test_mata_kuliah_sks_constraint(self, db):
        """Test SKS harus antara 1-6"""
        with pytest.raises(Exception):
            mata_kuliah = MataKuliah(
                kode="IF201",
                nama="Invalid Course",
                sks=10,  # Invalid SKS
                semester=2,
                program_studi="teknik_informatika"
            )
            db.add(mata_kuliah)
            db.commit()


class TestEnrollmentModel:
    """Test class untuk Enrollment model"""
    
    def test_create_enrollment(self, db):
        """Test membuat enrollment baru"""
        # Create mahasiswa
        mahasiswa = Mahasiswa(
            nim="2024-10-0001",
            nama="John Doe",
            email="john@example.com",
            no_telepon="081234567890",
            tanggal_lahir="2000-01-01",
            jenis_kelamin=JenisKelamin.LAKI_LAKI,
            program_studi="teknik_informatika",
            tahun_masuk=2024
        )
        db.add(mahasiswa)
        
        # Create mata kuliah
        mata_kuliah = MataKuliah(
            kode="IF201",
            nama="Data Structures",
            sks=3,
            semester=2,
            program_studi="teknik_informatika"
        )
        db.add(mata_kuliah)
        db.commit()
        
        # Create enrollment
        enrollment = Enrollment(
            nim="2024-10-0001",
            mata_kuliah_id=mata_kuliah.id,
            nilai=85,
            semester=2,
            tahun_akademik="2024/2025",
            status=StatusEnrollment.SELESAI
        )
        db.add(enrollment)
        db.commit()
        
        assert enrollment.nim == "2024-10-0001"
        assert enrollment.nilai == 85
        assert enrollment.tahun_akademik == "2024/2025"
    
    def test_enrollment_unique_per_tahun(self, db):
        """Test enrollment unik per tahun akademik"""
        # Create mahasiswa
        mahasiswa = Mahasiswa(
            nim="2024-10-0001",
            nama="John Doe",
            email="john@example.com",
            no_telepon="081234567890",
            tanggal_lahir="2000-01-01",
            jenis_kelamin=JenisKelamin.LAKI_LAKI,
            program_studi="teknik_informatika",
            tahun_masuk=2024
        )
        db.add(mahasiswa)
        
        # Create mata kuliah
        mata_kuliah = MataKuliah(
            kode="IF201",
            nama="Data Structures",
            sks=3,
            semester=2,
            program_studi="teknik_informatika"
        )
        db.add(mata_kuliah)
        db.commit()
        
        # Create first enrollment
        enrollment1 = Enrollment(
            nim="2024-10-0001",
            mata_kuliah_id=mata_kuliah.id,
            nilai=85,
            semester=2,
            tahun_akademik="2024/2025"
        )
        db.add(enrollment1)
        db.commit()
        
        # Try to create duplicate enrollment
        enrollment2 = Enrollment(
            nim="2024-10-0001",
            mata_kuliah_id=mata_kuliah.id,
            nilai=90,
            semester=2,
            tahun_akademik="2024/2025"
        )
        db.add(enrollment2)
        
        with pytest.raises(Exception):
            db.commit()
    
    def test_enrollment_nilai_constraint(self, db):
        """Test nilai harus antara 0-100"""
        mahasiswa = Mahasiswa(
            nim="2024-10-0001",
            nama="John Doe",
            email="john@example.com",
            no_telepon="081234567890",
            tanggal_lahir="2000-01-01",
            jenis_kelamin=JenisKelamin.LAKI_LAKI,
            program_studi="teknik_informatika",
            tahun_masuk=2024
        )
        db.add(mahasiswa)
        
        mata_kuliah = MataKuliah(
            kode="IF201",
            nama="Data Structures",
            sks=3,
            semester=2,
            program_studi="teknik_informatika"
        )
        db.add(mata_kuliah)
        db.commit()
        
        with pytest.raises(Exception):
            enrollment = Enrollment(
                nim="2024-10-0001",
                mata_kuliah_id=mata_kuliah.id,
                nilai=150,  # Invalid nilai
                semester=2,
                tahun_akademik="2024/2025"
            )
            db.add(enrollment)
            db.commit()
