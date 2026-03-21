from datetime import datetime
from backend.database.db import db

class Series(db.Model):
    __tablename__='series'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    price = db.Column(db.Float, default=10.0)
    thumbnail_url = db.Column(db.String(500))
    upload_by_admin_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id':self.id,'title':self.title,'description':self.description,'category':self.category,'price':self.price,'thumbnail_url':self.thumbnail_url}
