import cv2

a = cv2.imread('/home/robotica/catkin_robotica/src/mi_robot_8/scripts/saquese.jpg')
cv2.imshow("a", a)

cv2.waitKey(0)
cv2.destroyAllWindows()