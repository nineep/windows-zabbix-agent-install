@echo off
"C:\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe" -i 0 --query-gpu=utilization.gpu --format=csv,noheader,nounits>c0.txt
type c0.txt

