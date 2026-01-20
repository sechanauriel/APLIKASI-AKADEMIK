"""
Models untuk aplikasi akademik

Class Diagram:
┌─────────────────────┐
│     Mahasiswa       │
├─────────────────────┤
│ - nim (PK)          │
│ - nama              │
│ - email             │
│ - no_telepon        │
│ - alamat            │
│ - tanggal_lahir     │
│ - jenis_kelamin     │
│ - program_studi     │
│ - tahun_masuk       │
│ - status            │
│ - created_at        │
│ - updated_at        │
├─────────────────────┤
│ + get_full_info()   │
│ + is_active()       │
└─────────────────────┘
         │
         │ (FK: enrollments)
         │
         ▼
┌─────────────────────┐
│     Enrollment      │
├─────────────────────┤
│ - id (PK)           │
│ - nim (FK)          │
│ - mata_kuliah_id(FK)│
│ - nilai             │
│ - semester          │
│ - tahun_akademik    │
│ - status            │
│ - created_at        │
└─────────────────────┘
         │
         │ (FK: mata_kuliah_id)
         │
         ▼
┌─────────────────────┐
│     MataKuliah      │
├─────────────────────┤
│ - id (PK)           │
│ - kode              │
│ - nama              │
│ - deskripsi         │
│ - sks               │
│ - semester          │
│ - program_studi     │
│ - created_at        │
│ - updated_at        │
├─────────────────────┤
│ + get_info()        │
└─────────────────────┘
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Enum, Index, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base


class StatusMahasiswa(str, PyEnum):
    """Status mahasiswa"""
    AKTIF = "aktif"
    TIDAK_AKTIF = "tidak_aktif"
    LULUS = "lulus"
    KELUAR = "keluar"


class StatusEnrollment(str, PyEnum):
    """Status enrollment"""
    TERDAFTAR = "terdaftar"
    MENGAMBIL = "mengambil"
    SELESAI = "selesai"
    BATAL = "batal"


class JenisKelamin(str, PyEnum):
    """Jenis kelamin"""
    LAKI_LAKI = "laki-laki"
    PEREMPUAN = "perempuan"


class Mahasiswa(Base):
    """Model untuk Mahasiswa - implementasi OOP class diagram"""
    __tablename__ = "mahasiswa"
    
    # Attributes
    nim = Column(String(20), primary_key=True, index=True, nullable=False)
    nama = Column(String(100), nullable=False, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    no_telepon = Column(String(15), nullable=False)
    alamat = Column(Text, nullable=True)
    tanggal_lahir = Column(String(10), nullable=False)  # Format: YYYY-MM-DD
    jenis_kelamin = Column(Enum(JenisKelamin), nullable=False)
    program_studi = Column(String(50), nullable=False)
    tahun_masuk = Column(Integer, nullable=False)
    status = Column(Enum(StatusMahasiswa), default=StatusMahasiswa.AKTIF, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="mahasiswa", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("tahun_masuk >= 2000 AND tahun_masuk <= 2100", name="check_tahun_masuk"),
        UniqueConstraint('email', name='uq_mahasiswa_email'),
        Index('idx_mahasiswa_program_studi', 'program_studi'),
        Index('idx_mahasiswa_tahun_masuk', 'tahun_masuk'),
    )
    
    # Methods
    def get_full_info(self) -> dict:
        """Get informasi lengkap mahasiswa"""
        return {
            "nim": self.nim,
            "nama": self.nama,
            "email": self.email,
            "program_studi": self.program_studi,
            "tahun_masuk": self.tahun_masuk,
            "status": self.status.value,
        }
    
    def is_active(self) -> bool:
        """Cek apakah mahasiswa aktif"""
        return self.status == StatusMahasiswa.AKTIF
    
    def __repr__(self) -> str:
        return f"<Mahasiswa(nim={self.nim}, nama={self.nama})>"


class MataKuliah(Base):
    """Model untuk Mata Kuliah"""
    __tablename__ = "mata_kuliah"
    
    # Attributes
    id = Column(Integer, primary_key=True, index=True)
    kode = Column(String(20), nullable=False, unique=True, index=True)
    nama = Column(String(100), nullable=False, index=True)
    deskripsi = Column(Text, nullable=True)
    sks = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
    program_studi = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="mata_kuliah", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("sks >= 1 AND sks <= 6", name="check_sks"),
        CheckConstraint("semester >= 1 AND semester <= 8", name="check_semester"),
        UniqueConstraint('kode', name='uq_mata_kuliah_kode'),
        Index('idx_mata_kuliah_program_studi', 'program_studi'),
        Index('idx_mata_kuliah_semester', 'semester'),
    )
    
    # Methods
    def get_info(self) -> dict:
        """Get informasi mata kuliah"""
        return {
            "id": self.id,
            "kode": self.kode,
            "nama": self.nama,
            "sks": self.sks,
            "semester": self.semester,
            "program_studi": self.program_studi,
        }
    
    def __repr__(self) -> str:
        return f"<MataKuliah(kode={self.kode}, nama={self.nama})>"


class Enrollment(Base):
    """Model untuk Enrollment (Nilai Mahasiswa)"""
    __tablename__ = "enrollment"
    
    # Attributes
    id = Column(Integer, primary_key=True, index=True)
    nim = Column(String(20), ForeignKey("mahasiswa.nim", ondelete="CASCADE"), nullable=False, index=True)
    mata_kuliah_id = Column(Integer, ForeignKey("mata_kuliah.id", ondelete="CASCADE"), nullable=False, index=True)
    nilai = Column(Float, nullable=True)  # Nullable sampai grade diberikan
    semester = Column(Integer, nullable=False)
    tahun_akademik = Column(String(9), nullable=False)  # Format: 2023/2024
    status = Column(Enum(StatusEnrollment), default=StatusEnrollment.TERDAFTAR, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    mahasiswa = relationship("Mahasiswa", back_populates="enrollments")
    mata_kuliah = relationship("MataKuliah", back_populates="enrollments")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("nilai IS NULL OR (nilai >= 0 AND nilai <= 100)", name="check_nilai_range"),
        CheckConstraint("semester >= 1 AND semester <= 8", name="check_enrollment_semester"),
        UniqueConstraint('nim', 'mata_kuliah_id', 'tahun_akademik', name='uq_enrollment_per_tahun'),
        Index('idx_enrollment_nim_tahun', 'nim', 'tahun_akademik'),
    )
    
    def __repr__(self) -> str:
        return f"<Enrollment(nim={self.nim}, mata_kuliah_id={self.mata_kuliah_id})>"
