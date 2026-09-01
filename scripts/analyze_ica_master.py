import pandas as pd
import json

excel_path = "/run/media/camilo-q/DATA/USER/1.CQ_PC/1.Personal/1.CQ_dev/1.Zam_Cof/Base-de-datos-Medicamentos-y-Biologicos-agosto-3-de-2026.xlsx"

df = pd.read_excel(excel_path, skiprows=1)

# Inspect column names
cols = [
    'Reg_ICA', 'Titular', 'Estado', 'Producto', 'Activos', 'Cantidades',
    'Indicaciones', 'Precauciones', 'Laboratorio_Productor', 'Pais_Origen',
    'Importador', 'Empaques', 'Especies', 'Tiempo_Retiro', 'Tipo_Medicamento'
]
df.columns = cols[:len(df.columns)]

print(f"Total registros cargados en base de datos ICA: {len(df)}")

# Filter only VIGENTE
df['Estado_Clean'] = df['Estado'].astype(str).str.strip().str.upper()
df_vigente = df[df['Estado_Clean'] == 'VIGENTE'].copy()
print(f"Total Productos con Registro ICA VIGENTE: {len(df_vigente)}")

# 1. Distribución por País de Origen (Fabricado Nacional vs Importado)
def get_origin(val):
    val_str = str(val).strip().upper()
    if val_str in ['NAN', 'NONE', '', 'S.I.', 'SIN INFORMACIÓN']:
        return 'NO ESPECIFICADO'
    elif 'COLOMBIA' in val_str:
        return 'COLOMBIA (Fabricado Nacional)'
    else:
        return 'EXTRANJERO (Importado)'

df_vigente['Origen_Clasif'] = df_vigente['Pais_Origen'].apply(get_origin)

print("\n=== ORIGEN DE LOS PRODUCTOS VIGENTES (Fabricado vs Importado) ===")
print(df_vigente['Origen_Clasif'].value_counts())

print("\n=== TOP 10 PAÍSES DE ORIGEN DE PRODUCTOS IMPORTADOS ===")
df_imp = df_vigente[df_vigente['Origen_Clasif'] == 'EXTRANJERO (Importado)'].copy()
df_imp['Pais_Clean'] = df_imp['Pais_Origen'].astype(str).str.strip().str.upper()
print(df_imp['Pais_Clean'].value_counts().head(10))

# 2. Distribución por Tipo de Medicamento ICA
print("\n=== DISTRIBUCIÓN POR TIPO DE MEDICAMENTO ICA ===")
print(df_vigente['Tipo_Medicamento'].astype(str).str.strip().value_counts().head(15))

# 3. Top Titulares de Registros Sanitarios Vigentes
print("\n=== TOP 20 EMPRESAS CON MAYOR NÚMERO DE REGISTROS VIGENTES ===")
print(df_vigente['Titular'].astype(str).str.strip().value_counts().head(20))

# 4. Búsqueda específica de HEEL en la base oficial ICA
print("\n=== REGISTROS DE HEEL COLOMBIA EN BASE OFICIAL ICA ===")
heel_mask = df_vigente.astype(str).apply(lambda row: row.str.contains('HEEL|TRAUMEEL|ZEEL|ENGYSTOL|SPASCUPREEL|HOMOTOXICOLOG', case=False).any(), axis=1)
df_heel = df_vigente[heel_mask]
print(f"Total productos de Heel / Biorreguladora encontrados: {len(df_heel)}")
print(df_heel[['Reg_ICA', 'Titular', 'Producto', 'Pais_Origen', 'Tipo_Medicamento']].to_string())

# Export clean files
df_vigente.to_csv('ica_medicamentos_vigentes_agosto_2026.csv', index=False, encoding='utf-8-sig')
df_heel.to_csv('ica_registros_heel_colombia.csv', index=False, encoding='utf-8-sig')
print("\nExported ica_medicamentos_vigentes_agosto_2026.csv and ica_registros_heel_colombia.csv")

