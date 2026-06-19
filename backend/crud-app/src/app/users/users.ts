import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UserService, User } from '../services/user';

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

  formUser: User = {
    name: '',
    email: '',
    phone: '',
    address: ''
  };

  errorMessage = '';
  successMessage = '';

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.userService.getUsers().subscribe({
      next: (data) => {
        this.users = data;
        this.errorMessage = '';
      },
      error: (err) => {
        console.error('Error loading users:', err);
        this.errorMessage = 'Failed to load users';
      }
    });
  }

  openCreateForm(): void {
    this.editingUser = null;
    this.formUser = { name: '', email: '', phone: '', address: '' };
    this.showForm = true;
    this.errorMessage = '';
    this.successMessage = '';
  }

  openEditForm(user: User): void {
    this.editingUser = user;
    this.formUser = { ...user };
    this.showForm = true;
    this.errorMessage = '';
    this.successMessage = '';
  }

  closeForm(): void {
    this.showForm = false;
    this.editingUser = null;
    this.formUser = { name: '', email: '', phone: '', address: '' };
  }

  submitForm(): void {
    if (!this.validateForm()) return;
    this.editingUser ? this.updateUser() : this.createUser();
  }

  validateForm(): boolean {
    if (!this.formUser.name?.trim()) {
      this.errorMessage = 'Name is required';
      return false;
    }
    if (!this.formUser.email?.trim()) {
      this.errorMessage = 'Email is required';
      return false;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.formUser.email)) {
      this.errorMessage = 'Please enter a valid email address';
      return false;
    }
    this.errorMessage = '';
    return true;
  }

  createUser(): void {
    this.userService.createUser(this.formUser).subscribe({
      next: () => {
        this.successMessage = 'User created successfully';
        this.closeForm();
        this.loadUsers();
      },
      error: (err) => {
        this.errorMessage = err.error?.error || 'Failed to create user';
      }
    });
  }

  updateUser(): void {
    if (!this.editingUser?.id) {
      this.errorMessage = 'User ID not found';
      return;
    }
    this.userService.updateUser(this.editingUser.id, this.formUser).subscribe({
      next: () => {
        this.successMessage = 'User updated successfully';
        this.closeForm();
        this.loadUsers();
      },
      error: (err) => {
        this.errorMessage = err.error?.error || 'Failed to update user';
      }
    });
  }

  deleteUser(user: User): void {
    if (!user.id) {
      this.errorMessage = 'User ID not found';
      return;
    }
    if (confirm(`Are you sure you want to delete ${user.name}?`)) {
      this.userService.deleteUser(user.id).subscribe({
        next: () => {
          this.successMessage = 'User deleted successfully';
          this.loadUsers();
        },
        error: (err) => {
          this.errorMessage = err.error?.error || 'Failed to delete user';
        }
      });
    }
  }
}