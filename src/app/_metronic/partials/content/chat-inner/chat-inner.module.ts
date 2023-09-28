import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { InlineSVGModule } from 'ng-inline-svg-2';
import { ChatInnerComponent } from './chat-inner.component';
import { TranslateModule } from '@ngx-translate/core';

@NgModule({
  declarations: [ChatInnerComponent],
  imports: [CommonModule, InlineSVGModule, TranslateModule],
  exports: [ChatInnerComponent],
})
export class ChatInnerModule {}
