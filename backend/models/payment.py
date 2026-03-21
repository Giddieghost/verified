from datetime import datetime
from backend.database.db import db

class Payment(db.Model):
    __tablename__='payments'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    amount=db.Column(db.Float, nullable=False)
    currency=db.Column(db.String(10), default='KES')
    method=db.Column(db.String(50), default='mpesa')
    status=db.Column(db.String(50), default='pending')
    transaction_id=db.Column(db.String(255), unique=True)
    phone_number=db.Column(db.String(20))
    description=db.Column(db.Text)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id':self.id,'user_id':self.user_id,'amount':self.amount,'status':self.status,'transaction_id':self.transaction_id,'created_at':self.created_at.isoformat()}
