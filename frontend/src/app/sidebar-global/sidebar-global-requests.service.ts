import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { visualizationRequests } from "../utils/requestsType";
import { RequestsType } from "../utils/requestsType";

@Injectable({
    providedIn: "root"
})
export class SidebarGlobalRequestsService {
    // array of tuples
    toVisualizeList: Array<[RequestsType, any]> = [];

    constructor(private http: HttpClient) {}

    recoverFollowed(url) {
        return this.http.get(url);
    }

    getData(url, type = "", params = {}) {
        if (type === "post") return this.http.post(url, {});
        if (type === "delete") return this.http.delete(url, {});

        return this.http.get(url, { params: params });
    }

    add_toVisualizeList(tuple) {
        this.toVisualizeList.push(tuple);
    }

    get_toVisualizeList(visType) {
        var listToReturn = [];
        for (let pair of this.toVisualizeList) {
            if (visualizationRequests[visType].includes(pair[0])) {
                listToReturn.push(pair);
            }
        }
        return listToReturn;
    }

    is_inVisualizeList(tuple) {
        return this.toVisualizeList.some(
            elem => elem[0] === tuple[0] && elem[1] === tuple[1]
        );
    }
}
