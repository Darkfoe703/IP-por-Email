##################################################################
#
# "IP por E-mail"
# Autor:	Marco Romero
# Contacto:	marcoromero_1@hotmail.com
# Año:		2017-2018
# Copyright © 2018
# 
##################################################################

# -*- coding: utf-8 -*-

# Importa los módulos necesarios
from tkinter import *
from tkinter import ttk, font, messagebox
from urllib.request import urlopen
from datetime import datetime, date, time, timedelta
from threading import Thread
from pathlib import Path
from win32com.client import Dispatch
import urllib, sys, re, threading, time, base64, os
import smtplib, errno, webbrowser, winshell
# Para los botones con link
import tkinter as tk

v_ppal = Tk()
v_conf = Toplevel(v_ppal)
v_acerca = Toplevel(v_ppal, bg="black")

sys.setrecursionlimit(2880)

class Temporizador(Thread):
	"""Temporiza el intervalo en el que se vuelve
	a hacer las comprobaciones de IP"""
	def __init__(self, funcion0, funcion1, funcion2, funcion3, funcion4):
					# (combo_intv, carga_ip, obtener_ip, guarda_ip, email)
		super(Temporizador, self).__init__()
		self._estado = False
		self.it = funcion0 # combo_intv()
		self.cargaIP = funcion1 # carga_ip()
		self.obtenIP = funcion2 # obtener_ip()
		self.fun_gIP = funcion3 # guarda_ip()
		self.fun_email = funcion4 # email()

	def run(self):
		# Toma la hora del sistema
		hora = datetime.now()
		# Es igual a 6, 12 o 24
		auxIT = self.it()
		# Hace la suma de la hora actual+intervalo
		it = timedelta(minutes=auxIT)
		# HORA de la próx. comprobación
		hra_objetivo = (hora + it)

		while self._estado != False:
			# La barra deestado recibe la hora objetivo de comprobación
			bar_estado_intv(hra_objetivo)
			# Se fija si existe un archivo con la IP
			exte = os.path.isfile('DATA/_IP.SNT')
				# Si no hay:
			if exte == False:
				# Se obtine la IP
				ipN = self.obtenIP()
				# se la guarda
				self.fun_gIP(ipN)
				# se la envía
				self.fun_email(ipN)
			#else:
				# aquí se podría implementar que,
				# si el archivo contiene una IP
				# se compruebe de primeras si es la actual...

			# La HORA ACTUAL es mayor o igual la HORA OBJETIVO
			if hra_objetivo <= datetime.now():

				# Carga la IP guardada, si existe
				aux = self.cargaIP()
				# Le quita el salto de línea
				ip0 = aux.rstrip("\n")
				# Obtine la IP de la web
				ipN = self.obtenIP()
				# Ajusta el intervalo
				hora = datetime.now()
				it = timedelta(minutes=self.it)
				hra_objetivo = (hora + it)
				bar_estado_intv(hra_objetivo)
				# Compara las IPs
				if ipN != ip0:
					# Si son distintas, guarda y envía la nueva
					self.fun_gIP(ipN)
					self.fun_email(ipN)
				else:
					pass
			time.sleep(1)
			
		else:
			try:
				#print("Detenido")
				bar_estado_intv("DETENIDO")
				time.sleep(5)
				self.run()
			except RecursionError as err:
				error_muerto()

	def _stop(self):
		self._estado = False

	def _start(self):
		self._estado = True



def mostrar(ventana):
	v_ppal.attributes("-disabled", 1)
	ventana.deiconify()
	#ventana.attributes("-topmost", 1)

def ocultar(ventana):
	v_ppal.attributes("-disabled", 0)
	ventana.withdraw()

def ejecutar(f):
	v_ppal.after(200,f)

def carga_datos():
	# Llama a la funcion que decodifica Base64
	aux1 = decodif('DATA/_SCNFTG.SNT')
	if aux1 != '':
		datos = (str(aux1, 'utf-8')).split('\n')
		return datos
	else:
		# Si el archivo no existe o no se puede leer
		# se simulan los datos
		datos = ['', '', '', '', '', 'False', '12hs', 'FIN']
		return datos

def carga_mje():
	# Llama a la funcion que decodifica Base64
	aux1 = decodif('DATA/_SMNJTE.SNT')
	if aux1 != '':
		mje_gdado = (str(aux1, 'utf-8'))
		# Quita el ultimo elemeto q es un salto
		#if mje_gdado[1] == '\n':
		#	mje_gdado = mje_gdado.pop(1)
		return mje_gdado
	else:
		# Si el archivo no existe o no se puede leer
		# se simulan el mensaje
		mje_gdado = ''
		return mje_gdado

