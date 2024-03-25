from sqlalchemy.sql import func
from api import db

class menues(db.Model):
    __tablename__ = "menues"
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    sep = db.Column(db.String(300))  # Removed collation specification
    menu = db.Column(db.String(300))  # Removed collation specification
    create_date = db.Column(db.DateTime, default=func.now())
    update_date = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    
    def __init__(self, sep, menu, create_date=None, update_date=None):
        self.sep = sep
        self.menu = menu
        # Only set create_date and update_date if explicitly provided
        if create_date is not None:
            self.create_date = create_date
        if update_date is not None:
            self.update_date = update_date