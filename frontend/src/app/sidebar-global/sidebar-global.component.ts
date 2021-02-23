import { Component, OnInit, Input } from "@angular/core";
import { MatSidenavModule } from "@angular/material/sidenav";
import { socialNetworks } from "../utils/config";
import { SidebarGlobalRequestsService } from "./sidebar-global-requests.service";
import { RequestsType } from "../utils/requestsType";
import { URLS } from "../utils/urls";
import { Response } from "@angular/http";

@Component({
    selector: "app-sidebar-global",
    templateUrl: "./sidebar-global.component.html",
    styleUrls: ["./sidebar-global.component.css"]
})
export class SidebarGlobalComponent implements OnInit {
    @Input() drawerLeft: MatSidenavModule;
    @Input() drawerRight: MatSidenavModule;

    socialNetworks = socialNetworks;
    activeTab = 0;

    // ngModels
    accountModel = ["Twitter", "SSalud_mx"];
    newsModel =
        "https://www.lanueva.com/nota/2019-9-12-20-2-0-actrices-argentinas-realizo-una-nueva-denuncia-de-acoso-sexual-en-el-ambiente-artistico";
    hashtagModel = "#BancoNacion";

    waitingForJob = false;

    jobID = [];
    intervalToCheck;

    constructor(
        private requestsService: SidebarGlobalRequestsService,
        private urlsService: URLS
    ) {}

    ngOnInit() {
        this.intervalToCheck = setInterval(() => {
            this.checkJobID();
        }, 2000);
    }

    checkJobID(){
        if (this.jobID.length === 0){
            return ;
        }

        var url = this.urlsService.getJobsStatus(this.jobID[0]);

        this.requestsService.getData(url).subscribe(response => {
            if (response["data"]["task_status"] === "finished"){
                this.requestsService.add_toVisualizeList(this.jobID[1]);
                this.waitingForJob = false;
                this.jobID = [];
            }           
        });
    }

    setActiveTab(tab) {
        this.activeTab = tab;
    }

    followAccount() {
        var accountStr = this.accountModel[0] + "-" + this.accountModel[1];
        var tuple = [RequestsType.SOCIALMEDIA, accountStr];

        var url = this.urlsService.getFollowAccount(
            this.accountModel[0],
            this.accountModel[1]
        );

        this.urlsService.ACCOUNTS +
            "/" +
            this.accountModel[0].toLowerCase() +
            "/" +
            this.accountModel[1];

        this.waitingForJob = true;
        this.requestsService.getData(url, "post").subscribe((response: Response) => {
            this.jobID = [response.toString(), tuple];
        });
    }

    canNoFollow() {
        var accountStr = this.accountModel[0] + "-" + this.accountModel[1];
        var tuple = [RequestsType.SOCIALMEDIA, accountStr];

        return this.requestsService.is_inVisualizeList(tuple) || this.waitingForJob;
    }

    checkNews() {
        var tuple = [RequestsType.NEWSPAPER, this.newsModel];
        var url = this.urlsService.NEWSPAPER;
        var paramsUrl = { newUrl: this.newsModel };
        // encodeURIComponent(this.newsModel);

        this.waitingForJob = true;
        this.requestsService
            .getData(url, "get", paramsUrl)
            .subscribe(response => {
                this.waitingForJob = false;
                this.requestsService.add_toVisualizeList(tuple);
            });
    }

    searchHashtag() {
        var tuple = [RequestsType.HASHTAG, this.hashtagModel];
        var url = this.urlsService.HASHTAG;

        this.waitingForJob = true;
        this.requestsService.getData(url).subscribe(response => {
            this.waitingForJob = false;
            this.requestsService.add_toVisualizeList(tuple);
        });
    }
}
