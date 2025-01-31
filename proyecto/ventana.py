import tkinter as tk
from PIL import Image, ImageTk
from PIL import Image as PilImage
from keras.models import load_model
import cv2
from tkinter import *
import numpy as np
import imutils

camara = None
model = None
class_names = None
lblVideo = None
pantalla = None


def scanning():
    global camara
    if camara is not None:
        ret, frame = camara.read()
        if ret:
            # Resize:
            frame = imutils.resize(frame, width=600)

            # Convertir de BGR a RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Rotar la imagen
            frame_rgb = imutils.rotate_bound(frame_rgb, 90)

            im = PilImage.fromarray(frame_rgb)
            # im = im.rotate(-270)
            img = ImageTk.PhotoImage(image=im)

            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, scanning)

        else:
            camara.release()


def on_key_press(event):
    global camara, model, class_names, pantalla, image_path
    key = event.keysym


    if key == "Return":  # Tecla Enter
        # Agrega aquí la lógica que deseas realizar al presionar Enter
        print("Escaneando...")

        ret, image = camara.read()
        if ret:
            # Convierte la imagen en una matriz numpy y ajústala al formato de entrada del modelo.
            image = np.asarray(image, dtype=np.float32)

            # Normaliza la matriz de imagen al rango [0, 1]
            image = image / 255.0

            # Redimensiona la imagen al tamaño de entrada del modelo y agrega una dimensión adicional para el lote
            image = cv2.resize(image, (224, 224))
            image = np.expand_dims(image, axis=0)

            # Realiza la predicción con el modelo
            prediction = model.predict(image)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]

            class_name = class_name[2:]

            # Imprime la predicción y el puntaje de confianza
            print("Puntaje de confianza:", str(np.round(confidence_score * 100))[:-2], "%")

            if confidence_score > 0.6:
                print("Clase:", class_name, end="")

                if class_name == "Plastico\n":
                    print("Contenedor Amarillo")
                    image_path = "../Imagenes/plastico.png"

                elif class_name == "Papel\n":
                    print("Contenedor Azul")
                    image_path = "../Imagenes/papelCarton.png"

                elif class_name == "Carton\n":
                    print("Contenedor Azul")
                    image_path = "../Imagenes/papelCarton.png"

                elif class_name == "Vidrio\n":
                    print("Contenedor Verde")
                    image_path = "../Imagenes/vidrio.png"

                elif class_name == "Organico\n":
                    print("Contenedor Naranja/Gris")
                    image_path = "../Imagenes/organico.png"

                contenedor = tk.PhotoImage(file=image_path)

                # Crea un widget Label para mostrar la imagen en una posición específica
                label_image = Label(pantalla, image=contenedor)
                label_image.image = contenedor  # Guarda una referencia para evitar que la imagen sea eliminada por el recolector de basura
                label_image.place(x=160, y=265)
            else:
                print("ERROR en la Deteccion, pidele ayuda a un adulto.")

    elif key == "Escape":  # Tecla Esc
        # Agrega aquí la lógica que deseas realizar al presionar Esc
        print("Saliendo...")
        camara.release()
        cv2.destroyAllWindows()
        pantalla.destroy()


def ventana_principal(opcion):
    global model, class_names, lblVideo, camara, pantalla
    pantalla = Tk()
    pantalla.title("RECICLAJE INTELIGENTE")
    pantalla.geometry("1024x814")

    # Configurar para que la ventana no sea redimensionable
    pantalla.resizable(width=False, height=False)

    fondo = tk.PhotoImage(file="../Imagenes/fondo.png")
    background = Label(image=fondo)
    background.place(x=0, y=0, relwidth=1, relheight=1)

    if opcion == "1":
        # Load the model
        model = load_model("../modelo_organico/keras_model.h5", compile=False)

        # Load the labels
        class_names = open("../modelo_organico/labels.txt", "r").readlines()
    else:
        # Load the model
        model = load_model("../modelo_plastico/keras_model.h5", compile=False)

        # Load the labels
        class_names = open("../modelo_plastico/labels.txt", "r").readlines()

    lblVideo = Label(pantalla)
    lblVideo.place(x=580, y=128)

    # CAMARA puede ser 0 o 1 según la cámara predeterminada de tu computadora
    camara = cv2.VideoCapture(0)
    camara.set(3, 550)  # ALTURA
    camara.set(4, 415)  # ANCHO

    scanning()

    # modelo.grabar_camara("1")
    pantalla.bind("<Key>", on_key_press)

    pantalla.mainloop()


if __name__ == '__main__':
    ventana_principal("2")
