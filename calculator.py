import cv2
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)  # Limit detection to one hand
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
        self.clicked = False

    def draw(self, img):
        if self.clicked:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (255, 255, 255), cv2.FILLED)
            cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 50), cv2.FONT_HERSHEY_PLAIN,
                        2, (0, 0, 0), 3)  # Bold text
        else:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (225, 225, 225), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                          (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 50), cv2.FONT_HERSHEY_PLAIN,
                        2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            self.clicked = True
            return True
        return False

myEquation = ""
delayCounter = 0

# Buttons
buttonValues = [['7', '8', '9', '*'],
                ['4', '5', '6', '-'],
                ['1', '2', '3', '+'],
                ['0', '/', '.', '=']]

# Create Buttons
buttonList = []
for x in range(4):
    for y in range(4):
        xpos = x * 65 + 210
        ypos = y * 65 + 110
        buttonList.append(Button((xpos, ypos), 65, 65, buttonValues[y][x]))

# Add erase button
eraseButton = Button((210, 370), 260, 65, 'Erase')
buttonList.append(eraseButton)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    # Draw calculator background
    cv2.rectangle(img, (210, 50), (210 + 260, 65 + 100),
                  (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (210, 50), (210 + 260, 65 + 100),
                  (50, 50, 50), 3)

    for button in buttonList:
        button.draw(img)

    # Drawing the Equation/Result
    cv2.putText(img, myEquation, (220, 90), cv2.FONT_HERSHEY_PLAIN,
                2, (50, 50, 50), 2)

    if results.multi_hand_landmarks:
        for idx, handLms in enumerate(results.multi_hand_landmarks):
            # Check if the detected hand is the right hand
            hand_label = results.multi_handedness[idx].classification[0].label
            if hand_label == "Right":
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                
                h, w, c = img.shape
                thumb_tip = handLms.landmark[4]
                index_tip = handLms.landmark[8]
                thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
                index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
                distance = math.hypot(index_x - thumb_x, index_y - thumb_y)
                
                if distance < 14 and delayCounter == 0:
                    for button in buttonList:
                        if button.checkClick(index_x, index_y):
                            myValue = button.value
                            if myValue == "=":
                                try:
                                    myEquation = str(eval(myEquation))
                                except:
                                    myEquation = "Error"
                            elif myValue == "Erase":
                                myEquation = myEquation[:-1]  # Remove last character
                            else:
                                myEquation += myValue
                            delayCounter = 1
                
                # Draw a line between the two points
                cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 255), 3)
                
                # Draw circles at the tip points
                cv2.circle(img, (thumb_x, thumb_y), 10, (255, 0, 0), cv2.FILLED)  # Blue for thumb
                cv2.circle(img, (index_x, index_y), 10, (0, 255, 0), cv2.FILLED)  # Green for index finger
    
    # Counter for button press delay
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0
            for button in buttonList:
                button.clicked = False

    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('c'):
        break

cap.release()
cv2.destroyAllWindows()