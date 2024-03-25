from sqlalchemy.sql import func
from api import db

class enhancement_history(db.Model):
    __tablename__ = "enhancement_history"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user = db.Column(db.String(300))  # Removed collation specification
    item_name = db.Column(db.String(300))  # Removed collation specification
    room = db.Column(db.String(300))  # Removed collation specification
    before_level = db.Column(db.Integer)
    change_level = db.Column(db.Integer)
    current_level = db.Column(db.Integer)
    create_date = db.Column(db.DateTime, default=func.now())
    update_date = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    # Consolidated __init__ method with optional parameters for dates
    def __init__(
        self, 
        user, 
        item_name, 
        room, 
        before_level, 
        change_level, 
        current_level, 
        create_date=None, 
        update_date=None
    ):
        self.user = user
        self.item_name = item_name
        self.room = room
        self.before_level = before_level
        self.change_level = change_level
        self.current_level = current_level
        # Only set create_date and update_date if explicitly provided
        if create_date is not None:
            self.create_date = create_date
        if update_date is not None:
            self.update_date = update_date