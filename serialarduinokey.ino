//#include <util/atomic.h>
#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/UInt16.h>
#include <std_msgs/Float32MultiArray.h>
#include <std_msgs/Int16.h>

#define ENCODER_A       2 // Amarillo
#define ENCODER_B       3 // Verde
#define ENCODER_C       19 // Amarillo
#define ENCODER_D       18// Verde

//Motor A
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
int a = 255;
int b = 200;
unsigned long t1=0;
unsigned long t2;
unsigned long t3=0;
unsigned long t4;
float rpmd=0.0;
float rpmi=0.0;
boolean n=false;
boolean u=false;
long velder;
long velizq;

ros::NodeHandle nh;

std_msgs::Int16 velderecha;
std_msgs::Int16 velizquierda;
std_msgs::String tecla;
std_msgs::Float32MultiArray vel;

void velzCallback(const std_msgs::Float32MultiArray& vel) {
  velder = vel.data[0];
  velizq = vel.data[1];
}
void subscriberCallback(const std_msgs::String& tecla) {
  String orden = tecla.data;
  if(orden=="w"){
    Adelante(a,b);
    n=false;
    u=false;
  }
  else if(orden=="a"){
    Izquierda(a,b);
    n=true;
    u=false;
  }
  else if(orden=="s"){
    Atras(a,b);
    n=true;
    u=true;
  }
  else if(orden=="d"){
    Derecha(a,b);
    n=false;
    u=true;
  }
  else{
    Parar();
  }
}

ros::Subscriber<std_msgs::String> teclas_subscriber("teclas", &subscriberCallback);
ros::Subscriber<std_msgs::Float32MultiArray> velz_subscriber("velz", &velzCallback);
ros::Publisher sender1("velocidadder",&velderecha);
ros::Publisher sender2("velocidadizq",&velizquierda);

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
  //node_handle.initNode();
  //node_handle.subscribe(teclas_subscriber);
  nh.initNode();
  nh.subscribe(teclas_subscriber);
  nh.advertise(sender1);
  nh.advertise(sender2);
  nh.subscribe(velz_subscriber);
  //Serial.begin(9600);
}

void loop(){

  po2=pos;
  po4=fos;
  t2=millis();
  t4=millis();
  ss1=abs(po2-po1)*1000/(t2-t1);
  ss2=abs(po4-po3)*1000/(t4-t3);
  rpmd=60*ss1/224;
  rpmi=60*ss2/224;
  po1=po2;
  po3=po4;
  t1=t2;
  t3=t4;
  if(n==true){
    rpmd=-rpmd;
    }
  if(u==true){
    rpmi=-rpmi;
    }
  nh.spinOnce(); 
  velderecha.data = int(rpmd);
  velizquierda.data = int(rpmi+3);
  sender1.publish(&velderecha);
  sender2.publish(&velizquierda);
  nh.spinOnce(); 
  delay(100);

  if(rpmd > velder && rpmd != 0){
    a = a-1;
  }
  else if(rpmd < velder && rpmd != 0){
    a = a+1;
  }
  else if(rpmi > velizq && rpmi != 0){
    b = b-1;
  }
  else if(rpmi < velizq && rpmi != 0){
    b = b+1;
  }
  if(a > 255){
    a = 255;
  }
  if(b > 255){
    b = 255;
  }
 
  
  //Serial.print(rpm1);
  //Serial.print(" ");
  //Serial.print(rpm2);
  //Serial.println(" ");
 //delay(200);

 //node_handle.spinOnce();
}

void leerEncoder(){
  int b=digitalRead(ENCODER_B);
  if(b>0){
    pos=pos+1;  
  }
  else {
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
  void Atras (int a, int b)
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

void Adelante (int a, int b)
{
 //Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, HIGH);
 analogWrite (ENA, 255); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, HIGH);
 analogWrite (ENB, 255); //Velocidad motor B
}

void Izquierda (int a, int b)
{
 //Direccion motor A
 digitalWrite (IN1, HIGH);
 digitalWrite (IN2, LOW);
 analogWrite (ENA, 255); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, LOW);
 digitalWrite (IN4, HIGH);
 analogWrite (ENB, 255); //Velocidad motor A
}

void Derecha (int a, int b)
{
 //Direccion motor A
 digitalWrite (IN1, LOW);
 digitalWrite (IN2, HIGH);
 analogWrite (ENA, 255); //Velocidad motor A
 //Direccion motor B
 digitalWrite (IN3, HIGH);
 digitalWrite (IN4, LOW);
 analogWrite (ENB, 255); //Velocidad motor A
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
