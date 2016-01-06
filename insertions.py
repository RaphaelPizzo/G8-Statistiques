import pandas as pd
from datetime import datetime
from app import db
from app import modeles

# On vide les tables dans un ordre logique
modeles.Vehicule.query.delete()
modeles.Conducteur.query.delete()
modeles.Station.query.delete()
modeles.Secteur.query.delete()
modeles.Utilisateur.query.delete()
modeles.Adresse.query.delete()

################
### Adresses ###
################

def inserer_adresse(ligne):
    adresse = modeles.Adresse(
        nom_rue=ligne['nom_rue'],
        numero=ligne['numero'],
        cp=ligne['cp'],
        ville=ligne['ville'],
        position='POINT({0} {1})'.format(ligne['lat'], ligne['lon'])
    )
    db.session.add(adresse)
    db.session.commit()

# On remet à neuf la clé qui s'auto-incrémente
db.session.execute('TRUNCATE TABLE adresses RESTART IDENTITY CASCADE;')
adresses = pd.read_csv('app/data/adresses.csv', encoding='utf8')
adresses.apply(inserer_adresse, axis=1)


####################
### Utilisateurs ###
####################

def inserer_utilisateur(ligne):
    utilisateur = modeles.Utilisateur(
        prenom=ligne['prenom'].lower().capitalize(),
        nom=ligne['nom'].lower().capitalize(),
        email=ligne['email'],
        telephone=str(ligne['telephone']),
        categorie=ligne['categorie'],
        confirmation=True,
        notification_sms=True,
        notification_email=True,
        inscription=datetime.utcnow(),
        adresse=ligne['adresse'],
        mdp=ligne['mdp']
    )
    db.session.add(utilisateur)
    db.session.commit()

utilisateurs = pd.read_csv('app/data/utilisateurs.csv')
utilisateurs.apply(inserer_utilisateur, axis=1)

################################
### Véhicules et conducteurs ###
################################

def inserer_vehicule_conducteur(ligne):
    vehicule = modeles.Vehicule(
        immatriculation=ligne['immatriculation'],
        places=ligne['places'],
        couleur=ligne['couleur'],
        marque=ligne['marque']
    )
    conducteur = modeles.Conducteur(
        telephone=str(ligne['telephone']),
        email=ligne['email'],
        prenom=ligne['prenom'],
        nom=ligne['nom'],
        libre=True,
        #station=ligne['station'],
        position='POINT({0} {1})'.format(ligne['lat'], ligne['lon']),
        adresse=1,
        inscription=datetime.utcnow()
    )
    db.session.add(vehicule)
    db.session.add(conducteur)
    db.session.commit()
    # Clés étangère (problème de l'oeuf de de la poule...)
    vehicule.conducteur = conducteur.telephone
    db.session.commit()

vehicules = pd.read_csv('app/data/vehicules.csv')
conducteurs = pd.read_csv('app/data/conducteurs.csv')
data = pd.concat([vehicules, conducteurs], axis=1)
data.apply(inserer_vehicule_conducteur, axis=1)

########################################
############# Courses ##################
########################################

def inserer_course(ligne):
	course = modeles.Course(
		utilisateur=str(ligne['utilisateur']),
		conducteur=str(ligne['conducteur']),
		finie=True,
		places=ligne['places'],
		priorite=ligne['priorite'],
		debut=ligne['debut'],
		fin=ligne['fin'],
		retour= False,
		commentaire=ligne['commentaire'],
		depart=ligne['depart'],
		arrivee=ligne['arrivee'],
	)
	db.session.add(course)
	db.session.commit()

db.session.execute('TRUNCATE TABLE courses RESTART IDENTITY CASCADE;')
courses = pd.read_csv('app/data/courses.csv')
courses.apply(inserer_course, axis=1)


########################################
############# Factures #################
########################################

def inserer_facture(ligne):
	facture = modeles.Facture(
		course=ligne['course'],
		forfait=ligne['forfait'],
		estimation=ligne['estimation'],
		montant=ligne['montant'],
		rabais=ligne['rabais'],
		paiement=ligne['paiement'],
	)
	db.session.add(facture)
	db.session.commit()

db.session.execute('TRUNCATE TABLE factures RESTART IDENTITY CASCADE;')
factures = pd.read_csv('app/data/factures.csv')
factures.apply(inserer_facture, axis=1)

########################################
############# Positions ################
########################################

def inserer_position(ligne):
	position = modeles.Positions(
		conducteur=str(ligne['conducteur']),
		moment=ligne['moment'],
		positions='POINT({0} {1})'.format(ligne['lat'], ligne['lon']),
	)
	db.session.add(position)
	db.session.commit()

positions = pd.read_csv('app/data/positions.csv')
positions.apply(inserer_position, axis=1)
		



