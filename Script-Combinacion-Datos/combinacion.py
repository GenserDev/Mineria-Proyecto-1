import pandas as pd
import pyreadstat
import os
from pathlib import Path

# Rutas
datos_dir = Path(__file__).parent.parent / "Datos"
output_file = Path(__file__).parent.parent / "datos_combinados.csv"
dataframes = []

# Leer archivos 
archivos_sav = sorted(datos_dir.glob("*.sav"))

print(f"Se encontraron {len(archivos_sav)} archivos .sav")
print("Leyendo archivos...")

for archivo_sav in archivos_sav:
    try:
        df, meta = pyreadstat.read_sav(str(archivo_sav))        
        df['año del dato'] = archivo_sav.stem
        
        dataframes.append(df)
        print(f"✓ {archivo_sav.name} ({len(df)} registros)")
        
    except Exception as e:
        print(f"✗ Error al leer {archivo_sav.name}: {e}")

# Combinar todos los dataframes
if dataframes:
    df_combinado = pd.concat(dataframes, ignore_index=True)
    
    # Guardar como CSV
    df_combinado.to_csv(output_file, index=False, encoding='utf-8')
    
    print("\n" + "="*50)
    print(f"Archivo generado: {output_file}")
    print(f"Total de registros: {len(df_combinado)}")
    print(f"Total de columnas: {len(df_combinado.columns)}")
    print(f"Columna 'año del dato' agregada: ✓")
    print("="*50)
else:
    print("No se encontraron archivos .sav para procesar")
