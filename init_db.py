from app import application, db
from models import User, Progress

with application.app_context():
    db.create_all()
    print("База данных успешно инициализирована в instance/database.db")