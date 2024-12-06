from sqlalchemy import Column, Integer, String, Float, DateTime, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

Base = declarative_base()

class CandidateData(Base):
    __tablename__ = 'donnee_candidat'

    id = Column(Integer, primary_key=True)
    type_ligne = Column(String)
    identifiant_element = Column(Integer)
    structure = Column(String)
    statut_element = Column(String)
    nom_base_francais = Column(String)
    nom_attribut_francais = Column(String)
    nom_frontiere_francais = Column(String)
    code_categorie = Column(String)
    tags_francais = Column(ARRAY(String))
    unite_francais = Column(String)
    contributeur = Column(String)
    programme = Column(String)
    url_programme = Column(String)
    source = Column(String)
    localisation_geographique = Column(String)
    sous_localisation_geographique_francais = Column(String)
    date_creation = Column(DateTime)
    date_modification = Column(DateTime)
    periode_validite = Column(String)
    incertitude = Column(String)
    regulations = Column(String)
    transparence = Column(String)
    qualite = Column(String)
    qualite_ter = Column(String)
    qualite_gr = Column(String)
    qualite_tir = Column(String)
    qualite_c = Column(String)
    qualite_p = Column(String)
    qualite_m = Column(String)
    commentaire_francais = Column(String)
    type_poste = Column(String)
    nom_poste_francais = Column(String)
    total_poste_non_decompose = Column(Float)
    co2f = Column(Float)
    ch4f = Column(Float)
    ch4b = Column(Float)
    n2o = Column(Float)
    code_gaz_sup_1 = Column(String)
    valeur_gaz_sup_1 = Column(Float)
    code_gaz_sup_2 = Column(String)



# Pydantic model for DataItem validation
class CandidateDataModel(BaseModel):
    type_ligne: Optional[str] = None
    identifiant_element: Optional[str] = None
    structure: Optional[str] = None
    statut_element: Optional[str] = None
    nom_base_francais: Optional[str] = None
    nom_attribut_francais: Optional[str] = None
    nom_frontiere_francais: Optional[str] = None
    code_categorie: Optional[str] = None
    tags_francais: Optional[str] = None
    unite_francais: Optional[str] = None
    contributeur: Optional[str] = None
    programme: Optional[str] = None
    url_programme: Optional[str] = None
    source: Optional[str] = None
    localisation_geographique: Optional[str] = None
    sous_localisation_geographique_francais: Optional[str] = None
    date_creation: Optional[datetime] = None
    date_modification: Optional[datetime] = None
    periode_validite: Optional[str] = None
    incertitude: Optional[str] = None
    regulations: Optional[str] = None
    transparence: Optional[str] = None
    qualite: Optional[str] = None
    qualite_ter: Optional[str] = None
    qualite_gr: Optional[str] = None
    qualite_tir: Optional[str] = None
    qualite_c: Optional[str] = None
    qualite_p: Optional[str] = None
    qualite_m: Optional[str] = None
    commentaire_francais: Optional[str] = None
    type_poste: Optional[str] = None
    nom_poste_francais: Optional[str] = None
    total_poste_non_decompose: Optional[float] = None
    co2f: Optional[float] = None
    ch4f: Optional[float] = None
    ch4b: Optional[float] = None
    n2o: Optional[float] = None
    code_gaz_sup_1: Optional[str] = None
    valeur_gaz_sup_1: Optional[float] = None
    code_gaz_sup_2: Optional[str] = None
    valeur_gaz_sup_2: Optional[float] = None
    code_gaz_sup_3: Optional[str] = None
    valeur_gaz_sup_3: Optional[float] = None
    code_gaz_sup_4: Optional[str] = None
    valeur_gaz_sup_4: Optional[float] = None
    code_gaz_sup_5: Optional[str] = None
    valeur_gaz_sup_5: Optional[float] = None
    autres_ges: Optional[float] = None
    co2b: Optional[float] = None
