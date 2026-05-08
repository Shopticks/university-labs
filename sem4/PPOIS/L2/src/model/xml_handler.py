from datetime import date
from pathlib import Path
from xml.dom.minidom import Document
from xml.sax import parse as sax_parse
from xml.sax.handler import ContentHandler

from src.model.pet_record import PetRecord


FIELDS = ["pet_name", "birth_date", "last_visit_date", "vet_name", "diagnosis"]
DATE_FIELDS = {"birth_date", "last_visit_date"}
ROOT_TAG = "pet_records"
ITEM_TAG = "pet_record"


class _DOMExporter:
    def export(self, records: list[PetRecord], path: Path) -> None:
        doc = Document()
        root = doc.createElement(ROOT_TAG)
        doc.appendChild(root)

        for record in records:
            item = doc.createElement(ITEM_TAG)
            for field_name in FIELDS:
                value = getattr(record, field_name)
                serialized = value.isoformat() if field_name in DATE_FIELDS else str(value)

                child = doc.createElement(field_name)
                child.appendChild(doc.createTextNode(serialized))
                item.appendChild(child)
            root.appendChild(item)

        path.write_text(doc.toprettyxml(indent="  "), encoding="utf-8")


class _SAXContentHandler(ContentHandler):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[PetRecord] = []
        self._current: dict | None = None
        self._buf: list[str] = []
        self._field: str | None = None

    def startElement(self, name, attrs):
        if name == ITEM_TAG:
            self._current = {}
        elif name in FIELDS and self._current is not None:
            self._field = name
            self._buf = []

    def characters(self, content):
        if self._field is not None:
            self._buf.append(content)

    def endElement(self, name):
        if name in FIELDS and self._current is not None:
            text = "".join(self._buf).strip()
            self._current[name] = date.fromisoformat(text) if name in DATE_FIELDS else text
            self._field = None
            self._buf = []
        elif name == ITEM_TAG and self._current is not None:
            self.records.append(PetRecord(**self._current))
            self._current = None


class _SAXImporter:
    def import_(self, path: Path) -> list[PetRecord]:
        handler = _SAXContentHandler()
        sax_parse(str(path), handler)
        return handler.records


class XmlHandler:
    def __init__(self) -> None:
        self._exporter = _DOMExporter()
        self._importer = _SAXImporter()

    def export(self, records: list[PetRecord], path: Path) -> None:
        self._exporter.export(records, path)

    def import_(self, path: Path) -> list[PetRecord]:
        return self._importer.import_(path)
