// DeadReckoning.ino
// INCLUDES: ----------
#include <PID_v1.h>
// CONSTANTS: ----------
#define R (.04299)
#define L (.1)
#define D (.22)
#define COUNT_PER_REV (2248.86)
#define PULSES_PER_COUNT (1.0)
#define SECONDS_PER_MICROSECOND (1e-6)
// PIN DEFINITIONS: ----------
#define EN 13
#define IN1 9
#define IN2 8
#define IN3 3
#define IN4 2
#define ENC1 10
#define ENC2 11
#define ENC3 5
#define ENC4 6
// GLOBAL VARIABLES: ----------
double bezierXP[4] = {0.0, 0.0, 1.0, 1.0};
double bezierYP[4] = {0.0, 1.0, 1.0, 0.0};
double currentU;
double currentX;
double currentY;
double currentTheta;
double t;
double omegaLeft;
double omegaRight;
double leftPWM;
double rightPWM;
double omegaLeftTarg;
double omegaRightTarg;
PID leftPID(&omegaLeft, &leftPWM, &omegaLeftTarg, .3333, 1.0, .185, DIRECT);
PID rightPID(&omegaRight, &rightPWM, &omegaRightTarg, .3333, 1.0, .185, DIRECT);
// BEZIER UTILS: ----------
double getBezierX(int u) {
  return bezierXP[0] + bezierXP[1]*u + bezierXP[2]*u*u + bezierXP[3]*u*u*u;
}
double getBezierY(int u) {
  return bezierYP[0] + bezierYP[1]*u + bezierYP[2]*u*u + bezierYP[3]*u*u*u;
}
double getBezierDX(int u) {
  return bezierXP[1] + 2*bezierXP[2]*u + 3*bezierXP[3]*u*u;
}
double getBezierDY(int u) {
  return bezierYP[1] + 2*bezierYP[2]*u + 3*bezierYP[3]*u*u;
}
// VELOCITY IO: ----------
void readOmegas(){
  // Read
  int pulseLeft = pulseIn(ENC1, HIGH, 50000);
  int pulseRight = pulseIn(ENC3, HIGH, 50000);
  
  // Left motor
  if(pulseLeft == 0)
    omegaLeft = 0.0;
  else
    omegaLeft = TWO_PI / (pulseLeft * PULSES_PER_COUNT * COUNT_PER_REV * SECONDS_PER_MICROSECOND);
  // Right motor
  if(pulseRight == 0)
    omegaRight = 0.0;
  else
    omegaRight = TWO_PI / (pulseRight * PULSES_PER_COUNT * COUNT_PER_REV * SECONDS_PER_MICROSECOND);
    
}
void writePWMs() {
  // Compute the actual values from the PID
  int leftPWMReal = max(min((int) leftPWM, 255), 0);
  int rightPWMReal = max(min((int) rightPWM, 255), 0);
  // Write the values
  analogWrite(IN1, leftPWMReal);
  analogWrite(IN3, rightPWMReal);
  
}
// MAIN FUNCTIONS: ----------
void setup() {
  Serial.begin(9600);
  
  // Setup pins
  pinMode(EN, OUTPUT);
  
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENC1, INPUT);
  pinMode(ENC2, INPUT);
  pinMode(ENC3, INPUT);
  pinMode(ENC4, INPUT);
  // Parameter setup
  currentU = 0.0;
  currentX = 0.0;
  currentY = 0.0;
  currentTheta = 0.0;
  t = millis()/1000.0;
  omegaLeftTarg = 10;
  omegaRightTarg = 10;
  // PID
  leftPID.SetMode(AUTOMATIC);
  rightPID.SetMode(AUTOMATIC);
  // Start motor controller
  digitalWrite(EN, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN4, LOW);
}
void loop() {
  // Read the velocities
  readOmegas();
  double newT = millis() / 1000.0;
  // Update state
  double xDot = omegaRight * (R/2 * cos(currentTheta) - D/L * sin(currentTheta)) + omegaLeft * (R/2 * cos(currentTheta) + D/L * sin(currentTheta));
  double yDot = omegaRight * (R/2 * sin(currentTheta) + D/L * cos(currentTheta)) + omegaLeft * (R/2 * sin(currentTheta) - D/L * cos(currentTheta));
  double thetaDot = omegaRight * R/D - omegaLeft * R/D;
  currentX += xDot * (newT - t);
  currentY += yDot * (newT - t);
  currentTheta += thetaDot * (newT - t);
  t = newT;
  
  // Compute and write the needed PID
  //leftPID.Compute();
  //rightPID.Compute();
  leftPWM = 50;
  rightPWM = 50;
  writePWMs();

  Serial.print("currentTheta: ");
  Serial.println(currentTheta);
  Serial.print("omegaLeft: ");
  Serial.println(omegaLeft);
  Serial.print("omegaRight: ");
  Serial.println(omegaRight);
  Serial.println();
  
}
