'''

Samuel Akwei-Sekyere, 2020

Assign USB ports with webcam names

'''
import pickle
import cv2
import subprocess
import time


class CameraAssignment():
	def __init__(self):
		self.video_devices = []
		self.port_assignment = dict()
		self.camera = dict()
		self.camera_file = 'camera_assignment.pkl'
		# self.names = []

	def get_connected_cameras(self):
	#Gets the list of valid video cameras

		devices_list_query = subprocess.run(['ls','/dev/'],stdout=subprocess.PIPE)

		devices_list = devices_list_query.stdout.decode('utf-8') #decoded
		grab_lines = devices_list.split('\n')

		self.video_devices = []

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

	def assignDevicePorts(self,video_device):

		ports_list_query = subprocess.run(['v4l2-ctl','--list-devices'],stdout=subprocess.PIPE)

		ports_list = ports_list_query.stdout.decode('utf-8') #decoded
		grab_lines = ports_list.split('\n')

		current_port = ''

		self.port_assignment = dict() #expecting a one-to-one match for usb ports

		for line in grab_lines:
			#print(line[0:1])
			if line[0:1] == '\t':
				#print(line[6:11])
				if line[6:] in video_device:
					device_name = line[1:] #remove the tab
					self.port_assignment[current_port] = str(device_name)
					self.camera[input('Write the name of the camera: ')] = current_port

			else:
				#current_port = str(line)
				current_port = line[line.find("(")+1:line.find(")")]


if __name__ == '__main__':
	camera = CameraAssignment()

	cameras_assigned = []

	while True:
		camera.get_connected_cameras()

		for i in camera.video_devices:
			if i not in cameras_assigned:
				camera.assignDevicePorts([i])
				cameras_assigned.append(i)

		continue_query = input("Do you want to add more cameras? Type 'y' or 'n': ")
		if continue_query == 'y':
			ready = input("Type anything when additional device has been inserted: ")
				
			if ready:
				pass

		elif continue_query == 'n':
			print('Completed.')
			break
		else:
			print('Did not understand. You may have to restart.')

	save_file = open(camera.camera_file, "wb")
	pickle.dump(camera.camera, save_file)
	save_file.close()

	# cv2.imshow('frame',gray)
# 	if cv2.waitKey(1) & 0xFF == ord('q'):
# 		break