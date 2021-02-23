import { Pipe, PipeTransform } from "@angular/core";
import { RequestsType } from "../utils/requestsType";

@Pipe({
	name: "listToVisualize"
})
export class ListToVisualizePipe implements PipeTransform {
	transform(value: any, args?: any): any {
		return this.getText(value);
	}

	getText(toVis) {
		var typeToVis = toVis[0];
		var objToVis = toVis[1];
		if (typeToVis.valueOf() === RequestsType.SOCIALMEDIA) {
			var accStr = objToVis.split("-");
			return "SocialMedia - " + accStr[1] + " (" + accStr[0] + ")";
		}
		if (typeToVis.valueOf() === RequestsType.NEWSPAPER) {
			return "Newspaper - " + objToVis;
		}

		return typeToVis + " - " + objToVis;
	}
}
