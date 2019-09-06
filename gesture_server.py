import cv2
import numpy as np
from flask import Flask, jsonify, request

cap=cv2.VideoCapture(0)
number = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE']
fingers = [ '3']
count = 0
end = False
font = cv2.FONT_HERSHEY_SIMPLEX

app = Flask(__name__)

@app.route('/fingers', methods=['POST'])

def get_gesture():
	if(request.json["Hand_Scan"] == "ON"):
		cap = cv2.VideoCapture(0)
		#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 900)
		#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
		number = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE']
		fingers = [ '3']
		count = 0
		end = False
		font = cv2.FONT_HERSHEY_SIMPLEX

		while(cap.isOpened()):
			_,feed=cap.read()
			feed = cv2.flip(feed, 1)
			cv2.rectangle(feed,(50,100),(300,400),(0,255,0),0)

			image=feed[100:400,50:300]
			#image=cv2.imread('C:\Users\Admin\Desktop\hand.jpg')
			img=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
			blur=cv2.GaussianBlur(img,(35,35),0)
			ret,thresh = cv2.threshold(blur, 0, 255, 1+cv2.THRESH_OTSU)
			contours, hierarchy = cv2.findContours(thresh, 1, 1)
			max_area=0
			pos=0

			for i in contours:
				area=cv2.contourArea(i)
				if area>max_area:
					max_area=area
					pos=i
			
			peri=cv2.arcLength(pos,True)
			approx=cv2.approxPolyDP(pos,0.02*peri,True)
			hull=cv2.convexHull(pos)
			#print len(hull)
			#cv2.polylines(image,[approx],True,(0,255,255))
			#cv2.drawContours(image,[approx],-1,(255,100,50),2)
			cv2.drawContours(image,[hull],-1,(0,0,255),2)
			hull = cv2.convexHull(pos,returnPoints = False)
			defects = cv2.convexityDefects(pos,hull)
			num=0
			l=defects.shape[0]
			for i in range(1,defects.shape[0]):
				s,e,f,d = defects[i,0]
				far = tuple(pos[f][0])
				if d>10000:
					num+=1
					cv2.circle(image,far,3,[0,0,255],-1)

			s = number[num] if (num < 5) else 'Error'
			if(str(num+1) == str(fingers[0])):
				count += 1
			else:
				count = 0

			feed[100:400,50:300] = image
			
			if(max_area < 25000):
				cv2.putText(feed,s,(50,450), font, 1,(255,10,10),2,cv2.LINE_AA)
			else:
				cv2.putText(feed, "Insert/adjust hand", (50,450), font, 1,(255,10,10),2,cv2.LINE_AA)
			
			cv2.putText(feed,"Show " + str(fingers[0]) + " fingers",(50,50), font, 1,(255,10,10),2,cv2.LINE_AA)
			cv2.putText(feed, str(count), (500,50), font, 1,(255,10,10),2,cv2.LINE_AA)
			cv2.imshow('Feed',feed)

			if(count > 50):
				end = True

			#cv2.imshow('image',thresh)
			k=cv2.waitKey(10)
			if (k==27 or (end)):
				break
		cv2.destroyAllWindows()
	return jsonify({"Output": "Success"})  

if __name__ == '__main__':
    app.run(debug=True)