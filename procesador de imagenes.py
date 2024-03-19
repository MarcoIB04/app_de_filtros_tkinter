import cv2
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
import numpy

class ImageProcessorApp:
    image = None
    file_path = None
    def __init__(self, root):

        fuente_botones = Font(family="Arial", size=13, weight="normal")
        fuente_titulo = Font(family="Arial", size=20, weight="bold")


        #Creacion del root y definicion de su nombre y geometria 
        self.root = root
        self.root.title("Procesador de Imagenes")
        self.root.geometry("800x600")

        frame_labels = tk.Frame(root, background="#1b1b32")
        frame_buttons = tk.Frame(root, background="#1b1b32")

        #Crear los elementos del frame de etiquetas
        # Crear una etiqueta
        self.etiqueta = tk.Label(frame_labels, text="Bienvenido al procesador de imageness", background="#1b1b32",fg="white", font=fuente_titulo)
        self.load_button = tk.Button(frame_labels, text="Abrir imagen", fg="white", command=self.load_image, background="#6441a5", activebackground="#00101e", font=fuente_botones, activeforeground="white")
        self.restart_button = tk.Button(frame_labels, text="Reiniciar imagen", fg="white", command=self.restart, background="#6441a5", activebackground="#00101e", font=fuente_botones, activeforeground="white")

        #Frame del canvas principal
        frame = tk.Frame(root)
        frame2 = tk.Frame(root)

        y_scrollbar = tk.Scrollbar(frame, orient="vertical", background="#1b1b32", bg="#1b1b32")
        x_scrollbar = tk.Scrollbar(frame, orient="horizontal", background="#1b1b32", bg="#1b1b32") 
        y_scrollbar2 = tk.Scrollbar(frame2, orient="vertical", background="#1b1b32", bg="#1b1b32")
        x_scrollbar2 = tk.Scrollbar(frame2, orient="horizontal", background="#1b1b32", bg="#1b1b32") 
        self.canvas = tk.Canvas(frame, yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set, background="#1b1b32")
        self.canvas2 = tk.Canvas(frame2, background="#1b1b32")



        #Crear los botones
        self.smooth_button = tk.Button(frame_buttons, text="Escala de grises", fg="white", command=self.smooth_image, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.binary_button = tk.Button(frame_buttons, text="Binarizado", fg="white", command=self.binary, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.superBinary_button = tk.Button(frame_buttons, text="Binarizado por promedio", fg="white", command=self.superBinary, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.negative_button = tk.Button(frame_buttons, text="Negativo", fg="white", command=self.negative, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.suavizarx3_button = tk.Button(frame_buttons, text="Suavizar (3x3)", fg="white", command=self.suavizarx3, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.suavizarx9_button = tk.Button(frame_buttons, text="Suavizar (9x9)", fg="white", command=self.suavizarx9, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.roberts_button = tk.Button(frame_buttons, text="Suavizar con mascara Roberts", fg="white", command=self.filtro_roberts, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.sobel_button = tk.Button(frame_buttons, text="Suavizar con mascara Sobel", fg="white", command=self.filtro_sobel, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.prewitt_button = tk.Button(frame_buttons, text="Suavizar con mascara Prewitt", fg="white", command=self.filtro_prewitt, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.canny_button = tk.Button(frame_buttons, text="Suavizar con algoritmo Canny", fg="white", command=self.filtro_canny, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")


        #Divisiones de celdas para grid 
        #Division del root
        self.root.columnconfigure(0,weight=3)
        self.root.columnconfigure(1,weight=3)
        self.root.columnconfigure(2,weight=3)
        self.root.columnconfigure(3,weight=3)
        self.root.columnconfigure(4,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.root.rowconfigure(1,weight=1)
        self.root.rowconfigure(2,weight=3)
        self.root.rowconfigure(3,weight=3)
        self.root.rowconfigure(4,weight=3)
        self.root.rowconfigure(5,weight=3)
        self.root.rowconfigure(6,weight=3)
        #Division del frame para las etiquetas
        frame_labels.rowconfigure(0,weight=1)
        frame_labels.rowconfigure(2,weight=1)
        frame_labels.columnconfigure(0,weight=1)
        frame_labels.columnconfigure(1,weight=1)
        #Division del frame que contiene los botones
        frame_buttons.columnconfigure(0,weight=1)
        frame_buttons.rowconfigure(0,weight=1)
        frame_buttons.rowconfigure(1,weight=3)
        frame_buttons.rowconfigure(2,weight=1)
        frame_buttons.rowconfigure(3,weight=3)
        frame_buttons.rowconfigure(4,weight=1)
        frame_buttons.rowconfigure(5,weight=3)
        frame_buttons.rowconfigure(6,weight=1)
        frame_buttons.rowconfigure(7,weight=3)
        frame_buttons.rowconfigure(8,weight=1)
        frame_buttons.rowconfigure(9,weight=3)
        frame_buttons.rowconfigure(10,weight=1)
        frame_buttons.rowconfigure(11,weight=3)
        frame_buttons.rowconfigure(12,weight=1)
        frame_buttons.rowconfigure(13,weight=3)
        frame_buttons.rowconfigure(14,weight=1)
        frame_buttons.rowconfigure(15,weight=3)
        frame_buttons.rowconfigure(16,weight=1)
        frame_buttons.rowconfigure(17,weight=3)
        frame_buttons.rowconfigure(18,weight=1)
    
        #Acomodar todos los objetos en los frames
        #Acomodar los elementos del root principal
        #Frames
        frame_labels.grid(row=0, column=0, columnspan=5, rowspan=2, sticky="NESW")
        frame_buttons.grid(row=2, column=4, columnspan=1, rowspan=5, sticky="NESW")

        #Acomodar los elementos del frame de etiquetas
        self.etiqueta.grid(row=0, column=0, columnspan=2, rowspan=1, sticky="NESW")
        self.load_button.grid(row=1, column=0, columnspan=1, rowspan=1, sticky="NESW", padx=(5,5))
        self.restart_button.grid(row=1, column=1, columnspan=1, rowspan=1, sticky="NESW", padx=(5,5))

        #Acomodar los botones
        self.smooth_button.grid(column=0,columnspan=1,row=0,rowspan=1, sticky="NESW")
        self.binary_button.grid(column=0,columnspan=1,row=2,rowspan=1, sticky="NESW")
        self.superBinary_button.grid(column=0,columnspan=1,row=4,rowspan=1, sticky="NESW")
        self.negative_button.grid(column=0,columnspan=1,row=6,rowspan=1, sticky="NESW")
        self.suavizarx3_button.grid(column=0,columnspan=1,row=8,rowspan=1, sticky="NESW")
        self.suavizarx9_button.grid(column=0,columnspan=1,row=10,rowspan=1, sticky="NESW")
        self.roberts_button.grid(column=0,columnspan=1,row=12,rowspan=1, sticky="NESW")
        self.sobel_button.grid(column=0,columnspan=1,row=14,rowspan=1, sticky="NESW")
        self.prewitt_button.grid(column=0,columnspan=1,row=16,rowspan=1, sticky="NESW")
        self.canny_button.grid(column=0,columnspan=1,row=18,rowspan=1, sticky="NESW")

        #Acomodar el canvas y los scrollbars	
        frame.grid(row=2, column=2, columnspan=2, rowspan=5, sticky="NESW")
        frame2.grid(row=2, column=0, columnspan=2, rowspan=5, sticky="NESW")
        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")
        y_scrollbar2.pack(side="right", fill="y")
        x_scrollbar2.pack(side="bottom", fill="x")
        self.canvas.pack(expand=True, fill="both")
        self.canvas2.pack(expand=True, fill="both")
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # Configurar las barras de desplazamiento
        y_scrollbar.config(command=self.canvas.yview)
        x_scrollbar.config(command=self.canvas.xview)
        y_scrollbar2.config(command=self.canvas2.yview)
        x_scrollbar2.config(command=self.canvas2.xview)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas2.config(scrollregion=self.canvas2.bbox("all"))
    

    #Funciones de cargar, mostrar y reiniciar imagen
    def load_image(self):
        file_path = filedialog.askopenfilename( title="Seleccionar Imagen", filetypes=[("Archivos PNG", "*.png"), ("Archivos JPG", "*.jpg")])
        if file_path:
            self.image_path = file_path
            self.image = cv2.imread(self.image_path)
            self.display2_image()

    def display2_image(self):
        if self.image is not None:
            # Convertir la imagen a un tipo de datos compatible (por ejemplo, 8 bits sin signo)
            self.image = self.image.astype(numpy.uint8)
            
            # Convertir la imagen al espacio de color RGB
            img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(img) 						
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk								
            self.canvas.config(scrollregion = self.canvas.bbox("all"))
            self.canvas2.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas2.image = img_tk								
            self.canvas2.config(scrollregion = self.canvas2.bbox("all"))
    
    def display_image(self):
        if self.image is not None:
            # Convertir la imagen a un tipo de datos compatible (por ejemplo, 8 bits sin signo)
            self.image = self.image.astype(numpy.uint8)
            
            # Convertir la imagen al espacio de color RGB
            img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(img) 						
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk								
            self.canvas.config(scrollregion = self.canvas.bbox("all"))

    def restart(self):
        if self.image is not None:
            self.image = cv2.imread(self.image_path)
            self.display_image()    
            
    def on_mouse_move(self, event):
        if self.image is None: return
        x_canvas = event.x
        y_canvas = event.y

    def smooth_image(self):
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        if self.image is not None:
            # Aplicar algún filtro, por ejemplo escala de grises
            filas, columnas, canales = self.image.shape
            for f in range(filas):
                for c in range(columnas):
                    pro = (numpy.uint16(self.image[f,c,0]) + self.image[f,c,1] + self.image[f,c,2]) // 3
                    self.image[f,c,0] = numpy.uint8(pro)
                    self.image[f,c,1] = numpy.uint8(pro)
                    self.image[f,c,2] = numpy.uint8(pro)
            self.display_image()

    def binary(self):
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        if self.image is not None:
            # Aplicar algún filtro, por ejemplo escala de grises
            filas, columnas, canales = self.image.shape
            for f in range(filas):
                for c in range(columnas):
                    pro = (numpy.uint16(self.image[f,c,0]) + self.image[f,c,1] + self.image[f,c,2]) // 3
                    if pro >= 128:
                        self.image[f,c,0] = numpy.uint8(255)
                        self.image[f,c,1] = numpy.uint8(255)
                        self.image[f,c,2] = numpy.uint8(255)
                    else:
                        self.image[f,c,0] = numpy.uint8(0)
                        self.image[f,c,1] = numpy.uint8(0)
                        self.image[f,c,2] = numpy.uint8(0)

            self.display_image()

    def superBinary(self):
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        i = 0
        suma = 0
        filas, columnas, canales = self.image.shape
        for f in range(filas):
            for c in range(columnas):
                promind =int(((self.image[f,c,0])+(self.image[f,c,2])+(self.image[f,c,1]))//3)
                suma = suma + promind
                i = i +  1
        prom = suma //i
        print(prom)
        for f in range(filas):
            for c in range(columnas):
                promind =((self.image[f,c,0])+(self.image[f,c,2])+(self.image[f,c,1]))//3
                if promind >= prom:
                    self.image[f,c,0] = numpy.uint8(255)
                    self.image[f,c,1] = numpy.uint8(255)
                    self.image[f,c,2] = numpy.uint8(255)
                else:
                    self.image[f,c,0] = numpy.uint8(0)
                    self.image[f,c,1] = numpy.uint8(0)
                    self.image[f,c,2] = numpy.uint8(0)
            self.display_image()

    def negative(self):
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        if self.image is not None:
            # Aplicar algún filtro, por ejemplo escala de grises
            filas, columnas, canales = self.image.shape
            for f in range(filas):
                for c in range(columnas):
                    for k in range(canales):
                        self.image[f,c,k] = numpy.uint8(255-self.image[f,c,k])

            self.display_image()
                        
    def suavizarx3(self):
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        filas, columnas, canales = self.image.shape
        new_image = numpy.ndarray(shape=self.image.shape, dtype=numpy.uint8)
        for f in range(filas):
            for c in range(columnas):
                f1, f2 = f-1, f+1
                c1, c2 = c-1, c+1
                if f1<0: f1 = 0
                if c1<0: c1 = 0
                if f2>filas-1: f2 = filas-1
                if c2>columnas-1: c2 = columnas-1

                region_roja = 0
                for i in range(f1, f2+1):
                    for e in range(c1, c2+1):
                        region_roja = region_roja  + self.image[i,e,0]
                region_roja = region_roja//9

                region_verde = 0
                for i in range(f1, f2+1):
                    for e in range(c1, c2+1):
                        region_verde = region_verde  + self.image[i,e,1]
                region_verde = region_verde//9

                region_azul = 0
                for i in range(f1, f2+1):
                    for e in range(c1, c2+1):
                        region_azul = region_azul  + self.image[i,e,2]
                region_azul = region_azul//9

                new_image[f,c] = [numpy.uint8(region_roja), numpy.uint8(region_verde), numpy.uint8(region_azul)]
            if f%50==0 or f==filas-1:    
                root.update()
        self.image = new_image
        self.display_image()

    def suavizarx9(self):
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        filas, columnas, canales = self.image.shape
        new_image = numpy.ndarray(shape=self.image.shape, dtype=numpy.uint8)
                # Verificar si hay una imagen cargada

        for f in range(filas):
            for c in range(columnas):
                f1, f2 = f-4, f+4
                c1, c2 = c-4, c+4
                if f1<0: f1 = 0
                if c1<0: c1 = 0
                if f2>filas-1: f2 = filas-1
                if c2>columnas-1: c2 = columnas-1

                region_roja = 0
                for i in range(f1, f2+1):
                    for e in range(c1, c2+1):
                        region_roja = region_roja  + self.image[i,e,0]
                region_roja = region_roja//81

                region_verde = 0
                for i in range(f1, f2+1):
                    for e in range(c1, c2+1):
                        region_verde = region_verde  + self.image[i,e,1]
                region_verde = region_verde//81

                region_azul = 0
                for i in range(f1, f2+1):
                    for e in range(c1, c2+1):
                        region_azul = region_azul  + self.image[i,e,2]
                region_azul = region_azul//81

                new_image[f,c] = [numpy.uint8(region_roja), numpy.uint8(region_verde), numpy.uint8(region_azul)]
            if f%50==0 or f==filas-1:    
                root.update()
        self.image = new_image
        self.display_image()

    def filtro_roberts(self):
        # Verificar si hay una imagen cargada
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        
        # Convierte la imagen a escala de grises
        gris = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        
        # Aplicar un suavizado Gaussiano para eliminar el ruido
        gris_suavizado = cv2.GaussianBlur(gris, (5, 5), 0)
        
        # Obtener dimensiones de la imagen
        alto, ancho = gris_suavizado.shape
        
        # Crear una matriz para almacenar los bordes detectados
        bordes_roberts = numpy.zeros((alto, ancho), dtype=numpy.uint8)
        
        # Máscaras de Roberts
        mascara_x = numpy.array([[1, 0], [0, -1]])
        mascara_y = numpy.array([[0, 1], [-1, 0]])
        
        # Aplicar el filtro de detección de bordes Roberts
        for y in range(alto - 1):
            for x in range(ancho - 1):
                gx = numpy.sum(gris_suavizado[y:y+2, x:x+2] * mascara_x)
                gy = numpy.sum(gris_suavizado[y:y+2, x:x+2] * mascara_y)
                gradiente = int(numpy.sqrt(gx**2 + gy**2))
                if gradiente > 255:
                    gradiente = 255
                bordes_roberts[y, x] = gradiente
        
        # Actualiza la imagen en la aplicación y la muestra
        self.image = bordes_roberts
        self.display_image()

    """Filtro sobel usando funciones nativas de opencv para poder compararlo con el filtro propio, ESTE FILTRO NO SE USA EN LA APP, SOLO ESTA PARA CUESTION DE PRUEBAS"""
    def filtro_roberts_cv(self):
        # Verificar si hay una imagen cargada
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        
        # Convierte la imagen a escala de grises
        gris = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        
        # Aplica el filtro de detección de bordes Roberts
        roberts_x = cv2.filter2D(gris, -1, numpy.array([[1, 0], [0, -1]]))
        roberts_y = cv2.filter2D(gris, -1, numpy.array([[0, 1], [-1, 0]]))
        
        # Combina los resultados de los filtros x e y
        bordes_roberts = cv2.addWeighted(roberts_x, 0.5, roberts_y, 0.5, 0)
        
        # Actualiza la imagen en la aplicación y la muestra
        self.image = bordes_roberts
        self.display_image()

    def filtro_sobel(self):
        # Verificar si hay una imagen cargada
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        
        # Convierte la imagen a escala de grises
        gris = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        # Aplicar un suavizado Gaussiano para eliminar el ruido
        gris_suavizado = cv2.GaussianBlur(gris, (5, 5), 0)
        
        # Obtener dimensiones de la imagen
        alto, ancho = gris_suavizado.shape
        
        # Crear una matriz para almacenar los bordes detectados
        bordes_sobel = numpy.zeros((alto, ancho), dtype=numpy.uint8)
        
        # Máscaras Sobel en direcciones x e y
        mascara_sobel_x = numpy.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        mascara_sobel_y = numpy.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
        
        # Aplicar el filtro de detección de bordes Roberts con máscaras Sobel
        for y in range(alto - 2):
            for x in range(ancho - 2):
                gx = numpy.sum(gris_suavizado[y:y+3, x:x+3] * mascara_sobel_x)
                gy = numpy.sum(gris_suavizado[y:y+3, x:x+3] * mascara_sobel_y)
                gradiente = int(numpy.sqrt(gx**2 + gy**2))
                if gradiente > 255:
                    gradiente = 255
                bordes_sobel[y, x] = gradiente
        
        # Actualiza la imagen en la aplicación y la muestra
        self.image = bordes_sobel
        self.display_image()

    """Filtro sobel usando funciones nativas de opencv para poder compararlo con el filtro propio, ESTE FILTRO NO SE USA EN LA APP, SOLO ESTA PARA CUESTION DE PRUEBAS"""
    def filtro_sobel_cv(self):
        # Verificar si hay una imagen cargada
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        
        # Convierte la imagen a escala de grises
        gris = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        
        # Aplicar un suavizado Gaussiano para eliminar el ruido
        gris_suavizado = cv2.GaussianBlur(gris, (5, 5), 0)
        
        # Obtener los bordes utilizando el operador Sobel
        sobel_x = cv2.Sobel(gris_suavizado, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gris_suavizado, cv2.CV_64F, 0, 1, ksize=3)
        
        # Calcular la magnitud de los gradientes
        gradientes = cv2.magnitude(sobel_x, sobel_y)
        
        # Convertir los gradientes a uint8 para visualización
        bordes_sobel = cv2.convertScaleAbs(gradientes)
        
        # Mostrar los bordes en la aplicación
        self.image = bordes_sobel
        self.display_image()


    def filtro_prewitt(self):
        # Verificar si hay una imagen cargada
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        
        # Convierte la imagen a escala de grises
        gris = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        
        # Aplicar un suavizado Gaussiano para eliminar el ruido
        gris_suavizado = cv2.GaussianBlur(gris, (5, 5), 0)
        
        # Obtener dimensiones de la imagen
        alto, ancho = gris_suavizado.shape
        
        # Crear una matriz para almacenar los bordes detectados
        bordes_prewitt = numpy.zeros((alto, ancho), dtype=numpy.uint8)
        
        # Máscaras Sobel en direcciones x e y
        mascara_prewitt_x = numpy.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        mascara_prewitt_y = numpy.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        
        # Aplicar el filtro de detección de bordes Roberts con máscaras Sobel
        for y in range(alto - 2):
            for x in range(ancho - 2):
                gx = numpy.sum(gris_suavizado[y:y+3, x:x+3] * mascara_prewitt_x)
                gy = numpy.sum(gris_suavizado[y:y+3, x:x+3] * mascara_prewitt_y)
                gradiente = int(numpy.sqrt(gx**2 + gy**2))
                if gradiente > 255:
                    gradiente = 255
                bordes_prewitt[y, x] = gradiente
        
        # Actualiza la imagen en la aplicación y la muestra
        self.image = bordes_prewitt
        self.display_image()

    def filtro_canny(self):
        # Verificar si hay una imagen cargada
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        
        # Convierte la imagen a escala de grises
        gris = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        
        # Aplicar un suavizado Gaussiano para reducir el ruido
        gris_suavizado = cv2.GaussianBlur(gris, (5, 5), 0)
        
        # Calcular gradientes con Sobel
        gradiente_x = cv2.Sobel(gris_suavizado, cv2.CV_64F, 1, 0, ksize=3)
        gradiente_y = cv2.Sobel(gris_suavizado, cv2.CV_64F, 0, 1, ksize=3)
        
        # Calcular la magnitud y la dirección del gradiente
        magnitud_gradiente = numpy.sqrt(gradiente_x**2 + gradiente_y**2)
        direccion_gradiente = numpy.arctan2(gradiente_y, gradiente_x)
        
        # Aplicar la supresión de no máximos
        bordes_suprimidos = numpy.zeros_like(magnitud_gradiente)
        for i in range(1, magnitud_gradiente.shape[0] - 1):
            for j in range(1, magnitud_gradiente.shape[1] - 1):
                direccion = direccion_gradiente[i, j] * 180 / numpy.pi
                if (0 <= direccion < 22.5) or (157.5 <= direccion <= 180):
                    vecinos = [magnitud_gradiente[i, j-1], magnitud_gradiente[i, j], magnitud_gradiente[i, j+1]]
                elif (22.5 <= direccion < 67.5):
                    vecinos = [magnitud_gradiente[i-1, j-1], magnitud_gradiente[i, j], magnitud_gradiente[i+1, j+1]]
                elif (67.5 <= direccion < 112.5):
                    vecinos = [magnitud_gradiente[i-1, j], magnitud_gradiente[i, j], magnitud_gradiente[i+1, j]]
                else:
                    vecinos = [magnitud_gradiente[i-1, j+1], magnitud_gradiente[i, j], magnitud_gradiente[i+1, j-1]]
                if magnitud_gradiente[i, j] >= max(vecinos):
                    bordes_suprimidos[i, j] = magnitud_gradiente[i, j]
        
        # Aplicar umbrales
        umbral_alto = 100
        umbral_bajo = 50
        bordes_canny = numpy.zeros_like(bordes_suprimidos)
        bordes_canny[bordes_suprimidos >= umbral_alto] = 255
        bordes_canny[(bordes_suprimidos >= umbral_bajo) & (bordes_suprimidos < umbral_alto)] = 128
        
        # Mostrar los bordes en la aplicación
        self.image = bordes_canny
        self.display_image()

    """Filtro sobel usando funciones nativas de opencv para poder compararlo con el filtro propio, ESTE FILTRO NO SE USA EN LA APP, SOLO ESTA PARA CUESTION DE PRUEBAS"""
    def filtro_canny_cv(self):
        # Verificar si hay una imagen cargada
        if self.image is None:
            messagebox.showerror("Error", "Debe cargar una imagen primero.")
            return
        
        # Convierte la imagen a escala de grises
        gris = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        
        # Aplicar un suavizado Gaussiano para eliminar el ruido
        gris_suavizado = cv2.GaussianBlur(gris, (5, 5), 0)
        
        # Aplicar el detector de bordes Canny
        bordes_canny = cv2.Canny(gris_suavizado, 50, 150)  # Umbral bajo y alto
        
        # Mostrar los bordes en la aplicación
        self.image = bordes_canny
        self.display_image()


root = tk.Tk()
app = ImageProcessorApp(root)
root.mainloop()