def carga_ip():
	try:
		lect_IP = open('DATA/_IP.SNT', 'r')
		IP_gdada = lect_IP.read()
		lect_IP.close()
	# Si no existe escribe un "" en su lugar
	except OSError as err:
		IP_gdada = ''

	return IP_gdada

def decodif(archivo):
	try:
		# Abre y lee el archivo escrito en Base64
		aux1 = open(archivo, 'r')
		aux2 = aux1.read()
		# lo cierra
		aux1.close()
		# Convierte lo leido a cristiano
		aux = base64.b64decode(bytes(aux2, 'utf-8'))
		return aux
	except OSError as err:
		aux = ''
		return aux

def iniciar():
	# Se asegura que la configuración no esté vacía
	sec = seguro_inicio()
	if sec == "OK":
		# Deshabilita el boton INICIAR y CONFIG
		bt_ini.config(state=DISABLED)
		bt_det.config(state=NORMAL)
		bt_conf.config(state=DISABLED)
		# Inicia el temporizador
		temp_comp._start()
	else:
		mjes_error("Revise la configuración por favor.")
		return "error"

def detener():
	temp_comp._stop()
	bt_ini.config(state=NORMAL)
	bt_conf.config(state=NORMAL)
	bt_det.config(state=DISABLED)

def seguro_inicio():
	servidor = cpo_sv.get()
	puerto = cpo_puerto.get()
	usuario = cpo_usr.get()
	contra = cpo_ctña.get()
	contraR = cpo_Rctña.get()
	dest = cpo_para.get()

	if servidor == "":
		return "error"
	elif puerto == "":
		return "error"
	elif usuario == "":
		return "error"
	elif contra== "":
		return "error"
	elif contraR == "":
		return "error"
	elif dest == "":
		return "error"
	else:
		return "OK"

def combo_intv():
	aux = cbo_hs.get()
	if aux == "06hs":
		aux = 6
	elif aux == "12hs":
		aux = 12
	else:
		aux = 24
	return aux

def a_bandeja(ventana):
	ventana.iconify()

def acep_conf():
	"""Definición que se ejecuta al pulsar ACEPTAR
	en la ventana de configuración """
	# Lee todos los campos de v_conf
	servidor = cpo_sv.get()
	puerto = cpo_puerto.get()
	usuario = cpo_usr.get()
	contra = cpo_ctña.get()
	contraR = cpo_Rctña.get()
	dest = cpo_para.get()
	mje = cpo_mje.get("1.0","end-1c")
	chk = chk_ini.state()
	interv = cbo_hs.get()
	# Asigna un T o F según el estado del checkbutton
	if chk:
		ini = "True"
		crear_acceso()
	else:
		ini = "False"
		borrar_acceso()
	# Comprueba q la contraseña se haya introducido correctamente
	if contra != contraR:
		mjes_error("La contraseña no coincide.")
		mostrar(v_conf)
		cpo_ctña.delete(0, END)
		cpo_Rctña.delete(0, END)
		return "Error"
	else:
		# Guarda los datos de configuración juntos en una lista
		config = [servidor, puerto, usuario,
			contra, dest, ini, interv]
	# llama a la función para guardar en archivo
	guard_config_mje(config, mje)
	# oculta la ventana de configuraciones (v_conf)
	ocultar(v_conf)

def restablecer():
	cpo_sv.delete(0, END)
	cpo_usr.delete(0, END)
	cpo_puerto.delete(0, END)
	cpo_ctña.delete(0, END)
	cpo_Rctña.delete(0, END)
	cpo_para.delete(0, END)
	cpo_mje.insert(INSERT, "")

def guard_config_mje(configuracion, mensaje):
	config = configuracion
	mje = mensaje
	# Guarda la configuracíon en un archivo
	gua_config = open('DATA/_SCNFTG.SNT', 'w')
	gua_config.writelines([config[0], "\n", config[1], "\n", config[2],
			"\n", config[3], "\n", config[4], "\n", config[5], "\n", 
			config[6], "\n", "FIN", "\n"])
	gua_config.close()
	# Y el mensaje personalizado en un archivo separado
	
	gua_mje = open('DATA/_SMNJTE.SNT', 'w')
	gua_mje.writelines([mje])
	gua_mje.close()


	# Llama a la función para codificar los archivos
	codif('DATA/_SCNFTG.SNT')
	codif('DATA/_SMNJTE.snt')

