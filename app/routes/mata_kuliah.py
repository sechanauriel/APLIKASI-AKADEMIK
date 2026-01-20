"""REST API endpoints untuk Mata Kuliah"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import MataKuliah
from app.schemas import MataKuliahCreate, MataKuliahUpdate, MataKuliahResponse

router = APIRouter(prefix="/api/mata-kuliah", tags=["Mata Kuliah"])


@router.post(
    "", 
    response_model=MataKuliahResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Buat Mata Kuliah Baru",
    description="Membuat mata kuliah baru"
)
def create_mata_kuliah(
    mata_kuliah_data: MataKuliahCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk membuat mata kuliah baru
    
    - **kode**: Kode unik mata kuliah
    - **nama**: Nama mata kuliah
    - **sks**: SKS (1-6)
    - **semester**: Semester (1-8)
    - **program_studi**: Program studi yang menyelenggarakan
    """
    
    # Cek apakah kode sudah digunakan
    existing_kode = db.query(MataKuliah).filter(
        MataKuliah.kode == mata_kuliah_data.kode
    ).first()
    
    if existing_kode:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Kode mata kuliah '{mata_kuliah_data.kode}' sudah terdaftar"
        )
    
    # Create mata kuliah baru
    db_mata_kuliah = MataKuliah(
        kode=mata_kuliah_data.kode,
        nama=mata_kuliah_data.nama,
        deskripsi=mata_kuliah_data.deskripsi,
        sks=mata_kuliah_data.sks,
        semester=mata_kuliah_data.semester,
        program_studi=mata_kuliah_data.program_studi
    )
    
    db.add(db_mata_kuliah)
    try:
        db.commit()
        db.refresh(db_mata_kuliah)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error membuat mata kuliah: {str(e)}"
        )
    
    return db_mata_kuliah


@router.get(
    "", 
    response_model=list[MataKuliahResponse],
    summary="List Mata Kuliah",
    description="Mendapatkan list semua mata kuliah"
)
def list_mata_kuliah(
    skip: int = 0,
    limit: int = 10,
    program_studi: str = None,
    semester: int = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk mendapatkan list mata kuliah
    
    Query parameters:
    - **skip**: Jumlah record yang di-skip
    - **limit**: Jumlah record yang ditampilkan
    - **program_studi**: Filter berdasarkan program studi
    - **semester**: Filter berdasarkan semester
    """
    
    query = db.query(MataKuliah)
    
    if program_studi:
        query = query.filter(MataKuliah.program_studi.ilike(f"%{program_studi}%"))
    
    if semester:
        if not (1 <= semester <= 8):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Semester harus antara 1-8"
            )
        query = query.filter(MataKuliah.semester == semester)
    
    limit = min(limit, 100)
    mata_kuliah_list = query.offset(skip).limit(limit).all()
    
    return mata_kuliah_list


@router.get(
    "/{mata_kuliah_id}", 
    response_model=MataKuliahResponse,
    summary="Get Detail Mata Kuliah",
    description="Mendapatkan detail mata kuliah berdasarkan ID"
)
def get_mata_kuliah(mata_kuliah_id: int, db: Session = Depends(get_db)):
    """Endpoint untuk mendapatkan detail mata kuliah"""
    
    mata_kuliah = db.query(MataKuliah).filter(MataKuliah.id == mata_kuliah_id).first()
    
    if not mata_kuliah:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mata kuliah dengan ID {mata_kuliah_id} tidak ditemukan"
        )
    
    return mata_kuliah


@router.put(
    "/{mata_kuliah_id}", 
    response_model=MataKuliahResponse,
    summary="Update Mata Kuliah",
    description="Mengupdate data mata kuliah"
)
def update_mata_kuliah(
    mata_kuliah_id: int,
    mata_kuliah_data: MataKuliahUpdate,
    db: Session = Depends(get_db)
):
    """Endpoint untuk mengupdate mata kuliah"""
    
    mata_kuliah = db.query(MataKuliah).filter(MataKuliah.id == mata_kuliah_id).first()
    
    if not mata_kuliah:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mata kuliah dengan ID {mata_kuliah_id} tidak ditemukan"
        )
    
    # Cek apakah kode baru sudah digunakan
    if mata_kuliah_data.kode and mata_kuliah_data.kode != mata_kuliah.kode:
        existing_kode = db.query(MataKuliah).filter(
            MataKuliah.kode == mata_kuliah_data.kode
        ).first()
        
        if existing_kode:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Kode mata kuliah '{mata_kuliah_data.kode}' sudah terdaftar"
            )
    
    # Update field yang disediakan
    update_data = mata_kuliah_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(mata_kuliah, field, value)
    
    try:
        db.commit()
        db.refresh(mata_kuliah)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error mengupdate mata kuliah: {str(e)}"
        )
    
    return mata_kuliah


@router.delete(
    "/{mata_kuliah_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Mata Kuliah",
    description="Menghapus mata kuliah"
)
def delete_mata_kuliah(mata_kuliah_id: int, db: Session = Depends(get_db)):
    """Endpoint untuk menghapus mata kuliah"""
    
    mata_kuliah = db.query(MataKuliah).filter(MataKuliah.id == mata_kuliah_id).first()
    
    if not mata_kuliah:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mata kuliah dengan ID {mata_kuliah_id} tidak ditemukan"
        )
    
    try:
        db.delete(mata_kuliah)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error menghapus mata kuliah: {str(e)}"
        )
