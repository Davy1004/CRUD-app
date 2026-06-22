from models.task import Task
from models.project import Project
from database.db import db
from logger_config import get_logger

logger = get_logger(__name__)


class TaskService:
    """Service class for task CRUD operations"""

    def create_task(self, data):
        logger.debug(f"Service: Creating task with data: {data}")
        title = (data.get('title') or '').strip()
        if not title:
            logger.warning("Service: Task title is required")
            raise ValueError('Task title is required')

        project_id = data.get('project_id')
        if not project_id:
            raise ValueError('project_id is required')

        # Ensure the parent project exists, else the FK insert errors obscurely.
        if not Project.query.get(project_id):
            raise ValueError('Project not found')

        task = Task(
            title=title,
            completed=bool(data.get('completed', False)),
            project_id=project_id
        )
        db.session.add(task)
        db.session.commit()
        logger.info(f"Service: Task created - ID: {task.id}")
        return task

    def get_all_tasks(self, status=None, project_id=None):
        """status: 'completed' | 'pending' | None. Optional project_id filter."""
        logger.debug(f"Service: Fetching tasks (status={status}, project_id={project_id})")
        query = Task.query
        if status == 'completed':
            query = query.filter(Task.completed.is_(True))
        elif status == 'pending':
            query = query.filter(Task.completed.is_(False))
        if project_id:
            query = query.filter(Task.project_id == project_id)
        return query.order_by(Task.created_at.desc()).all()

    def get_task_by_id(self, task_id):
        return Task.query.get(task_id)

    def update_task(self, task_id, data):
        logger.debug(f"Service: Updating task - ID: {task_id}")
        task = Task.query.get(task_id)
        if not task:
            return None

        if 'title' in data:
            title = (data.get('title') or '').strip()
            if not title:
                raise ValueError('Task title cannot be empty')
            task.title = title
        if 'completed' in data:
            task.completed = bool(data['completed'])
        if 'project_id' in data:
            if not Project.query.get(data['project_id']):
                raise ValueError('Project not found')
            task.project_id = data['project_id']

        db.session.commit()
        logger.info(f"Service: Task updated - ID: {task_id}")
        return task

    def delete_task(self, task_id):
        logger.debug(f"Service: Deleting task - ID: {task_id}")
        task = Task.query.get(task_id)
        if not task:
            return False
        db.session.delete(task)
        db.session.commit()
        logger.info(f"Service: Task deleted - ID: {task_id}")
        return True