def guarda_ip(ip):
	# Guarda la IP en un archivo
	data = open('DATA/_IP.SNT', 'w')
	data.writelines([ip, "\n"])
	data.close()

def codif(archivo):
	# Abre el archivo escrito en cristiano
	# lo lee y lo cierra.
	try:
		aux1 = open(archivo, 'r')
		aux2 = aux1.read()
		aux1.close()
		# Convierte lo leido a Base64
		b64 = base64.b64encode(bytes(aux2, "utf-8"))

		aux1 = open(archivo, 'w')
		aux1.write(str(b64, 'utf-8'))
		aux1.close()
	except OSError as err:
		return "Error"

def obtener_ip():
	# Intenta conectar a la web
	try:
		url = "http://www.cualesmiip.com/"
		# Se conecta y lee la pagina web
		web = urlopen(url).read()
		# descarga el HTML de la pagina
		html = str(web)
		# se analiza y se separa el codigo hasta obetener la IP
		cortado1 = html.split("<!-- ")
		cortado2 = cortado1[7]
		cortado3 = cortado2.split(" ")
		# se guarda la IP en una variable
		DireccionIP = cortado3[4]

		return DireccionIP
	# En caso de error de conexión
	except urllib.error.URLError:
		mjes_error("No se ha podido conectar. Revise su conexión a Internet")
		return ("Error")

def email(ip):
	try:
		IP = ip
		# Datos
		username = cpo_usr.get()
		password = cpo_ctña.get()
		servidor = cpo_sv.get()
		puerto = cpo_puerto.get()
		auxiliar = (servidor+":"+puerto)

		mje = cpo_mje.get("1.0","end-1c")

		fromaddr = cpo_usr.get()
		toaddrs  = cpo_para.get()
		msg = """From: IP por E-mail <%s>
To: Para <%s>
Subject: IP %s

%s %s


Este mensaje ha sido enviado desde "IP por E-mail" de
Sol Negro Team - Desarrollo de Software (C) 2018.
Por favor no conteste este mensaje.
                                                @Darkfoe703 - SNT
""" %(fromaddr, toaddrs, IP, mje, IP)
		 
		# Enviando el correo
		server = smtplib.SMTP(auxiliar)
		server.starttls()
		server.login(username,password)
		server.sendmail(fromaddr, toaddrs, msg)
		server.quit()
	except smtplib.SMTPAuthenticationError as err:
		mjes_error("El Usuario y/o Contraseña no son válidos.\nRevise la configuración.")
	except UnicodeEncodeError as err:
		mjes_error("Ha incluido un caracter no permitido en el mensaje")
	except:
		mjes_error("No se ha podido establecer conexión con el servidor.\nRevise su conexión a Internet.")

def bar_estado_intv(hora):
	if hora != 'DETENIDO':
		aux = ("%s:%s" %(hora.hour, hora.minute))
		barraEstado.config(text=("  **Próxima comprobación: "+aux+"**"))
	else:
		aux = hora
		barraEstado.config(text=("  **Próxima comprobación: "+aux+"**"))

def crear_acceso():
	try:
		# Reconoce la carpeta de Inicio
		startup = winshell.startup()
		ruta = os.path.join(startup, "IP por Email - vCC.lnk")
		# Cual es el archivo al q se le hará un link
		objetivo = os.path.abspath('Final.py')
		dir_objetivo = os.getcwd()
		# Indica la dirección del ícono
		icono = os.path.join(os.getcwd(), "recs\IP_ico.ico")
		print(icono)
		# Crea el acceso con los dato brindados
		shell = Dispatch('WScript.Shell')
		shortcut = shell.CreateShortCut(ruta)
		shortcut.Targetpath = objetivo
		shortcut.WorkingDirectory = dir_objetivo
		shortcut.IconLocation = icono
		shortcut.save()
	except:
		mjes_error("No se pudo crear el acceso directo.")

def borrar_acceso():
	startup = winshell.startup()
	accesoD = os.path.join(startup, "IP por Email - vCC.lnk")
	aux = os.path.isfile(accesoD)
	# Si el acceso directo existe lo borra
	if aux == True:
		winshell.delete_file(accesoD, allow_undo=False,
			no_confirm=True ,silent=True)
	pass

