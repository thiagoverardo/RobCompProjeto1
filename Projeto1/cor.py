#! /usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = ["Rachel P. B. Moraes", "Igor Montagner", "Fabio Miranda"]


import rospy
import numpy as np
import tf
import math
import cv2
import time
from geometry_msgs.msg import Twist, Vector3, Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import cormodule
from math import pi
from std_msgs.msg import UInt8
from sensor_msgs.msg import LaserScan
import argparse
import mobilenet_simples as mnet
import visao_module


bumper = None


lista = None
minimonoventa = None
minimotrezentosesessenta = None
minimocentoeoitenta = None
minimoduzentosesetenta = None


def scaneou(dado):
	global dadominimo
	global dadomaximo
	global noventa
	global centoeoitenta
	global duzentosesetenta
	global trezentosesessenta
	global lista
	global minimonoventa
	global minimotrezentosesessenta
	global minimocentoeoitenta
	global minimoduzentosesetenta

	dadominimo = dado.range_min
	dadomaximo = dado.range_max
	lista = list(dado.ranges)
	#print(lista)


	noventa = []
	centoeoitenta = []
	duzentosesetenta = []
	trezentosesessenta = []


	for e in range(0,360):
		if e < 90:
			if lista[e] < dadomaximo and lista[e] > dadominimo:
				noventa.append(lista[e])
		if e >= 90 and e < 180:
			if lista[e] < dadomaximo and lista[e] > dadominimo:
				centoeoitenta.append(lista[e])
		if e >= 180 and e < 270:
			if lista[e] < dadomaximo and lista[e] > dadominimo:
				duzentosesetenta.append(lista[e])
		if e >= 270 and e < 360:
			if lista[e] < dadomaximo and lista[e] > dadominimo:
				trezentosesessenta.append(lista[e])

	minimonoventa = min(noventa)
	minimocentoeoitenta = min(centoeoitenta)
	minimoduzentosesetenta = min(duzentosesetenta)
	minimotrezentosesessenta = min(trezentosesessenta)


def BUMPER(dado):
	global bumper
	bumper = dado.data


bridge = CvBridge()
cv_image = None
media = []
centro = []
atraso = 1.5E9 # 1 segundo e meio. Em nanossegundos
area = 0.0 # Variavel com a area do maior contorno
# Só usar se os relógios ROS da Raspberry e do Linux desktop estiverem sincronizados. 
# Descarta imagens que chegam atrasadas demais
check_delay = False 

# A função a seguir é chamada sempre que chega um novo frame
def roda_todo_frame(imagem):
	print("frame")
	global cv_image
	global media
	global centro
	global area
	global area2
	global result_frame
	global resultados
	global centro2

	now = rospy.get_rostime()
	imgtime = imagem.header.stamp
	lag = now-imgtime # calcula o lag
	delay = lag.nsecs
	print("delay ", "{:.3f}".format(delay/1.0E9))
	if delay > atraso and check_delay==True:
		print("Descartando por causa do delay do frame:", delay)
		return 
	try:
		antes = time.clock()
		cv_image = bridge.compressed_imgmsg_to_cv2(imagem, "bgr8")
		media, centro, area =  cormodule.identifica_cor(cv_image)
		centro2, result_frame, resultados = visao_module.processa(cv_image)
		depois = time.clock()
		cv2.imshow('Camera', cv_image)
	except CvBridgeError as e:
		print('ex', e)


bumper = 0

