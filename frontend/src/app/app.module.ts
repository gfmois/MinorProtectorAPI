import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ToastrModule } from 'ngx-toastr';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppComponent } from './app.component';
import { appConfig } from './app.config'; // Importa la configuración aquí

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot(),
    RouterModule.forRoot([]) // Aquí puedes importar tus rutas si las tienes definidas en app.routes.ts
  ],
  providers: [
    appConfig.providers // Usa los proveedores de la configuración
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
