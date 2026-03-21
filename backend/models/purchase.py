from datetime import datetime, timedelta
from backend.database.db import db

class Purchase(db.Model):
    __tablename__='purchases'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id=db.Column(db.Integer, db.ForeignKey('movies.id'))
    series_id=db.Column(db.Integer, db.ForeignKey('series.id'))
    episode_ids=db.Column(db.String(500))
    payment_id=db.Column(db.Integer, db.ForeignKey('payments.id'))
    access_expiry=db.Column(db.DateTime)
    purchased_at=db.Column(db.DateTime, default=datetime.utcnow)

    def set_expiry(self, days=7):
        self.access_expiry = datetime.utcnow() + timedelta(days=days)

    def is_expired(self):
        return datetime.utcnow() > self.access_expiry

    def to_dict(self):
        return {'id':self.id, 'user_id':self.user_id, 'movie_id':self.movie_id, 'series_id':self.series_id, 'access_expiry': self.access_expiry.isoformat() if self.access_expiry else None}