if __name__=="__main__":
	rospy.init_node("cor")
	topico_imagem = "/kamera"
	
	recebe_bumper = rospy.Subscriber("/bumper", UInt8, BUMPER)
	recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)
	recebedor = rospy.Subscriber(topico_imagem, CompressedImage, roda_todo_frame, queue_size=4, buff_size = 2**24)
	

	font = cv2.FONT_HERSHEY_SIMPLEX
	#cv2.putText(result_frame,'Bicicletas:{0}'.format(len(result_tuples)),(0,50), font, 2,(255,255,255),2,cv2.LINE_AA)
	print("Usando ", topico_imagem)

	velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

	try:

		while not rospy.is_shutdown():
			vel = Twist(Vector3(0,0,0), Vector3(0,0,0))
			vel_andar = Twist(Vector3(0.15,0,0), Vector3(0,0,0))
			vel_andar_rapido = Twist(Vector3(0.2,0,0), Vector3(0,0,0))
			vel_parar = Twist(Vector3(0,0,0), Vector3(0,0,0))
			vel_re = Twist(Vector3(-0.1,0,0), Vector3(0,0,0))
			vel_girar_45horario = Twist(Vector3(0,0,0), Vector3(0,0,-pi/4))
			vel_girar_45antihorario = Twist(Vector3(0,0,0), Vector3(0,0,pi/4))
			vel_fugir = Twist(Vector3(0.2,0,0), Vector3(0,0,0))
			vel_direitinha = Twist(Vector3(0.15,0,0), Vector3(0,0,-0.8))
			vel_esquerdinha = Twist(Vector3(0.15,0,0), Vector3(0,0,0.8))
			vel_direitinha_fugir = Twist(Vector3(-0.15,0,0), Vector3(0,0,-0.8))
			vel_esquerdinha_fugir = Twist(Vector3(-0.15,0,0), Vector3(0,0,0.8))

			velocidade90 = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0.4))
			velocidade180 = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0.4))
			velocidade270 = Twist(Vector3(0, 0, 0), Vector3(0, 0, -0.4))
			velocidade360 = Twist(Vector3(0, 0, 0), Vector3(0, 0, -0.4))
			velocidadere = Twist(Vector3(-1, 0, 0), Vector3(0, 0, 0))
			velocidadefrente = Twist(Vector3(0.4, 0, 0), Vector3(0, 0, 0))
			velocidadeparar = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))

			if bumper == 0:

				if len(resultados) != 0:
					if media[0]<centro2[0]:
						velocidade_saida.publish(vel_direitinha_fugir)
						rospy.sleep(0.1)
					elif media[0]>centro2[0]:
						velocidade_saida.publish(vel_esquerdinha_fugir)
						rospy.sleep(0.1)
						
				elif len(media) != 0 and len(centro) != 0:

					print("Média dos vermelhos: {0}, {1}".format(media[0], media[1]))
					print("Centro dos vermelhos: {0}, {1}".format(centro[0], centro[1]))
					print("Area: {0}".format(area))

					if media[0]<centro[0] and area < 200000:
						velocidade_saida.publish(vel_direitinha)
						rospy.sleep(0.1)
					elif media[0]>centro[0] and area < 200000:
						velocidade_saida.publish(vel_esquerdinha)
						rospy.sleep(0.1)
					else:
						velocidade_saida.publish(vel_andar)
						rospy.sleep(0.1)

				if minimonoventa < 0.15:
					velocidade_saida.publish(velocidadeparar)
					rospy.sleep(1)
					velocidade_saida.publish(velocidadere)
					rospy.sleep(1)
					velocidade_saida.publish(velocidade360)
					rospy.sleep(2)			
				if minimocentoeoitenta < 0.15:
					velocidade_saida.publish(velocidadeparar)
					rospy.sleep(1)
					velocidade_saida.publish(velocidade270)
					rospy.sleep(2)
				if minimoduzentosesetenta < 0.15:
					velocidade_saida.publish(velocidadeparar)
					rospy.sleep(1)
					velocidade_saida.publish(velocidade180)
					rospy.sleep(2)
				if minimotrezentosesessenta < 0.15:
					velocidade_saida.publish(velocidadeparar)
					rospy.sleep(1)
					velocidade_saida.publish(velocidadere)
					rospy.sleep(1)
					velocidade_saida.publish(velocidade90)
					rospy.sleep(2)

			if bumper == 1:

				velocidade_saida.publish(vel_re)
				rospy.sleep(0.5)
				velocidade_saida.publish(vel_girar_45horario)
				rospy.sleep(0.5)

				bumper = 0


			if bumper == 2:

				velocidade_saida.publish(vel_re)
				rospy.sleep(0.5)
				velocidade_saida.publish(vel_girar_45antihorario)
				rospy.sleep(0.5)

				bumper = 0



			if bumper == 3:

				velocidade_saida.publish(vel_andar_rapido)
				rospy.sleep(0.5)
				velocidade_saida.publish(vel_girar_45antihorario)
				rospy.sleep(0.5)

				bumper = 0


			if bumper == 4:

				velocidade_saida.publish(vel_andar_rapido)
				rospy.sleep(0.5)
				velocidade_saida.publish(vel_girar_45horario)
				rospy.sleep(0.5)
				bumper = 0


	except rospy.ROSInterruptException:
		print("Ocorreu uma exceção com o rospy")



