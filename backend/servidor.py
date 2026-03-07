import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from fitness_api.app import aplicacion

if __name__ == "__main__":
    aplicacion.run(host="0.0.0.0", port=5000, debug=True)
