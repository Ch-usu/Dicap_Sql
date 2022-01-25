import tkinter
import mysql.connector
import pandas

def inicio_sesion(host,user,password):
    """"""
    try:
        coneccion = mysql.connector.connect(host=host,user=user,password=password)
        label_inicio_mensaje.config(text="Conexion exitosa")
        base_de_datos(coneccion)
        return coneccion
    except mysql.connector.Error as err:
        label_inicio_mensaje.config(text="Error al conectar")

def base_de_datos(coneccion):
    """"""
    datos = pandas.read_sql("SHOW DATABASES",coneccion)
    frame_base_datos.delete(0,tkinter.END)
    for i in list(datos['Database']):
        frame_base_datos.insert(frame_base_datos.size() + 1, i)

def tablas():
    """"""
    global db
    db = frame_base_datos.get(frame_base_datos.curselection())
    coneccion = inicio_sesion(entrada_host.get(),entrada_user.get(),entrada_pass.get())
    datos = pandas.read_sql("SHOW TABLES FROM " +  db, coneccion)
    frame_tablas.delete(0,tkinter.END)
    frame_tablas2.delete(0,tkinter.END)
    for i in list(datos[list(datos)[0]]):
        frame_tablas.insert(frame_tablas.size() + 1, i)
        frame_tablas2.insert(frame_tablas2.size() + 1, i)

def batchhistory():
    global batch
    batch = frame_tablas.get(frame_tablas.curselection())
    coneccion = inicio_sesion(entrada_host.get(),entrada_user.get(),entrada_pass.get())
    datos = pandas.read_sql("SELECT * FROM " + db + "." + batch, coneccion)
    frame_batch.delete(0,tkinter.END)
    frame_batch.insert(frame_batch.size() + 1, "inicio de operacion                        fin de operacion")
    global numero_batch
    numero_batch = 100
    for i in range(numero_batch):
        frame_batch.insert(frame_batch.size() + 1, str(datos['Start_Time'][i]) + "                 " + str(datos['End_Time'][i]))

def mas_batch():
    global numero_batch
    coneccion = inicio_sesion(entrada_host.get(),entrada_user.get(),entrada_pass.get())
    datos = pandas.read_sql("SELECT * FROM " + db + "." + batch, coneccion) 
    old_numero_batch = numero_batch
    numero_batch += 100
    for i in range(old_numero_batch,numero_batch):
        frame_batch.insert(frame_batch.size() + 1, str(datos['Start_Time'][i]) + "                 " + str(datos['End_Time'][i]))

def exportar():
    trend = frame_tablas2.get(frame_tablas2.curselection())
    batch = frame_batch.get(frame_batch.curselection())
    start_time = batch[0:19]
    end_time = batch[36:55]
    coneccion = inicio_sesion(entrada_host.get(),entrada_user.get(),entrada_pass.get())
    datos = pandas.read_sql("SELECT * FROM " + db + "." + trend + " WHERE Time_Stamp BETWEEN '" + start_time + "' AND '" + end_time + "'", coneccion)
    #datos.to_excel(start_time.replace(' ','-') + 'y' +  end_time.replace(' ','-') +".xlsx")
    nombre = start_time.replace('-','') + end_time.replace('-','') +".xlsx"
    nombre = nombre.replace(' ','')
    nombre = nombre.replace(':','')
    print(nombre)
    datos.to_excel(nombre)

#initialize the window
root = tkinter.Tk()
root.title('DicapSql')
root.geometry("550x800")
root.resizable(False,False)

#login
label_host = tkinter.Label(root, text="Incerte el host")
label_host.place(x=50,y=10)
entrada_host = tkinter.Entry(root)
entrada_host.place(x=50,y=30)
label_user = tkinter.Label(root, text="Incerte el usuario")
label_user.place(x=200,y=10)
entrada_user = tkinter.Entry(root)
entrada_user.place(x=200,y=30)
label_pass = tkinter.Label(root, text="Incerte la contraseña")
label_pass.place(x=400,y=10)
entrada_pass = tkinter.Entry(root)
entrada_pass.place(x=400,y=30)
boton_inicio = tkinter.Button(root, text="Iniciar sesión", command=lambda:inicio_sesion(entrada_host.get(),entrada_user.get(),entrada_pass.get()))
boton_inicio.place(x=225,y=60)
label_inicio_mensaje = tkinter.Label(root, text="")
label_inicio_mensaje.place(x=225,y=90)

