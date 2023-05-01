# Pacemaker_sim

## Background
The complications associated with 3rd degree AV nodal block include bradycardia and reduced ability to adapt heart rate when needed. While this condition is treatable with a pacemaker, contingent algorithms need to be in place for paroxysmal arrhythmias like tachycardia or fibrillation which may occur acutely, and which may exacerbate cardiac issues if the pacemaker does not accommodate for them. One algorithm for dealing with acute paroxysmal tachycardias is a mode-switching pacemaker. Under this paradigm, the pacemaker contains the algorithm for two separate pacing modes and can appropriately detect when to automatically switch between the modes. This project contains the simulation of a heart which is apt for a mode-switching pacemaker, and the development of the algorithm for a mode-switching pacemaker to correctly pace the heart. The simulated heart can acutely switch between normal sinus rhythm, atrial fibrillation, 3rd degree AV nodal block, and 3rd degree AV nodal block with atrial fibrillation. The two pacing modes chosen to address this malfunctioning heart include a VDD mode for pace-matching the ventricles to the atria, and a VVI mode for holding the ventricles at a constant rate when the atria are undergoing fibrillation. A concurrent live simulation and graphing program show the appropriate pacing of the ventricles when required, no pacing of the ventricles when not required, and appropriate mode-switching at the onset/offset of atrial fibrillation. 

## Installation
1. Install Python 3.11

2. Clone this repository 
```bash
git clone https://github.com/hershkovichl/Pacemaker_sim
```

3. Load dependencies 
```bash
pip install -r requirements.txt
```

## Running
To execute the program with plotting, run 
```bash
python ECG_tracing.py
```

## Additional Information
ECG_tracing.py contains all code for plotting the output of the heart and pacemaker simulations

heart_activity.py contains the Heart object, and its necessary Rhythm objects for defining SA node and AV node behavior

Pacemaker.py contains the code for a VVI pacemaker, VDD pacemaker, and a ModeSwitching pacemaker which automatically switches between the two. The HardwareSystem class handles the I/O that is universal to all 3 pacing modes.

VVI.cpp contains the original code for this project, which was the initial template for the VVI class in Pacemaker.py
