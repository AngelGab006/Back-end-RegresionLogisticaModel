#!/usr/bin/env bash
# Usa Gunicorn para arrancar tu app.py
# El formato es: gunicorn [nombre_del_archivo_flask]:[nombre_de_la_instancia_flask]
gunicorn main:app