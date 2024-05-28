import { Component, ElementRef, ViewChild } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FileUploadService } from './file-upload.service';
import { CommonModule } from '@angular/common';
import { ToastrService } from 'ngx-toastr';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,CommonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  selectedFile: File | null = null;
  imageToShow: string | ArrayBuffer | null = null;

  constructor(
    private fileUploadService: FileUploadService,
    private toastr: ToastrService
  ) {}

  // Functionality

  onFileSelected(event: Event): void {    
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      this.submitImage()
      this.readImage();
    }
  }


  submitImage() {
    if (this.selectedFile) {
      this.fileUploadService.uploadFile(this.selectedFile).subscribe(
        response => {
          this.toastr.success(response.msg.faces.msg,'La subida del archivo ha sido exitosa');          
        },
        error => {
          this.toastr.error(error.error.msg, 'La subida del archivo ha fallado');
        }
      );
    } else {
      this.toastr.error('No file selected', 'La subida del archivo ha fallado');
    }
  }

  // Style
  onDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.toggleDragOver(true);
  }

  onDrop(event: any) {
    event.preventDefault();
    event.stopPropagation();
    this.toggleDragOver(false);
    this.selectedFile = event.dataTransfer.files[0];
    this.readImage();
    this.submitImage()
  }

  onDragLeave(event: any) {
    event.preventDefault();
    event.stopPropagation();
    this.toggleDragOver(false);
  }

   readImage() {
    if (this.selectedFile) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.imageToShow = e.target?.result as string | ArrayBuffer;
      };
      reader.readAsDataURL(this.selectedFile);
    }
  }

  private toggleDragOver(isDragging: boolean) {
    const mainElement = document.querySelector('.main');
    const dropDialog = document.querySelector('.drop-dialog');
    if (mainElement && dropDialog) {
      if (isDragging) {
        mainElement.classList.add('dragover');
        dropDialog.classList.add('dragover');
      } else {
        dropDialog.classList.remove('dragover');
        mainElement.classList.remove('dragover');
      }
    }
  }

}
