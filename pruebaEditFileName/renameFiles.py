import os
from pathlib import Path

carpeta = Path(r'C:\Users\HUAWEI\Desktop\pruebaEditFileName\files')
cont=1

for archivo in carpeta.iterdir():
    if archivo.suffix==".txt":
        nuevo_nombre=f'arhivo_{cont:04d}.txt'
        archivo.rename(carpeta / nuevo_nombre)
        cont+=1