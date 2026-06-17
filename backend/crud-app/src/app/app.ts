import { Component } from '@angular/core';
import { UsersComponent } from './users/users';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [UsersComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App { }