def sitio_web():
	home = str(Path.home())
	aux = (home+"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
	print(aux)
	#webbrowser.open_new_tab("google.com")

def mail_contacto():
	webbrowser.open_new_tab("mailto:marcoromero_1@hotmail.com")

def donacion_web():
	pass

def mjes_error(tipo):
	# Crea un fichero con la hora y los errores
	# producidos
	hoy = datetime.now()
	aux0 = ("%s" %hoy)
	aux = open('error.txt', 'a')
	aux.write("%s %s\n" %(aux0, tipo))
	aux.close()
	messagebox.showwarning("¡Atención!",tipo)

def error_muerto():
	aux2 = "La aplicaión se detuvo por estar fuera de uso demasiado tiempo."
	hoy = datetime.now()
	aux0 = ("%s" %hoy)
	aux = open('error.txt', 'a')
	aux.write("%s %s\n" %(aux0, aux2))
	aux.close()
	mjes_error(aux2)
	v_ppal.destroy()

#=================================================================
#
#					DISEÑO VENTANA PPAL
#=================================================================
# Titulo
v_ppal.title("IP por E-mail - Versión CC")
# Tamaño y centrado de la ventana
AnchoPantalla = v_ppal.winfo_screenwidth()
AltoPantalla = v_ppal.winfo_screenheight()
x=(AnchoPantalla/2)
y=(AltoPantalla/2)
ancho_ppal = 320
alto_ppal = 415
v_ppal.geometry('%dx%d+%d+%d' % (ancho_ppal, alto_ppal,
	(x-(ancho_ppal/2)), (y-(alto_ppal/2))))
v_ppal.resizable(0, 0)
v_ppal.iconbitmap('recs/IP_ico.ico')

# -----------------------ELEMENTOS PPAL---------------------------
# Carga imagen de Ppal de archivo
imagen_ppal = PhotoImage(file="recs/image.gif")
# La muestra como una etiqueta
lbl_img = Label(v_ppal, image=imagen_ppal)
lbl_img.place(x=0, y=0)

# Creación de barra de Menú
barraMenu = Menu(v_ppal)
# Menu Archivo
menuArchivo = Menu(barraMenu, tearoff=0)
menuArchivo.add_command(label="Salir", command=v_ppal.quit)
barraMenu.add_cascade(label="Archivo", menu=menuArchivo)

# Menu de Ayuda
menuAyuda = Menu(barraMenu, tearoff=0)
menuAyuda.add_command(label="Ayuda de configuración")
menuAyuda.add_command(label="Acerca de IP por E-mail",
	command=lambda:ejecutar(mostrar(v_acerca)))
barraMenu.add_cascade(label="Ayuda", menu=menuAyuda)

# Muestra la barra de menu
v_ppal.config(menu=barraMenu)

# Barra de estado
barraEstado = ttk.Label(v_ppal, relief='groove', width=320,
	foreground="light green", background="black",
	font="courier 10 bold", justify="right")
barraEstado.place(width=320, x=0, y=301)

#------------------------Botones----------------------------------
# Botón para INICIAR el envio de emails
bt_ini = ttk.Button(v_ppal, text="Iniciar", command=iniciar)
bt_ini.place(height=30, width=100, x=10, y=328)
# Botón para DETENER el envio de emails
bt_det = ttk.Button(v_ppal, text="Detener", command=detener)
bt_det.place(height=30, width=100, x=112, y=328)
bt_det.config(state=DISABLED)
# Para llamar a la ventada de CONFIGURACIÓN (v_conf)
bt_conf = ttk.Button(v_ppal, text="Configuración...",
	command=lambda:ejecutar(mostrar(v_conf)))
bt_conf.place(height=30, width=123,  x=10, y=360)  # Se carga el botón
# Botón para OCULTAR la aplicación en el taskbar
bt_oc = ttk.Button(v_ppal, text="Ocultar", 
	command=lambda:ejecutar(a_bandeja(v_ppal)))
bt_oc.place(height=30, width=77, x=135, y=360)
# Botón de SALIR
bt_salir = ttk.Button(v_ppal, text="Salir", command=exit)
bt_salir.place(height=65, width=92, x=220, y=328)

#=================================================================
#
#              PROGRAMA PRINCIPAL
#=================================================================
try:
	if not os.path.exists('DATA'):
		os.makedirs('DATA')
	else:
		pass
except OSError as e:
	pass

datos = carga_datos()
# Estado del check
chk_value = BooleanVar()
if datos[5] == 'False':
	chk_value.set(False)
elif datos[5] == "":
	chk_value.set(False)
else:
	chk_value.set(True)
# Estado del Combobox
if datos[6] == "06hs":
	intrv_val = 0
	intrv_tmp = 6
elif datos[6]== "12hs":
	intrv_val = 1
	intrv_tmp = 12
else:
	intrv_val = 2
	intrv_tmp = 24

mensaje = carga_mje()

#=================================================================
#
#			DISEÑO VENTANA CONFIG
#=================================================================
v_conf.title("Configuración")
# Tamaño y posición
ancho_conf = 320
alto_conf = 360
v_conf.geometry('%dx%d+%d+%d' % (ancho_conf, alto_conf,
	(x-(ancho_conf/2)), ((y-(alto_conf/2)))+20))
v_conf.resizable(0, 0)
v_conf.iconbitmap('recs/Config_ico.ico')

# ---------------------ELEMENTOS CONFIG---------------------------
# ------------ Cuadro SMTP ---------------------------------------
fm_sv = ttk.LabelFrame(v_conf, text="SMTP ", height=135, width=310,
	relief="groove", borderwidth=3)
fm_sv.place(x=5, y=4)

etq_sv = ttk.Label(fm_sv, text="Servidor: ", width=70)
etq_sv.place(width=70, x=2, y=2)

cpo_sv = ttk.Entry(fm_sv, width=125)
cpo_sv.insert(0, datos[0])
cpo_sv.place(width=125, x=72, y=2)
cpo_sv.focus()

etq_puerto = ttk.Label(fm_sv, text="Puerto: ", width=50)
etq_puerto.place(width=50, x=202, y=2)

cpo_puerto = ttk.Entry(fm_sv, width=54)
cpo_puerto.insert(0, datos[1])
cpo_puerto.place(width=54, x=245, y=2)

etq_usr = ttk.Label(fm_sv, text="Usuario: ", width=70)
etq_usr.place(width=70, x=2, y=30)

cpo_usr = ttk.Entry(fm_sv, width=226)
cpo_usr.insert(0, datos[2])
cpo_usr.place(width=226, x=72, y=30)

etq_ctña = ttk.Label(fm_sv, text="Contraseña: ", width=70)
etq_ctña.place(width=70, x=2, y=58)

cpo_ctña = ttk.Entry(fm_sv, show='*', width=226)
cpo_ctña.insert(0, datos[3])
cpo_ctña.place(width=226, x=72, y=58)

etq_Rctña = ttk.Label(fm_sv, text="Repita: ", width=70)
etq_Rctña.place(width=70, x=2, y=84)

cpo_Rctña = ttk.Entry(fm_sv, show='*', width=226)
cpo_Rctña.insert(0, datos[3])
cpo_Rctña.place(width=226, x=72, y=84)
# ------------------------------------------------------
# ----- Cuadro EMAIL -----------------------------------
fm_email = ttk.LabelFrame(v_conf, text="E-mail ", height=122, width=310,
	relief="groove", borderwidth=3)
fm_email.place(x=5, y=140)

etq_para = ttk.Label(fm_email, text="Para: ", width=70)
etq_para.place(width=70, x=2, y=2)

cpo_para = ttk.Entry(fm_email, width=226)
cpo_para.insert(0, datos[4])
cpo_para.place(width=226, x=72, y=2)

etq_mje = ttk.Label(fm_email, text="Mensaje: ", width=70)
etq_mje.place(width=70, x=2, y=30)

cpo_mje = Text(fm_email, width=226, height=64, font="Arial, 10")
cpo_mje.insert(INSERT, mensaje)
scroll_mje = ttk.Scrollbar(cpo_mje, orient=VERTICAL, command=cpo_mje.yview)
scroll_mje.pack(side=RIGHT, fill=Y)
cpo_mje['yscrollcommand']=scroll_mje.set
cpo_mje.place(width=226, height=64, x=72, y=30)
# ------------------------------------------------------
# ----- Cuadro CONFIG GENERALES-------------------------
fm_cfg = ttk.LabelFrame(v_conf, text="General ", height=60, width=310,
	relief="groove", borderwidth=3)
fm_cfg.place(x=5, y=263)

chk_ini = ttk.Checkbutton(fm_cfg, compound=RIGHT,
	text="Iniciar con el Sistema", width=135, variable=chk_value)
chk_ini.place(width=135, x=2, y=2)

etq_frc = ttk.Label(fm_cfg, text="Comprobar cada: ", width=100)
etq_frc.place(width=100, x=145, y=3)

valores_cbo = StringVar()
cbo_hs = ttk.Combobox(fm_cfg, state='readonly', textvariable=valores_cbo,
	width=55)
cbo_hs['values'] = ('06hs', '12hs', '24hs')
cbo_hs.current(intrv_val)
cbo_hs.place(width=55, x=244, y=3)

# ----------------------BOTONES CONFIG ---------------------------
bt_rst = ttk.Button(v_conf, text="Restablecer",
	command=restablecer)
bt_rst.place(x=2, y=330)

bt_aceptar = ttk.Button(v_conf, text="Aceptar",
	command=acep_conf)
bt_aceptar.place(x=155, y=330)

bt_cancel = ttk.Button(v_conf, text="Cancelar",
	command=lambda:ejecutar(ocultar(v_conf)))
bt_cancel.place(x=235, y=330)

#=================================================================
#
#              DISEÑO VENTANA ACERCA DE...
#-----------------------------------------------------------------
v_acerca.title("Acerca de IP por E-mail")
# Tamaño y posición
ancho_acer = 350
alto_acer = 300
v_acerca.geometry('%dx%d+%d+%d' % (ancho_acer, alto_acer,
	(x-(ancho_acer/2)), (y-(alto_acer/2))))
v_acerca.resizable(0, 0)
v_acerca.attributes("-toolwindow", 1)
v_acerca.iconbitmap('recs/IP_ico.ico')

# ---------------------ELEMENTOS ACERCA --------------------------

img_acerca = PhotoImage(file='recs/IP_ico.gif')
etq_img = ttk.Label(v_acerca, image=img_acerca, background="black")
etq_img.place(x=14, y=14)

etq_titulo = ttk.Label(v_acerca, text="""IP por E-mail - vCC""",
	font="calibri 14", justify="center", foreground="light green",
background="black")
etq_titulo.place(x=130, y=14)

etq_vsn = ttk.Label(v_acerca, text="Version 3.1 Build 357",
	font="arial 9", foreground="light green", background="black")
etq_vsn.place(x=145, y=50)

etq_desc = ttk.Label(v_acerca, font="arial 10", foreground="light green",
	background="black", justify="left")
etq_desc.config(text="""Aplicación simple para comprobar y enviar la dirección
IP pública.
Posibilita un servidor casero, bajo un servicio de
direcciones dinámicas.

Creado por "Sol Negro Team" Desarrollo de Software
	 Copiright © 2018 - Marco Romero""")
etq_desc.place(x=14, y=100)
# Botón de página WEB
webBt = tk.Button(v_acerca, bg='#000000', fg='#357fde', relief='flat',
                font="calibri 9", underline=True, compound=CENTER,
                activebackground='#000000', bd=0,
                activeforeground="light green",
                text="Sitio del Sol Negro Team",
                height=0,
                command=sitio_web)
webBt.place(x=14, y=215)
# Botón de email
mailBt = tk.Button(v_acerca, bg='#000000', fg='#357fde', relief='flat',
                font="calibri 9", underline=True, compound=CENTER,
                activebackground='#000000', bd=0,
                activeforeground="light green",
                text="marcoromero_1@hotmail.com",
                height=0,
                command=mail_contacto)
mailBt.place(x=165, y=215)
# Botón de terminos de licencia
img_licen = PhotoImage(file='recs/licenciaCC.gif')
licenBt = tk.Button(v_acerca, bg='#FFFFFF', image=img_licen,
				relief='flat', bd=0, padx=1, pady=1,
				activebackground='#357fde',
				command=sitio_web)
licenBt.place(x=40, y=250)
# Botón de Donación
img_Dona = PhotoImage(file='recs/donate.gif')
donateBt = tk.Button(v_acerca, bg='#000000', image=img_Dona,
				relief='flat', bd=0, padx=1, pady=1,
				activebackground='#357fde',
				command=donacion_web)
donateBt.place(x=180, y=247)

#-----------------------------------------------------------------

# Maneja el cerrar con la X del admin. de ventanas
v_conf.protocol("WM_DELETE_WINDOW", lambda:ocultar(v_conf))
v_acerca.protocol("WM_DELETE_WINDOW", lambda:ocultar(v_acerca))
# Oculta las ventanas TopLevel
v_conf.withdraw()
v_acerca.withdraw()

# Inicializa el hilo del temporizador
temp_comp = Temporizador(combo_intv, carga_ip, obtener_ip, guarda_ip, email)
temp_comp.setDaemon(True)
temp_comp.start()


if chk_ini.state():
	iniciar()

# Loop PPAL
v_ppal.mainloop()