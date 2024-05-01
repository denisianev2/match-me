from flask import Blueprint
import modules.db.db as db

common_bp = Blueprint("common", __name__, url_prefix="/common")


@common_bp.get("/theatres")
def get_all_theatres():
    return db.get_all_theatres()


@common_bp.get("/roles")
def get_all_roles():
    return db.get_all_roles()


@common_bp.get("/titles")
def get_all_titles():
    return db.get_all_titles()


@common_bp.get("/cities")
def get_all_cities():
    return db.get_all_cities()


@common_bp.get("/countries")
def get_all_countries():
    return db.get_all_countries()


@common_bp.get("/interests")
def get_all_interests():
    return db.get_all_interests()


@common_bp.get("/strengths")
def get_all_strengths():
    return db.get_all_strengths()
