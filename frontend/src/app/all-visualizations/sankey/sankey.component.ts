import { Component, OnInit } from "@angular/core";
import { BaseComponent } from "../base/base.component";
import { CommunicationService } from "../../visualizations/communication.service";
import { visualizationTypes } from "../../utils/visualizationTypes";
import { dateToString } from "../../utils/common";
import { Emotions } from "../../utils/emotions";
import { Interactions } from "../../utils/interactions";
import { Multimedia } from "../../utils/multimedia";
import { SidebarGlobalRequestsService } from "../../sidebar-global/sidebar-global-requests.service";
import { URLS } from "../../utils/urls";

@Component({
    selector: "app-sankey",
    templateUrl: "./sankey.component.html",
    styleUrls: ["./sankey.component.css"]
})
export class SankeyComponent extends BaseComponent implements OnInit {
    graph = {};

    dateRange = [];
    recoveredData;
    selectedToVisualize;
    selectedModel;

    constructor(
        private communicationService: CommunicationService,
        private requestsService: SidebarGlobalRequestsService,
        private urlsService: URLS,
        private emotionsEnum: Emotions,
        private interactionsEnum: Interactions,
        private multimediaEnum: Multimedia
    ) {
        super();
    }

    ngOnInit() {}

    getToVisualize() {
        return this.requestsService.get_toVisualizeList("sankey");
    }

    onRemove() {
        this.communicationService.removeVisualization("sankey");
    }
    
    askForData_and_visualize() {
        var requestType = this.selectedModel[0];
        var requestObj = this.selectedModel[1];

        var url = this.urlsService.getMultimediaInteraction(
            requestType,
            requestObj
        );

        this.requestsService.getData(url).subscribe(response => {
            this.recoveredData = this.prepareData(response);
            this.selectedToVisualize = true;
            this.updateGraph();
        });
    }

    prepareData(response) {
        var labels = [];
        var colors = [];
        var source = [];
        var target = [];
        var values = [];

        Object.entries(response).forEach(([key, value]) => {
            if (!labels.includes(key)) {
                labels.push(key);
                colors.push(this.multimediaEnum.getColors(key));
            }
        });

        Object.entries(response["image"]).forEach(([key, value]) => {
            if (!labels.includes(key)) {
                labels.push(key);
                colors.push(this.interactionsEnum.getColors(key));
            }
        });

        var source_n = 1;
        var actual = 5;
        Object.entries(response).forEach(([key, value]) => {
            if (key != "total") {
                source.push(0);
                target.push(source_n);
                actual = 5;
                Object.entries(value).forEach(([key2, value2]) => {
                    if (key2 == "total") {
                        values.push(value2);
                    } else {
                        source.push(source_n);
                        target.push(actual);
                        values.push(value2);
                        actual++;
                    }
                });
                source_n++;
            }
        });

        var recove = {
            labels: labels,
            colors: colors,
            source: source,
            target: target,
            values: values
        };

        return recove;
    }

    updateGraph() {
        var data = [
            {
                type: "sankey",
                orientation: "h",
                node: {
                    pad: 15,
                    thickness: 30,
                    line: {
                        color: "grey",
                        width: 0.3
                    },
                    label: this.recoveredData["labels"],
                    color: this.recoveredData["colors"]
                },

                link: {
                    source: this.recoveredData["source"],
                    target: this.recoveredData["target"],
                    value: this.recoveredData["values"]
                }
            }
        ];

        var layout = {
            margin: { l: 5, r: 5, b: 5, t: 5, pad: 0 },
            height: 400,
            font: {
                size: 12
            }
        };

        this.graph["data"] = data;
        this.graph["layout"] = layout;
    }
}
