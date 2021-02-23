import { BaseComponent } from "../all-visualizations/base/base.component";
import { MultimediaComponent } from "../all-visualizations/multimedia/multimedia.component";
import { InteractionComponent } from "../all-visualizations/interaction/interaction.component";
import { BubbleComponent } from "../all-visualizations/bubble/bubble.component";
import { RadarComponent } from "../all-visualizations/radar/radar.component";
import { SankeyComponent } from "../all-visualizations/sankey/sankey.component";
import { WordcloudComponent } from "../all-visualizations/wordcloud/wordcloud.component";
import { TimeseriesComponent } from "../all-visualizations/timeseries/timeseries.component";
import { RequestsType } from "../utils/requestsType";

export var visualizationTypes = {
    multimedia: MultimediaComponent,
    interaction: InteractionComponent,
    bubble: BubbleComponent,
    radar: RadarComponent,
    sankey: SankeyComponent,
    wordcloud: WordcloudComponent,
    timeseries: TimeseriesComponent
};

export var visualizationIcons = {
    multimedia: "hdr_weak",
    interaction: "forum",
    bubble: "bubble_chart",
    radar: "flare",
    sankey: "label_important",
    wordcloud: "cloud",
    timeseries: "timeline"
};

export var visualizationText = {
    multimedia: "Euler Diagram",
    interaction: "Hasse Diagram",
    bubble: "Bubble Chart",
    radar: "Radar Chart",
    sankey: "Sankey Diagram",
    wordcloud: "Word Cloud",
    timeseries: "Time Series Chart"
};
