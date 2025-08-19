from eralchemy2 import render_er
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    favorite_characters = db.relationship(
        "FavoriteCharacter",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def serialize(self):
        return {"id": self.id, "username": self.username, "email": self.email}


class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)        
    api_id = db.Column(db.String(64), unique=True,
                       index=True, nullable=False)  
    name = db.Column(db.String(120), nullable=False)

    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)                 

    favorited_by = db.relationship(
        "FavoriteCharacter",
        back_populates="character",
        cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "id": self.id,
            "api_id": self.api_id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
        }


class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_characters"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey(
        "characters.id"), nullable=False)

    __table_args__ = (db.UniqueConstraint(
        "user_id", "character_id", name="uq_user_character"),)

    user = db.relationship("User", back_populates="favorite_characters")
    character = db.relationship("Character", back_populates="favorited_by")

    def serialize(self):
        return {"id": self.id, "user_id": self.user_id, "character_id": self.character_id}


if __name__ == "__main__":
    try:
        render_er(db.Model, "diagram.png")
        print("diagram.png generado")
    except Exception as e:
        print("Error generando el diagrama:", e)
        raise
