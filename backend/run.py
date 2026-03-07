"""Lanzador de la API. Ejecutar: python run.py"""
import subprocess
import sys
import os

if __name__ == "__main__":
    directorio = os.path.dirname(os.path.abspath(__file__))
    servidor = os.path.join(directorio, "servidor.py")
    sys.exit(subprocess.call([sys.executable, servidor]))
