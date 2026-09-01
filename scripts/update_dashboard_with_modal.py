import pandas as pd
import json
import os

# 1. Load Master ICA Dataset (8,129 active records)
df_ica = pd.read_csv('ica_medicamentos_vigentes_agosto_2026.csv')
print(f"Master ICA Dataset loaded: {len(df_ica)} records")

# Standardize column values
df_ica['Titular'] = df_ica['Titular'].astype(str).str.strip().str.upper()
df_ica['Tipo_Medicamento'] = df_ica['Tipo_Medicamento'].astype(str).str.strip()
df_ica['Pais_Origen'] = df_ica['Pais_Origen'].astype(str).str.strip().str.upper()
df_ica['Origen_Clasif'] = df_ica['Origen_Clasif'].astype(str).str.strip()
df_ica['Especies'] = df_ica['Especies'].astype(str).str.strip()

# Fill NaN with empty string
df_ica = df_ica.fillna('')

total_regs = len(df_ica)
total_titulares = df_ica['Titular'].nunique()
nacionales = len(df_ica[df_ica['Origen_Clasif'].str.contains('COLOMBIA')])
importados = len(df_ica[df_ica['Origen_Clasif'].str.contains('EXTRANJERO')])

# Top 15 Types of Medicines
tipo_med_counts = df_ica['Tipo_Medicamento'].value_counts().head(12).to_dict()

# Top 10 Countries of Origin
paises_importados = df_ica[df_ica['Origen_Clasif'].str.contains('EXTRANJERO')]['Pais_Origen'].value_counts().head(10).to_dict()

# Top 20 Titulares
top_titulares = df_ica['Titular'].value_counts().head(20).to_dict()

# Target Species Breakdown
species_counts = {
    'Bovinos': len(df_ica[df_ica['Especies'].str.contains('BOVIN|GANAD', case=False, na=False)]),
    'Caninos (Perros)': len(df_ica[df_ica['Especies'].str.contains('CANIN|PERR', case=False, na=False)]),
    'Felinos (Gatos)': len(df_ica[df_ica['Especies'].str.contains('FELIN|GAT', case=False, na=False)]),
    'Equinos (Caballos)': len(df_ica[df_ica['Especies'].str.contains('EQUIN|CABALL', case=False, na=False)]),
    'Porcinos (Cerdos)': len(df_ica[df_ica['Especies'].str.contains('PORCIN|CERD', case=False, na=False)]),
    'Aves (Avicultura)': len(df_ica[df_ica['Especies'].str.contains('AVE|POLL|GALLIN', case=False, na=False)]),
    'Peces / Acuicultura': len(df_ica[df_ica['Especies'].str.contains('PEZ|PECES|TILAPIA|TRUCHA|ACUIC', case=False, na=False)])
}

# Load Financials Ranking
df_rank_imp = pd.read_csv('ranking_consolidado_importadores_distribuidores.csv')
rank_imp_records = df_rank_imp[['NIT', 'RazonSocial', 'Subtipo', 'Ciudad', 'Total_5Y_20_24']].head(15).fillna(0).to_dict(orient='records')

df_rank_fab = pd.read_csv('directorio_laboratorios_veterinarios_ciiu_2100.csv')
df_rank_fab['Total_5Y_20_24'] = df_rank_fab[['Ingresos_COP_M_2020', 'Ingresos_COP_M_2021', 'Ingresos_COP_M_2022', 'Ingresos_COP_M_2023', 'Ingresos_COP_M_2024']].sum(axis=1)
rank_fab_records = df_rank_fab[['NIT', 'RazonSocial', 'Categoria', 'Ciudad', 'Total_5Y_20_24']].sort_values(by='Total_5Y_20_24', ascending=False).head(15).fillna(0).to_dict(orient='records')

# Full structured records with all detailed fields for fact sheet modal
cols_all = [
    'Reg_ICA', 'Titular', 'Estado', 'Producto', 'Activos', 'Cantidades',
    'Indicaciones', 'Precauciones', 'Laboratorio_Productor', 'Pais_Origen',
    'Importador', 'Empaques', 'Especies', 'Tiempo_Retiro', 'Tipo_Medicamento', 'Origen_Clasif'
]

records_table = df_ica[cols_all].to_dict(orient='records')

dashboard_payload = {
    'summary': {
        'total_registros_vigentes': total_regs,
        'total_titulares_unicos': total_titulares,
        'fabricados_colombia': nacionales,
        'importados_extranjero': importados,
        'porc_nacional': round((nacionales / total_regs) * 100, 1),
        'porc_importado': round((importados / total_regs) * 100, 1),
        'dane_produccion_fabril_cop_b': 11.15,
        'dane_valor_agregado_cop_b': 7.42,
        'dane_empleo_directo': 31556,
        'dane_ventas_veterinarias_cpc_cop_b': 1.18,
        'dane_exportaciones_veterinarias_cop_b': 0.17
    },
    'charts': {
        'tipo_medicamento': tipo_med_counts,
        'paises_importados': paises_importados,
        'top_titulares': top_titulares,
        'species_breakdown': species_counts,
        'top_fabricantes_finanzas': rank_fab_records,
        'top_importadores_finanzas': rank_imp_records
    },
    'products': records_table
}

with open('dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_payload, f, ensure_ascii=False)

print(f"Generated complete dashboard_data.json with full fact sheet details ({os.path.getsize('dashboard_data.json') / 1024:.1f} KB)")

