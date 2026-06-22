import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProjectService, Project } from '../services/project.service';
import { TaskService, Task } from '../services/task.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.html'
})
export class DashboardComponent implements OnInit {
  projects: Project[] = [];
  tasks: Task[] = [];

  newProjectName = '';
  newProjectDesc = '';
  projectError = '';

  newTaskTitle = '';
  selectedProjectId: number | null = null;
  taskError = '';

  filter = 'all';
  success = '';

  constructor(private projectSvc: ProjectService, private taskSvc: TaskService) {}

  ngOnInit() {
    this.loadProjects();
    this.loadTasks();
  }

  flash(msg: string) {
    this.success = msg;
    setTimeout(() => (this.success = ''), 2500);
  }

  loadProjects() {
    this.projectSvc.getProjects().subscribe({
      next: (p) => {
        this.projects = p;
        if (!this.selectedProjectId && p.length) this.selectedProjectId = p[0].id!;
      }
    });
  }

  loadTasks() {
    this.taskSvc.getTasks(this.filter).subscribe({ next: (t) => (this.tasks = t) });
  }

  addProject() {
    this.projectError = '';
    if (!this.newProjectName.trim()) {
      this.projectError = 'Project name is required.';
      return;
    }
    this.projectSvc.createProject({
      name: this.newProjectName.trim(),
      description: this.newProjectDesc.trim()
    }).subscribe({
      next: () => {
        this.newProjectName = ''; this.newProjectDesc = '';
        this.loadProjects(); this.flash('Project added.');
      },
      error: (e) => (this.projectError = e?.error?.error || 'Could not add project.')
    });
  }

  deleteProject(id: number) {
    if (!confirm('Delete this project and all its tasks?')) return;
    this.projectSvc.deleteProject(id).subscribe({
      next: () => { this.loadProjects(); this.loadTasks(); this.flash('Project deleted.'); }
    });
  }

  addTask() {
    this.taskError = '';
    if (!this.newTaskTitle.trim()) {
      this.taskError = 'Task title is required.';
      return;
    }
    if (!this.selectedProjectId) {
      this.taskError = 'Create a project first.';
      return;
    }
    this.taskSvc.createTask({
      title: this.newTaskTitle.trim(),
      project_id: this.selectedProjectId
    }).subscribe({
      next: () => { this.newTaskTitle = ''; this.loadTasks(); this.loadProjects(); this.flash('Task added.'); },
      error: (e) => (this.taskError = e?.error?.error || 'Could not add task.')
    });
  }

  toggleTask(t: Task) {
    this.taskSvc.updateTask(t.id!, { completed: !t.completed }).subscribe({
      next: () => this.loadTasks()
    });
  }

  deleteTask(id: number) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    this.taskSvc.deleteTask(id).subscribe({
      next: () => { this.loadTasks(); this.loadProjects(); this.flash('Task deleted.'); }
    });
  }

  onFilterChange() {
    this.loadTasks();
  }

  projectName(id: number): string {
    return this.projects.find((p) => p.id === id)?.name || '—';
  }
}
