import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import 'rxjs/add/operator/map';

@Injectable()
export class RaspberryService {
	raspURL = 'http://192.168.50.103:5000';

  constructor(public http: Http) { }

  //-------------------------------------------------
  //Darm-deel
  //-------------------------------------------------

  //Initiates panicmode
  getPressed() {
    return this.http.get(`${this.raspURL}/getButtonStatus`)
      .map(res => res.json());
  }

  //Gets soundlevel
  getSoundLevel(): any {
    return this.http.get(`${this.raspURL}/getSound`)
      .map(res => res.json());
  }

  //Gets ultrasound-distance
  getDistance(): any {
    return this.http.get(`${this.raspURL}/getDistance`)
      .map(res => res.json());
  }

  //Gets lightlevel
  getLightLevel(): any {
    return this.http.get(`${this.raspURL}/getLight`)
      .map(res => res.json());
  }

  //Gets temperature
  getTemperature(): any {
    return this.http.get(`${this.raspURL}/getTemp`)
      .map(res => res.json());
  }

}