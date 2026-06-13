import os

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/produtos_db"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

app = FastAPI()


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)


class ProdutoCreate(BaseModel):
    nome: str = Field(..., min_length=1)
    preco: float = Field(..., gt=0)
    estoque: int = 0
    ativo: bool = True


class ProdutoResponse(ProdutoCreate):
    id: int

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/produtos", response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()


@app.post(
    "/produtos",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo = Produto(**produto.model_dump())

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


@app.get("/produtos/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(
        Produto.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return produto


@app.delete(
    "/produtos/{produto_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(
        Produto.id == produto_id
    ).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    db.delete(produto)
    db.commit()