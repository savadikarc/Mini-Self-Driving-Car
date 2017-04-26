#include<Servo.h>
Servo myservo ;

#define vcc1 2
#define vcc2 3
#define m1 10
#define m2 11
#define pwm1 5
#define pwm2 6
#define m3 8
#define m4 9
#define B A1
#define F A2
#define R A3
#define L A4
#define S A5

uint8_t f = 0, b = 0, r = 0, l = 0, s = 0, ch = 0 ;
int fcount = 0, bcount = 0, lcount = 0, rcount = 0, scount = 0 ;
int angle = 93, maxright = 113, maxleft = 73 ; 
byte c ;
unsigned char cmd = 'f' ;

void setup() {
  Serial.begin(9600) ;
  pinMode(A1, INPUT) ;
  pinMode(A2, INPUT) ;
  pinMode(A3, INPUT) ;
  pinMode(A4, INPUT) ;
  pinMode(A5, INPUT) ;
  pinMode(2, OUTPUT) ;
  pinMode(3, OUTPUT) ;
  pinMode(5, OUTPUT) ;
  pinMode(6, OUTPUT) ;
  pinMode(8, OUTPUT) ;
  pinMode(9, OUTPUT) ;
  pinMode(10, OUTPUT) ;
  pinMode(11, OUTPUT) ;
  pinMode(12, OUTPUT) ;

  digitalWrite(vcc1, HIGH) ;
  digitalWrite(vcc2, HIGH) ;
  analogWrite(pwm1, 0) ;
  analogWrite(pwm2, 0) ;
 
  
  myservo.attach(7) ;
  myservo.write(93) ;
  delay(1000) ;

  Serial.println("Initialized") ;
}

void loop() {
  if(Serial.available()>0){
    c = Serial.read() ;
    if(c == 49){
      Serial.println("Start") ;
    }
    if(c == 50){
      Serial.println("Sending") ;
      
      b = digitalRead(B) ;
      f = digitalRead(F) ;
      r = digitalRead(R) ;
      l = digitalRead(L) ;
      s = digitalRead(S) ;
      
      
      if(f == LOW){//Forward
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
      else if(l == LOW){//Left
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
            else if(r == LOW){//Right
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
                  else if(b == LOW){
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
                        else if(s == LOW){
                                  scount++ ;    
                                  cmd = 's' ;
                                  if(scount%1 == 0){
                                    analogWrite(pwm1, 0) ;
                                    analogWrite(pwm2, 0) ;
                                    scount = 0 ;
                                  }    
                               }
      
      Serial.println(cmd) ;
      delay(7) ;
    }
    if(c == 51){
      analogWrite(pwm1, 0) ;
      analogWrite(pwm2, 0) ;
    }
  }
}
