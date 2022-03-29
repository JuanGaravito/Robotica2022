//#include <util/atomic.h>
#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/UInt16.h>
#define ENCODER_A       2 // Amarillo
#define ENCODER_B       3 // Verde
#define ENCODER_C       19 // Amarillo
#define ENCODER_D       18// Verde

int ENA = 10;
int IN1 = 9;
int IN2 = 8;

// Motor B
int ENB = 5;
int IN3 = 7;
int IN4 = 6;


int pos=0;
int fos=0;
long po1=0;
long po2;
long po3=0;
long po4;
long ss1;
long ss2;
unsigned long t1=0;
unsigned long t2;
unsigned long t3=0;
unsigned long t4;

ros::NodeHandle node_handle;

std_msgs::String tecla;
void subscriberCallback(const std_msgs::String& tecla) {
  String orden = tecla.data;
    if(orden=="w"){
    Adelante();
  }
  else if(orden=="a"){
    Izquierda();
  }
   else if(orden=="s"){
   Atras();
  }

  else if(orden=="d"){
    Derecha();
  }
  else{
    Parar();
  }
 
}

ros::Subscriber<std_msgs::String> teclas_subscriber("teclas", &subscriberCallback);

void setup(){
 

 pinMode (ENA, OUTPUT);
 pinMode (ENB, OUTPUT);
 pinMode (IN1, OUTPUT);
 pinMode (IN2, OUTPUT);
 pinMode (IN3, OUTPUT);
 pinMode (IN4, OUTPUT);

  //Encoders como entradas
  pinMode(ENCODER_A, INPUT);
  pinMode(ENCODER_B, INPUT);
 attachInterrupt(digitalPinToInterrupt(ENCODER_A),leerEncoder,RISING); 
  pinMode(ENCODER_C, INPUT);
  pinMode(ENCODER_D, INPUT);
 attachInterrupt(digitalPinToInterrupt(ENCODER_C),leerEncoder2,RISING); 
 //Serial.begin(9600);
  node_handle.initNode();
  node_handle.subscribe(teclas_subscriber);

}

void loop(){


  po2=abs(pos);
  po4=abs(fos);
  t2=millis();
  t4=millis();
  ss1=(po2-po1)*1000/(t2-t1);
  ss2=(po4-po3)*1000/(t4-t3);
  po1=po2;
  po3=po4;
  t1=t2;
  t3=t4;

 
  //Serial.print(pos);
  //Serial.print(" ");
  //Serial.print(fo
  +s);
  //Serial.print(" ");
  //Serial.print(ss1);
 // Serial.print(" ");
 // Serial.print(ss2);
 // Serial.println(" ");

 node_handle.spinOnce();
 delay(100);


  

}

void leerEncoder(){
  int b=digitalRead(ENCODER_B);
  if(b>0){
    pos=pos+1;  
  }
  else{
    pos=pos-1;
  }

  }
  
void leerEncoder2(){
  int d=digitalRead(ENCODER_D);
  if(d>0){
    fos=fos+1;  
  }
  else{
    fos=fos-1;
  }

  }

  void Atras ()
{
 //Direccion motor A
 digitalWrite (IN1, HIGH);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, 255); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, HIGH);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, 255); //Velocidad motor B
}

void Adelante ()
{
 //Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, HIGH);
 analogWrite (ENA, 128); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, HIGH);
 analogWrite (ENB, 128); //Velocidad motor B
}

void Derecha ()
{
 //Direccion motor A
 digitalWrite (IN1, HIGH);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, 200); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, HIGH);
 analogWrite (ENB, 100); //Velocidad motor A
}

void Izquierda ()
{
 //Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, HIGH);
 analogWrite (ENA, 100); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, HIGH);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, 200); //Velocidad motor A
}

void Parar ()
{
 //Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, 0); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, 0); //Velocidad motor A
}
