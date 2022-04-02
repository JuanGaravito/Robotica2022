Instrucciones para correr exitosamente el taller 2:
1. Revisar que la conectividad sea adecuada (Master y slave conectados a la misma red wifi y las IP configuradas en el bash).
2. En la terminal del slave, correr serialarduinokey
3. En la terminal del master, correr los nodos robot_teleop y robot_interface0 
4. Cuando se abra la interfaz gráfica, se podrá manejar el robot con las teclas 'w' (avanzar), 'a' (rotar a la izquierda), 's' (retroceder), 'd' (rotar a la derecha).
5. Luego de realizar el recorrido, hacer click en el botón 'Guardar recorrido' de la interfaz y escribir el nombre del archivo en la terminal.
Para abrir el archivo...
6. con el rosocore funcioando. abri una nueva terminal. en esta nueva terinal correr el archivo robot_player_server0.py
7. abrir una nueva terminal en la cual se debe correr el codigo de la siguiente forma rosrun [package] robot_player_client0 [nombre del archvio]
8. uan vez corrido se mostrara la lista de todas las acciones guardadas en el archivo

