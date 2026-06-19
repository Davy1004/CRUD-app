# Angular Debugging Guide

## Using Debug Utilities in Browser Console

The Angular application includes comprehensive debugging utilities accessible from the browser console.

### Access Debug Utilities

Open the browser **Developer Console** (F12 or Right-click → Inspect → Console tab) and use these utilities:

---

## 1. DebugLogger - Logging System

### Set Log Level
```javascript
DebugLogger.setLogLevel('DEBUG');  // DEBUG, INFO, WARN, ERROR
```

### Log Messages
```javascript
// Debug
DebugLogger.debug('Loading users...', { count: 5 });

// Info
DebugLogger.info('User created successfully', { id: 1 });

// Warning
DebugLogger.warn('Form validation failed');

// Error
DebugLogger.error('Network error occurred', error);
```

### View All Logs
```javascript
const logs = DebugLogger.getLogs();
console.table(logs);
```

### Export Logs
```javascript
// View as JSON string
const logString = DebugLogger.exportLogs();
console.log(logString);

// Download as file
DebugLogger.downloadLogs();  // Creates debug-logs-{timestamp}.json
```

### Clear Logs
```javascript
DebugLogger.clearLogs();
```

---

## 2. HttpErrorTracker - HTTP Error Monitoring

### View All Tracked Errors
```javascript
const errors = HttpErrorTracker.getErrors();
console.table(errors);
```

### Get Error Statistics
```javascript
const stats = HttpErrorTracker.getStats();
console.log(stats);

// Example output:
// {
//   totalErrors: 5,
//   errorsByStatus: { 404: 2, 500: 3 },
//   errorsByContext: { loadUsers: 2, createUser: 3 },
//   recentError: {...}
// }
```

### Clear Error History
```javascript
HttpErrorTracker.clear();
```

---

## 3. PerformanceMonitor - Performance Tracking

### Time Operations
```javascript
// Start timing
PerformanceMonitor.startTimer('userCreation');

// ... do work ...

// End timing (returns duration in ms)
const duration = PerformanceMonitor.endTimer('userCreation');
console.log(`Operation took ${duration}ms`);
```

### View All Measurements
```javascript
const measurements = PerformanceMonitor.getMeasurements();
console.table(measurements);
```

### Get Performance Statistics
```javascript
const stats = PerformanceMonitor.getStats();
console.log(stats);

// Example output:
// {
//   totalMeasurements: 25,
//   uniqueLabels: 4,
//   averageDurations: {
//     loadUsers: 145.23,
//     createUser: 234.56,
//     updateUser: 198.45,
//     deleteUser: 176.23
//   }
// }
```

### Get Average Duration for Specific Operation
```javascript
const avgDuration = PerformanceMonitor.getAverageDuration('loadUsers');
console.log(`Average load time: ${avgDuration}ms`);
```

---

## 4. StateInspector - Component State Tracking

### Take State Snapshot
```javascript
// Inside component or in console after component loads
StateInspector.takeSnapshot('users-list', { users: window.usersData });
```

### View Snapshots
```javascript
// Get specific snapshot
const snapshot = StateInspector.getSnapshot('users-list');
console.log(snapshot);

// Get all snapshots
const allSnapshots = StateInspector.getAllSnapshots();
console.table(allSnapshots);
```

### Compare State Changes
```javascript
// Compare current state with previous state
const previousState = { users: [] };
const changes = StateInspector.compareSnapshots('users-list', previousState);
console.log(changes);

// Output shows which fields changed:
// {
//   users: {
//     previous: [],
//     current: [{id: 1, name: 'John'}, ...]
//   }
// }
```

---

## Debugging Workflows

### Workflow 1: Debugging User Creation

```javascript
// 1. Set log level to see all details
DebugLogger.setLogLevel('DEBUG');

// 2. Clear previous data
DebugLogger.clearLogs();
HttpErrorTracker.clear();

// 3. Perform action in UI (click "Create User" button)

// 4. View detailed logs
DebugLogger.getLogs().filter(log => log.message.includes('create'));

// 5. Check for errors
HttpErrorTracker.getStats();

// 6. View performance
PerformanceMonitor.getAverageDuration('createUser');
```

### Workflow 2: Debugging API Errors

```javascript
// 1. Enable all logs
DebugLogger.setLogLevel('DEBUG');

// 2. Perform action that causes error
// (Try to create user with invalid email)

// 3. Check what errors occurred
HttpErrorTracker.getErrors().map(e => ({
  status: e.status,
  context: e.context,
  message: e.message
}));

// 4. View complete error details
const recentError = HttpErrorTracker.getStats().recentError;
console.log(recentError);

// 5. Check logs for more context
DebugLogger.getLogs().filter(log => log.level === 'ERROR');
```

### Workflow 3: Performance Analysis

