export class Emotions {
    public ANGER = "anger";
    public ANTICIPATION = "anticipation";
    public DISGUST = "disgust";
    public FEAR = "fear";
    public JOY = "joy";
    public SADNESS = "sadness";
    public SURPRISE = "surprise";
    public TRUST = "trust";

    public EMOTIONS = [
        this.ANGER,
        this.ANTICIPATION,
        this.DISGUST,
        this.FEAR,
        this.JOY,
        this.SADNESS,
        this.SURPRISE,
        this.TRUST
    ];

    constructor() {}

    getColors(emotion: String) {
        if (emotion == this.ANGER) {
            return "rgb(204,51,51)";
        }
        if (emotion == this.ANTICIPATION) {
            return "rgb(204,102,51)";
        }
        if (emotion == this.DISGUST) {
            return "rgb(102,51,153)";
        }
        if (emotion == this.FEAR) {
            return "rgb(51,153,102)";
        }
        if (emotion == this.JOY) {
            return "rgb(255,204,102)";
        }
        if (emotion == this.SADNESS) {
            return "rgb(0,51,204)";
        }
        if (emotion == this.SURPRISE) {
            return "rgb(153,204,255)";
        }
        if (emotion == this.TRUST) {
            return "rgb(153,204,102)";
        }
    }
}
