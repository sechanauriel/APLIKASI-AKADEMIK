"""REST API endpoints untuk Enrollment (Nilai Mahasiswa)"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Enrollment, Mahasiswa, MataKuliah
from app.schemas import EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse

router = APIRouter(prefix="/api/enrollment", tags=["Enrollment"])


@router.post(
    "", 
    response_model=EnrollmentResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Buat Enrollment Baru",
    description="Mendaftarkan mahasiswa ke mata kuliah"
)
def create_enrollment(
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk membuat enrollment baru
    
    - **nim**: NIM mahasiswa
    - **mata_kuliah_id**: ID mata kuliah
    - **semester**: Semester (1-8)
    - **tahun_akademik**: Format YYYY/YYYY
    """
    
    # Validasi mahasiswa exist
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.nim == enrollment_data.nim).first()
    if not mahasiswa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mahasiswa dengan NIM '{enrollment_data.nim}' tidak ditemukan"
        )
    
    # Validasi mata kuliah exist
    mata_kuliah = db.query(MataKuliah).filter(
        MataKuliah.id == enrollment_data.mata_kuliah_id
    ).first()
    if not mata_kuliah:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mata kuliah dengan ID {enrollment_data.mata_kuliah_id} tidak ditemukan"
        )
    
    # Cek apakah mahasiswa sudah terdaftar di mata kuliah ini untuk tahun akademik ini
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.nim == enrollment_data.nim,
        Enrollment.mata_kuliah_id == enrollment_data.mata_kuliah_id,
        Enrollment.tahun_akademik == enrollment_data.tahun_akademik
    ).first()
    
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mahasiswa sudah terdaftar di mata kuliah ini untuk tahun akademik {enrollment_data.tahun_akademik}"
        )
    
    # Create enrollment baru
    db_enrollment = Enrollment(
        nim=enrollment_data.nim,
        mata_kuliah_id=enrollment_data.mata_kuliah_id,
        nilai=enrollment_data.nilai,
        semester=enrollment_data.semester,
        tahun_akademik=enrollment_data.tahun_akademik,
        status=enrollment_data.status
    )
    
    db.add(db_enrollment)
    try:
        db.commit()
        db.refresh(db_enrollment)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error membuat enrollment: {str(e)}"
        )
    
    return db_enrollment


@router.get(
    "", 
    response_model=list[EnrollmentResponse],
    summary="List Enrollment",
    description="Mendapatkan list enrollment dengan filter"
)
def list_enrollment(
    skip: int = 0,
    limit: int = 10,
    nim: str = None,
    tahun_akademik: str = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk mendapatkan list enrollment
    
    Query parameters:
    - **skip**: Jumlah record yang di-skip
    - **limit**: Jumlah record yang ditampilkan
    - **nim**: Filter berdasarkan NIM mahasiswa
    - **tahun_akademik**: Filter berdasarkan tahun akademik
    """
    
    query = db.query(Enrollment)
    
    if nim:
        query = query.filter(Enrollment.nim == nim)
    
    if tahun_akademik:
        query = query.filter(Enrollment.tahun_akademik == tahun_akademik)
    
    limit = min(limit, 100)
    enrollment_list = query.offset(skip).limit(limit).all()
    
    return enrollment_list


@router.get(
    "/{enrollment_id}", 
    response_model=EnrollmentResponse,
    summary="Get Detail Enrollment",
    description="Mendapatkan detail enrollment"
)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    """Endpoint untuk mendapatkan detail enrollment"""
    
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment dengan ID {enrollment_id} tidak ditemukan"
        )
    
    return enrollment


@router.put(
    "/{enrollment_id}", 
    response_model=EnrollmentResponse,
    summary="Update Enrollment",
    description="Mengupdate data enrollment (nilai dan status)"
)
def update_enrollment(
    enrollment_id: int,
    enrollment_data: EnrollmentUpdate,
    db: Session = Depends(get_db)
):
    """Endpoint untuk mengupdate enrollment"""
    
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment dengan ID {enrollment_id} tidak ditemukan"
        )
    
    # Update field yang disediakan
    update_data = enrollment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(enrollment, field, value)
    
    try:
        db.commit()
        db.refresh(enrollment)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error mengupdate enrollment: {str(e)}"
        )
    
    return enrollment


@router.delete(
    "/{enrollment_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Enrollment",
    description="Menghapus enrollment"
)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    """Endpoint untuk menghapus enrollment"""
    
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment dengan ID {enrollment_id} tidak ditemukan"
        )
    
    try:
        db.delete(enrollment)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error menghapus enrollment: {str(e)}"
        )


@router.get(
    "/mahasiswa/{nim}/transkrip",
    response_model=list[EnrollmentResponse],
    summary="Get Transkrip Mahasiswa",
    description="Mendapatkan transkrip lengkap mahasiswa"
)
def get_transkrip_mahasiswa(nim: str, db: Session = Depends(get_db)):
    """
    Endpoint untuk mendapatkan transkrip lengkap mahasiswa
    
    Menampilkan semua enrollment dan nilai mahasiswa
    """
    
    # Validasi mahasiswa exist
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()
    if not mahasiswa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mahasiswa dengan NIM '{nim}' tidak ditemukan"
        )
    
    enrollments = db.query(Enrollment).filter(
        Enrollment.nim == nim
    ).order_by(Enrollment.tahun_akademik.desc()).all()
    
    return enrollments