```javascript
// 1. Start fresh measurements
PerformanceMonitor.clear();

// 2. Perform multiple operations in the UI
// (Load users, create user, update user, delete user)

// 3. Get statistics
const stats = PerformanceMonitor.getStats();
console.table(stats.averageDurations);

// 4. Identify slow operations
const slowest = Object.entries(stats.averageDurations)
  .sort((a, b) => b[1] - a[1])[0];
console.log(`Slowest operation: ${slowest[0]} (${slowest[1]}ms)`);

// 5. View detailed measurements
console.table(PerformanceMonitor.getMeasurements());
```

### Workflow 4: State Mutation Debugging

```javascript
// 1. Clear snapshots
StateInspector.clear();

// 2. Perform action in UI
// (Open form, fill fields, submit)

// 3. View state changes
const changes = StateInspector.compareSnapshots('edit-form', {
  formUser: { name: '', email: '' }
});
console.log(changes);

// 4. View final state
const finalState = StateInspector.getSnapshot('edit-form');
console.log(finalState);
```

---

## Common Debugging Tasks

### Check if API is responding
```javascript
fetch('http://localhost:5000/api/health')
  .then(res => res.json())
  .then(data => console.log('API Status:', data))
  .catch(err => console.error('API Error:', err));
```

### Monitor all network requests
```javascript
// In DevTools Network tab:
// 1. Open DevTools (F12)
// 2. Go to Network tab
// 3. Perform actions in the app
// 4. View all requests/responses
```

### Check component state
```javascript
// In Angular, expose component to window for debugging
// Add to component:
// ngOnInit() {
//   (window as any).debugComponent = this;
// }

// Then in console:
console.log(window.debugComponent.users);
console.log(window.debugComponent.formUser);
```

### View form validation
```javascript
// Check if form is valid
console.log(window.debugComponent.validateForm());

// View form errors
console.log(window.debugComponent.errorMessage);
```

### Monitor HTTP requests
```javascript
// View all errors
HttpErrorTracker.getErrors().forEach(error => {
  console.log(`[${error.status}] ${error.context}: ${error.message}`);
});
```

---

## Using Chrome DevTools

### 1. Breakpoints
- Click on line number to set breakpoint
- Code execution pauses when breakpoint is hit
- Use Step Over, Step Into, Step Out buttons to debug

### 2. Console Logging
```javascript
// In browser console while app is running
console.log('Current users:', window.usersComponent?.users);

// Use logging from debug utilities
DebugLogger.debug('Testing debug output');
```

### 3. Network Monitoring
- Open Network tab (F12 → Network)
- Filter by XHR for API calls
- Click request to view:
  - Request headers and body
  - Response status and body
  - Timing information

### 4. Performance Profiling
- Open Performance tab (F12 → Performance)
- Click Record
- Perform user actions
- Click Stop
- Analyze flame graph and timeline

---

## Error Messages and Solutions

| Error | Meaning | Solution |
|-------|---------|----------|
| `Failed to load users` | API not responding | Check Flask server is running |
| `Network error occurred` | CORS or connection issue | Check backend CORS config |
| `Form validation: Email is required` | Missing email field | Fill email in form |
| `Invalid email format` | Email doesn't match regex | Use format: test@example.com |
| `Email already exists` | Duplicate email in DB | Use different email |

---

## Export and Share Debug Data

### Export All Debug Data
```javascript
const debugData = {
  logs: DebugLogger.getLogs(),
  errors: HttpErrorTracker.getErrors(),
  performance: PerformanceMonitor.getMeasurements(),
  stats: {
    errorStats: HttpErrorTracker.getStats(),
    perfStats: PerformanceMonitor.getStats()
  },
  timestamp: new Date().toISOString()
};

// Download as JSON
const blob = new Blob([JSON.stringify(debugData, null, 2)], { type: 'application/json' });
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = `debug-data-${Date.now()}.json`;
a.click();
```

---

## Tips and Tricks

1. **Copy to clipboard:**
   ```javascript
   copy(DebugLogger.getLogs());  // Copies to clipboard
   ```

2. **Pretty print JSON:**
   ```javascript
   console.table(HttpErrorTracker.getErrors());
   ```

3. **Filter logs:**
   ```javascript
   DebugLogger.getLogs().filter(log => log.level === 'ERROR');
   ```

4. **Find slow operations:**
   ```javascript
   PerformanceMonitor.getMeasurements()
     .sort((a, b) => b.duration - a.duration)
     .slice(0, 5);
   ```

5. **Monitor in real-time:**
   ```javascript
   setInterval(() => {
     const stats = HttpErrorTracker.getStats();
     console.clear();
     console.log('Current Error Count:', stats.totalErrors);
   }, 1000);
   ```

---

## Need More Help?

- Check browser console for detailed error messages
- Review `debug-logs-*.json` files for historical data
- Use Network tab to inspect API requests/responses
- Enable browser DevTools for step-by-step debugging

**Happy debugging!** 🐛
