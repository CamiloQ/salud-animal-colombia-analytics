import pandas as pd
import json

# 1. Load domestic pharma labs (CIIU 2100)
df_c2100 = pd.read_csv('directorio_laboratorios_veterinarios_ciiu_2100.csv')
df_c2100['NIT'] = df_c2100['NIT'].astype(str)
df_c2100['Subtipo'] = df_c2100['Categoria'].apply(lambda x: 'FABRICANTE_NACIONAL_VET' if x == 'VETERINARIO_ESPECIALIZADO' else 'FABRICANTE_NACIONAL_MIXTO')

# 2. Load expanded importers and distributors
with open('financials_expanded_importers.json') as f:
    fin_exp = json.load(f)

df_fin_exp = pd.DataFrame(fin_exp)
df_fin_exp['NIT'] = df_fin_exp['NIT'].astype(str)

df_meta_exp = pd.read_csv('empresas_ampliadas_salud_animal_colombia.csv')
df_meta_exp['NIT'] = df_meta_exp['NIT'].astype(str)

# Merge metadata with financials
df_exp_merged = df_fin_exp.merge(df_meta_exp[['NIT', 'CIIU', 'Ciudad', 'Tamano']], on='NIT', how='left')

# Categorize expanded companies
def categorize_expanded(row):
    nit = str(row['NIT'])
    if nit in ['830033494', '900490865', '860000753', '901186367', '860514325', '900524514']:
        return 'IMPORTADOR_MULTINACIONAL'
    elif nit in ['800164767', '811047208', '860069284']:
        return 'DISTRIBUIDOR_MAYORISTA_PET'
    elif nit in ['800221724']:
        return 'NUTRICION_SALES_GANADERAS'
    elif nit in ['860026895', '891304762', '890901271']:
        return 'NUTRICION_BALANCEADOS_GIGANTE'
    else:
        return 'OTRO_COMERCIAL'

df_exp_merged['Subtipo'] = df_exp_merged.apply(categorize_expanded, axis=1)
df_exp_merged.to_csv('estados_financieros_consolidados_importadores_distribuidores.csv', index=False, encoding='utf-8-sig')

# Create pivot of all top players (2020-2024)
years = [2020, 2021, 2022, 2023, 2024]
for c in ['Ingresos', 'Costos', 'UtilidadBruta', 'UtilidadOperativa', 'EBITDA', 'UtilidadNeta', 'TotalActivos', 'TotalPatrimonio']:
    df_exp_merged[c] = pd.to_numeric(df_exp_merged[c], errors='coerce')

pivot_exp = df_exp_merged.pivot_table(index=['NIT', 'RazonSocial', 'Subtipo', 'Ciudad', 'Tamano'], columns='Anio', values='Ingresos', aggfunc='first').reset_index()

for y in years:
    if y not in pivot_exp.columns:
        pivot_exp[y] = 0.0

pivot_exp['Total_5Y_20_24'] = pivot_exp[years].sum(axis=1)
pivot_exp = pivot_exp.sort_values(by='Total_5Y_20_24', ascending=False)

pivot_exp.to_csv('ranking_consolidado_importadores_distribuidores.csv', index=False, encoding='utf-8-sig')
print("Successfully generated master consolidated datasets!")
print("\n=== RANKING DE VENTAS 5 AÑOS (2020-2024) IMPORTADORES Y DISTRIBUIDORES (COP $ MILLONES) ===")
cols_p = ['NIT', 'RazonSocial', 'Subtipo', 'Ciudad', 2020, 2021, 2022, 2023, 2024, 'Total_5Y_20_24']
print(pivot_exp[cols_p].to_string())

