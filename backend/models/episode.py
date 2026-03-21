from datetime import datetime
from backend.database.db import db

class Episode(db.Model):
    __tablename__='episodes'
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    episode_number = db.Column(db.Integer)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)
    video_url = db.Column(db.String(500))
    thumbnail_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'id':self.id,'series_id':self.series_id,'episode_number':self.episode_number,'title':self.title,'duration':self.duration,'video_url':self.video_url}
