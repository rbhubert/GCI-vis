import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { RequestsType } from "../utils/requestsType";

@Injectable({
    providedIn: "root"
})
export class DataService {
    constructor(
        private http: HttpClient,
        private requestsType: RequestsType
    ) {}

    getTimeSeries(socialNetwork: string, account: string, date: string) {
        var timeseriesURL =
            //       this.urls.ACTIVITY +
            socialNetwork.toLowerCase() + "/" + account + "/" + date;

        return this.http.get(timeseriesURL);
    }

    getHasse(socialNetwork: string, account: string, date: string) {
        var interactionURL =
            //     this.urls.INTERACTION +
            socialNetwork.toLowerCase() + "/" + account + "/" + date;
        return this.http.get(interactionURL);
    }

    getEuler(socialNetwork: string, account: string, date: string) {
        var multimediaURL =
            //    this.urls.MULTIMEDIA +
            socialNetwork.toLowerCase() + "/" + account + "/" + date;
        return this.http.get(multimediaURL);
    }

    getRadar(socialNetwork: string, account: string, date: string) {
        var interactionURL =
            //    this.urls.EMOTIONS_RADAR +
            socialNetwork.toLowerCase() + "/" + account + "/" + date;
        return this.http.get(interactionURL);
    }

    getBubble(socialNetwork: string, account: string, date: string) {
        var interactionURL =
            //     this.urls.EMOTIONS +
            socialNetwork.toLowerCase() + "/" + account + "/" + date;
        return this.http.get(interactionURL);
    }

    getSankey(socialNetwork: string, account: string, date: string) {
        var interactionURL =
            //     this.urls.MULTIMEDIA_INTERACTION +
            socialNetwork.toLowerCase() + "/" + account + "/" + date;
        return this.http.get(interactionURL);
    }

    getWordcloud(socialNetwork: string, account: string, date: string) {
        var wordcloudURL =
            //     this.urls.WORDCLOUD +
            socialNetwork.toLowerCase() + "/" + account + "/" + date;
        return this.http.get(wordcloudURL);
    }
}
