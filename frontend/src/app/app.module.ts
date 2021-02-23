import "hammerjs";

import { BrowserModule } from "@angular/platform-browser";
import { NgModule } from "@angular/core";
import { AppComponent } from "./app.component";

// BrowserAnimationsModule para animaciones
// NoopAnimationsModule para no-animaciones
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";

// angular components
import { MatSidenavModule } from "@angular/material/sidenav";
import { MatButtonModule } from "@angular/material/button";
import { MatDividerModule } from "@angular/material/divider";
import { MatExpansionModule } from "@angular/material/expansion";
import { MatSelectModule } from "@angular/material/select";
import { FormsModule } from "@angular/forms";
import { HttpClientModule } from "@angular/common/http";
import { MatRadioModule } from "@angular/material/radio";
import { MatIconModule } from "@angular/material/icon";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material";
import { MatDatepickerModule } from "@angular/material/datepicker";
import { MatNativeDateModule } from "@angular/material";
import { MatChipsModule } from "@angular/material/chips";
import { MatCardModule } from "@angular/material/card";
import { DragDropModule } from "@angular/cdk/drag-drop";
import { MatGridListModule } from "@angular/material/grid-list";
import { MatListModule } from "@angular/material/list";
import { MatAutocompleteModule } from "@angular/material/autocomplete";
import { ReactiveFormsModule } from "@angular/forms";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { MatProgressBarModule } from "@angular/material/progress-bar";
//import { RouterModule, Routes } from "@angular/router";

// components
import { VisualizationsComponent } from "./visualizations/visualizations.component";
import { AddVisualizationComponent } from "./add-visualization/add-visualization.component";
import { BaseComponent } from "./all-visualizations/base/base.component";
import { MultimediaComponent } from "./all-visualizations/multimedia/multimedia.component";
import { InteractionComponent } from "./all-visualizations/interaction/interaction.component";
import { BubbleComponent } from "./all-visualizations/bubble/bubble.component";
import { RadarComponent } from "./all-visualizations/radar/radar.component";
import { SankeyComponent } from "./all-visualizations/sankey/sankey.component";
import { WordcloudComponent } from "./all-visualizations/wordcloud/wordcloud.component";
import { TimeseriesComponent } from "./all-visualizations/timeseries/timeseries.component";
import { SidebarGlobalComponent } from "./sidebar-global/sidebar-global.component";
import { AccountFollowedManagerComponent } from "./sidebar-global/account-followed-manager/account-followed-manager.component";
import { PageNotFoundComponent } from "./page-not-found/page-not-found.component";
import { UserSettingsComponent } from './user-settings/user-settings.component';

// external components
import { PlotlyModule } from "angular-plotly.js";
import { AgWordCloudModule } from "node_modules/angular4-word-cloud";

// global services
import { CommunicationService } from "./visualizations/communication.service";
import { DataService } from "./visualizations/data.service";

// enums
import { URLS } from "./utils/urls";
import { Emotions } from "./utils/emotions";
import { Interactions } from "./utils/interactions";
import { Multimedia } from "./utils/multimedia";
import { RequestsType } from "./utils/requestsType";
import { ListToVisualizePipe } from "./pipes/list-to-visualize.pipe";


// const appRoutes: Routes = [
//   { path: 'settings', component: UserSettingsComponent },
//   { path: 'u', component: HeroListComponent },
// ];


@NgModule({
    declarations: [
        AppComponent,
        VisualizationsComponent,
        AddVisualizationComponent,
        BaseComponent,
        MultimediaComponent,
        InteractionComponent,
        BubbleComponent,
        RadarComponent,
        SankeyComponent,
        WordcloudComponent,
        TimeseriesComponent,
        SidebarGlobalComponent,
        ListToVisualizePipe,
        AccountFollowedManagerComponent,
        PageNotFoundComponent,
        UserSettingsComponent
    ],
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        MatSidenavModule,
        MatButtonModule,
        MatDividerModule,
        MatExpansionModule,
        MatDatepickerModule,
        MatFormFieldModule,
        MatIconModule,
        MatNativeDateModule,
        MatInputModule,
        MatSelectModule,
        FormsModule,
        HttpClientModule,
        MatRadioModule,
        MatChipsModule,
        MatCardModule,
        DragDropModule,
        MatGridListModule,
        MatListModule,
        MatAutocompleteModule,
        ReactiveFormsModule,
        PlotlyModule,
        MatProgressBarModule,
        MatProgressSpinnerModule,
        AgWordCloudModule.forRoot()
    ],
    providers: [
        CommunicationService,
        DataService,
        HttpClientModule,
        URLS,
        Emotions,
        Interactions,
        Multimedia,
        RequestsType
    ],
    bootstrap: [AppComponent],
    entryComponents: [
        BaseComponent,
        InteractionComponent,
        MultimediaComponent,
        BubbleComponent,
        RadarComponent,
        SankeyComponent,
        WordcloudComponent,
        TimeseriesComponent
    ]
})
export class AppModule {}
