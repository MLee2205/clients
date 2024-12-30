# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    sexe= db.Column(db.String(100),  nullable=False)
    num_cni= db.Column(db.String(100), nullable=False)
    telephone= db.Column(db.Integer,  nullable=False)
    email = db.Column(db.String(100),  nullable=False)

    def __repr__(self):
        return f'<Client {self.nom}>'
    
    def serialize(self):
        return {
            
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'sexe': self.sexe,
            'num_cni': self.num_cni,
            'telephone': self.telephone,
            'email': self.email

        }


from sqlalchemy import text
"""from your_application import db  # Assurez-vous d'importer votre instance de base de données
"""
def reset_sequence(table_name, id_column):
    # Exécute la commande pour réinitialiser la séquence
    sql = f"""
    SELECT setval(pg_get_serial_sequence(:table_name, :id_column), coalesce(max({id_column}), 1) )
    FROM {table_name};
    """
    db.session.execute(text(sql), {'table_name': table_name, 'id_column': id_column})
    db.session.commit()
