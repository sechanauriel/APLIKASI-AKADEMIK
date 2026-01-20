"""Pydantic schemas untuk validasi input"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from app.models import StatusMahasiswa, StatusEnrollment, JenisKelamin


# ============ MAHASISWA SCHEMAS ============

class MahasiswaBase(BaseModel):
    """Base schema untuk Mahasiswa - validasi input"""
    nama: str = Field(..., min_length=3, max_length=100, description="Nama mahasiswa")
    email: EmailStr = Field(..., description="Email mahasiswa")
    no_telepon: str = Field(..., min_length=10, max_length=15, description="Nomor telepon")
    alamat: Optional[str] = Field(None, max_length=255, description="Alamat mahasiswa")
    tanggal_lahir: str = Field(..., description="Tanggal lahir (format: YYYY-MM-DD)")
    jenis_kelamin: JenisKelamin = Field(..., description="Jenis kelamin")
    program_studi: str = Field(..., min_length=3, max_length=50, description="Program studi")
    tahun_masuk: int = Field(..., ge=2000, le=2100, description="Tahun masuk")
    status: Optional[StatusMahasiswa] = Field(
        StatusMahasiswa.AKTIF, 
        description="Status mahasiswa"
    )
    
    @field_validator('tanggal_lahir')
    @classmethod
    def validate_tanggal_lahir(cls, v):
        """Validasi format tanggal lahir"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Tanggal lahir harus format YYYY-MM-DD')
    
    @field_validator('nama')
    @classmethod
    def validate_nama(cls, v):
        """Validasi nama tidak boleh hanya angka"""
        if v.isdigit():
            raise ValueError('Nama tidak boleh hanya berisi angka')
        return v


class MahasiswaCreate(MahasiswaBase):
    """Schema untuk membuat Mahasiswa baru"""
    pass


class MahasiswaUpdate(BaseModel):
    """Schema untuk update Mahasiswa"""
    nama: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    no_telepon: Optional[str] = Field(None, min_length=10, max_length=15)
    alamat: Optional[str] = Field(None, max_length=255)
    tanggal_lahir: Optional[str] = None
    jenis_kelamin: Optional[JenisKelamin] = None
    program_studi: Optional[str] = Field(None, min_length=3, max_length=50)
    status: Optional[StatusMahasiswa] = None
    
    @field_validator('tanggal_lahir')
    @classmethod
    def validate_tanggal_lahir(cls, v):
        """Validasi format tanggal lahir"""
        if v is None:
            return v
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Tanggal lahir harus format YYYY-MM-DD')


class MahasiswaResponse(MahasiswaBase):
    """Schema response untuk Mahasiswa"""
    nim: str = Field(..., description="Nomor Identitas Mahasiswa")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ MATA KULIAH SCHEMAS ============

class MataKuliahBase(BaseModel):
    """Base schema untuk Mata Kuliah - validasi input"""
    kode: str = Field(..., min_length=3, max_length=20, description="Kode mata kuliah")
    nama: str = Field(..., min_length=3, max_length=100, description="Nama mata kuliah")
    deskripsi: Optional[str] = Field(None, max_length=500, description="Deskripsi mata kuliah")
    sks: int = Field(..., ge=1, le=6, description="Satuan Kredit Semester (1-6)")
    semester: int = Field(..., ge=1, le=8, description="Semester (1-8)")
    program_studi: str = Field(..., min_length=3, max_length=50, description="Program studi")
    
    @field_validator('kode')
    @classmethod
    def validate_kode(cls, v):
        """Validasi kode mata kuliah"""
        if not v.isupper() and not v.isalnum():
            raise ValueError('Kode harus alphanumeric')
        return v


class MataKuliahCreate(MataKuliahBase):
    """Schema untuk membuat Mata Kuliah baru"""
    pass


class MataKuliahUpdate(BaseModel):
    """Schema untuk update Mata Kuliah"""
    kode: Optional[str] = Field(None, min_length=3, max_length=20)
    nama: Optional[str] = Field(None, min_length=3, max_length=100)
    deskripsi: Optional[str] = Field(None, max_length=500)
    sks: Optional[int] = Field(None, ge=1, le=6)
    semester: Optional[int] = Field(None, ge=1, le=8)
    program_studi: Optional[str] = Field(None, min_length=3, max_length=50)


class MataKuliahResponse(MataKuliahBase):
    """Schema response untuk Mata Kuliah"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ ENROLLMENT SCHEMAS ============

class EnrollmentBase(BaseModel):
    """Base schema untuk Enrollment - validasi input"""
    nim: str = Field(..., description="NIM mahasiswa")
    mata_kuliah_id: int = Field(..., description="ID mata kuliah")
    nilai: Optional[float] = Field(None, ge=0, le=100, description="Nilai (0-100)")
    semester: int = Field(..., ge=1, le=8, description="Semester")
    tahun_akademik: str = Field(..., description="Tahun akademik (format: YYYY/YYYY)")
    status: Optional[StatusEnrollment] = Field(
        StatusEnrollment.TERDAFTAR,
        description="Status enrollment"
    )
    
    @field_validator('tahun_akademik')
    @classmethod
    def validate_tahun_akademik(cls, v):
        """Validasi format tahun akademik"""
        parts = v.split('/')
        if len(parts) != 2:
            raise ValueError('Tahun akademik harus format YYYY/YYYY')
        try:
            int(parts[0])
            int(parts[1])
        except ValueError:
            raise ValueError('Tahun akademik harus format YYYY/YYYY')
        return v


class EnrollmentCreate(EnrollmentBase):
    """Schema untuk membuat Enrollment baru"""
    pass


class EnrollmentUpdate(BaseModel):
    """Schema untuk update Enrollment"""
    nilai: Optional[float] = Field(None, ge=0, le=100)
    status: Optional[StatusEnrollment] = None


class EnrollmentResponse(EnrollmentBase):
    """Schema response untuk Enrollment"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ ERROR SCHEMAS ============

class ErrorResponse(BaseModel):
    """Schema untuk error response"""
    detail: str
    error_code: Optional[str] = None
    timestamp: Optional[datetime] = None


class ValidationErrorResponse(BaseModel):
    """Schema untuk validation error response"""
    detail: list
    error_code: str = "VALIDATION_ERROR"
