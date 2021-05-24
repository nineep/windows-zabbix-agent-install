@echo off
"C:\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe" -i 0 --query-gpu=memory.total --format=csv,noheader,nounits>a0.txt
type a0.txt


