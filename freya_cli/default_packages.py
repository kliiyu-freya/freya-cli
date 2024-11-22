core = {
    "name": "core",
    "version": "latest",
    "image": "hello-world:latest",
    "ports": [6672],
    "ipv4": "192.168.168.2"
}

dashboard = {
    "name": "dashboard",
    "version": "latest",
    "image": "hello-world:latest",
    "ports": [6673],
    "ipv4": "192.168.168.3"
}

default_packages = [core, dashboard]