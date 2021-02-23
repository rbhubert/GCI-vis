import { Component, OnInit } from "@angular/core";
import { BaseComponent } from "../base/base.component";
import { CommunicationService } from "../../visualizations/communication.service";
import { DataService } from "../../visualizations/data.service";
import { visualizationTypes } from "../../utils/visualizationTypes";
import { dateToString } from "../../utils/common";
import { SidebarGlobalRequestsService } from "../../sidebar-global/sidebar-global-requests.service";
import { URLS } from "../../utils/urls";

@Component({
    selector: "app-interaction",
    templateUrl: "./interaction.component.html",
    styleUrls: ["./interaction.component.css"]
})
export class InteractionComponent extends BaseComponent implements OnInit {
    graph = {};

    dateRange = [];
    recoveredData;
    selectedToVisualize;
    selectedModel;

    constructor(
        private communicationService: CommunicationService,
        private requestsService: SidebarGlobalRequestsService,
        private urlsService: URLS
    ) {
        super();
    }

    ngOnInit() {}

    onRemove() {
        this.communicationService.removeVisualization("interaction");
    }

    getToVisualize() {
        return this.requestsService.get_toVisualizeList("interaction");
    }

    askForData_and_visualize() {
        var requestType = this.selectedModel[0];
        var requestObj = this.selectedModel[1];

        var url = this.urlsService.getInteraction(requestType, requestObj);

        this.requestsService.getData(url).subscribe(response => {
            this.recoveredData = response;
            this.selectedToVisualize = true;
            this.updateGraph();
        });
    }

    updateGraph() {
        // calcular circulos
        var calculate_sizes = [];
        var texts = [];
        var max_value = this.recoveredData["sets"][0]["size"];
        for (let x of this.recoveredData["sets"]) {
            var text_x = x["sets"].join();
            var result = 2 + (8 * x["size"]) / max_value;

            calculate_sizes.push(result);
            texts.push("#" + text_x + ": " + x["size"]);
        }

        var sizerefx = 0.125;

        var trace1 = {
            x: [55, 40, 55, 70, 40, 55, 70, 55],
            y: [30, 70, 70, 70, 110, 110, 110, 150],
            mode: "markers",
            marker: {
                color: [
                    "rgb(255,255,255)", //total
                    "rgb(204,204,51)", // comment
                    "rgb(0,0,204)", // retweet 55 70
                    "rgb(255,0,0)", // fav 70 70
                    "rgb(51,204,51)", // comm y retweet 40 110
                    "rgb(255,153,51)", // comment y fav 55 110
                    "rgb(153,0,204)", // retweet y fav 70 110
                    "rgb(51,51,0)" // comm fav ret 55 150
                ],
                line: {
                    color: "black",
                    width: 2
                },
                opacity: [1, 1, 1, 1, 1, 1, 1, 1],
                size: calculate_sizes,
                sizeref: sizerefx
            },
            text: texts,
            hoverinfo: "text"
        };

        var trace0 = {
            x: [55, 40, 55, 55, 55, 70],
            y: [30, 70, 30, 70, 30, 70],
            mode: "lines",
            line: {
                color: "black"
            }
        };

        var trace2 = {
            x: [40, 40, 40, 55],
            y: [70, 110, 70, 110],
            mode: "lines",
            line: {
                color: "rgb(204,204,51)"
            }
        };

        var trace3 = {
            x: [55, 70, 55, 40],
            y: [70, 110, 70, 110],
            mode: "lines",
            line: {
                color: "rgb(0,0,204)"
            }
        };

        var trace4 = {
            x: [70, 55, 70, 70],
            y: [70, 110, 70, 110],
            mode: "lines",
            line: {
                color: "rgb(255,0,0)"
            }
        };

        var trace5 = {
            x: [40, 55, 55, 55, 70, 55],
            y: [110, 150, 110, 150, 110, 150],
            mode: "lines",
            line: {
                color: "black"
            }
        };

        var data = [trace0, trace2, trace3, trace4, trace5, trace1];

        var layout = {
            showlegend: false,
            margin: { l: 5, r: 5, b: 5, t: 5, pad: 0 },
            height: 400,
            xaxis: {
                autorange: true,
                showgrid: false,
                zeroline: false,
                showline: false,
                ticks: "",
                showticklabels: false,
                fixedrange: true
            },
            yaxis: {
                autorange: true,
                showgrid: false,
                zeroline: false,
                showline: false,
                ticks: "",
                showticklabels: false,
                fixedrange: true
            },
            hovermode: "closest"
        };

        this.graph["data"] = data;
        this.graph["layout"] = layout;
    }
}
