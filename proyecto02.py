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
        self.root = root
        self.root.title("Procesador de Imágenes")
        self.root.geometry("800x600")
        self.root.background="red"
        #print(self.root.configure())

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

        frame_labels = tk.Frame(root, background="#1b1b32")
        frame_labels.grid(row=1, column=0, columnspan=5, rowspan=1, sticky="NESW")

        frame_labels.rowconfigure(0,weight=1)
        frame_labels.columnconfigure(0,weight=1)
        frame_labels.columnconfigure(1,weight=1)
        frame_labels.columnconfigure(2,weight=1)
        frame_labels.columnconfigure(3,weight=1)
    

        # Crear una etiqueta
        fuente_titulo = Font(family="Arial", size=20, weight="bold")
        self.etiqueta = tk.Label(root, text="Bienvenido al procesador de imagenes", background="#1b1b32",fg="white", font=fuente_titulo)
        self.etiqueta.grid(row=0, column=0, columnspan=5, rowspan=1, sticky="NESW")

        fuente_etiquetas = Font(family="Arial", size=16, weight="bold")
        self.etiquetaR = tk.Label(frame_labels, text="Componente roja", background="#1b1b20",fg="red", borderwidth=10, font=fuente_etiquetas)
        self.etiquetaR.grid(row=1, column=1, columnspan=1, rowspan=1, sticky="NESW", padx=(5,5))

        self.etiquetaG = tk.Label(frame_labels, text="Componente verde", background="#1b1b20",fg="green", font=fuente_etiquetas)
        self.etiquetaG.grid(row=1, column=2, columnspan=1, rowspan=1, sticky="NESW", padx=(5,5))

        self.etiquetaB = tk.Label(frame_labels, text="Componente Azul",  background="#1b1b20",fg="blue", font=fuente_etiquetas)
        self.etiquetaB.grid(row=1, column=3, columnspan=1, rowspan=1, sticky="NESW", padx=(5,5))

        fuente_botones = Font(family="Arial", size=13, weight="normal")
        self.load_button = tk.Button(frame_labels, text="Abrir imagen", fg="white", command=self.load_image, background="#9932CC", activebackground="#00471b", font=fuente_botones, activeforeground="white")
        self.load_button.grid(row=1, column=0, columnspan=1, rowspan=1, sticky="NESW", padx=(5,5))


        frame_buttons = tk.Frame(root, background="#1b1b32")
        frame_buttons.grid(row=2, column=4, columnspan=1, rowspan=5, sticky="NESW")
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


        self.smooth_button = tk.Button(frame_buttons, text="Blanco y negro", fg="white", command=self.smooth_image, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.smooth_button.grid(column=0,columnspan=1,row=0,rowspan=1, sticky="NESW")
        self.binary_button = tk.Button(frame_buttons, text="Binarizado", fg="white", command=self.binary, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.binary_button.grid(column=0,columnspan=1,row=2,rowspan=1, sticky="NESW")
        self.superBinary_button = tk.Button(frame_buttons, text="Binarizado por promedio", fg="white", command=self.superBinary, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.superBinary_button.grid(column=0,columnspan=1,row=4,rowspan=1, sticky="NESW")
        self.negative_button = tk.Button(frame_buttons, text="Negativo", fg="white", command=self.negative, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.negative_button.grid(column=0,columnspan=1,row=6,rowspan=1, sticky="NESW")
        self.suavizarx3_button = tk.Button(frame_buttons, text="Suavizar (3x3)", fg="white", command=self.suavizarx3, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.suavizarx3_button.grid(column=0,columnspan=1,row=8,rowspan=1, sticky="NESW")
        self.suavizarx9_button = tk.Button(frame_buttons, text="Suavizar (9x9)", fg="white", command=self.suavizarx9, background="#9932CC", activebackground="#00471b", font=fuente_botones,activeforeground="white")
        self.suavizarx9_button.grid(column=0,columnspan=1,row=10,rowspan=1, sticky="NESW")


        # Frame para contener el Canvas y las barras de desplazamiento 	
        frame = tk.Frame(root)
        frame.grid(row=2, column=0, columnspan=4, rowspan=5, sticky="NESW")
        # Barra de desplazamiento vertical
        y_scrollbar = tk.Scrollbar(frame, orient="vertical", background="#1b1b32", bg="#1b1b32")
        y_scrollbar.pack(side="right", fill="y")
        # Barra de desplazamiento horizontal
        x_scrollbar = tk.Scrollbar(frame, orient="horizontal", background="#1b1b32", bg="#1b1b32") 
        x_scrollbar.pack(side="bottom", fill="x")

        # Canvas para mostrar la imagen
        self.canvas = tk.Canvas(frame, yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set, background="#1b1b32")
        self.canvas.pack(expand=True, fill="both")
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # Configurar las barras de desplazamiento
        y_scrollbar.config(command=self.canvas.yview)
        x_scrollbar.config(command=self.canvas.xview)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def load_image(self):
        file_path = filedialog.askopenfilename( title="Seleccionar Imagen", filetypes=[("Archivos PNG", "*.png"), ("Archivos JPG", "*.jpg")])
        if file_path:
            self.image_path = file_path
            print(file_path)
            self.image = cv2.imread(file_path)
            self.display_image()
    
    def display_image(self):
        if self.image is not None:
            img_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(img) 						
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk								
            self.canvas.config(scrollregion = self.canvas.bbox("all"))
            
    def on_mouse_move(self, event):
        if self.image is None: return
        x_canvas = event.x
        y_canvas = event.y
		# Imprimir las coordenadas con respecto al Canvas 
        if y_canvas < len(self.image) and x_canvas < len(self.image[0]):
           self.etiquetaR.config(text=str("Componente roja: : "+ str(self.image[y_canvas][x_canvas][2])))
           self.etiquetaG.config(text=str("Componente verde: "+ str(self.image[y_canvas][x_canvas][1])))
           self.etiquetaB.config(text=str("Componente azul: "+str(self.image[y_canvas][x_canvas][0])))

    def smooth_image(self):
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
        if self.image is not None:
            # Aplicar algún filtro, por ejemplo escala de grises
            filas, columnas, canales = self.image.shape
            for f in range(filas):
                for c in range(columnas):
                    for k in range(canales):
                        self.image[f,c,k] = numpy.uint8(255-self.image[f,c,k])

            self.display_image()
                        
    def suavizarx3(self):
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
                region = self.image[f1:f2+1,c1:c2+1]
                valor  = region.mean()
                new_image[f,c] = [numpy.uint8(valor), numpy.uint8(valor), numpy.uint8(valor)]
            if f%50==0 or f==filas-1:    
                root.update()
        self.image = new_image
        self.display_image()

    def suavizarx9(self):
        filas, columnas, canales = self.image.shape
        new_image = numpy.ndarray(shape=self.image.shape, dtype=numpy.uint8)
        for f in range(filas):
            for c in range(columnas):
                #Tenemos que especificar el tamano de nuestra region y como sera de 9 por nueve y el pixel evaluado sera el central debemos contemplar 4 de cada lado.
                f1, f2 = f-4, f+4
                c1, c2 = c-4, c+4
                if f1<0: f1 = 0
                if c1<0: c1 = 0
                if f2>filas-1: f2 = filas-1
                if c2>columnas-1: c2 = columnas-1
                region = self.image[f1:f2+1,c1:c2+1]
                valor  = region.mean()
                new_image[f,c] = [numpy.uint8(valor), numpy.uint8(valor), numpy.uint8(valor)]
            if f%50==0 or f==filas-1:    
                root.update()
        self.image = new_image
        self.display_image()








root = tk.Tk()
app = ImageProcessorApp(root)
root.mainloop()
