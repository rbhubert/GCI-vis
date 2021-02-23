import { Component, OnInit } from "@angular/core";
import { BaseComponent } from "../base/base.component";
import { CommunicationService } from "../../visualizations/communication.service";
import { SidebarGlobalRequestsService } from "../../sidebar-global/sidebar-global-requests.service";
import { DataService } from "../../visualizations/data.service";
import { visualizationTypes } from "../../utils/visualizationTypes";
import { dateToString } from "../../utils/common";
import { Emotions } from "../../utils/emotions";
import { URLS } from "../../utils/urls";

@Component({
    selector: "app-radar",
    templateUrl: "./radar.component.html",
    styleUrls: ["./radar.component.css"]
})
export class RadarComponent extends BaseComponent implements OnInit {
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
        return this.requestsService.get_toVisualizeList("radar");
    }

    onRemove() {
        this.communicationService.removeVisualization("radar");
    }

    askForData_and_visualize() {
        var requestType = this.selectedModel[0];
        var requestObj = this.selectedModel[1];

        var url = this.urlsService.getEmotionsRadar(requestType, requestObj);

        this.requestsService.getData(url).subscribe(response => {
            this.recoveredData = response;
            this.selectedToVisualize = true;
            this.updateGraph();
        });
    }

    updateGraph() {
        var theta = Object.keys(this.recoveredData["emotions"]);
        var data = [];
        var higher = 0;

        var trace = {
            type: "scatterpolar",
            r: [
                Number.MAX_SAFE_INTEGER,
                0,
                Number.MAX_SAFE_INTEGER,
                0,
                Number.MAX_SAFE_INTEGER,
                0,
                Number.MAX_SAFE_INTEGER,
                0,
                Number.MAX_SAFE_INTEGER,
                0,
                Number.MAX_SAFE_INTEGER,
                0,
                Number.MAX_SAFE_INTEGER,
                0,
                Number.MAX_SAFE_INTEGER,
                0
            ],
            theta: theta,
            fill: "toself",
            name: "grid",
            marker: {
                color: "rgb(200, 200, 200)",
                size: 1
            }
        };

        data.push(trace);

        Object.entries(this.recoveredData["keys"]).forEach(
            ([keyemo, valueemo]) => {
                // importa el valueemo
                var i = theta.indexOf(String(valueemo));
                var arraySent = [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ];
                arraySent.splice(
                    i,
                    1,
                    this.recoveredData["emotions"][theta[i]]
                );
                i = i + 1;
                arraySent.splice(
                    i,
                    1,
                    this.recoveredData["emotions"][theta[i]]
                );
                i = i - 2;
                if (i < 0) {
                    i = theta.length - 1;
                }
                arraySent.splice(
                    i,
                    1,
                    this.recoveredData["emotions"][theta[i]]
                );

                var trace = {
                    type: "scatterpolar",
                    r: arraySent,
                    theta: theta,
                    fill: "toself",
                    fillcolor: this.emotionsEnum.getColors(String(valueemo)),
                    opacity: 0.7,
                    line: {
                        color: this.emotionsEnum.getColors(String(valueemo))
                    },
                    marker: {
                        size: 1
                    }
                };

                data.push(trace);
                higher = Math.max(
                    higher,
                    this.recoveredData["emotions"][String(valueemo)]
                );
            }
        );

        var layout = {
            height: 400,
            polar: {
                radialaxis: {
                    visible: false,
                    range: [0, higher],
                    fixedrange: true
                },
                angularaxis: {
                    showgrid: false, // Oculta las lineas del grafico
                    ticklen: 10,
                    tickcolor: "#FFFFFF",
                    fixedrange: true
                }
            },
            showlegend: false
        };

        this.graph["data"] = data;
        this.graph["layout"] = layout;
    }
}
