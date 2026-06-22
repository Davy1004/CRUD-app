from database.db import db
from datetime import datetime


class Project(db.Model):
    """Project model"""
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One project has many tasks. cascade ensures deleting a project
    # removes its tasks instead of leaving orphaned rows with a dangling FK.
    tasks = db.relationship(
        'Task',
        backref='project',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def to_dict(self, include_tasks=False):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'task_count': len(self.tasks),
        }
        if include_tasks:
            data['tasks'] = [t.to_dict() for t in self.tasks]
        return data

    def __repr__(self):
        return f'<Project {self.name}>'
