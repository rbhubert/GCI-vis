export class Multimedia {
    public VIDEOS = "video";
    public IMAGES = "image";
    public LINKS = "link";
    public TEXT = "text";
    // agregar las de facebook también
    constructor() {}

    getColors(multimedia: String) {
        if (multimedia == this.VIDEOS) {
            return "rgb(255,153,51)";
        }
        if (multimedia == this.IMAGES) {
            return "rgb(102,153,255)";
        }
        if (multimedia == this.LINKS) {
            return "rgb(153,204,102)";
        }
        if (multimedia == this.TEXT) {
            return "rgb(153,102,204)";
        }

        return "black";
        // agregar las de fb también
    }
}
