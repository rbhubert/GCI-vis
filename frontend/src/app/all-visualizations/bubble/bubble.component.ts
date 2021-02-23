import { Component, OnInit } from "@angular/core";
import { BaseComponent } from "../base/base.component";
import { SidebarGlobalRequestsService } from "../../sidebar-global/sidebar-global-requests.service";
import { CommunicationService } from "../../visualizations/communication.service";
import { dateToString } from "../../utils/common";
import { Emotions } from "../../utils/emotions";
import { URLS } from "../../utils/urls";

@Component({
    selector: "app-bubble",
    templateUrl: "./bubble.component.html",
    styleUrls: ["./bubble.component.css"]
})
export class BubbleComponent extends BaseComponent implements OnInit {
    graph = {};

    dateRange = [];
    recoveredData;
    selectedToVisualize;
    selectedModel;

    constructor(
        private communicationService: CommunicationService,
        private requestsService: SidebarGlobalRequestsService,
        private emotionsEnum: Emotions,
        private urlsService: URLS
    ) {
        super();
    }

    ngOnInit() {}

    getToVisualize() {
        return this.requestsService.get_toVisualizeList("bubble");
    }

    onRemove() {
        this.communicationService.removeVisualization("bubble");
    }

    askForData_and_visualize() {
        var requestType = this.selectedModel[0];
        var requestObj = this.selectedModel[1];

        var url = this.urlsService.getEmotions(requestType, requestObj);
        this.requestsService.getData(url).subscribe(response => {
            this.recoveredData = response;
            this.selectedToVisualize = true;
            this.updateGraph();
        });
    }

    updateGraph() {
        var recoveredData = this.recoveredData;

        var dates = [];
        var values = [];
        var emotions = {};

        Object.entries(recoveredData).forEach(([key, content]) => {
            dates.push(key);
            values.push(content["value"]);
            Object.entries(content["emotions"]).forEach(
                ([keyemo, valueemo]) => {
                    if (keyemo in emotions) {
                        emotions[keyemo].push(valueemo);
                    } else {
                        emotions[keyemo] = [valueemo];
                    }
                }
            );
        });

        var data = [];
        Object.entries(emotions).forEach(([keyemo, valueemo]) => {
            var nvalues = [];
            Object.values(valueemo).forEach(val => {
                nvalues.push(val * 50);
            });

            var trace1 = {
                name: keyemo,
                mode: "markers",
                x: dates,
                y: values,
                marker: {
                    color: this.emotionsEnum.getColors(keyemo),
                    size: nvalues,
                    sizemode: "area"
                }
            };
            data.push(trace1);
        });

        var sinceD = dates[0];
        var untilD = dates[Object.keys(recoveredData).length];

        var layout = {
            margin: { l: 5, r: 5, b: 20, t: 5, pad: 0 },
            height: 400,
            xaxis: {
                range: [sinceD, untilD]
            },
            yaxis: {
                autorange: true,
                type: "linear",
                showgrid: false,
                showticklabels: false
            },
            legend: {
                orientation: "v",
                xanchor: "left",
                bgcolor: "rgb(248, 248, 248)",
                x: 1.1,
                y: 1
            }
        };

        this.graph["data"] = data;
        this.graph["layout"] = layout;
    }
}
