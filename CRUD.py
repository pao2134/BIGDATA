from tkinter import *
from tkinter import messagebox
from asyncio.windows_events import NULL
import sqlite3 as sq3
'''
=====================================================
PARTE FUNCIONAL
=====================================================
'''
def conectar():
    global con
    global cur
    con=sq3.connect('mi_db.db')
    cur=con.cursor()
    messagebox.showinfo("STATUS", "¡Conectado con la bbdd!")

def salir():
    resp=messagebox.askquestion('Confirme', "¿Desea salir del programa?")
    if resp=="yes":
        raiz.destroy()
def buscar_escuelas(actualiza):
  con=sq3.connect('mi_db.db')
  cur=con.cursor()
  if actualiza:
    cur.execute('SELECT _id, localidad, provincia FROM escuelas WHERE nombre=?', (escuela.get(),))
  else:
    cur.execute('SELECT nombre from escuelas')
  
  resultado=cur.fetchall()
  retorno=[]
  for e in resultado:
    if actualiza:
      provincia.set(e[2])
      localidad.set(e[1])
    esc=e[0]
    retorno.append(esc)
  
  con.close()
  return retorno
    
#buscar_escuelas(False)

def limpiar():
    legajo.set('')
    alumno.set('')
    email.set('')
    calificacion.set('')
    localidad.set('')
    provincia.set('')
    escuela.set('Seleccione')
    legajo_input.config(state="normal")

def mostrar_licencia():
# CREATIVE COMMONS GNU GPL https://www.gnu.org/licenses/gpl-3.0.txt
  msg = '''
  Demo de un sistema CRUD en Python para gestión 
  de alumnos
  Copyright (C) 2022 - Karin Fleischer
  Email: kkkk@bue.edu.ar\n=======================================
  This program is free software: you can redistribute it 
  and/or modify it under the terms of the GNU General Public 
  License as published by the Free Software Foundation, 
  either version 3 of the License, or (at your option) any 
  later version.
  This program is distributed in the hope that it will be 
  useful, but WITHOUT ANY WARRANTY; without even the 
  implied warranty of MERCHANTABILITY or FITNESS FOR A 
  PARTICULAR PURPOSE.  See the GNU General Public License 
  for more details.
  You should have received a copy of the GNU General Public 
  License along with this program.  
  If not, see <https://www.gnu.org/licenses/>.'''
  messagebox.showinfo("LICENCIA", msg)

def mostrar_acercade():
    messagebox.showinfo("ACERCA DE...", "Creado por XXXXXXX \npara Codo a Codo - Big Data \nNoviembre 2022")

#Con Ctrl+k+c puedo comentar todas las lineas seleccionadas


def listar():
    class Table():
        def __init__(self, raiz2):
            nombre_cols=['Legajo', 'Alumno', 'Calificacion', 'Email', 'Escuela', 'Localidad', 'Provincia']
            for i in range(cant_cols):
                self.e=Entry(frameppal)
                self.e.config(bg='black', fg='lightgreen')
                self.e.grid(row=0, column=i)
                self.e.insert(END, nombre_cols[i])#Que ponga uno a continuacion dle otro
                #self.e.config(state='readonly')
                for fila in range(cant_filas):
                    for col in range(cant_cols):
                        self.e=Entry(frameppal)
                        self.e.config(bg='blue', fg='black')
                        self.e.grid(row=fila+1, column=col)
                        self.e.insert(END, resultado[fila][col])
                        self.e.config(state='readonly')
    raiz2=Tk()
    raiz2.title('listado alumnos')
    frameppal=Frame(raiz2)
    frameppal.pack(fill='both')
    framecerrar=Frame(raiz2)
    framecerrar.pack(fill='both')

    boton_cerrar=Button(framecerrar, text='Cerrar', command=raiz2.destroy)
    boton_cerrar.config(bg=framebotones_color_boton, fg=framebotones_color_texto)
    boton_cerrar.pack(fill='both')
    #boton_cerrar.grid(row=0, column=0)
    con=sq3.connect('mi_db.db')
    cur=con.cursor()
    query1 = '''SELECT alumnos.legajo, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id'''
    cur.execute(query1)
    resultado=cur.fetchall()

    cant_filas=len(resultado)
    cant_cols=(len(resultado[0]))

    tabla=Table(frameppal)
    con.close()
    raiz2.mainloop

