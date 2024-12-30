from flask import Flask, render_template,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from schemas import ClientSchema
from model import Client, db
import jwt
import datetime
from model import *




#################################### CONFIGURATION DE L APPLICATION FLASK #################################

#l'objet flask pour instancier une application
app = Flask(__name__)
#ma = Marshmallow(app)


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://yvanna:1234@localhost/utilisateur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser SQLAlchemy avec l'application
db.init_app(app) 




####################fonction de creation  du jwt pour recuperer l'id de l user dans les autres microservices##


SECRET_KEY = 'votre_clé_secrète'  # Remplacez par une clé secrète plus complexe

def create_jwt(client_id, user_name,user_surname,num_cni,email):
    payload = {
        'user_id': client_id,
        'user_name' :user_name,
        'user_surname' :user_surname,
        'num_cni' : num_cni,
        'email' : email,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)  # Durée de validité du token
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token





####################################################creation de l'API########################################

#definir une route vers la page d accueil
@app.route('/')
def accueil():
    db.create_all()
    return render_template('accueil.html')





####################### AJOUT D UN NOUVEAU CLIENT ###########################################################

#route vers le formulaire d inscription
@app.route('/clients/templates/creation')
def client_form():
    return render_template('creation.html')

     
#point de terminaison de la creation de client
@app.route('/clients/templates/creation', methods=['POST'])
def add_client():

    # Récupérer les données du formulaire
    nom = request.form['nom']
    prenom = request.form['prenom']
    sexe = request.form['sexe']
    num_cni = request.form['num_cni']
    telephone = request.form['telephone']
    email = request.form['email']

    # Réinitialiser la séquence avant d'insérer
    reset_sequence('clients', 'id')

    # Créer un nouvel enregistrement de client
    new_client = Client(nom=nom, prenom=prenom, sexe=sexe, num_cni=num_cni, telephone=telephone, email=email)
    db.session.add(new_client)
    db.session.commit()

    # Récupérer l'ID du nouveau client
    client_id = new_client.id  # Récupération de l'ID

    # Créer le JWT
    token = create_jwt(client_id,nom,prenom,num_cni,email)


    return (render_template('confirmation.html', client_id=client_id, token=token))




################################## LECTURE ##################################################################

#point de terminaison pour la lecture de  la base de donnees clients

@app.route('/clients/lecture',  methods=['GET'])
def lecture():
    client= Client.query.all()

    return jsonify([cli.serialize() for cli in client])





####################### MODIFICATION ######################################################################

#point de terminaison pour recuperer un client a partir de l'id

@app.route('/clients/templates/edition/<int:client_id>', methods=['GET'])
def edit_client_form(client_id):
    client = Client.query.get(client_id)
    
    if not client:
        return jsonify({'error': 'Client non trouvé'}), 404

    # Afficher le formulaire de modification 
    return render_template('edition.html', client=client)



#point de terminaison pour valider la modification 

@app.route('/clients/templates/edition/<int:client_id>', methods=['POST'])
def update_client(client_id):
    client = Client.query.get(client_id)
    
    if not client:
        return jsonify({'error': 'Client non trouvé'}), 404

    # Récupérer les données du formulaire
    data = request.form 
    client.nom = data.get('nom', client.nom)
    client.prenom = data.get('prenom', client.prenom)
    client.sexe = data.get('sexe', client.sexe)
    client.num_cni = data.get('num_cni', client.num_cni)
    client.telephone = data.get('telephone', client.telephone)
    client.email = data.get('email', client.email)

    # Enregistrer les modifications dans la base de données
    db.session.commit()
     # Créer le JWT
    token = create_jwt(client.id,client.nom,client.prenom,client.num_cni,client.email)
    client_id=client.id
    
    return (render_template('confirmation.html', client_id=client_id, token=token))





##################### SUPPRESSION #########################################################################

#point de terminaison pour la suppression des clients
@app.route('/clients/delete/<int:client_id>', methods = ['POST'])
def delete(client_id):
    clients = Client.query.get(client_id)

   
    if not clients:
        return jsonify({'error': 'Client non trouvé'}), 404

    # Supprimer le client de la session
    db.session.delete(clients)
    db.session.commit()
    
    return render_template('accueil.html')




############################ execution de l'application ####################################################

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host="127.0.0.1", port=5001) 


