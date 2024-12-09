from sqlalchemy import Column, Integer, String, Float, DateTime, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

Base = declarative_base()

class EmissionsData(Base):
    __tablename__ = 'donnees_emissions'

    id = Column(Integer, primary_key=True)
    type_ligne = Column('Type Ligne', String)
    identifiant_element = Column('Identifiant de l\'élément', Integer)
    structure = Column('Structure', String)
    statut_element = Column('Statut de l\'élément', String)
    nom_base_francais = Column('Nom base français', String)
    nom_attribut_francais = Column('Nom attribut français', String)
    nom_frontiere_francais = Column('Nom frontière français', String)
    code_categorie = Column('Code de la catégorie', String)
    tags_francais = Column('Tags français', ARRAY(String))
    unite_francais = Column('Unité français', String)
    contributeur = Column('Contributeur', String)
    programme = Column('Programme', String)
    url_programme = Column('Url du programme', String)
    source = Column('Source', String)
    localisation_geographique = Column('Localisation géographique', String)
    sous_localisation_geographique_francais = Column('Sous-localisation géographique français', String)
    date_creation = Column('Date de création', DateTime)
    date_modification = Column('Date de modification', DateTime)
    periode_validite = Column('Période de validité', String)
    incertitude = Column('Incertitude', String)
    regulations = Column('Réglementations', String)
    transparence = Column('Transparence', String)
    qualite = Column('Qualité', String)
    qualite_ter = Column('Qualité TeR', String)
    qualite_gr = Column('Qualité GR', String)
    qualite_tir = Column('Qualité TiR', String)
    qualite_c = Column('Qualité C', String)
    qualite_p = Column('Qualité P', String)
    qualite_m = Column('Qualité M', String)
    commentaire_francais = Column('Commentaire français', String)
    type_poste = Column('Type poste', String)
    nom_poste_francais = Column('Nom poste français', String)
    total_poste_non_decompose = Column('Total poste non décomposé', Float)
    co2f = Column('CO2f', Float)
    ch4f = Column('CH4f', Float)
    ch4b = Column('CH4b', Float)
    n2o = Column('N2O', Float)
    code_gaz_sup_1 = Column('Code gaz supplémentaire 1', String)
    valeur_gaz_sup_1 = Column('Valeur gaz supplémentaire 1', Float)
    code_gaz_sup_2 = Column('Code gaz supplémentaire 2', String)
    valeur_gaz_sup_2 = Column('Valeur gaz supplémentaire 2', Float)
    code_gaz_sup_3 = Column('Code gaz supplémentaire 3', String)
    valeur_gaz_sup_3 = Column('Valeur gaz supplémentaire 3', Float)
    code_gaz_sup_4 = Column('Code gaz supplémentaire 4', String)
    valeur_gaz_sup_4 = Column('Valeur gaz supplémentaire 4', Float)
    code_gaz_sup_5 = Column('Code gaz supplémentaire 5', String)
    valeur_gaz_sup_5 = Column('Valeur gaz supplémentaire 5', Float)
    autres_ges = Column('Autres GES', Float)
    co2b = Column('CO2b', Float)


# Pydantic model for DataItem validation
class EmissionsDataModel(BaseModel):
    type_ligne: Optional[str] = None
    identifiant_element: Optional[int] = None
    structure: Optional[str] = None
    statut_element: Optional[str] = None
    nom_base_francais: Optional[str] = None
    nom_attribut_francais: Optional[str] = None
    nom_frontiere_francais: Optional[str] = None
    code_categorie: Optional[str] = None
    tags_francais: Optional[List[str]] = None
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

    class Config:
        from_attributes = True
