import { Component, OnInit, Input } from "@angular/core";
import { CommunicationService } from "../visualizations/communication.service";
import {
    visualizationTypes,
    visualizationIcons,
    visualizationText
} from "../utils/visualizationTypes";
import { RequestsType, visualizationRequests } from "../utils/requestsType";
import { FormControl } from "@angular/forms";
import { Observable, BehaviorSubject } from "rxjs";
import { map, startWith } from "rxjs/operators";
@Component({
    selector: "app-add-visualization",
    templateUrl: "./add-visualization.component.html",
    styleUrls: ["./add-visualization.component.css"]
})
export class AddVisualizationComponent implements OnInit {
    @Input() disableVis: boolean;

    requestsTypes: String[] = [];
    requestModel: String = RequestsType.ALL;

    visualizations = [];

    constructor(private communication: CommunicationService) {
        for (let requestsKey of Object.entries(RequestsType)) {
            this.requestsTypes.push(requestsKey[1]);
        }
    }

    ngOnInit() {
        this.communication.addVis.subscribe(visType => {
            this.visualizations.push(visType);
        });

        this.communication.removeVis.subscribe(visType => {
            const index = this.visualizations.indexOf(visType, 0);
            if (index > -1) {
                this.visualizations.splice(index, 1);
            }
        });
        this.getKeys();
    }

    addVisualization(visType) {
        this.communication.addVisualization(visType);
    }

    getKeys() {
        return Object.keys(visualizationTypes);
    }

    inArray(element) {
        return this.visualizations.includes(element);
    }

    getIcon(element) {
        return visualizationIcons[element];
    }

    getText(element) {
        return visualizationText[element];
    }

    canShow(visType) {
        if (this.requestModel.valueOf() === RequestsType.ALL.valueOf())
            return true;
        else
            return visualizationRequests[visType].includes(
                this.requestModel.valueOf()
            );
    }

    changeRequestType(request) {
        this.requestModel = request.name;
    }
}
