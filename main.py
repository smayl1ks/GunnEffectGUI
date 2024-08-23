#----------------------------------------------------------------------------
#Author : Roman Shchiptsov, email: schiptsov.roman@gmail.com
#File   : main.py
#Revise : 17-07-2024
#----------------------------------------------------------------------------

# To run the GUI and core in different processes
from multiprocessing import Process

# This file includes all settings to run program
from app.settings import *

# Console mode (not created)
# imoirt argparse
# argparse.ArgumentParser() --no-gui

if __name__ == '__main__':
    gui = Process(target=run_gui, args=shared_data)
    core = Process(target=run_core, args=shared_data)

    gui.start(); core.start()
    gui.join() ;core.join()