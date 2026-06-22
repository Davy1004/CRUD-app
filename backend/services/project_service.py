from models.project import Project
from database.db import db
from logger_config import get_logger

logger = get_logger(__name__)


class ProjectService:
    """Service class for project CRUD operations"""

    def create_project(self, data):
        logger.debug(f"Service: Creating project with data: {data}")
        name = (data.get('name') or '').strip()
        if not name:
            logger.warning("Service: Project name is required")
            raise ValueError('Project name is required')

        project = Project(
            name=name,
            description=(data.get('description') or '').strip()
        )
        db.session.add(project)
        db.session.commit()
        logger.info(f"Service: Project created - ID: {project.id}")
        return project

    def get_all_projects(self):
        logger.debug("Service: Fetching all projects")
        return Project.query.order_by(Project.created_at.desc()).all()

    def get_project_by_id(self, project_id):
        logger.debug(f"Service: Fetching project by ID: {project_id}")
        return Project.query.get(project_id)

    def update_project(self, project_id, data):
        logger.debug(f"Service: Updating project - ID: {project_id}")
        project = Project.query.get(project_id)
        if not project:
            return None

        if 'name' in data:
            name = (data.get('name') or '').strip()
            if not name:
                raise ValueError('Project name cannot be empty')
            project.name = name
        if 'description' in data:
            project.description = (data.get('description') or '').strip()

        db.session.commit()
        logger.info(f"Service: Project updated - ID: {project_id}")
        return project

    def delete_project(self, project_id):
        logger.debug(f"Service: Deleting project - ID: {project_id}")
        project = Project.query.get(project_id)
        if not project:
            return False
        db.session.delete(project)
        db.session.commit()
        logger.info(f"Service: Project deleted - ID: {project_id}")
        return True
