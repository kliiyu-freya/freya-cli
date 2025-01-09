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
    "image": "ghcr.io/kliiyu-freya/dashboard:dev",
    "ports": [(8089, 8080)],
    "ipv4": "192.168.168.4"
}

system_monitor = {
    "name": "system_monitor",
    "version": "latest",
    "image": "ghcr.io/kliiyu-freya/system_monitor:latest",
    "volumes": ["/proc:/host_proc:ro", "/sys:/host_sys:ro"],
    "environment": ["PROC_PATH=/host_proc", "SYS_PATH=/host_sys"],
    "cap_add": ["SYS_ADMIN"],
    "privileged": True,
    "network_mode": "host"
}

friday = {
    "name": "friday",
    "version": "latest",
    "image": "ghcr.io/kliiyu-freya/friday:latest",
}

spotify = {
    "name": "spotify",
    "version": "latest",
    "image": "ghcr.io/kliiyu-freya/spotify:latest",
}

default_packages = [
    core,
    mqtt_broker,
    dashboard,
    system_monitor,
    friday,
    spotify
]