# CRUD-------------
# CREAR
def crear():
    query_buscar = '''SELECT alumnos.legajo FROM alumnos WHERE alumnos.legajo= '''
    cur.execute(query_buscar+legajo.get())
    resultado=cur.fetchall()
    if resultado ==[]:
        id_escuela=int(buscar_escuelas(True)[0])
        datos=(id_escuela, legajo.get(), alumno.get(), calificacion.get(), email.get())
        cur.execute("INSERT INTO alumnos (id_escuela, legajo, nombre, nota, email) VALUES (?,?,?,?,?)",datos)
        con.commit()
        messagebox.showinfo("STATUS", "registro agregado")
        limpiar()
    else:
        messagebox.showerror("ERROR","El número de legajo ya existe")
        legajo.set("")
        limpiar()
    

# LEER
def buscar_legajo():
    query_buscar = '''SELECT alumnos.legajo, alumnos.nombre, alumnos.nota, alumnos.email, escuelas.nombre, escuelas.localidad, escuelas.provincia FROM alumnos INNER JOIN escuelas ON alumnos.id_escuela = escuelas._id WHERE alumnos.legajo='''
    
    cur.execute(query_buscar+legajo.get()) #ejecuta el query + lo que le ponemos en el imput como legajo, entonces con esto completa el query
    resultado=cur.fetchall()
    if resultado ==[]:
        messagebox.showerror("ERROR","El numero de legajo no existe")
        legajo.set("")
    else:
        print(resultado)
        for campo in resultado:
            alumno.set(campo[1])
            email.set(campo[3])
            calificacion.set(campo[2])
            localidad.set(campo[5])
            provincia.set(campo[6])
            escuela.set(campo[4])
            legajo_input.config(state='disable')
# ACTUALIZAR
def actualizar():
    id_escuela=int(buscar_escuelas(True)[0])
    datos=(id_escuela, alumno.get(), calificacion.get(), email.get())
    cur.execute("UPDATE alumnos SET id_escuela=?, nombre=?, nota=?, email=? WHERE legajo="+legajo.get(), datos)
    con.commit()
    messagebox.showinfo('STATUS', 'Registro actualizado')
    limpiar()
# BORRAR 
def borrar():
    resp=messagebox.askquestion("BORRAR", '¿Está seguro que desea borrar el registro?')
    if resp:
        cur.execute('DELETE FROM alumnos WHERE legajo='+legajo.get())
        con.commit()
        messagebox.showinfo("STATUS", 'Registro eliminado')
        limpiar()


'''
=====================================================
INTERFAZ GRAFICA
=====================================================
'''
esp_x=10
esp_y=10
#colores para el framecampos
framecampos_color_fondo='cyan'
framecampos_color_letras='red'

framebotones_color_fondo='plum'
framebotones_color_boton='plum'
framebotones_color_texto='black'



#Creamos la raiz y la nombramos

raiz=Tk()
raiz.title('Python CRUD-Comision 22624')

#creamos el primer menu y sus submenues en cascada

barramenu=Menu(raiz)
raiz.config(menu=barramenu)

bbddmenu=Menu(barramenu, tearoff=0)
bbddmenu.add_command(label='Conectar con BBDD', command=conectar)#el conectar es la función que definimos
bbddmenu.add_command(label='Listar alumnos', command=listar)
bbddmenu.add_command(label='Salir del programa', command=salir)#salir la definimos nosotros

borrarmenu=Menu(barramenu, tearoff=0)
borrarmenu.add_command(label='Limpiar formulario', command=limpiar)

ayudamenu=Menu(barramenu, tearoff=0)
ayudamenu.add_command(label='Licencia', command=mostrar_licencia)
ayudamenu.add_command(label='Acerca de..', command=mostrar_acercade)

barramenu.add_cascade(label='BBDD', menu=bbddmenu)
barramenu.add_cascade(label='Limpiar', menu=borrarmenu)
barramenu.add_cascade(label='Acerca de..', menu=ayudamenu)

#----------------FRAME CAMPOS----------------------
def config_label(mi_label, fila):
    espaciado_label={'column':0, 'sticky':'e', 'padx':esp_x, 'pady':esp_y}
    color_labels={'bg':framecampos_color_fondo, 'fg':framecampos_color_letras}
    mi_label.grid(row=fila, **espaciado_label)
    mi_label.config(**color_labels)

framecampos=Frame(raiz) #notese objeto de tipo frame
framecampos.config(bg=framecampos_color_fondo)
framecampos.pack(fill='both') #este meotodo se usa para adaptar el frame al tamaño del contenido
'''
"STICKY"
        n
    nw      ne
w               e
    sw      se
        s
'''




#Apunte: posicionamienta de elementos en tkinter:
#https://recursospython.com/guias-y-manuales/posicionar-elementos-en-tkinter/
legajolabel=Label(framecampos, text='Legajo')
config_label(legajolabel,0)
#legajolabel.grid(row=0, column=0, sticky='e', padx=10, pady=10)#donde lo ubicamos, y el padding en x y en y

