# ecoact_testtechnique

## Exploration

Pour ce test technique, j'ai passé un certain temps à essayer de comprendre la donnée. Celle ci est très peu structurée et elle était assez difficile à comprendre. Les données couvrent des concepts différents, proviennent de différentes sources, et les informations que je peux y extraire traduisent des concepts différents (les unités sont très variables, 

Pour l'explorer et l'exploiter, je me suis reposé en premier sur le champ 'Code de la catégorie' qui me donne une information sur le type d'information. Ce champ donne une information hiérarchisée sur le type de donnée. En prenant le premier niveau de ce champ, je peux décomposer mes données en une liste de valeurs : 
- Achats de biens
- Achats de services
- Combustibles
- Electricité
- PRG
- Process et émissions fugitives
- Réseaux de chaleur / froid
- Statistiques territoriales
- Traitement des déchets
- Transport de marchandises
- Transport de personnes
- UTCF

Pour chacune de ces catégories, on a sous catégories allant jsuq'à une profondeur de 5 sous catégories. 

Je fais le choix de me limiter aux données Combustibles, en France métropolitaine, et actives (selon le champ 'Statut de l'élément'). Ainsi, je peux construire un dashboard avec les émissions équivalent CO2 par unité des combustibles français, selon plusieurs niveaux d'aggrégation (fossile ou organique, puis gaz, solide ou liquide, puis le détail des émissions par élémént, et je laisse le choix de l'unité). 
Dans combustibles , il y a les informations à propos des pouvoirs calorifiques que j'ai choisi d'ignorer.
Il y a donc trois courbes dans mon dashboard : le taux d'émisision par unité par type (fossile ou organique), par état (liquide, soliden gaz) et selon une unité.
Puis, pour un combustible donné, le mix des émissions par type de gaz à effet de serre, puis le taux par poste d'émission.

###Propreté des données
Pour présenter une visualisation fiable, je me suis bien assuré d'avoir des données bein propres et d'avoir des aggrégats qui fonctionnent bien. 
Par exemple, je cherche des éléments uniques en discriminant par : la concaténation des champs 'nom base' et 'nom attribut', les trois premières valeurs du champ 'code de la catégorie', le champ 'unité français', et le 'type ligne' (qui prend valeur entre Poste et Elément).

J'obtiens un élément unique, et une liste de postes pour ce même élément. Ainsi, je me suis bien assuré d'avoir des données uniques. 
Par exemple, j'ai pu relever que l'indentifiant de l'élément est parfois le même pour un poste correspondant à l'élément, mais ce n'est pas toujours vrai. 

## Questions aux PO
Il faut noter que travailler sur les combustibles est un choix arbitraire que j'ai fait dans ce test technique. Le but ici est de montrer un POC de dashboard pour le cadre de l'entetien. Ce qui me mène à des questions que je peux poser au PO :
- Quel est le besoin pour ce dashboard ? En particulier, quelles sont les données que je cherche à comparer ? J'ai des détails d'émission en France Métropolitaine, en Europe et Outre-Mer, voulons nous comparer les zones géographiques ? Souhaitons nous exploiter d'autres inforations comme les types de réglementation, la transparence ? 
- Quelles sont les informations pertinents à croiser pour un dashboard efficace ? Ici je n'ai mis que les informations sur les Combustibles.
- Quels sont les défis en terme de performance attendus pour l'API, et les applis web en dash ? 
- Il y a t il une métrique pour évaluer l'efficacité des outils de visualisation ? Pouvons nous mesurer l'impact des outils au traffic par courbe ou dashboard ?
- Quelles sont les données que nous souhaitons laisser à disposition en API ? Je n'ai pas pris en compte le champ qualité des données, est ce à prendre en compte ?
- Je n'ai exploité que les données actives, il y a t il un usage pour les données d'archive ?
- Je peux aussi penser à des questions plus larges, quelles seraient les questions auxquelles on souhaite répondre avec ces dashboards ? Idéalement, je ferai un peu de recherche utilisateur avec des experts pour essayer d'identifer des points bloquants auxquels je peux répondre pour leur faire gagner du temps.
- J'ai fait un choix de design de laisser le choix de l'unité dans le dashboard : ca pose un problème de design dans la mesure où oues unités peuvent couvrir des substances différentes. J'ai fait ce choix car je n'ai pas réussi à imaginer un moyen efficace de comparer tous les combustibles d'une même catégorie quelque soit leur unité. Ca peut être une piste de réflexion avec un PO, à savoir comment bien comparer les émissions entre deux combustibles (ou dans une mesure plus large deux éléments référencés dans la base) si ceux ci n'ont pas d'unité en commun.

## Routing

L'application se décompose en deux liens : 
- /dashboard pour accéder au dashboard
- /api/combustibles pour le call api pour récupérer les données combustibles

## Code
Pour importer les données ,j'ai préféré convertir le fichier xlsx en .csv, contenu dans le folder data.
J'utilise SQLAlchemy comme ORM, et pydantic pour typer.
J'ai intégré l'API avec FastAPI. J'ai mis un seul call pour toutes les données combustibles valides en France métropolitaine. 

### Lancer localement
Définir un fichier.env, avec DATABASE_URL défini pour l'url de la base de données, et SOURCE_FILE_PATH si la localisation du fichier de données a changé.
Installer les packages avec ```pip install -r requirements.txt```

Le code fonctionne en deux temps : mettre à jour le schema et l'unique table de la base de données avec ```python src/update_db.py```.


### Lancer avec docker

Avec docker : Le projet est dockerisé, pour lancer le script on peut lancer la commande ```docker-compse up``` depuis la racine du projet, puis aller sur l'url ```http://localhost:4500/``` une fois que le container est lancé ( ```http://localhost:4500/dashboard/``` pour accéder au dashboard ).


### Fichiers et dossiers : 
- **data**: dossier contenant les données à importer
- **src**: contenu du code
- **dashboard.py**: le dashboard en Dash.
- **app.py**: application dash à lancer une fois que la base est à jour.
- **config.py**: configurations du code
- **models.py**: modèle sqlAlchemy de la table à insérer en base
- **update_db.py** : script pour mettre à jour la base. Celui ci efface le schema et le recréée à chaque lancement.
- **db.py** : la connection à la db
  - **helpers** : module pour processer les données
    - **data.cleaning.py**: cleane ;lles données pour les insérer en base
    - **mapping.py** : mapping des noms de colonne vers un nom de variable des informations en base

## Pistes d'amélioration
- Dans les graphes au détail du dashboard, il peut être amélioré en permettant la sélection de plusieurs combustibles et de comparer leurs taux d'émission au détail. Je peux aussi exposer les tables brutes liées aux informations. Donner un détail des émissions par poste.
- Intégrer des validations pydantics dans la déclaration du modèle pour avoir des validations de données efficaces. Je n'ai pas pris le temps de le faire.
- Compléter l'API, intégrer des règles REST, la rendre plus exhaustive.
  
