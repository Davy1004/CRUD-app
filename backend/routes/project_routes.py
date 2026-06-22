from flask import Blueprint, jsonify, request
from services.project_service import ProjectService
from logger_config import get_logger

project_bp = Blueprint('projects', __name__)
project_service = ProjectService()
logger = get_logger(__name__)


@project_bp.route('/projects', methods=['POST'])
def create_project():
    try:
        data = request.get_json() or {}
        project = project_service.create_project(data)
        return jsonify({
            'message': 'Project created successfully',
            'project': project.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@project_bp.route('/projects', methods=['GET'])
def get_projects():
    try:
        projects = project_service.get_all_projects()
        return jsonify([p.to_dict() for p in projects]), 200
    except Exception as e:
        logger.error(f"Error fetching projects: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@project_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    try:
        project = project_service.get_project_by_id(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        return jsonify(project.to_dict(include_tasks=True)), 200
    except Exception as e:
        logger.error(f"Error fetching project {project_id}: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@project_bp.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        data = request.get_json() or {}
        project = project_service.update_project(project_id, data)
        if not project:
            return jsonify({'error': 'Project not found'}), 404
        return jsonify({
            'message': 'Project updated successfully',
            'project': project.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating project {project_id}: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@project_bp.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        success = project_service.delete_project(project_id)
        if not success:
            return jsonify({'error': 'Project not found'}), 404
        return jsonify({'message': 'Project deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Error deleting project {project_id}: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500