alumnolabel=Label(framecampos, text='Alumno')
config_label(alumnolabel,1)
#alumnolabel.grid(row=1, column=0, sticky='e', padx=10, pady=10)

emaillabel=Label(framecampos, text='Email')
config_label(emaillabel,2)
#emaillabel.grid(row=2, column=0, sticky='e', padx=10, pady=10)

calificacionlabel=Label(framecampos, text='Calificacion')
config_label(calificacionlabel,3)
#calificacionlabel.grid(row=3, column=0, sticky='e', padx=10, pady=10)

escuelalabel=Label(framecampos, text='Escuela')
config_label(escuelalabel,4)
#escuelalabel.grid(row=4, column=0, sticky='e', padx=10, pady=10)

localidadlabel=Label(framecampos, text='Localidad')
config_label(localidadlabel,5)
#localidadlabel.grid(row=5, column=0, sticky='e', padx=10, pady=10)

provincialabel=Label(framecampos, text='Provincia')
config_label(provincialabel,6)
#provincialabel.grid(row=6, column=0, sticky='e', padx=10, pady=10)

#========================== INPUTS ==============================

#para los inputs tenemos que definir variables, pero estas son propias de tkinter:
'''
entero = IntVar()
flotante = DoubleVar()
cadena = StringVar()
booleano = BooleanVar()
'''
#necesito variables:
legajo=StringVar()
alumno=StringVar()
email=StringVar()
calificacion=DoubleVar()
escuela=StringVar()
localidad=StringVar()
provincia=StringVar()

#luego creo y ubico los inputs

legajo_input=Entry(framecampos, textvariable=legajo)
legajo_input.grid(row=0, column=1, padx=10, pady=10)#donde lo ubicamos y el padding en x y en Y
alumno_input=Entry(framecampos, textvariable=alumno)
alumno_input.grid(row=1, column=1, padx=10, pady=10)
email_input=Entry(framecampos, textvariable=email)
email_input.grid(row=2, column=1, padx=10, pady=10)
calificacion_input=Entry(framecampos, textvariable=calificacion)
calificacion_input.grid(row=3, column=1, padx=10, pady=10)
escuela.set('Seleccione')
escuelas=buscar_escuelas(False)
escuela_option = OptionMenu(framecampos, escuela,*escuelas)
escuela_option.grid(row=4, column=1, padx=10, pady=10, sticky='w')
#escuela_input=Entry(framecampos, textvariable='escuela')
#escuela_input.grid(row=4, column=1, padx=10, pady=10)

localidad_input=Entry(framecampos, textvariable=localidad)
localidad_input.grid(row=5, column=1, padx=10, pady=10)
localidad_input.config(state='readonly')
provincia_input=Entry(framecampos, textvariable=provincia)
provincia_input.grid(row=6, column=1, padx=10, pady=10)
provincia_input.config(state="readonly")

#---------------------FRAME BOTONES-----------------------
framebotones=Frame(raiz)
framebotones.config(bg=framebotones_color_fondo)
framebotones.pack(fill='both')

boton_crear=Button(framebotones, text='Crear', command=crear)
boton_crear.config(bg=framebotones_color_boton, fg=framebotones_color_texto)
boton_crear.grid(row=1, column=0, sticky="e", padx=10, pady=10)

boton_leer=Button(framebotones, text='Leer', command=buscar_legajo)
boton_leer.config(bg=framebotones_color_boton, fg=framebotones_color_texto)
boton_leer.grid(row=1, column=1, sticky="e", padx=10, pady=10)

boton_actualizar=Button(framebotones, text='Actualizar', command=actualizar)
boton_actualizar.config(bg=framebotones_color_boton, fg=framebotones_color_texto)
boton_actualizar.grid(row=1, column=2, sticky="e", padx=10, pady=10)
boton_borrar=Button(framebotones, text='Borrar', command=borrar)
boton_borrar.config(bg=framebotones_color_boton, fg=framebotones_color_texto)
boton_borrar.grid(row=1, column=3, sticky="e", padx=10, pady=10)

#------------FRAMECOPY------------------

framecopy=Frame(raiz)
framecopy.config(bg='black')
framecopy.pack(fill='both', expand='true')

copylabel=Label(framecopy, text='©2022 Copyright: Codo a Codo C#22624.')
copylabel.config(bg='black', fg='white')
copylabel.grid(row=0, column=3, padx=30, pady=10)

#copylabel=Text('Este es un texto de prueba2') este no funciono
raiz.mainloop()