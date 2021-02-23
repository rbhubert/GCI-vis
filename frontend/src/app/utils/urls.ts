import { RequestsType } from "../utils/requestsType";

export class URLS {
	public BASE_URL = "http://localhost:5000/";
	public ACCOUNTS = this.BASE_URL + "accounts";
	public NEWSPAPER = this.BASE_URL + "newspaper";
	public HASHTAG = this.BASE_URL + "hashtag";
	constructor() {}

	getJobsStatus(jobId){
		return this.BASE_URL + "tasks/" + jobId; 
	}

	getFollowedAccounts() {
		return this.ACCOUNTS;
	}

	getFollowedNewspapers() {
		return this.NEWSPAPER;
	}

	getFollowedHashtags() {
		return this.HASHTAG;
	}

	getFollowAccount(socialNetwork, account) {
		return (
			this.ACCOUNTS + "/" + socialNetwork.toLowerCase() + "/" + account
		);
	}

	getActivity(requestType, requestObj) {
		if (requestType.valueOf() === RequestsType.SOCIALMEDIA.valueOf()) {
			var url = this.BASE_URL + "activity/";
			return url + this.endUrl(requestType, requestObj);
		}
	}

	getWordcloud(requestType, requestObj) {
		var url = this.BASE_URL + "wordcloud/";
		return url + this.endUrl(requestType, requestObj);
	}

	getMultimedia(requestType, requestObj) {
		if (requestType.valueOf() === RequestsType.SOCIALMEDIA.valueOf()) {
			var url = this.BASE_URL + "multimedia/";
			return url + this.endUrl(requestType, requestObj);
		}
	}

	getInteraction(requestType, requestObj) {
		if (requestType.valueOf() === RequestsType.SOCIALMEDIA.valueOf()) {
			var url = this.BASE_URL + "interaction/";
			return url + this.endUrl(requestType, requestObj);
		}
	}

	getMultimediaInteraction(requestType, requestObj) {
		if (requestType.valueOf() === RequestsType.SOCIALMEDIA.valueOf()) {
			var url = this.BASE_URL + "multimediaInteraction/";
			return url + this.endUrl(requestType, requestObj);
		}
	}

	getEmotions(requestType, requestObj) {
		var url = this.BASE_URL + "emotions/";
		return url + this.endUrl(requestType, requestObj);
	}

	getEmotionsRadar(requestType, requestObj) {
		var url = this.BASE_URL + "emotions/radar/";
		return url + this.endUrl(requestType, requestObj);
	}

	endUrl(requestType, requestObj) {
		if (requestType.valueOf() === RequestsType.SOCIALMEDIA.valueOf()) {
			var accStr = requestObj.split("-");
			return (
				"socialmedia/" + accStr[0].toLowerCase() + "/" + accStr[1] + "/"
			);
		}
		if (requestType.valueOf() === RequestsType.NEWSPAPER.valueOf()) {
			return "newspaper?newUrl=" + requestObj;
		}
	}
}
