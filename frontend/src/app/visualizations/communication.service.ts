import { Injectable } from "@angular/core";
import { BehaviorSubject } from "rxjs";

@Injectable({
    providedIn: "root"
})
export class CommunicationService {
    private messageAdd = new BehaviorSubject("");
    private messageRemove = new BehaviorSubject("");

    addVis = this.messageAdd.asObservable();
    removeVis = this.messageRemove.asObservable();

    alreadyVisualize: Array<[any, any]> = new Array<[any, any]>();

    constructor() {}

    addVisualization(visualization: string) {
        this.messageAdd.next(visualization);
    }

    removeVisualization(visualization: string) {
        this.messageRemove.next(visualization);
    }

    addVisualize(tuple) {
        this.alreadyVisualize.push(tuple);
    }

    removeVisualize(tuple) {
        const index = this.alreadyVisualize.indexOf(tuple, 0);
        if (index > -1) {
            this.alreadyVisualize.splice(index, 1);
        }
    }
}
