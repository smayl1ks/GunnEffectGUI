from pathlib import Path

# Global data
APP_NAME = "GunnEffectGUI"
VERSION = "1.0.0"

PROFILES_PATH = Path(__file__).parent / "profiles"
PROFILES_DICT = {pathFILE.name: str(pathFILE)
                 for pathFILE in PROFILES_PATH.iterdir()}

RESOURCES_PATH = Path(__file__).parent / "gui" / "resources"
RESOURCES_IMAG = RESOURCES_PATH / "img"
IMG_DICT = {pathIMG.name: str(pathIMG)
                 for pathIMG in RESOURCES_IMAG.iterdir()}

# Frequency for write to shared array
WRITE_FREQUENCY = 30

# Function for running gui and core
from app.core.run_core import run_core
from app.gui.run_gui import run_gui

# Shared memory for gui and core
from multiprocessing.sharedctypes import Array, Value
from app.core.algorithm import ArraySizePy
from ctypes import c_double, c_bool, c_int

# Flag to control core process
should_terminate = Value(c_bool, False)

# Computing delay in core
sleep_time = Value(c_int, 0)

U0 = Value(c_double, 250.0)
shr_j = Array(c_double, ArraySizePy // 2) # max lenght can be сhange
shr_E = Array(c_double, ArraySizePy)
shr_ne = Array(c_double, ArraySizePy)
shr_p = Array(c_double, ArraySizePy)
shr_Gi = Array(c_double, ArraySizePy)
# -->
shared_data = (U0, shr_j, shr_E, shr_ne,
               shr_p, shr_Gi, sleep_time,
               should_terminate)
