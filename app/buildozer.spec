[app]

# Título de la aplicación
title = File Explorer Test

# Nombre del paquete
package.name = fileexplorer

# Dominio del paquete
package.domain = com.test

# Directorio fuente
source.dir = .

# Extensiones a incluir
source.include_exts = py,png,jpg,kv,atlas

# Versión
version = 0.1

# Requisitos - VERSIÓN SIMPLIFICADA
requirements = python3,kivy==2.2.1

# Orientación
orientation = portrait

# Pantalla completa
fullscreen = 0

# Permisos de Android
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# API de Android
android.api = 33

# API mínima
android.minapi = 21

# Versión de NDK
android.ndk = 25b

# Arquitecturas
android.archs = arm64-v8a

# Aceptar licencias
android.accept_sdk_license = True

[buildozer]

# Nivel de log
log_level = 2

# No advertir si es root
warn_on_root = 0
