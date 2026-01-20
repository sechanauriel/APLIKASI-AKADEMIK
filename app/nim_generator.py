"""NIM Generator - Generate identifier unik dengan format institusional"""
from sqlalchemy.orm import Session
from app.models import Mahasiswa
from datetime import datetime


class NIMGenerator:
    """
    NIM Generator dengan format institusional:
    TAHUN-KODE_PRODI-NOMOR_URUT
    
    Contoh: 2024-10-0001
    - 2024: Tahun masuk
    - 10: Kode program studi (TI=10, SI=20, IF=30, etc)
    - 0001: Nomor urut (4 digit)
    """
    
    # Mapping kode program studi
    PROGRAM_STUDI_CODES = {
        "teknik_informatika": "10",
        "sistem_informasi": "20",
        "ilmu_komputer": "30",
        "rekayasa_perangkat_lunak": "40",
        "cybersecurity": "50",
    }
    
    @staticmethod
    def get_prodi_code(program_studi: str) -> str:
        """
        Get kode program studi dari nama program studi
        
        Args:
            program_studi: Nama program studi
            
        Returns:
            Kode program studi (2 digit)
            
        Raises:
            ValueError: Jika program studi tidak ditemukan
        """
        program_studi_lower = program_studi.lower().replace(" ", "_")
        
        if program_studi_lower not in NIMGenerator.PROGRAM_STUDI_CODES:
            available = ", ".join(NIMGenerator.PROGRAM_STUDI_CODES.keys())
            raise ValueError(
                f"Program studi '{program_studi}' tidak ditemukan. "
                f"Program studi yang tersedia: {available}"
            )
        
        return NIMGenerator.PROGRAM_STUDI_CODES[program_studi_lower]
    
    @staticmethod
    def generate_nim(db: Session, program_studi: str, tahun_masuk: int) -> str:
        """
        Generate NIM unik dengan format TAHUN-KODE_PRODI-NOMOR_URUT
        
        Args:
            db: Database session
            program_studi: Nama program studi
            tahun_masuk: Tahun masuk mahasiswa
            
        Returns:
            NIM yang unik (string format YYYY-KK-NNNN)
            
        Raises:
            ValueError: Jika program studi tidak valid
        """
        # Validasi program studi
        prodi_code = NIMGenerator.get_prodi_code(program_studi)
        
        # Cari nomor urut terakhir untuk tahun dan program studi ini
        last_nim = db.query(Mahasiswa).filter(
            Mahasiswa.tahun_masuk == tahun_masuk,
            Mahasiswa.program_studi == program_studi
        ).order_by(Mahasiswa.nim.desc()).first()
        
        if last_nim:
            # Extract nomor urut dari NIM terakhir
            # Format: YYYY-KK-NNNN
            parts = last_nim.nim.split("-")
            last_number = int(parts[2])
            next_number = last_number + 1
        else:
            next_number = 1
        
        # Format NIM: TAHUN-KODE_PRODI-NOMOR_URUT
        nim = f"{tahun_masuk}-{prodi_code}-{next_number:04d}"
        
        return nim
    
    @staticmethod
    def validate_nim_format(nim: str) -> bool:
        """
        Validasi format NIM
        
        Args:
            nim: NIM yang akan divalidasi
            
        Returns:
            True jika format valid, False sebaliknya
        """
        parts = nim.split("-")
        
        if len(parts) != 3:
            return False
        
        try:
            # Cek format YYYY-KK-NNNN
            int(parts[0])  # Tahun (4 digit)
            int(parts[1])  # Kode prodi (2 digit)
            int(parts[2])  # Nomor urut (4 digit)
            
            return (
                len(parts[0]) == 4 and
                len(parts[1]) == 2 and
                len(parts[2]) == 4
            )
        except ValueError:
            return False
    
    @staticmethod
    def parse_nim(nim: str) -> dict:
        """
        Parse NIM ke dalam komponen-komponennya
        
        Args:
            nim: NIM yang akan diparse
            
        Returns:
            Dictionary dengan keys: tahun_masuk, kode_prodi, nomor_urut
            
        Raises:
            ValueError: Jika format NIM tidak valid
        """
        if not NIMGenerator.validate_nim_format(nim):
            raise ValueError(f"Format NIM '{nim}' tidak valid. Harus format YYYY-KK-NNNN")
        
        parts = nim.split("-")
        return {
            "tahun_masuk": int(parts[0]),
            "kode_prodi": parts[1],
            "nomor_urut": int(parts[2]),
        }


def generate_unique_nim(db: Session, program_studi: str, tahun_masuk: int) -> str:
    """
    Convenience function untuk generate NIM unik
    
    Args:
        db: Database session
        program_studi: Nama program studi
        tahun_masuk: Tahun masuk
        
    Returns:
        NIM yang unik
    """
    return NIMGenerator.generate_nim(db, program_studi, tahun_masuk)
