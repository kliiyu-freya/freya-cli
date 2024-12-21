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
    "ports": [80, 6673],
    "network_mode": "host",
    "restart": "always",
    "volumes": ["./nginx/nginx.conf:/etc/nginx/nginx.conf", "./dist:/usr/share/nginx/html"],
    "enmvironment": ["AVAHI_NAME=freya"]
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

default_packages = [
    core, 
    mqtt_broker, 
    dashboard, 
    system_monitor
]