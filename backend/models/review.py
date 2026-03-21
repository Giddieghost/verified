from datetime import datetime
from backend.database.db import db

class Review(db.Model):
    __tablename__='reviews'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id=db.Column(db.Integer, db.ForeignKey('movies.id'))
    series_id=db.Column(db.Integer, db.ForeignKey('series.id'))
    rating=db.Column(db.Integer)
    comment=db.Column(db.Text)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id':self.id,'user_id':self.user_id,'movie_id':self.movie_id,'series_id':self.series_id,'rating':self.rating,'comment':self.comment,'created_at':self.created_at.isoformat()}
