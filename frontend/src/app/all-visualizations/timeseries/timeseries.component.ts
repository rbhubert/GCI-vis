import { Component, OnInit } from "@angular/core";
import { BaseComponent } from "../base/base.component";
import { CommunicationService } from "../../visualizations/communication.service";
import { visualizationTypes } from "../../utils/visualizationTypes";
import { dateToString, monthNames } from "../../utils/common";
import { Emotions } from "../../utils/emotions";
import { Interactions } from "../../utils/interactions";
import { SidebarGlobalRequestsService } from "../../sidebar-global/sidebar-global-requests.service";
import { URLS } from "../../utils/urls";

@Component({
    selector: "app-timeseries",
    templateUrl: "./timeseries.component.html",
    styleUrls: ["./timeseries.component.css"]
})
export class TimeseriesComponent extends BaseComponent implements OnInit {
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
        private interactionsEnum: Interactions
    ) {
        super();
    }

    ngOnInit() {}

    getToVisualize() {
        return this.requestsService.get_toVisualizeList("timeseries");
    }

    onRemove() {
        this.communicationService.removeVisualization("timeseries");
    }

    askForData_and_visualize() {
        var requestType = this.selectedModel[0];
        var requestObj = this.selectedModel[1];

        var url = this.urlsService.getActivity(requestType, requestObj);

        this.requestsService.getData(url).subscribe(response => {
            this.recoveredData = response;
            this.selectedToVisualize = true;
            this.updateGraph();
        });
    }

    updateGraph() {
        var dates = [];
        var values = [];
        var interactions = {};
        var emotions = {};
        var texts = [];

        Object.entries(this.recoveredData).forEach(([key, content]) => {
            dates.push(key);
            values.push(content["value"]);
            var hash = Object.keys(content["hashtags"])
                .sort(function(a, b) {
                    return content["hashtags"][b] - content["hashtags"][a];
                })
                .slice(0, 3)
                .map(function(e) {
                    return "#" + e;
                });

            var hashText = "Hashtags: " + hash.join("<br>");
            Object.entries(content["interactions"]).forEach(
                ([keyint, valueint]) => {
                    if (keyint in interactions) {
                        interactions[keyint].push(valueint);
                    } else {
                        interactions[keyint] = [valueint];
                    }
                }
            );

            Object.entries(content["emotions"]).forEach(
                ([keyemo, valueemo]) => {
                    if (keyemo in emotions) {
                        emotions[keyemo].push(valueemo);
                    } else {
                        emotions[keyemo] = [valueemo];
                    }
                }
            );

            var dateDate = new Date(key.toString());
            var dateText =
                monthNames[dateDate.getMonth()] +
                " " +
                dateDate.getUTCDate() +
                ", " +
                dateDate.getFullYear();

            texts.push(
                dateText +
                    "<br>" +
                    "Official posts: " +
                    content["value"] +
                    "<br>" +
                    hashText
            );
        });

        //traces
        var data = [];

        var trace = {
            type: "bar",
            name: "activity level",
            x: dates,
            y: values,
            marker: {
                color: "rgb(204,204,204)",
                opacity: 0.4,
                line: {
                    color: "rgb(153,153,153)",
                    width: 1.5
                }
            },
            text: texts,
            hoverinfo: "text"
        };
        data.push(trace);

        Object.entries(emotions).forEach(([keyemo, valueemo]) => {
            var trace1 = {
                type: "scatter",
                mode: "lines",
                name: keyemo,
                x: dates,
                y: valueemo,
                visible: "legendonly",
                line: {
                    color: this.emotionsEnum.getColors(keyemo),
                    shape: "spline",
                    smoothing: 0.5
                }
            };
            data.push(trace1);
        });

        Object.entries(interactions).forEach(([keyint, valueint]) => {
            var trace2 = {
                type: "scatter",
                mode: "lines",
                name: keyint,
                yaxis: "y2",
                x: dates,
                y: valueint,
                visible: "legendonly",
                text: valueint,
                hoverinfo: "text+name",
                line: {
                    color: this.interactionsEnum.getColors(keyint),
                    shape: "spline",
                    smoothing: 0.5,
                    width: 3,
                    dash: "dot"
                }
            };
            data.push(trace2);
        });

        var sinceDate_aux = Object.keys(this.recoveredData)[0];
        //dateToString(this.dateRange[0]);
        var untilDate_aux;
        if (this.dateRange[1] == null) {
            untilDate_aux = dateToString(new Date());
        } else {
            untilDate_aux = dateToString(this.dateRange[1]);
        }

        var layout = {
            xaxis: {
                range: [sinceDate_aux, untilDate_aux],
                rangeslider: { range: [sinceDate_aux, untilDate_aux] },
                type: "date"
            },
            yaxis: {
                autorange: true,
                type: "linear"
            },
            yaxis2: {
                autorange: true,
                title: "interactions",
                titlefont: { color: "rgb(148, 103, 189)" },
                tickfont: { color: "rgb(148, 103, 189)" },
                overlaying: "y",
                side: "right",
                zeroline: false
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
