import uuid
from datetime import date
from typing import Any

from PySide6.QtCore import QObject, Signal
from sqlalchemy import create_engine, UUID, String, Date, text
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, Query

from src.model.pet_record import PetRecord


class Base(DeclarativeBase):
    pass


class PetRecordORM(Base):
    __tablename__ = "pet_records"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    pet_name: Mapped[str] = mapped_column(String(length=50), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    last_visit_date: Mapped[date] = mapped_column(Date, nullable=False)
    vet_name: Mapped[str] = mapped_column(String(length=200), nullable=False)
    diagnosis: Mapped[str] = mapped_column(String(length=500), nullable=False)


class DBManager(QObject):
    data_changed = Signal()

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        dbname: str = "vetjournal",
        user: str = "postgres",
        password: str = "password",
    ):
        super().__init__()
        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
        self._engine = create_engine(url, echo=False)
        Base.metadata.create_all(self._engine)

    @staticmethod
    def _to_orm(r: PetRecord) -> PetRecordORM:
        return PetRecordORM(
            pet_name=r.pet_name,
            birth_date=r.birth_date,
            last_visit_date=r.last_visit_date,
            vet_name=r.vet_name,
            diagnosis=r.diagnosis,
        )

    @staticmethod
    def _from_orm(r: PetRecordORM) -> PetRecord:
        return PetRecord(
            pet_name=r.pet_name,
            birth_date=r.birth_date,
            last_visit_date=r.last_visit_date,
            vet_name=r.vet_name,
            diagnosis=r.diagnosis,
            id=r.id,
        )

    def _build_filter_query(self, session: Session, criteria: dict[str, Any]) -> Query:
        query = session.query(PetRecordORM)
        if pet_name := criteria.get("pet_name"):
            query = query.filter(PetRecordORM.pet_name.ilike(f"%{pet_name}%"))
        if vet_name := criteria.get("vet_name"):
            query = query.filter(PetRecordORM.vet_name.ilike(f"%{vet_name}%"))
        if diagnosis := criteria.get("diagnosis_phrase"):
            query = query.filter(PetRecordORM.diagnosis.ilike(f"%{diagnosis}%"))
        if birth_date := criteria.get("birth_date"):
            query = query.filter(PetRecordORM.birth_date == birth_date)
        if last_visit_date := criteria.get("last_visit_date"):
            query = query.filter(PetRecordORM.last_visit_date == last_visit_date)
        return query

    def get_total_count(self) -> int:
        with Session(self._engine) as session:
            return session.query(PetRecordORM).count()

    def get_page(self, page: int, per_page: int) -> list[PetRecord]:
        with Session(self._engine) as session:
            offset = (page - 1) * per_page
            rows = (
                session.query(PetRecordORM)
                .order_by(PetRecordORM.last_visit_date.desc(), PetRecordORM.id)
                .offset(offset)
                .limit(per_page)
                .all()
            )
            return [self._from_orm(r) for r in rows]

    def get_all(self) -> list[PetRecord]:
        with Session(self._engine) as session:
            rows = (
                session.query(PetRecordORM)
                .order_by(PetRecordORM.last_visit_date.desc(), PetRecordORM.id)
                .all()
            )
            return [self._from_orm(r) for r in rows]

    def add(self, record: PetRecord) -> None:
        with Session(self._engine) as session:
            session.add(self._to_orm(record))
            session.commit()
        self.data_changed.emit()

    def search(self, criteria: dict[str, Any]) -> list[PetRecord]:
        with Session(self._engine) as session:
            query = self._build_filter_query(session, criteria)
            return [self._from_orm(r) for r in query.all()]

    def count_matching(self, criteria: dict[str, Any]) -> int:
        with Session(self._engine) as session:
            return self._build_filter_query(session, criteria).count()

    def delete_matching(self, criteria: dict[str, Any]) -> int:
        with Session(self._engine) as session:
            query = self._build_filter_query(session, criteria)
            count = query.delete(synchronize_session=False)
            session.commit()
        if count > 0:
            self.data_changed.emit()
        return count

    def replace_all(self, records: list[PetRecord]) -> None:
        with Session(self._engine) as session:
            session.query(PetRecordORM).delete()
            session.add_all(self._to_orm(r) for r in records)
            session.commit()
        self.data_changed.emit()

    def close(self) -> None:
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None