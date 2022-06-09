import cv2
import numpy as np

color = input("Ingrese el color de la pelota: ")

#if color != "azul" or color != "amarillo" or color != "rojo":
 #  color = input("Porfavor ingrese un color válido: ")

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    # width = int(cap.get(3))
    # height = int(cap.get(4))
    # (0,0)  esquina superior izquierda

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if color.lower() == "n":
        lower_blue = np.array([0,0,0])
        upper_blue = np.array([255,255,255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

    if color.lower() == "azul":
        lower_blue = np.array([90,50,50])
        upper_blue = np.array([130,255,255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

    if color.lower() == "amarillo":
        lower_yellow = np.array([22, 43, 50], dtype="uint8")
        upper_yellow = np.array([100, 255, 255], dtype="uint8")
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    if color.lower() == "rojo":
        lower_red = np.array([90,130,140]) #161,155,84
        upper_red = np.array([169,235,255])
        mask = cv2.inRange(hsv, lower_red, upper_red)

    result = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow('video',result)
    cv2.imshow('mask1',mask)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 