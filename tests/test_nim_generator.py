"""Tests untuk NIM Generator"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Mahasiswa, StatusMahasiswa, JenisKelamin
from app.nim_generator import NIMGenerator, generate_unique_nim

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


class TestNIMGenerator:
    """Test class untuk NIM Generator"""
    
    def test_get_prodi_code_valid(self):
        """Test get_prodi_code dengan input valid"""
        assert NIMGenerator.get_prodi_code("teknik_informatika") == "10"
        assert NIMGenerator.get_prodi_code("sistem_informasi") == "20"
        assert NIMGenerator.get_prodi_code("ilmu_komputer") == "30"
    
    def test_get_prodi_code_case_insensitive(self):
        """Test get_prodi_code case insensitive"""
        assert NIMGenerator.get_prodi_code("Teknik Informatika") == "10"
        assert NIMGenerator.get_prodi_code("SISTEM INFORMASI") == "20"
    
    def test_get_prodi_code_invalid(self):
        """Test get_prodi_code dengan input invalid"""
        with pytest.raises(ValueError):
            NIMGenerator.get_prodi_code("program_tidak_ada")
    
    def test_validate_nim_format_valid(self):
        """Test validate_nim_format dengan format valid"""
        assert NIMGenerator.validate_nim_format("2024-10-0001") is True
        assert NIMGenerator.validate_nim_format("2023-20-0042") is True
    
    def test_validate_nim_format_invalid(self):
        """Test validate_nim_format dengan format invalid"""
        assert NIMGenerator.validate_nim_format("202410-0001") is False
        assert NIMGenerator.validate_nim_format("2024-10") is False
        assert NIMGenerator.validate_nim_format("2024-1a-0001") is False
    
    def test_parse_nim_valid(self):
        """Test parse_nim dengan format valid"""
        result = NIMGenerator.parse_nim("2024-10-0001")
        assert result["tahun_masuk"] == 2024
        assert result["kode_prodi"] == "10"
        assert result["nomor_urut"] == 1
    
    def test_parse_nim_invalid(self):
        """Test parse_nim dengan format invalid"""
        with pytest.raises(ValueError):
            NIMGenerator.parse_nim("invalid-nim-format")
    
    def test_generate_nim_first_mahasiswa(self, db):
        """Test generate_nim untuk mahasiswa pertama"""
        nim = generate_unique_nim(db, "teknik_informatika", 2024)
        assert nim == "2024-10-0001"
    
    def test_generate_nim_multiple_mahasiswa(self, db):
        """Test generate_nim untuk multiple mahasiswa"""
        # Create first mahasiswa
        nim1 = generate_unique_nim(db, "teknik_informatika", 2024)
        mahasiswa1 = Mahasiswa(
            nim=nim1,
            nama="Mahasiswa 1",
            email="mahasiswa1@example.com",
            no_telepon="081234567890",
            tanggal_lahir="2000-01-01",
            jenis_kelamin=JenisKelamin.LAKI_LAKI,
            program_studi="teknik_informatika",
            tahun_masuk=2024,
            status=StatusMahasiswa.AKTIF
        )
        db.add(mahasiswa1)
        db.commit()
        
        # Create second mahasiswa
        nim2 = generate_unique_nim(db, "teknik_informatika", 2024)
        assert nim2 == "2024-10-0002"
        
        mahasiswa2 = Mahasiswa(
            nim=nim2,
            nama="Mahasiswa 2",
            email="mahasiswa2@example.com",
            no_telepon="081234567891",
            tanggal_lahir="2000-01-02",
            jenis_kelamin=JenisKelamin.PEREMPUAN,
            program_studi="teknik_informatika",
            tahun_masuk=2024,
            status=StatusMahasiswa.AKTIF
        )
        db.add(mahasiswa2)
        db.commit()
        
        # Create third mahasiswa dengan tahun berbeda
        nim3 = generate_unique_nim(db, "teknik_informatika", 2023)
        assert nim3 == "2023-10-0001"
    
    def test_generate_nim_different_prodi(self, db):
        """Test generate_nim untuk program studi berbeda"""
        nim1 = generate_unique_nim(db, "teknik_informatika", 2024)
        mahasiswa1 = Mahasiswa(
            nim=nim1,
            nama="Mahasiswa 1",
            email="mahasiswa1@example.com",
            no_telepon="081234567890",
            tanggal_lahir="2000-01-01",
            jenis_kelamin=JenisKelamin.LAKI_LAKI,
            program_studi="teknik_informatika",
            tahun_masuk=2024,
            status=StatusMahasiswa.AKTIF
        )
        db.add(mahasiswa1)
        db.commit()
        
        # Create mahasiswa dari program studi berbeda
        nim2 = generate_unique_nim(db, "sistem_informasi", 2024)
        assert nim2 == "2024-20-0001"
