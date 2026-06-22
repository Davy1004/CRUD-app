from flask import Blueprint, jsonify, request
from services.task_service import TaskService
from logger_config import get_logger

task_bp = Blueprint('tasks', __name__)
task_service = TaskService()
logger = get_logger(__name__)


@task_bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json() or {}
        task = task_service.create_task(data)
        return jsonify({
            'message': 'Task created successfully',
            'task': task.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Supports ?status=completed|pending and ?project_id=<id>."""
    try:
        status = request.args.get('status')
        project_id = request.args.get('project_id', type=int)
        if status and status not in ('completed', 'pending'):
            return jsonify({'error': "status must be 'completed' or 'pending'"}), 400
        tasks = task_service.get_all_tasks(status=status, project_id=project_id)
        return jsonify([t.to_dict() for t in tasks]), 200
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = task_service.get_task_by_id(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(task.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching task {task_id}: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json() or {}
        task = task_service.update_task(task_id, data)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({
            'message': 'Task updated successfully',
            'task': task.to_dict()
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error updating task {task_id}: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        success = task_service.delete_task(task_id)
        if not success:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500
