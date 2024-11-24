core = {
    "name": "core",
    "version": "latest",
    "image": "ghcr.io/kliiyu-freya/freya:latest",
    "ports": [6672],
    "ipv4": "192.168.168.2"
}

mqtt_broker = {
    "name": "mqtt_broker",
    "version": "latest",
    "image": "eclipse-mosquitto:latest",
    "ports": [1883, 9001],
    "ipv4": "192.168.168.3"
}

dashboard = {
    "name": "dashboard",
    "version": "latest",
    "image": "ghcr.io/kliiyu-freya/dashboard:latest",
    "ports": [6673],
    "ipv4": "192.168.168.4"
}

default_packages = [core, mqtt_broker, dashboard]