@echo off
"C:\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe" -i 0 --query-gpu=memory.used --format=csv,noheader,nounits>b0.txt
type b0.txt

