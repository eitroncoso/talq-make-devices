import json
from datetime import datetime
import pytz
import argparse
 
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--classname", help="Nombre de la clase")
parser.add_argument("-n", "--name", help="Nombre del dispositivo")
parser.add_argument("-f", "--file", help="Ruta del archivo de plantilla")
args = parser.parse_args()

# Nombre del device class
deviceClassName = args.classname
# Nombre del dispositivo logico
deviceName = args.name
# Archivo con el template a crear
deviceFile = args.file

deviceTemplate = {
    "address": "00000000-0000-0000-0000-000000000000",
    "class": deviceClassName,
    "functions": [],
    "name": deviceName
}

deviceClassesTemplate = {
    "functions": [],
    "name": deviceClassName
}

def loadOAS ():
    f = open('./OAS/talq-data-model-2-4-1-update-6.json')
    data = json.load(f)
    return data

def loadDefaultValues ():
    f = open('./OAS/attributeDefault.json')
    data = json.load(f)
    return data

def loadNewDevice ():
    f = open(deviceFile)
    data = json.load(f)
    return data

def saveDevice (deviceClass, device):
    jsonObject = json.dumps(deviceClass, indent=4)
    with open(f"./devices/production/{deviceClassName}.json", "w") as outfile:
        outfile.write(jsonObject)

    jsonObject = json.dumps(device, indent=4)
    with open(f"./devices/production/{deviceClassName}_device.json", "w") as outfile:
        outfile.write(jsonObject)

def getAttributeFunctionModel(dataModel, function, attribute):
    functionType = getFunctionType(function)

    functionProperties = dataModel["components"]["schemas"][functionType]["allOf"][1]["properties"]

    if attribute not in functionProperties:
        properties = {
            'type': "error",
            'description': "error",
            'scope': ""
        }

        return properties

    attributeProperties = functionProperties[attribute]['allOf']
    type = attributeProperties[0]["$ref"][21:]
    properties = {
        'type': type,
        'description': attributeProperties[1]["description"],
        'scope': attributeProperties[1]["x-talq-scope"]
    }

    return properties

def getFunctionType (function):
    return ''.join((x for x in function if not x.isdigit()))

def timestamp ():
    today = datetime.now(pytz.timezone('America/Santiago'))
    iso_date = today.isoformat()
    return iso_date

def run():
    dataModel = loadOAS ()
    values = loadDefaultValues ()
    newDevice = loadNewDevice ()
    deviceClassFunctions = []
    deviceFunctions = []
    print(f"DEVICE: {deviceClassName}")

    for key in newDevice:
        print(f"FUNCTION: {key}")
        deviceFunction = {
            "id": key,
            "type": getFunctionType(key)
        }

        deviceClassFunction = {
            "functionId": key,
            "type": getFunctionType(key),
            "attributes": [],
            "events": []
        }

        for attribute in newDevice[key]["attributes"]:
            attributeModel = getAttributeFunctionModel (dataModel, key, attribute)
            deviceFunction[attribute] = {
                "timestamp": timestamp(),
                "type": attributeModel["type"],
                "value": values[attributeModel["type"]]
            }

            if "defaults" in newDevice[key]:
                if attribute in newDevice[key]["defaults"]:
                    deviceFunction[attribute]["value"] = newDevice[key]["defaults"][attribute]

            deviceClassFunction["attributes"].append({
                "description": attributeModel["description"],
                "name": attribute
            })

            if attributeModel["scope"] == "event":
                deviceClassFunction["events"].append({
                    "description": attributeModel["description"],
                    "type": attribute
                })
        
        deviceFunctions.append(deviceFunction)
        deviceClassFunctions.append(deviceClassFunction)
    
    deviceTemplate["functions"] = deviceFunctions
    deviceClassesTemplate["functions"] = deviceClassFunctions

    saveDevice(deviceClassesTemplate, deviceTemplate)

if __name__ == '__main__':
    run()
