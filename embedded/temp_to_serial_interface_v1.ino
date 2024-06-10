/* this program reads value from analog inputs on the stm32 
 * and sends values over serial line to host every two seconds.
 * note that values are raw and normalization must be done on host 
 *
 * serial data format is:

BEGIN
VALUE0=550
VALUE1=240
VALUE2=551
...
VALUE7=511
END

*/

#include <SoftwareSerial.h>
#define LED_BUILTIN PC13

SoftwareSerial mySerial (PA10, PA9);
int serial = 0;

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  mySerial.begin(9600);
  analogReadResolution(12);

}
 
// the loop function runs over and over again forever
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second

  mySerial.print("BEGIN\n");
  mySerial.print("SERIAL=");
  mySerial.print(serial);
  mySerial.print("\n");

  for (int i = PA0; i <= PA7; i++) {
    mySerial.print("VALUE");
    mySerial.print(i-PA0);
    mySerial.print("=");
    mySerial.print(analogRead(i));
    mySerial.print("\n");
  }

  serial ++;

  mySerial.print("END\n");

}
