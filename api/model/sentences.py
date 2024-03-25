from sqlalchemy.sql import func
from api import db

class sentences(db.Model):
    __tablename__ = "sentences"
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    sep = db.Column(db.String(30))  # Removed collation specification
    sentence = db.Column(db.Text)  # Removed collation specification
    create_date = db.Column(db.DateTime, default=func.now())
    update_date = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    
    def __init__(self, sep, sentence, create_date=None, update_date=None):
        self.sep = sep
        self.sentence = sentence
        # Only set create_date and update_date if explicitly provided
        if create_date is not None:
            self.create_date = create_date
        if update_date is not None:
            self.update_date = update_date