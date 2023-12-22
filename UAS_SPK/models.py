from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class tbl_cushion(Base):
    __tablename__ = 'tbl_cushion'
    brand_cushion: Mapped[str] = mapped_column(primary_key=True)
    reputasi_brand: Mapped[int] = mapped_column()
    kandungan_spf: Mapped[int] = mapped_column()
    ketahanan: Mapped[int] = mapped_column()
    isi_kemasan: Mapped[int] = mapped_column()
    harga: Mapped[int] = mapped_column()
    
    def __repr__(self) -> str:
        return f"tbl_cushion(brand_cushion={self.brand_cushion!r}, reputasi_brand={self.reputasi_brand!r})"