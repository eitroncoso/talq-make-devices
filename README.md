# Herramienta para creación de dispositivos lógicos TALQ

La herramienta de creación de dispositivos lógicos TALQ permite generar un dispositivo lógico, compuesto por un device class y un device template, mediante un archivo de plantilla que contiene los atributos y funciones requeridos.

El archivo de plantilla es un objeto que contiene los nombres de las funciones a utilizar (tipo de función + número). Cada una de estas funciones tiene un elemento obligatorio llamado "attributes", que incluye todos los atributos necesarios para dicha función. También puede incluir un elemento opcional llamado "defaults", que permite configurar los valores por defecto para cada uno de los atributos.

Una vez que el archivo de plantilla ha sido creado, se puede generar el dispositivo lógico utilizando el siguiente comando en la terminal:

```bash
python3 main.py -c "Nombre de la clase" -n "Nombre del dispositivo" -f "Ruta del archivo de plantilla"
```

Donde:

"-c" indica el nombre de la clase.
"-n" indica el nombre del dispositivo.
"-f" indica la ruta del archivo de plantilla.

Ejemplo:

```bash
python3 main.py -c cls:LuminaryView -n tls:LuminaryView -f luminaryView.json
```