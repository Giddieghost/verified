from datetime import datetime
from backend.database.db import db

class WatchHistory(db.Model):
    __tablename__='watch_history'
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id=db.Column(db.Integer, db.ForeignKey('movies.id'))
    episode_id=db.Column(db.Integer, db.ForeignKey('episodes.id'))
    progress_sec=db.Column(db.Integer, default=0)
    watched_at=db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id':self.id, 'user_id':self.user_id, 'movie_id':self.movie_id, 'episode_id':self.episode_id, 'progress_sec':self.progress_sec}
