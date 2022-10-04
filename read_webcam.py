'''
Erudite Lab.


Connecting to multiple webcams

sudo apt install v4l-utils


DEVICE LIST
	 v4l2-ctl --list-devices

CAMERAS CONNECTED LIST
	ls /dev/


'''

import numpy as np
import cv2
import subprocess
import time
import pickle

class readCameras():
	def __init__(self):
		self.camera_file = open('camera_assignment.pkl','rb')
		self.camera = pickle.load(self.camera_file)
		self.video_devices = []
		self.camera_port = dict()
		self.camera_objects = dict()

		self.get_connected_cameras()
		self.getVideoDevicePorts()
		# self.initialize_cameras() #important in implementation

		#print(self.video_devices)

	def get_connected_cameras(self):
		#Gets the list of valid video cameras

		devices_list_query = subprocess.run(['ls','/dev/'],stdout=subprocess.PIPE)

		devices_list = devices_list_query.stdout.decode('utf-8') #decoded
		grab_lines = devices_list.split('\n')

		#video_devices = []

		for line in grab_lines:
			try: #may not be up to count
				#print(line[0:5])
				if line[0:5] == 'video': #Look into it if it's a video camera
					cap = cv2.VideoCapture('/dev/'+str(line)) #Initialize capture
					#time.sleep(1)
					ret, _ = cap.read() #Check to see if it works

					if ret is True:
						self.video_devices.append(line)
			except:
				pass
			
		#print(video_devices)

		#return video_devices


	def getVideoDevicePorts(self):

		ports_list_query = subprocess.run(['v4l2-ctl','--list-devices'],stdout=subprocess.PIPE)

		ports_list = ports_list_query.stdout.decode('utf-8') #decoded
		grab_lines = ports_list.split('\n')

		current_port = ''

		for line in grab_lines:
			#print(line[0:1])
			if line[0:1] == '\t':
				#print(line[6:11])
				if line[6:] in self.video_devices:
					device_name = line[1:] #remove the tab
					self.camera_port[current_port] = str(device_name)

			else:
				#current_port = str(line)
				current_port = line[line.find("(")+1:line.find(")")]


		#return port_assignment

	def initialize_cameras(self):

#		print(self.camera)
#		print(self.camera_port)
		for key, value in self.camera.items():
			try:
				self.camera_objects[key] = cv2.VideoCapture(self.camera_port[value])
			except:
				print('Seems like not all cameras are connected')

	def grabFrame(self,camera_name):
		try:
			ret, frame = self.camera_objects[camera_name].read()

			if ret is True:
				return frame

			else:
				return 0
		except:
			print('Camera name not in dictionary')
			return - 1

	def releaseCameras(self):
		for key, value in self.camera_objects.items():
			value.release()


	def cameraStatus(self):
		self.connected_cameras = list()
		self.disconnected_cameras = list()

		for key, value in self.camera.items():
			try:
				cap = cv2.VideoCapture(self.camera_port[value])
				cap.release()

				cam_data = (key, self.camera_port[value]) # Returns (User-Defined Camera Name, Current Port)

				self.connected_cameras.append(cam_data)
			except:
				# print('Seems like not all cameras are connected')
				self.disconnected_cameras.append(str(key))

		# print(self.connected_cameras)
		# print('\n\n')
		# print(self.disconnected_cameras)

		return self.connected_cameras, self.disconnected_cameras

		# print(self.camera_objects)

#		ret, frame = cap.read()

# #cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('/dev/video1')
# cap = cv2.VideoCapture(4)

# while(True):
# 	# Capture frame-by-frame
# 	ret, frame = cap.read()

# 	# Our operations on the frame come here
# 	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# 	# Display the resulting frame
# 	cv2.imshow('frame',gray)
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 		break

# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()


# vd = get_connected_cameras()
# pa = getVideoDevicePorts(vd)


# camera_file = 'camera_desc.erdt'

# print(pa)
# if __name__ == '__main__':
# 	cam = readCameras()

# 	webcam_frame = cam.grabFrame('Webcam')
# 	cv2.imwrite('webcam.jpg',webcam_frame)

# 	right_frame = cam.grabFrame('Right')
# 	cv2.imwrite('rightcam.jpg',right_frame)


# 	left_frame = cam.grabFrame('Right')
# 	cv2.imwrite('leftcam.jpg',left_frame)

# if __name__ == '__main__':
# 	cam = readCameras()
# 	cam.cameraStatus()