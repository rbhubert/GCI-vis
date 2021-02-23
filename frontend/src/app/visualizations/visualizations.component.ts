import {
    Component,
    OnInit,
    AfterViewInit,
    ViewChild,
    QueryList,
    ElementRef,
    ComponentFactoryResolver,
    ComponentFactory,
    ViewContainerRef
} from "@angular/core";
import { CommunicationService } from "../visualizations/communication.service";
import { BaseComponent } from "../all-visualizations/base/base.component";
import { visualizationTypes } from "../utils/visualizationTypes";

@Component({
    selector: "app-visualizations",
    templateUrl: "./visualizations.component.html",
    styleUrls: ["./visualizations.component.css"]
})
export class VisualizationsComponent implements OnInit {
    @ViewChild("boundaryT", { read: ViewContainerRef })
    viewContainer: ViewContainerRef;
    componentFactory: ComponentFactory<BaseComponent>;
    components = [];

    constructor(
        private componentFactoryResolver: ComponentFactoryResolver,
        private communication: CommunicationService
    ) {}

    ngOnInit() {
        this.communication.addVis.subscribe(visType => {
            if (visType != "" && visType != undefined)
                this.onAddComponentClick(visType);
        });

        this.communication.removeVis.subscribe(visType => {
            if (visType != "" && visType != undefined)
                this.onRemoveComponentClick(visType);
        });
    }

    onAddComponentClick(visType) {
        // resolveComponentFactory depende del message (define la clase específica)
        this.componentFactory = this.componentFactoryResolver.resolveComponentFactory(
            visualizationTypes[visType]
        );
        let compo = this.viewContainer.createComponent(this.componentFactory);
        this.components.push(compo);
    }

    onRemoveComponentClick(visType) {
        const component = this.components.find(
            component =>
                component.instance instanceof visualizationTypes[visType]
        );
        const componentIndex = this.components.indexOf(component);

        if (componentIndex !== -1) {
            // Remove component from both view and array
            this.viewContainer.remove(this.viewContainer.indexOf(component));
            this.components.splice(componentIndex, 1);
        }
    }
}
