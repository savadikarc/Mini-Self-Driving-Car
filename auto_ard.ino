#include <SoftwareSerial.h>
#include <Servo.h>
unsigned char c ;
//#define vcc1 13
#define m1 10
#define m2 11
#define pwm1 5
#define pwm2 6
#define m3 8
#define m4 9

#define Rx 2
#define Tx 3
#define PWR 7

int fcount = 0, bcount = 0, lcount = 0, rcount = 0, scount = 0 ;
int angle = 93, maxright = 113, maxleft = 73 ; 

unsigned char cmd = 'f' ;

SoftwareSerial btSerial(Rx, Tx) ;
Servo myservo ;
void setup() {
  pinMode(PWR, OUTPUT) ;
  digitalWrite(PWR, LOW) ;
  pinMode(2, INPUT_PULLUP);
  pinMode(5, OUTPUT) ;
  pinMode(6, OUTPUT) ;
  pinMode(8, OUTPUT) ;
  pinMode(9, OUTPUT) ;
  pinMode(10, OUTPUT) ;
  pinMode(11, OUTPUT) ;
  pinMode(12, OUTPUT) ;
  //pinMode(13, OUTPUT) ; 

  digitalWrite(PWR, HIGH) ;
  
  //digitalWrite(vcc1, HIGH) ;
  analogWrite(pwm1, 0) ;
  analogWrite(pwm2, 0) ;

  myservo.attach(4) ;
  myservo.write(93) ;
  btSerial.begin(9600) ;
  delay(1000) ;
}

void loop() {
  if (btSerial.available()>0){
    c = btSerial.read() ;
      if(c == '0'){//Forward
        fcount++ ;
        cmd = 'f' ;
        if(fcount%1 == 0){
          if(angle > 95){
            angle = angle - 1 ;
          }
          else if(angle < 93){
            angle = angle + 1 ;
          }
          else angle = 93 ;
          myservo.write(angle) ;
          analogWrite(pwm1, 50) ;
          analogWrite(pwm2, 50) ;
          digitalWrite(m3, LOW) ;
          digitalWrite(m4, HIGH) ;
          digitalWrite(m1, HIGH) ;
          digitalWrite(m2, LOW) ;
          fcount = 0 ;
        }
      }
      else if(c == '2'){//Left
              lcount++ ;
              cmd = 'l' ;
              if(lcount%1 == 0){
                if(angle >= maxleft){
                  angle = angle - 1 ;
                }
                else angle = maxleft ;
                myservo.write(angle) ;
                analogWrite(pwm1, 50) ;
                analogWrite(pwm2, 50) ;
                digitalWrite(m3, LOW) ;
                digitalWrite(m4, HIGH) ;
                digitalWrite(m1, HIGH) ;
                digitalWrite(m2, LOW) ;
                lcount = 0 ;
              }
            }
            else if(c == '3'){//Right
                    rcount++ ;
                    cmd = 'r' ;
                    if(rcount%1 == 0){
                      if(angle <= maxright){
                        angle = angle + 1 ;
                      }
                      else angle = maxright ;
                      myservo.write(angle) ;
                      analogWrite(pwm1, 50) ;
                      analogWrite(pwm2, 50) ;
                      digitalWrite(m3, LOW) ;
                      digitalWrite(m4, HIGH) ;
                      digitalWrite(m1, HIGH) ;
                      digitalWrite(m2, LOW) ;
                      rcount = 0 ;
                    }
                  }
                  else if(c == '1'){
                          bcount++ ;
                          cmd = 'd' ;
                          if(bcount%1 == 0){
                            angle = 95 ;
                            myservo.write(angle) ;
                            digitalWrite(m3, HIGH) ;
                            digitalWrite(m4, LOW) ;
                            digitalWrite(m1, LOW) ;
                            digitalWrite(m2, HIGH) ;
                            analogWrite(pwm1, 50) ;
                            analogWrite(pwm2, 50) ;
                            bcount = 0 ;
                          }                      
                        }
                        else if(c == '4'){
                                  scount++ ;    
                                  cmd = 's' ;
                                  if(scount%1 == 0){
                                    analogWrite(pwm1, 0) ;
                                    analogWrite(pwm2, 0) ;
                                    scount = 0 ;
                                  }    
                               }
      delay(7) ;
  }
  
}
