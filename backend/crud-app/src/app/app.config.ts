import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    // withFetch enables the modern fetch backend. withCredentials is set
    // per-request in each service (Angular has no global flag), so the
    // session cookie is sent to the Render backend on every call.
    provideHttpClient(withFetch())
  ]
};
