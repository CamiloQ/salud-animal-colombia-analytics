import urllib.request
import json
import uuid
import gzip
import pandas as pd

resource_key = '9ff26bf1-19f7-4998-856d-a37146e06753'
cluster_api = 'https://wabi-paas-1-scus-api.analysis.windows.net'

def execute_pbi_query(query_dict):
    req_id = str(uuid.uuid4())
    act_id = str(uuid.uuid4())
    url = f'{cluster_api}/public/reports/querydata?synchronous=true'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'ActivityId': act_id,
        'RequestId': req_id,
        'X-PowerBI-ResourceKey': resource_key,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Encoding': 'gzip, deflate'
    }
    payload = {
        'version': '1.0.0',
        'queries': [{'Query': query_dict, 'QueryId': '', 'ApplicationContext': {'DatasetId': '4819355', 'Sources': [{'ReportId': 'any'}]}}],
        'cancelQueries': [],
        'modelId': 4819355
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req) as resp:
        raw = resp.read()
        if resp.info().get('Content-Encoding') == 'gzip' or raw[:2] == b'\x1f\x8b':
            raw = gzip.decompress(raw)
        return json.loads(raw.decode('utf-8'))

def decode_pbi_result(ds0, col_names):
    vdicts = ds0.get('ValueDicts', {})
    ph = ds0.get('PH', [])
    if not ph or not ph[0].get('DM0'):
        return []
    dm0 = ph[0]['DM0']
    schema = dm0[0].get('S', [])
    dn_map = [s.get('DN') for s in schema]
    
    rows = []
    prev_row = [None] * len(col_names)
    for row_idx, item in enumerate(dm0):
        r_mask = item.get('R', 0)
        null_mask = item.get('Ø', 0)
        c_vals = item.get('C', [])
        c_idx = 0
        current_row = [None] * len(col_names)
        for col_i in range(len(col_names)):
            if (r_mask & (1 << col_i)) != 0:
                current_row[col_i] = prev_row[col_i]
            elif (null_mask & (1 << col_i)) != 0:
                current_row[col_i] = None
            else:
                if c_idx < len(c_vals):
                    val_raw = c_vals[c_idx]
                    c_idx += 1
                    dn = dn_map[col_i]
                    if dn and dn in vdicts and isinstance(val_raw, int):
                        if val_raw < len(vdicts[dn]):
                            val = vdicts[dn][val_raw]
                        else:
                            val = val_raw
                    else:
                        val = val_raw
                    current_row[col_i] = val
                else:
                    current_row[col_i] = None
        prev_row = current_row
        rows.append(current_row)
    return rows

target_nits = [
    '830033494', # HEEL COLOMBIA LTDA
    '900490865', # ZOETIS COLOMBIA SAS
    '860000753', # BOEHRINGER INGELHEIM SA
    '901186367', # ELANCO COLOMBIA S.A.S
    '860514325', # VIRBAC COLOMBIA LTDA
    '900524514', # CEVA SALUD ANIMAL SAS
    '800164767', # GABRICA SAS
    '811047208', # JARAMILLO PETS S.A.S.
    '860069284', # AGROCAMPO SAS
    '800221724', # SOMEX S.A.S.
    '860026895', # ITALCOL SA
    '891304762', # ITALCOL DE OCCIDENTE S.A.
    '890901271'  # CONTEGRAL S.A.S.
]

measures_list = [
    ('a. Ingresos', 'Ingresos'),
    ('b. Costos', 'Costos'),
    ('c. Utilidad bruta', 'UtilidadBruta'),
    ('d. Gastos de administración', 'GastosAdmon'),
    ('e. Gastos de ventas', 'GastosVentas'),
    ('j. Utilidad operativa', 'UtilidadOperativa'),
    ('l. EBITDA', 'EBITDA'),
    ('v. Utilidad neta', 'UtilidadNeta'),
    ('p. Total activos', 'TotalActivos'),
    ('w. Total pasivos', 'TotalPasivos'),
    ('zb. Total patrimonio', 'TotalPatrimonio')
]

select_clause = [
    {'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'NIT'}, 'Name': 'NIT'},
    {'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'Razón social de la sociedad'}, 'Name': 'RazonSocial'},
    {'Column': {'Expression': {'SourceRef': {'Source': 'd'}}, 'Property': 'Año'}, 'Name': 'Anio'}
]

for m_prop, m_name in measures_list:
    select_clause.append({'Measure': {'Expression': {'SourceRef': {'Source': 'm'}}, 'Property': m_prop}, 'Name': m_name})

cols_fin = ['NIT', 'RazonSocial', 'Anio'] + [m[1] for m in measures_list]

nit_filter_values = [[{'Literal': {'Value': f"'{nit}'"}}] for nit in target_nits]

q_fin = {
  'Commands': [
    {
      'SemanticQueryDataShapeCommand': {
        'Query': {
          'Version': 2,
          'From': [
            {'Name': 'c', 'Entity': 'Caratulas consolidado', 'Type': 0},
            {'Name': 'd', 'Entity': 'dim_Fechas', 'Type': 0},
            {'Name': 'm', 'Entity': 'Medidas', 'Type': 0}
          ],
          'Select': select_clause,
          'Where': [
            {
              'Condition': {
                'In': {
                  'Expressions': [
                    {'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'NIT'}}
                  ],
                  'Values': nit_filter_values
                }
              }
            }
          ]
        },
        'Binding': {
          'Primary': {'Groupings': [{'Projections': list(range(len(cols_fin)))}]},
          'DataReduction': {'DataVolume': 4, 'Primary': {'Window': {'Count': 2000}}},
          'Version': 1
        },
        'ExecutionMetricsKind': 1
      }
    }
  ]
}

res_fin = execute_pbi_query(q_fin)
ds0 = res_fin['results'][0]['result']['data']['dsr']['DS'][0]
fin_rows = decode_pbi_result(ds0, cols_fin)
print(f"Decoded {len(fin_rows)} annual financial records for expanded import/distribution firms!")

with open('financials_expanded_importers.json', 'w', encoding='utf-8') as f:
    json.dump([dict(zip(cols_fin, r)) for r in fin_rows], f, ensure_ascii=False, indent=2)

df = pd.DataFrame([dict(zip(cols_fin, r)) for r in fin_rows])
df['Ingresos_COP_M'] = pd.to_numeric(df['Ingresos'], errors='coerce')
df['EBITDA_COP_M'] = pd.to_numeric(df['EBITDA'], errors='coerce')
df['UtilidadNeta_COP_M'] = pd.to_numeric(df['UtilidadNeta'], errors='coerce')

pivot_rev = df.pivot_table(index=['NIT', 'RazonSocial'], columns='Anio', values='Ingresos_COP_M')
print("\n=== INGRESOS OPERACIONALES (COP $ MILLONES) ===")
print(pivot_rev.to_string())

