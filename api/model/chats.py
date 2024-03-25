from sqlalchemy.sql import func
from api import db

class chats(db.Model):
    __tablename__ = "chats"
    
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    room = db.Column(db.String(300))  # Removed collation specification
    sender = db.Column(db.String(300))  # Removed collation specification
    msg = db.Column(db.Text)  # Removed collation specification
    isGroupChat = db.Column(db.Boolean, default=True)
    create_date = db.Column(db.DateTime, default=func.now())
    update_date = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    
    # Removed one of the duplicate __init__ methods to avoid confusion
    def __init__(self, room, sender, msg, isGroupChat, create_date=None, update_date=None):
        self.room = room
        self.sender = sender
        self.msg = msg
        self.isGroupChat = isGroupChat
        # Only set create_date and update_date if explicitly provided
        if create_date is not None:
            self.create_date = create_date
        if update_date is not None:
            self.update_date = update_date