import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';

import { RaspberryService } from '../../providers/raspberryService';
@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

	pressed: boolean;
	sound: number;
	distance: number;
	light: number;
	temperature: number;

  constructor(public navCtrl: NavController, private raspberryService: RaspberryService ) {
	setInterval(this.initiateBoard(), 1000);
  }

  //Calls all seperate methods & intializes in vars
  initiateBoard() {
  	this.getSound();
  	this.getTemperature();
  	this.getDistance();
  	this.getLight();
 //		this.getPanic();
  }

  panic() {
  }

  getPressed() {
  	this.raspberryService.getPressed().subscribe(response => {
	  	this.pressed = response.pressed;
/* 		if(response.status == 200) {
	  		this.pressed = response.pressed;
  		} else {
	  		console.log("SMTH WRONG W PRESSURE CALL");
	  		console.log(response);
	  	}	*/
  	});
  };

  getSound() {
  	this.raspberryService.getSoundLevel().subscribe(response => {
	  	this.sound = response.sound;
/*  	if(response.status == 200) {
  			console.log(response.sound);
  			this.sound = response.sound;

  		} else {
	  		console.log("SMTH WRONG W SOUND CALL");
	  		console.log(response);
	  	}	*/
  	});
  };

  getDistance() {
  	this.raspberryService.getDistance().subscribe(response => {
  		this.distance = response.ultrasound;	
/*  	if(response.status == 200) {
	  		this.distance = response.distance;
  		} else {
	  		console.log("SMTH WRONG W DISTANCE CALL");
	  		console.log(response);
	  	}*/
  	});
  };

  getLight() {
  	this.raspberryService.getLightLevel().subscribe(response => {
	  	this.light = response.light;
/* 		if(response.status == 200) {
	  		this.light = response.light;
  		} else {
	  		console.log("SMTH WRONG W LIGHT CALL");
	  		console.log(response);
	  	}	*/
  	});
  };

  getTemperature() {
  	this.raspberryService.getTemperature().subscribe(response => {
	  	this.temperature = response.temperature;
/*  		if(response.status == 200) {
  			console.log(response.temperature);
	  		this.temperature = response.temperature;
  		} else {
	  		console.log("SMTH WRONG W TEMPERATURE CALL");
	  		console.log(response);
	  	}	*/
  	});
  }
}
