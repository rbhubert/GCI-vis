export class Interactions {
    public COMMENTS = "comments";
    public FAVORITES = "favorites";
    public RETWEETS = "retweets";
    public NONE = "none";
    // agregar las de facebook también
    constructor() {}

    getColors(interaction: String) {
        if (interaction == this.COMMENTS) {
            return "rgb(204,204,51)";
        }
        if (interaction == this.FAVORITES) {
            return "rgb(255,0,0)";
        }
        if (interaction == this.RETWEETS) {
            return "rgb(0,0,204)";
        }
        if (interaction == this.NONE) {
            return "rgb(0,0,204)";
        }

        return "black";
        // agregar las de fb también
    }
}
