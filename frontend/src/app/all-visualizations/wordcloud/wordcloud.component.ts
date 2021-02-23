import { Component, OnInit, ElementRef, Renderer2 } from "@angular/core";
import { BaseComponent } from "../base/base.component";
import { CommunicationService } from "../../visualizations/communication.service";
import { SidebarGlobalRequestsService } from "../../sidebar-global/sidebar-global-requests.service";
import { visualizationTypes } from "../../utils/visualizationTypes";
import { dateToString } from "../../utils/common";
import { URLS } from "../../utils/urls";
import { Emotions } from "../../utils/emotions";

import * as D3 from "d3";
import { AgWordCloudData } from "node_modules/angular4-word-cloud";
declare let d3: any;
import * as cloud from "js/d3.layout.cloud";

@Component({
	selector: "app-wordcloud",
	templateUrl: "./wordcloud.component.html",
	styleUrls: ["./wordcloud.component.css"]
})
export class WordcloudComponent extends BaseComponent implements OnInit {
	WORDS: Array<AgWordCloudData> = [];

	dateRange = [];
	selectedToVisualize;
	selectedModel;

	constructor(
		private communicationService: CommunicationService,
		private renderer: Renderer2,
		private requestsService: SidebarGlobalRequestsService,
		private urlsService: URLS
	) {
		super();
	}

	ngOnInit() {}

	onRemove() {
		this.communicationService.removeVisualization("wordcloud");
	}

	getToVisualize() {
		return this.requestsService.get_toVisualizeList("wordcloud");
	}

	askForData_and_visualize() {
		this.WORDS = [];

		var requestType = this.selectedModel[0];
		var requestObj = this.selectedModel[1];

		var url = this.urlsService.getWordcloud(requestType, requestObj);

		this.requestsService.getData(url).subscribe(response => {
			D3.select("#visTest")
				.select("svg")
				.remove();

			Object.entries(response).forEach(([key, value]) => {
				this.WORDS.push(value);
			});

			this.selectedToVisualize = true;
			this.updateGraph();
		});
	}

	updateGraph() {
		var layout = cloud()
			.size([600, 600])
			.words(this.WORDS)
			.padding(5)
			.rotate(function() {
				return ~~(Math.random() * 2) * 90;
			})
			.font("Impact")
			.fontSize(function(d) {
				return d.size * 10;
			})
			.on("end", draw);

		layout.start();

		function draw(words) {
			D3.select("#visTest")
				.append("svg")
				.attr("width", layout.size()[0])
				.attr("height", layout.size()[1])
				.append("g")
				.attr(
					"transform",
					"translate(" +
						layout.size()[0] / 2 +
						"," +
						layout.size()[1] / 2 +
						")"
				)
				.selectAll("text")
				.data(words)
				.enter()
				.append("text")
				.style("font-size", function(d) {
					return d.size + "px";
				})
				.style("font-family", "Impact")
				.style("fill", function(d) {
					if (d.emotions.length > 0) {
						var x = new Emotions();
						return x.getColors(d.emotions[0]);
					} else {
						return "grey";
					}
				})
				.style("cursor", "help")
				.attr("text-anchor", "middle")
				.attr("transform", function(d) {
					return (
						"translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"
					);
				})
				.text(function(d) {
					return d.text;
				})
				.on("mouseover", handleMouseOver)
				.on("mouseout", handleMouseOut)
				.on("click", handleOnClick);
		}
		// Create Event Handlers for mouse
		function handleMouseOver(d, i) {
			D3.select(this)
				.style("font-size", function(d) {
					return d.size + 20 + "px";
				})
				.style("font-family", "Impact")
				.style("fill", function(d) {
					if (d.emotions.length > 0) {
						var x = new Emotions();
						return x.getColors(d.emotions[0]);
					} else {
						return "grey";
					}
				})
				.style("cursor", "help")
				.attr("text-anchor", "middle")

				.text(function(d) {
					return d.text;
				});
		}

		function handleMouseOut(d, i) {
			D3.select(this)
				.style("font-size", function(d) {
					return d.size + "px";
				})
				.style("font-family", "Impact")
				.style("fill", function(d) {
					if (d.emotions.length > 0) {
						var x = new Emotions();
						return x.getColors(d.emotions[0]);
					} else {
						return "grey";
					}
				})
				.style("cursor", "help")
				.attr("text-anchor", "middle")

				.text(function(d) {
					return d.text;
				});
		}

		function handleOnClick(d, i) {
			console.log("handle ONCLICK");
			console.log(d, i);
		}
	}

	wordClicked(word) {
		alert(word);
	}
}
