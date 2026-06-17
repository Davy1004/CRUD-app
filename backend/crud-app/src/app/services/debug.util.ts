/**
 * Angular Debugging Utilities
 * Provides logging, error tracking, and performance monitoring
 */

export interface LogLevel {
  DEBUG: number;
  INFO: number;
  WARN: number;
  ERROR: number;
}

export class DebugLogger {
  private static readonly LOG_LEVELS: LogLevel = {
    DEBUG: 0,
    INFO: 1,
    WARN: 2,
    ERROR: 3
  };

  private static currentLogLevel = this.LOG_LEVELS.DEBUG;
  private static logs: any[] = [];
  private static maxLogs = 1000;

  /**
   * Set the logging level
   */
  static setLogLevel(level: keyof LogLevel): void {
    this.currentLogLevel = this.LOG_LEVELS[level];
    console.log(`[DebugLogger] Log level set to: ${level}`);
  }

  /**
   * Debug level logging
   */
  static debug(message: string, data?: any): void {
    if (this.currentLogLevel <= this.LOG_LEVELS.DEBUG) {
      this.log('DEBUG', message, data, '#007bff');
    }
  }

  /**
   * Info level logging
   */
  static info(message: string, data?: any): void {
    if (this.currentLogLevel <= this.LOG_LEVELS.INFO) {
      this.log('INFO', message, data, '#28a745');
    }
  }

  /**
   * Warning level logging
   */
  static warn(message: string, data?: any): void {
    if (this.currentLogLevel <= this.LOG_LEVELS.WARN) {
      this.log('WARN', message, data, '#ffc107');
    }
  }

  /**
   * Error level logging
   */
  static error(message: string, data?: any): void {
    if (this.currentLogLevel <= this.LOG_LEVELS.ERROR) {
      this.log('ERROR', message, data, '#dc3545');
    }
  }

  /**
   * Internal logging method
   */
  private static log(level: string, message: string, data?: any, color?: string): void {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = {
      timestamp,
      level,
      message,
      data,
      url: window.location.href
    };

    // Store in memory
    this.logs.push(logEntry);
    if (this.logs.length > this.maxLogs) {
      this.logs.shift();
    }

    // Console output with styling
    const style = `color: ${color}; font-weight: bold; padding: 2px 6px; border-radius: 3px;`;
    console.log(`%c[${level}] ${timestamp}`, style, message, data || '');
  }

  /**
   * Get all stored logs
   */
  static getLogs(): any[] {
    return [...this.logs];
  }

  /**
   * Clear stored logs
   */
  static clearLogs(): void {
    this.logs = [];
    console.log('[DebugLogger] Logs cleared');
  }

  /**
   * Export logs as JSON
   */
  static exportLogs(): string {
    return JSON.stringify(this.logs, null, 2);
  }

  /**
   * Download logs as file
   */
  static downloadLogs(): void {
    const logs = this.exportLogs();
    const blob = new Blob([logs], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `debug-logs-${new Date().toISOString()}.json`;
    link.click();
    window.URL.revokeObjectURL(url);
  }
}

/**
 * HTTP Error Tracker for monitoring API errors
 */
export class HttpErrorTracker {
  private static errors: any[] = [];
  private static maxErrors = 100;

  /**
   * Track HTTP error
   */
  static trackError(error: any, context?: string): void {
    const errorEntry = {
      timestamp: new Date().toISOString(),
      status: error.status,
      message: error.message,
      url: error.url,
      context: context || 'Unknown',
      error: error
    };

    this.errors.push(errorEntry);
    if (this.errors.length > this.maxErrors) {
      this.errors.shift();
    }

    DebugLogger.error(`HTTP Error: ${error.status} - ${error.message}`, errorEntry);
  }

  /**
   * Get all tracked errors
   */
  static getErrors(): any[] {
    return [...this.errors];
  }

