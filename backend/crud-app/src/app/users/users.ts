import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UserService, User } from '../services/user';
import { DebugLogger, HttpErrorTracker, PerformanceMonitor, StateInspector } from '../services/debug.util';

@Component({
  selector: 'app-users',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './users.html',
  styleUrl: './users.css'
})
export class UsersComponent implements OnInit {

  users: User[] = [];
  showForm = false;
  editingUser: User | null = null;

  // Form data
  formUser: User = {
    name: '',
    email: '',
    phone: '',
    address: ''
  };

  errorMessage = '';
  successMessage = '';

  constructor(private userService: UserService) {
    DebugLogger.setLogLevel('DEBUG');
    DebugLogger.info('UsersComponent constructor initialized');
  }

  ngOnInit(): void {
    DebugLogger.debug('UsersComponent ngOnInit started');
    PerformanceMonitor.startTimer('loadUsers');
    this.loadUsers();
  }

  /**
   * Load all users from backend
   */
  loadUsers(): void {
    DebugLogger.debug('Loading users...');
    this.userService.getUsers().subscribe({
      next: (data) => {
        DebugLogger.info('Users loaded successfully', { count: data.length });
        PerformanceMonitor.endTimer('loadUsers');
        this.users = data;
        this.errorMessage = '';
        StateInspector.takeSnapshot('users-list', { users: this.users });
      },
      error: (err) => {
        DebugLogger.error('Error loading users', err);
        HttpErrorTracker.trackError(err, 'loadUsers');
        PerformanceMonitor.endTimer('loadUsers');
        this.errorMessage = 'Failed to load users';
      }
    });
  }

  /**
   * Open form for creating a new user
   */
  openCreateForm(): void {
    DebugLogger.debug('Opening create user form');
    this.editingUser = null;
    this.formUser = {
      name: '',
      email: '',
      phone: '',
      address: ''
    };
    this.showForm = true;
    this.errorMessage = '';
    this.successMessage = '';
  }

  /**
   * Open form for editing a user
   */
  openEditForm(user: User): void {
    DebugLogger.debug('Opening edit user form', { userId: user.id });
    this.editingUser = user;
    this.formUser = { ...user };
    this.showForm = true;
    this.errorMessage = '';
    this.successMessage = '';
    StateInspector.takeSnapshot('edit-form', { formUser: this.formUser });
  }

  /**
   * Close the form
   */
  closeForm(): void {
    DebugLogger.debug('Closing form');
    this.showForm = false;
    this.editingUser = null;
    this.formUser = {
      name: '',
      email: '',
      phone: '',
      address: ''
    };
  }

  /**
   * Submit form - Create or Update user
   */
  submitForm(): void {
    DebugLogger.debug('Form submitted');
    if (!this.validateForm()) {
      DebugLogger.warn('Form validation failed');
      return;
    }

    if (this.editingUser) {
      // Update existing user
      this.updateUser();
    } else {
      // Create new user
      this.createUser();
    }
  }

  /**
   * Validate form data
   */
  validateForm(): boolean {
    if (!this.formUser.name || !this.formUser.name.trim()) {
      this.errorMessage = 'Name is required';
      DebugLogger.warn('Form validation: Name is required');
      return false;
    }

    if (!this.formUser.email || !this.formUser.email.trim()) {
      this.errorMessage = 'Email is required';
      DebugLogger.warn('Form validation: Email is required');
      return false;
    }

    // Simple email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.formUser.email)) {
      this.errorMessage = 'Please enter a valid email address';
      DebugLogger.warn('Form validation: Invalid email format', { email: this.formUser.email });
      return false;
    }

