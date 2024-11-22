core = {
    "name": "core",
    "version": "latest",
    "image": "freya-core:latest",
    "ports": [6672]
}

dashboard = {
    "name": "dashboard",
    "version": "latest",
    "image": "freya-dashboard:latest",
    "ports": [6673]
}

default_packages = [core, dashboard]