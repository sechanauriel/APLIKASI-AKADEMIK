"""REST API endpoints untuk Mahasiswa"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Mahasiswa
from app.schemas import MahasiswaCreate, MahasiswaUpdate, MahasiswaResponse
from app.nim_generator import generate_unique_nim

router = APIRouter(prefix="/api/mahasiswa", tags=["Mahasiswa"])


@router.post(
    "", 
    response_model=MahasiswaResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Buat Mahasiswa Baru",
    description="Membuat mahasiswa baru dengan NIM yang di-generate otomatis"
)
def create_mahasiswa(
    mahasiswa_data: MahasiswaCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk membuat mahasiswa baru
    
    - **nama**: Nama mahasiswa (min 3 karakter)
    - **email**: Email unik mahasiswa
    - **no_telepon**: Nomor telepon (10-15 digit)
    - **tanggal_lahir**: Format YYYY-MM-DD
    - **jenis_kelamin**: laki-laki atau perempuan
    - **program_studi**: Nama program studi
    - **tahun_masuk**: Tahun masuk mahasiswa
    """
    
    # Cek apakah email sudah digunakan
    existing_email = db.query(Mahasiswa).filter(
        Mahasiswa.email == mahasiswa_data.email
    ).first()
    
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{mahasiswa_data.email}' sudah terdaftar"
        )
    
    try:
        # Generate NIM otomatis
        nim = generate_unique_nim(
            db,
            mahasiswa_data.program_studi,
            mahasiswa_data.tahun_masuk
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    # Create mahasiswa baru
    db_mahasiswa = Mahasiswa(
        nim=nim,
        nama=mahasiswa_data.nama,
        email=mahasiswa_data.email,
        no_telepon=mahasiswa_data.no_telepon,
        alamat=mahasiswa_data.alamat,
        tanggal_lahir=mahasiswa_data.tanggal_lahir,
        jenis_kelamin=mahasiswa_data.jenis_kelamin,
        program_studi=mahasiswa_data.program_studi,
        tahun_masuk=mahasiswa_data.tahun_masuk,
        status=mahasiswa_data.status
    )
    
    db.add(db_mahasiswa)
    try:
        db.commit()
        db.refresh(db_mahasiswa)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error membuat mahasiswa: {str(e)}"
        )
    
    return db_mahasiswa


@router.get(
    "", 
    response_model=list[MahasiswaResponse],
    summary="List Mahasiswa",
    description="Mendapatkan list semua mahasiswa dengan pagination"
)
def list_mahasiswa(
    skip: int = 0,
    limit: int = 10,
    program_studi: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk mendapatkan list mahasiswa
    
    Query parameters:
    - **skip**: Jumlah record yang di-skip (default: 0)
    - **limit**: Jumlah record yang ditampilkan (default: 10, max: 100)
    - **program_studi**: Filter berdasarkan program studi
    - **status**: Filter berdasarkan status (aktif, tidak_aktif, lulus, keluar)
    """
    
    query = db.query(Mahasiswa)
    
    if program_studi:
        query = query.filter(Mahasiswa.program_studi.ilike(f"%{program_studi}%"))
    
    if status:
        try:
            query = query.filter(Mahasiswa.status == status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Status '{status}' tidak valid"
            )
    
    limit = min(limit, 100)  # Max limit 100
    mahasiswa_list = query.offset(skip).limit(limit).all()
    
    return mahasiswa_list


@router.get(
    "/{nim}", 
    response_model=MahasiswaResponse,
    summary="Get Detail Mahasiswa",
    description="Mendapatkan detail mahasiswa berdasarkan NIM"
)
def get_mahasiswa(nim: str, db: Session = Depends(get_db)):
    """Endpoint untuk mendapatkan detail mahasiswa"""
    
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()
    
    if not mahasiswa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mahasiswa dengan NIM '{nim}' tidak ditemukan"
        )
    
    return mahasiswa


@router.put(
    "/{nim}", 
    response_model=MahasiswaResponse,
    summary="Update Mahasiswa",
    description="Mengupdate data mahasiswa"
)
def update_mahasiswa(
    nim: str,
    mahasiswa_data: MahasiswaUpdate,
    db: Session = Depends(get_db)
):
    """Endpoint untuk mengupdate mahasiswa"""
    
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()
    
    if not mahasiswa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mahasiswa dengan NIM '{nim}' tidak ditemukan"
        )
    
    # Cek apakah email baru sudah digunakan
    if mahasiswa_data.email and mahasiswa_data.email != mahasiswa.email:
        existing_email = db.query(Mahasiswa).filter(
            Mahasiswa.email == mahasiswa_data.email
        ).first()
        
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{mahasiswa_data.email}' sudah terdaftar"
            )
    
    # Update field yang disediakan
    update_data = mahasiswa_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(mahasiswa, field, value)
    
    try:
        db.commit()
        db.refresh(mahasiswa)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error mengupdate mahasiswa: {str(e)}"
        )
    
    return mahasiswa


@router.delete(
    "/{nim}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Mahasiswa",
    description="Menghapus mahasiswa beserta semua enrollmentnya"
)
def delete_mahasiswa(nim: str, db: Session = Depends(get_db)):
    """Endpoint untuk menghapus mahasiswa"""
    
    mahasiswa = db.query(Mahasiswa).filter(Mahasiswa.nim == nim).first()
    
    if not mahasiswa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mahasiswa dengan NIM '{nim}' tidak ditemukan"
        )
    
    try:
        db.delete(mahasiswa)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error menghapus mahasiswa: {str(e)}"
        )
