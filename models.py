from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Text, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
DATABASE_FILE_PATH = 'db.sqlite3'
class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password = Column(String(255))
    permissions = Column(String(255))

class Adresse(Base):
    __tablename__ = 'adresse'
    id = Column(Integer, primary_key=True)
    strasse = Column(String(255))
    plz = Column(String(10))
    stadt = Column(String(255))

    def __repr__(self):
        return f"<Adresse(strasse={self.strasse}, plz={self.plz}, stadt={self.stadt})>"


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    adresse_id = Column(Integer, ForeignKey('adresse.id'))
    adresse = relationship('Adresse')
    telefon = Column(String(17), nullable=True)

    def __repr__(self):
        return f"<Person(name={self.name}, adresse={self.adresse}, telefon={self.telefon})>"


class FestplattenImageNotebook(Base):
    __tablename__ = 'festplatten_image_notebook'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    beschreibung = Column(Text, nullable=True)

    def __repr__(self):
        return f"<FestplattenImageNotebook(name={self.name}, beschreibung={self.beschreibung})>"


class FestplattenImageServer(Base):
    __tablename__ = 'festplatten_image_server'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    beschreibung = Column(Text, nullable=True)

    def __repr__(self):
        return f"<FestplattenImageServer(name={self.name}, beschreibung={self.beschreibung})>"


class Schiene(Base):
    __tablename__ = 'schiene'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    status = Column(Enum('Lager', 'Unterwegs', 'Zurücksetzen', 'Imagen', 'Versand', 'Standort', 'Rückholung', 'Weiterleitung', 'Selbstabholung'), nullable=False)
    drucker_fuellstand_a = Column(Integer, default=100)
    drucker_fuellstand_b = Column(Integer, default=100)
    nighthawk = Column(String(10), default='Beispiel: NH 01')
    datum_kms_aktivierung = Column(Date)
    image_id = Column(Integer, ForeignKey('festplatten_image_notebook.id'))
    image = relationship('FestplattenImageNotebook')
    bemerkung = Column(String(500), default="Fehler/Bemerkung")

    def __repr__(self):
        return f"<Schiene(name={self.name}, status={self.status}, drucker_fuellstand_a={self.drucker_fuellstand_a}, drucker_fuellstand_b={self.drucker_fuellstand_b}, nighthawk={self.nighthawk}, datum_kms_aktivierung={self.datum_kms_aktivierung}, image={self.image}, bemerkung={self.bemerkung})>"


class Server(Base):
    __tablename__ = 'server'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    status = Column(Enum('Lager', 'Unterwegs', 'Zurücksetzen', 'Imagen', 'Versand', 'Standort', 'Rückholung', 'Weiterleitung', 'Selbstabholung'), nullable=False)
    image_id = Column(Integer, ForeignKey('festplatten_image_server.id'), nullable=True)
    image = relationship('FestplattenImageServer')
    bemerkung = Column(String(500), default="Fehler/Bemerkung")

    def __repr__(self):
        return f"<Server(name={self.name}, status={self.status}, image={self.image}, bemerkung={self.bemerkung})>"


class Kunde(Base):
    __tablename__ = 'kunde'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    typ = Column(Enum('Firma', 'Behörde'), nullable=False)
    adresse_id = Column(Integer, ForeignKey('adresse.id'))
    adresse = relationship('Adresse')

    def __repr__(self):
        return f"<Kunde(name={self.name}, typ={self.typ}, adresse={self.adresse})>"


class Ansprechpartner(Base):
    __tablename__ = 'ansprechpartner'
    id = Column(Integer, primary_key=True)
    kunde_id = Column(Integer, ForeignKey('kunde.id'), nullable=True)
    kunde = relationship('Kunde', back_populates='ansprechpartner')
    anrede = Column(Enum('Frau', 'Herr'), default='Herr')
    vorname = Column(String(255), nullable=True)
    nachname = Column(String(255), default='Müller/Meier/Schmitz')
    telefon = Column(String(17), nullable=True)

    def __repr__(self):
        return f"<Ansprechpartner(kunde={self.kunde}, anrede={self.anrede}, vorname={self.vorname}, nachname={self.nachname}, telefon={self.telefon})>"


class Kurs(Base):
    __tablename__ = 'kurs'
    id = Column(Integer, primary_key=True)
    va_nummer = Column(Integer, unique=True)
    thema = Column(String(50), default='Outlook')
    trainer_id = Column(Integer, ForeignKey('person.id'), nullable=True)
    trainer = relationship('Person', back_populates='kurse')
    kunde_id = Column(Integer, ForeignKey('kunde.id'), nullable=True)
    kunde = relationship('Kunde', back_populates='kurse')
    schiene_id = Column(Integer, ForeignKey('schiene.id'), nullable=True)
    schiene = relationship('Schiene', back_populates='kurse')
    server_id = Column(Integer, ForeignKey('server.id'), nullable=True)
    server = relationship('Server', back_populates='kurse')
    kurs_start = Column(DateTime, nullable=True)
    kurs_ende = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Kurs(va_nummer={self.va_nummer}, thema={self.thema}, trainer={self.trainer}, kunde={self.kunde}, schiene={self.schiene}, server={self.server}, kurs_start={self.kurs_start}, kurs_ende={self.kurs_ende})>"


class UebersichtsTabelle(Base):
    __tablename__ = 'uebersichtstabelle'
    id = Column(Integer, primary_key=True)
    kurs_id = Column(Integer, ForeignKey('kurs.id'))
    kurs = relationship('Kurs')
    von_datum = Column(Date, nullable=False)
    bis_datum = Column(Date, nullable=False)
    beschreibung = Column(Text)

    def __repr__(self):
        return f"<UebersichtsTabelle(kurs={self.kurs}, von_datum={self.von_datum}, bis_datum={self.bis_datum}, beschreibung={self.beschreibung})>"


# Create a SQLite database in memory and create tables
engine = create_engine(f'sqlite:///{DATABASE_FILE_PATH}')
# Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()
