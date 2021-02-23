import { Component, OnInit } from "@angular/core";
import { socialNetworks } from "../../utils/config";
import { SidebarGlobalRequestsService } from "../sidebar-global-requests.service";
import { URLS } from "../../utils/urls";
import { RequestsType } from "../../utils/requestsType";
@Component({
	selector: "app-account-followed-manager",
	templateUrl: "./account-followed-manager.component.html",
	styleUrls: ["./account-followed-manager.component.css"]
})
export class AccountFollowedManagerComponent implements OnInit {
	socialNetworks = socialNetworks;
	accountModel = ["Twitter", "SSalud_mx"];

	jobsIDs: Map<string, string[]> = new Map<string, string[]>();
	waitingForJob = false;
	intervalToCheck;

	constructor(
		private requestsService: SidebarGlobalRequestsService,
		private urlsService: URLS
	) {}

	ngOnInit() {
		this.intervalToCheck = setInterval(() => {
			this.waitingForJob = this.jobsIDs.size != 0;
			this.checkJobID();
		}, 2000);
	}

	getValues(){
		return Array.from(this.jobsIDs.values());
	}

	checkJobID() {
		if (!this.waitingForJob) {
			return;
		}

		Array.from(this.jobsIDs.keys()).forEach(key => {
			var url = this.urlsService.getJobsStatus(key);

			this.requestsService.getData(url).subscribe(response => {
				if (response["data"]["task_status"] === "finished") {
					var value = this.jobsIDs.get(key);
					this.requestsService.add_toVisualizeList(value);
					this.jobsIDs.delete(key);
				}
			});
		});
	}

	followAccount() {
		var accountStr = this.accountModel[0] + "-" + this.accountModel[1];
		var tuple = [RequestsType.SOCIALMEDIA, accountStr];

		var url = this.urlsService.getFollowAccount(
			this.accountModel[0],
			this.accountModel[1]
		);

		this.requestsService
			.getData(url, "post")
			.subscribe((response: Response) => {
				this.jobsIDs.set(response.toString(), tuple);
			});
	}

	canNoFollow() {
		var accountStr = this.accountModel[0] + "-" + this.accountModel[1];
		var tuple = [RequestsType.SOCIALMEDIA, accountStr];

		return this.requestsService.is_inVisualizeList(tuple);
	}
}
