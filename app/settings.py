from pathlib import Path

# Global data
APP_NAME = "GunnEffectGUI"
VERSION = "1.2.0"

PROFILES_PATH = Path(__file__).parent / "profiles"
PROFILES_DICT = {pathFILE.name: str(pathFILE)
                 for pathFILE in PROFILES_PATH.iterdir()}

RESOURCES_PATH = Path(__file__).parent / "gui" / "resources"
RESOURCES_IMAG = RESOURCES_PATH / "img"
IMG_DICT = {pathIMG.name: str(pathIMG)
                 for pathIMG in RESOURCES_IMAG.iterdir()}

# Frequency for write to shared array
WRITE_FREQUENCY = 30

# For saving model data (all shared_data) current state.
# When SAVING_STATE_DATA == CNT (counter in core) -> saving current data
# If there is data, core runs with it
SAVING_STATE_DATA_CNT = 100_000

SAVING_DATA_PATH = Path().cwd() / "data" / "SAVING_STATE_DATA"
SAVING_DATA_PATH.mkdir(parents=True, exist_ok=True)

SAVING_DATA_DICT = {pathIMG.name: str(pathIMG)
                    for pathIMG in SAVING_DATA_PATH.iterdir()}

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

U_START = 250.0
U0 = Value(c_double, U_START)

# max lenght can be сhange
MAX_LENGHT_Jt = ArraySizePy // 2
shr_j = Array(c_double, MAX_LENGHT_Jt)

shr_E = Array(c_double, ArraySizePy)
shr_ne = Array(c_double, ArraySizePy)
shr_p = Array(c_double, ArraySizePy)
shr_Gi = Array(c_double, ArraySizePy)

# -->
shared_data = (U0, shr_j, shr_E, shr_ne,
               shr_p, shr_Gi, sleep_time,
               should_terminate)
