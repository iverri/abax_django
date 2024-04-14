import json
import paho.mqtt.client as mqtt
from .models import BusInfo


def on_connect(client, userdata, flags, rc, properties=None):
    client.subscribe("/hfp/v2/journey/ongoing/vp/bus/+/+/+/+/+/+/+/2/#")
    client.subscribe("/hfp/v2/journey/ongoing/dep/bus/+/+/+/+/+/+/+/+/#")
    client.subscribe("/hfp/v2/journey/ongoing/vjout/bus/+/+/+/+/+/+/+/+/#")


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode("utf-8"))

    if "VP" in payload:
        data = payload["VP"]
        busID = data["veh"]
        if checkIfBusExists(busID):
            bus = BusInfo.objects.get(BusID=busID)
            bus.update_info(
                {
                    "Route": data["desi"],
                    "Direction": data["dir"],
                    "Latitute": data["lat"],
                    "Longitude": data["long"],
                    "LastUpdate": data["tst"],
                }
            )
        else:
            bus = BusInfo(
                BusID=busID,
                Info={
                    "Route": data["desi"],
                    "Direction": data["dir"],
                    "Latitute": data["lat"],
                    "Longitude": data["long"],
                    "LastUpdate": data["tst"],
                },
            )
            bus.save()

    elif "DEP" in payload:
        data = payload["DEP"]
        busID = data["veh"]
        if checkIfBusExists(busID):
            bus = BusInfo.objects.get(BusID=busID)
            bus.ubdate_info(
                {
                    "Route": data["desi"],
                    "Direction": data["dir"],
                    "Latitute": data["lat"],
                    "Longitude": data["long"],
                    "LastUpdate": data["tst"],
                    "LastStop": data["stop"],
                }
            )
        else:
            bus = BusInfo(
                BusID=busID,
                Info={
                    "Route": data["desi"],
                    "Direction": data["dir"],
                    "Latitute": data["lat"],
                    "Longitude": data["long"],
                    "LastUpdate": data["tst"],
                    "LastStop": data["stop"],
                },
            )
            bus.save()
    elif "VJOUT" in payload:
        bus = BusInfo.objects.filter(BusID=payload["VJOUT"]["veh"])
        bus.delete()


def checkIfBusExists(busID):
    return BusInfo.objects.filter(BusID=busID).exists()


client = mqtt.Client()
client.connect("mqtt.hsl.fi", 1883, 60)
client.on_connect = on_connect
client.on_message = on_message