  /**
   * Get error statistics
   */
  static getStats(): any {
    const stats: any = {
      totalErrors: this.errors.length,
      errorsByStatus: {},
      errorsByContext: {},
      recentError: this.errors[this.errors.length - 1] || null
    };

    this.errors.forEach(error => {
      stats.errorsByStatus[error.status] = (stats.errorsByStatus[error.status] || 0) + 1;
      stats.errorsByContext[error.context] = (stats.errorsByContext[error.context] || 0) + 1;
    });

    return stats;
  }

  /**
   * Clear error history
   */
  static clear(): void {
    this.errors = [];
  }
}

/**
 * Performance Monitor for tracking Angular performance
 */
export class PerformanceMonitor {
  private static timers: Map<string, number> = new Map();
  private static measurements: any[] = [];
  private static maxMeasurements = 500;

  /**
   * Start timing a section
   */
  static startTimer(label: string): void {
    this.timers.set(label, performance.now());
    DebugLogger.debug(`Timer started: ${label}`);
  }

  /**
   * End timing a section
   */
  static endTimer(label: string): number {
    const startTime = this.timers.get(label);
    if (!startTime) {
      DebugLogger.warn(`Timer not found: ${label}`);
      return 0;
    }

    const duration = performance.now() - startTime;
    this.timers.delete(label);

    const measurement = {
      timestamp: new Date().toISOString(),
      label,
      duration: Math.round(duration * 100) / 100 // Round to 2 decimal places
    };

    this.measurements.push(measurement);
    if (this.measurements.length > this.maxMeasurements) {
      this.measurements.shift();
    }

    DebugLogger.debug(`Timer ended: ${label} (${duration.toFixed(2)}ms)`);
    return duration;
  }

  /**
   * Get average duration for a label
   */
  static getAverageDuration(label: string): number {
    const matching = this.measurements.filter(m => m.label === label);
    if (matching.length === 0) return 0;
    const total = matching.reduce((sum, m) => sum + m.duration, 0);
    return Math.round((total / matching.length) * 100) / 100;
  }

  /**
   * Get all measurements
   */
  static getMeasurements(): any[] {
    return [...this.measurements];
  }

  /**
   * Get performance statistics
   */
  static getStats(): any {
    const labels = new Set(this.measurements.map(m => m.label));
    const stats: any = {
      totalMeasurements: this.measurements.length,
      uniqueLabels: labels.size,
      averageDurations: {}
    };

    labels.forEach(label => {
      stats.averageDurations[label] = this.getAverageDuration(label);
    });

    return stats;
  }

  /**
   * Clear measurements
   */
  static clear(): void {
    this.measurements = [];
    this.timers.clear();
  }
}

/**
 * State Inspector for debugging component state
 */
export class StateInspector {
  private static snapshots: Map<string, any> = new Map();

  /**
   * Take a snapshot of component state
   */
  static takeSnapshot(componentName: string, state: any): void {
    this.snapshots.set(componentName, {
      timestamp: new Date().toISOString(),
      state: JSON.parse(JSON.stringify(state))
    });
    DebugLogger.debug(`State snapshot taken: ${componentName}`, state);
  }

  /**
   * Get a snapshot
   */
  static getSnapshot(componentName: string): any {
    return this.snapshots.get(componentName);
  }

  /**
   * Get all snapshots
   */
  static getAllSnapshots(): any {
    return Object.fromEntries(this.snapshots);
  }

  /**
   * Compare two snapshots
   */
  static compareSnapshots(componentName: string, previousState: any): any {
    const current = this.snapshots.get(componentName)?.state;
    if (!current) {
      DebugLogger.warn(`Snapshot not found for: ${componentName}`);
      return null;
    }

    const changes: any = {};
    Object.keys(current).forEach(key => {
      if (JSON.stringify(current[key]) !== JSON.stringify(previousState[key])) {
        changes[key] = {
          previous: previousState[key],
          current: current[key]
        };
      }
    });

    return changes;
  }

  /**
   * Clear snapshots
   */
  static clear(): void {
    this.snapshots.clear();
  }
}