    this.errorMessage = '';
    DebugLogger.debug('Form validation passed');
    return true;
  }

  /**
   * Create a new user
   */
  createUser(): void {
    DebugLogger.debug('Creating new user', { email: this.formUser.email });
    PerformanceMonitor.startTimer('createUser');

    this.userService.createUser(this.formUser).subscribe({
      next: (response) => {
        DebugLogger.info('User created successfully', response);
        PerformanceMonitor.endTimer('createUser');
        this.successMessage = 'User created successfully';
        this.closeForm();
        this.loadUsers();
      },
      error: (err) => {
        DebugLogger.error('Error creating user', err);
        HttpErrorTracker.trackError(err, 'createUser');
        PerformanceMonitor.endTimer('createUser');
        this.errorMessage = err.error.error || 'Failed to create user';
      }
    });
  }

  /**
   * Update an existing user
   */
  updateUser(): void {
    if (!this.editingUser || !this.editingUser.id) {
      this.errorMessage = 'User ID not found';
      DebugLogger.error('Update failed: User ID not found');
      return;
    }

    DebugLogger.debug('Updating user', { userId: this.editingUser.id });
    PerformanceMonitor.startTimer('updateUser');

    this.userService.updateUser(this.editingUser.id, this.formUser).subscribe({
      next: (response) => {
        DebugLogger.info('User updated successfully', response);
        PerformanceMonitor.endTimer('updateUser');
        this.successMessage = 'User updated successfully';
        this.closeForm();
        this.loadUsers();
      },
      error: (err) => {
        DebugLogger.error('Error updating user', err);
        HttpErrorTracker.trackError(err, 'updateUser');
        PerformanceMonitor.endTimer('updateUser');
        this.errorMessage = err.error.error || 'Failed to update user';
      }
    });
  }

  /**
   * Delete a user
   */
  deleteUser(user: User): void {
    if (!user.id) {
      this.errorMessage = 'User ID not found';
      DebugLogger.error('Delete failed: User ID not found');
      return;
    }

    if (confirm(`Are you sure you want to delete ${user.name}?`)) {
      DebugLogger.debug('Deleting user', { userId: user.id });
      PerformanceMonitor.startTimer('deleteUser');

      this.userService.deleteUser(user.id).subscribe({
        next: (response) => {
          DebugLogger.info('User deleted successfully', response);
          PerformanceMonitor.endTimer('deleteUser');
          this.successMessage = 'User deleted successfully';
          this.loadUsers();
        },
        error: (err) => {
          DebugLogger.error('Error deleting user', err);
          HttpErrorTracker.trackError(err, 'deleteUser');
          PerformanceMonitor.endTimer('deleteUser');
          this.errorMessage = err.error.error || 'Failed to delete user';
        }
      });
    }
  }
}

/**
 * Load all users from backend
 */
loadUsers(): void {
  this.userService.getUsers().subscribe({
    next: (data) => {
      console.log('Users loaded:', data);
      this.users = data;
      this.errorMessage = '';
    },
    error: (err) => {
      console.error('Error loading users:', err);
      this.errorMessage = 'Failed to load users';
    }
  });
}

/**
 * Open form for creating a new user
 */
openCreateForm(): void {
  this.editingUser = null;
  this.formUser = {
    name: '',
    email: '',
    phone: '',
    address: ''
  };
  this.showForm = true;
  this.errorMessage = '';
  this.successMessage = '';
}

/**
 * Open form for editing a user
 */
openEditForm(user: User): void {
  this.editingUser = user;
  this.formUser = { ...user };
  this.showForm = true;
  this.errorMessage = '';
  this.successMessage = '';
}

/**
 * Close the form
 */
closeForm(): void {
  this.showForm = false;
  this.editingUser = null;
  this.formUser = {
    name: '',
    email: '',
    phone: '',
    address: ''
  };
}

/**
 * Submit form - Create or Update user
 */
submitForm(): void {
  if(!this.validateForm()) {
  return;
}

if (this.editingUser) {
  // Update existing user
  this.updateUser();
} else {
  // Create new user
  this.createUser();
}
  }

/**
 * Validate form data
 */
validateForm(): boolean {
  if (!this.formUser.name || !this.formUser.name.trim()) {
    this.errorMessage = 'Name is required';
    return false;
  }

  if (!this.formUser.email || !this.formUser.email.trim()) {
    this.errorMessage = 'Email is required';
    return false;
  }

  // Simple email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(this.formUser.email)) {
    this.errorMessage = 'Please enter a valid email address';
    return false;
  }

  this.errorMessage = '';
  return true;
}

/**
 * Create a new user
 */
createUser(): void {
  this.userService.createUser(this.formUser).subscribe({
    next: (response) => {
      console.log('User created:', response);
      this.successMessage = 'User created successfully';
      this.closeForm();
      this.loadUsers();
    },
    error: (err) => {
      console.error('Error creating user:', err);
      this.errorMessage = err.error.error || 'Failed to create user';
    }
  });
}

/**
 * Update an existing user
 */
updateUser(): void {
  if(!this.editingUser || !this.editingUser.id) {
  this.errorMessage = 'User ID not found';
  return;
}

this.userService.updateUser(this.editingUser.id, this.formUser).subscribe({
  next: (response) => {
    console.log('User updated:', response);
    this.successMessage = 'User updated successfully';
    this.closeForm();
    this.loadUsers();
  },
  error: (err) => {
    console.error('Error updating user:', err);
    this.errorMessage = err.error.error || 'Failed to update user';
  }
});
  }

/**
 * Delete a user
 */
deleteUser(user: User): void {
  if(!user.id) {
  this.errorMessage = 'User ID not found';
  return;
}

if (confirm(`Are you sure you want to delete ${user.name}?`)) {
  this.userService.deleteUser(user.id).subscribe({
    next: (response) => {
      console.log('User deleted:', response);
      this.successMessage = 'User deleted successfully';
      this.loadUsers();
    },
    error: (err) => {
      console.error('Error deleting user:', err);
      this.errorMessage = err.error.error || 'Failed to delete user';
    }
  });
}
  }
}