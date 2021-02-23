import { Component, OnInit } from "@angular/core";
import { BaseComponent } from "../base/base.component";
import { DataService } from "../../visualizations/data.service";
import { dateToString } from "../../utils/common";
import { URLS } from "../../utils/urls";
import { SidebarGlobalRequestsService } from "../../sidebar-global/sidebar-global-requests.service";
import { CommunicationService } from "../../visualizations/communication.service";

import * as D3 from "d3";
import * as venn from "js/diagram";

@Component({
    selector: "app-multimedia",
    templateUrl: "./multimedia.component.html",
    styleUrls: ["./multimedia.component.css"]
})
export class MultimediaComponent extends BaseComponent implements OnInit {
    private vennData;

    dateRange = [];
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

    getToVisualize() {
        return this.requestsService.get_toVisualizeList("multimedia");
    }

    onRemove() {
        this.communicationService.removeVisualization("multimedia");
    }

    askForData_and_visualize() {
        var requestType = this.selectedModel[0];
        var requestObj = this.selectedModel[1];

        var url = this.urlsService.getMultimedia(requestType, requestObj);

        this.requestsService.getData(url).subscribe(response => {
            this.selectedToVisualize = true;

            this.vennData = response;
            D3.select("#venn")
                .selectAll("svg")
                .remove();

            this.updateGraph();
        });
    }

    updateGraph() {
        // draw venn diagram
        var div = D3.select("#venn");
        div.datum(this.vennData).call(venn.VennDiagram());

        // add a tooltip
        var tooltip = D3.select(".venntooltip");

        // add listeners to all the groups to display tooltip on mouseover
        div.selectAll("g")
            .on("mouseover", function(d, i) {
                // sort all the areas relative to the current item
                venn.sortAreas(div, d);

                // Display a tooltip with the current size
                tooltip
                    .transition()
                    .duration(400)
                    .style("opacity", 0.9);
                tooltip.text(d["size"] + " shares");

                // highlight the current path
                var selection = D3.select(this)
                    .transition("tooltip")
                    .duration(400);
                selection
                    .select("path")
                    .style("stroke-width", 3)
                    .style("fill-opacity", d["sets"].length == 1 ? 0.4 : 0.1)
                    .style("stroke-opacity", 1);
            })

            .on("mousemove", function() {
                tooltip
                    .style("left", D3.event.pageX - 10 + "px")
                    .style("top", D3.event.pageY - 50 + "px");
            })

            .on("mouseout", function(d, i) {
                tooltip
                    .transition()
                    .duration(400)
                    .style("opacity", 0);
                var selection = D3.select(this)
                    .transition("tooltip")
                    .duration(400);
                selection
                    .select("path")
                    .style("stroke-width", 0)
                    .style("fill-opacity", d["sets"].length == 1 ? 0.25 : 0.0)
                    .style("stroke-opacity", 0);
            });
    }
}
