export class RequestsType {
    static ALL: string = "ALL";
	static SOCIALMEDIA: string = "SOCIALMEDIA";
	static NEWSPAPER: string = "NEWSPAPER";
	static HASHTAG: string = "HASHTAG";

	constructor() {}
}

export var visualizationRequests = {
    multimedia: [RequestsType.SOCIALMEDIA],
    interaction: [RequestsType.SOCIALMEDIA],
    bubble: [RequestsType.SOCIALMEDIA, RequestsType.NEWSPAPER],
    radar: [RequestsType.SOCIALMEDIA, RequestsType.NEWSPAPER],
    sankey: [RequestsType.SOCIALMEDIA],
    wordcloud: [RequestsType.SOCIALMEDIA, RequestsType.NEWSPAPER],
    timeseries: [RequestsType.SOCIALMEDIA]
};