#mostrar bases de datos
label_base_datos = tkinter.Label(root, text="Elija una base de datos")
label_base_datos.place(x=195,y=120)
frame1 = tkinter.Frame(root)
frame_base_datos = tkinter.Listbox(frame1,width = 25, height = 4, selectmode = tkinter.BROWSE, exportselection=False)
frame1.place(x=195,y=140)
scrollbar1 = tkinter.Scrollbar(frame1, orient="vertical")
frame_base_datos.pack(side=tkinter.LEFT,fill= tkinter.Y)
scrollbar1.config(command = frame_base_datos.yview)
scrollbar1.pack(side=tkinter.RIGHT, fill=tkinter.Y)
frame_base_datos.config(yscrollcommand=scrollbar1.set)
boton_base_datos = tkinter.Button(root, text="elegir", command=lambda:tablas())
boton_base_datos.place(x=250,y=225)

#mostrar tablas batch
label_tablas = tkinter.Label(root, text="Elija la tabla del batch")
label_tablas.place(x=100,y=275)
frame2 = tkinter.Frame(root)
frame_tablas = tkinter.Listbox(frame2,width = 25, height = 4, selectmode = tkinter.BROWSE, exportselection=False)
frame2.place(x=100,y=300)
scrollbar2 = tkinter.Scrollbar(frame2, orient="vertical")
frame_tablas.pack(side=tkinter.LEFT,fill= tkinter.Y)
scrollbar2.config(command = frame_tablas.yview)
scrollbar2.pack(side=tkinter.RIGHT, fill=tkinter.Y)
frame_tablas.config(yscrollcommand=scrollbar2.set)
boton_batch = tkinter.Button(root, text="elegir", command=lambda:batchhistory())
boton_batch.place(x=250,y=400)

#mostrar tablas trend
label_tablas2 = tkinter.Label(root, text="Elija la tabla del trend")
label_tablas2.place(x=300,y=275)
frame3 = tkinter.Frame(root)
frame_tablas2 = tkinter.Listbox(frame3,width = 25, height = 4, selectmode = tkinter.BROWSE, exportselection=False)
frame3.place(x=300,y=300)
scrollbar3 = tkinter.Scrollbar(frame3, orient="vertical")
frame_tablas2.pack(side=tkinter.LEFT,fill= tkinter.Y)
scrollbar3.config(command = frame_tablas2.yview)
scrollbar3.pack(side=tkinter.RIGHT, fill=tkinter.Y)
frame_tablas2.config(yscrollcommand=scrollbar3.set)

#mostrar tabla del batch
label_batch = tkinter.Label(root, text="Elija una fecha")
label_batch.place(x=225,y=450)
frame4 = tkinter.Frame(root)
frame_batch = tkinter.Listbox(frame4,width = 75, height = 10, selectmode = tkinter.BROWSE, exportselection=False)
frame4.place(x=35,y=475)
scrollbar4 = tkinter.Scrollbar(frame4, orient="vertical")
frame_batch.pack(side=tkinter.LEFT,fill= tkinter.Y)
scrollbar4.config(command = frame_batch.yview)
scrollbar4.pack(side=tkinter.RIGHT, fill=tkinter.Y)
frame_batch.config(yscrollcommand=scrollbar4.set)
boton_batch = tkinter.Button(root, text="exportar", command=lambda:exportar())
boton_batch.place(x=250,y=650)
boton_mas = tkinter.Button(root, text="mostrar mas", command=lambda:mas_batch())
boton_mas.place(x=30,y=630)


root.mainloop()