#! /usr/bin/env python
# -*- coding:utf-8 -*-

import rospy

import numpy as np

from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan




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





	


if __name__=="__main__":

	rospy.init_node("le_scan")

	velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )
	recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)



	while not rospy.is_shutdown():
		print("Oeee")
		velocidade90 = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0.4))
		velocidade180 = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0.4))
		velocidade270 = Twist(Vector3(0, 0, 0), Vector3(0, 0, -0.4))
		velocidade360 = Twist(Vector3(0, 0, 0), Vector3(0, 0, -0.4))
		velocidadere = Twist(Vector3(-1, 0, 0), Vector3(0, 0, 0))
		velocidadefrente = Twist(Vector3(0.4, 0, 0), Vector3(0, 0, 0))
		velocidadeparar = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))



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






		velocidade_saida.publish(velocidadefrente)
		rospy.sleep(0.1)


