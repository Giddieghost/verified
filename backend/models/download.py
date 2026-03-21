from datetime import datetime
from backend.database.db import db

class Download(db.Model):
    __tablename__='downloads'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id=db.Column(db.Integer, db.ForeignKey('movies.id'))
    episode_id=db.Column(db.Integer, db.ForeignKey('episodes.id'))
    file_path=db.Column(db.String(500))
    file_size=db.Column(db.Float)
    download_status=db.Column(db.String(50), default='completed')
    downloaded_at=db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id':self.id,'user_id':self.user_id,'movie_id':self.movie_id,'episode_id':self.episode_id,'download_status':self.download_status,'downloaded_at':self.downloaded_at.isoformat()}
