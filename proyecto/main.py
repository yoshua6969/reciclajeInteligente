import ventana

if __name__ == "__main__":

    while True:
        print("1.) Modelo con Organico\n"
              "2.) Modelo con Plastico\n"
              "3.) Salir")

        opcion = input("Opcion: ")

        if opcion in ["1", "2", "3"]:
            if opcion == "3":
                print("Cerrando Programa...")
                break
            else:
                ventana.ventana_principal(opcion)
        else:
            print("ERROR. Por favor introduce una opcion valida\n")
