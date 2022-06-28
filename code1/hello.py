
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Connection à la base de donnée et définition des tables pour sqlalchemy
engine = create_engine('sqlite:///data/base_chapitre.db', convert_unicode=True, echo=True,connect_args={"check_same_thread": False})
Base = declarative_base()
Base.metadata.reflect(engine)
class Chapitre(Base):
    __table__ = Base.metadata.tables['items_C']
class Sous_Chapitre(Base):
    __table__ = Base.metadata.tables['souschapitre_C']
class Objectifs(Base):
    __table__ = Base.metadata.tables['objectifs_C']
class Theme(Base):
    __table__ = Base.metadata.tables["theme"]
class Eleves(Base):
    __table__ = Base.metadata.tables["eleves"]
class Note(Base):
    __table__ = Base.metadata.tables["note"]

# Connection la base de donnée
db_session = scoped_session(sessionmaker(bind=engine))


id = 15