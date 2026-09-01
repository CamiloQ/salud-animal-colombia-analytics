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

# Let's search companies by keywords across the entire Supersociedades database!
cols_search = [
    'NIT', 'RazonSocial', 'CIIU', 'ObjetoSocial', 'Ciudad', 'Tamano'
]

keywords = [
    'HEEL', 'ZOETIS', 'BOEHRINGER', 'INTERVET', 'ELANCO', 'VIRBAC', 'CEVA SALUD',
    'GABRICA', 'JARAMILLO PETS', 'AGROCAMPO', 'TIERRAGRO', 'SOMEX', 'ITALCOL', 'CONTEGRAL',
    'LAIKA UNIVERSE', 'PUPPIS'
]

all_found = []

for kw in keywords:
    q = {
      'Commands': [
        {
          'SemanticQueryDataShapeCommand': {
            'Query': {
              'Version': 2,
              'From': [{'Name': 'c', 'Entity': 'Caratulas consolidado', 'Type': 0}],
              'Select': [
                {'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'NIT'}, 'Name': 'NIT'},
                {'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'Razón social de la sociedad'}, 'Name': 'RazonSocial'},
                {'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'Clasificación Industrial Internacional Uniforme Versión 4 A.C (CIIU)'}, 'Name': 'CIIU'},
                {'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'Objeto social principal'}, 'Name': 'ObjetoSocial'},
                {'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'Ciudad de la dirección del domicilio'}, 'Name': 'Ciudad'},
                {'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'Tamaño Empresa'}, 'Name': 'Tamano'}
              ],
              'Where': [
                {
                  'Condition': {
                    'Contains': {
                      'Left': {'Column': {'Expression': {'SourceRef': {'Source': 'c'}}, 'Property': 'Razón social de la sociedad'}},
                      'Right': {'Literal': {'Value': f"'{kw}'"}}
                    }
                  }
                }
              ]
            },
            'Binding': {
              'Primary': {'Groupings': [{'Projections': list(range(len(cols_search)))}]},
              'DataReduction': {'DataVolume': 3, 'Primary': {'Window': {'Count': 200}}},
              'Version': 1
            },
            'ExecutionMetricsKind': 1
          }
        }
      ]
    }
    try:
        res = execute_pbi_query(q)
        ds0 = res['results'][0]['result']['data']['dsr']['DS'][0]
        rows = decode_pbi_result(ds0, cols_search)
        print(f"Keyword '{kw}': Found {len(rows)} matching companies.")
        for r in rows:
            print(f"  NIT: {r[0]} | {r[1]} | CIIU: {r[2][:30] if r[2] else 'N/A'} | {r[4]}")
            all_found.append(r)
    except Exception as e:
        print(f"Error searching {kw}: {e}")

df_all = pd.DataFrame(all_found, columns=cols_search).drop_duplicates(subset=['NIT'])
print(f"\nTotal unique expanded companies identified: {len(df_all)}")
df_all.to_csv('empresas_ampliadas_salud_animal_colombia.csv', index=False, encoding='utf-8-sig')

