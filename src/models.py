from eralchemy2 import render_er
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    favorite_people = db.relationship(
        "FavoritePeople",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    favorite_planets = db.relationship(
        "FavoritePlanet",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class People(db.Model):
    __tablename__ = "people"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(50))
    skin_color = db.Column(db.String(50))
    eye_color = db.Column(db.String(50))
    birth_year = db.Column(db.String(20))
    gender = db.Column(db.String(20))

    favorites = db.relationship(
        "FavoritePeople",
        back_populates="people",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<People {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
        }


class Planet(db.Model):
    __tablename__ = "planets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    climate = db.Column(db.String(80))
    terrain = db.Column(db.String(80))
    population = db.Column(db.BigInteger)
    diameter = db.Column(db.Integer)
    gravity = db.Column(db.String(30))

    favorites = db.relationship(
        "FavoritePlanet",
        back_populates="planet",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Planet {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "diameter": self.diameter,
            "gravity": self.gravity,
        }


class FavoritePeople(db.Model):
    __tablename__ = "favorite_people"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "people_id", name="uq_user_people"),
    )

    user = db.relationship("User", back_populates="favorite_people")
    people = db.relationship("People", back_populates="favorites")

    def __repr__(self):
        return f"<FavoritePeople user={self.user_id} people={self.people_id}>"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
        }


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "planet_id", name="uq_user_planet"),
    )

    user = db.relationship("User", back_populates="favorite_planets")
    planet = db.relationship("Planet", back_populates="favorites")

    def __repr__(self):
        return f"<FavoritePlanet user={self.user_id} planet={self.planet_id}>"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }



if __name__ == "__main__":
    try:
        render_er(db.Model, "diagram.png")
        print("diagram.png generado")
    except Exception as e:
        print("Error generando el diagrama:", e)
        raise
