/*
  LED

  This example creates a Bluetooth® Low Energy peripheral with service that contains a
  characteristic to control an LED.

  The circuit:
  - Arduino MKR WiFi 1010, Arduino Uno WiFi Rev2 board, Arduino Nano 33 IoT,
    Arduino Nano 33 BLE, or Arduino Nano 33 BLE Sense board.

  You can use a generic Bluetooth® Low Energy central app, like LightBlue (iOS and Android) or
  nRF Connect (Android), to interact with the services and characteristics
  created in this sketch.

  This example code is in the public domain.
*/

#include <ArduinoBLE.h>

#include <LSM6DS3.h>
#include "Wire.h"

BLEService ledService("19B10000-E8F2-537E-4F6C-D104768A1214"); // Bluetooth® Low Energy LED Service

// BLE Float Characteristic - custom 128-bit UUID, BLERead -> allows reads, BLENotify -> Allows for real-time data streaming
// For more info: https://github.com/arduino-libraries/ArduinoBLE/blob/master/docs/api.md
BLEFloatCharacteristic switchCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLENotify);

// Part of Demo
// const int ledPin = LED_BUILTIN; // pin to use for the LED

// Create a instance of class LSM6DS3
LSM6DS3 myIMU(I2C_MODE, 0x6A);    // I2C device address 0x6A

float xangle = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  
  // Call .begin() to configure the IMUs
  if (myIMU.begin() != 0) {
      Serial.println("Device error");
  } else {
      Serial.println("Device OK!");
  }

//  // set LED pin to output mode
//  pinMode(ledPin, OUTPUT);

  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting Bluetooth® Low Energy module failed!");

    while (1);
  }

  // set advertised local name and service UUID:
  BLE.setLocalName("Best Ball IMU");
  BLE.setAdvertisedService(ledService);

  // add the characteristic to the service
  ledService.addCharacteristic(switchCharacteristic);

  // add service
  BLE.addService(ledService);

  // set the initial value for the characeristic: -> inital transmit value -> 0
  switchCharacteristic.writeValue(0);

  // start advertising
  BLE.advertise();

  Serial.println("BLE LED Peripheral");
}

// Initialize x gyro value to 0
float x_gyro = 0;
float y_gyro = 0;
float z_gyro = 0;
float magnitude = 0;
void loop() {
  // listen for Bluetooth® Low Energy peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central) {
    Serial.print("Connected to central: ");
    // print the central's MAC address:
    Serial.println(central.address());

    // while the central is still connected to peripheral:
    while (central.connected()) {
      Serial.print("X:");
      x_gyro = myIMU.readFloatGyroX();
      Serial.print("Y:");
      y_gyro = myIMU.readFloatGyroY();
      Serial.print("Z:");
      z_gyro = myIMU.readFloatGyroZ();
//      Serial.println(xangle);
//      xangle += .1 * x_gyro;
//      delay(1000);
      // if the remote device wrote to the characteristic,
      // use the value to control the LED:
      magnitude = round((sqrt(sq(x_gyro) + sq(y_gyro) + sq(z_gyro)))/6);
      switchCharacteristic.writeValue(magnitude);
//      Serial.print("Write Value: ");
//      Serial.println(x_gyro);
//      if (switchCharacteristic.written()) {
//        if (switchCharacteristic.value() == 1) {   // any value other than 0
//          Serial.println("LED on");
//          digitalWrite(ledPin, HIGH);         // will turn the LED on
//        } else {                              // a 0 value
//          Serial.println(F("LED off"));
//          digitalWrite(ledPin, LOW);          // will turn the LED off
//        }
      }
    }

    // when the central disconnects, print it out:
//    Serial.print(F("Disconnected from central: "));
//    Serial.println(central.address());
  }
