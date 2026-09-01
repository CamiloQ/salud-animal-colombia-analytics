import json

with open('dashboard_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Analítica: Salud Animal y Medicamentos Veterinarios en Colombia</title>
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>
<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: #f1f5f9;
    color: #0f172a;
  }}
  .card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }}
  .chart-container {{
    position: relative;
    height: 280px;
    width: 100%;
  }}
  /* Modal styling */
  .modal-overlay {{
    background-color: rgba(15, 23, 42, 0.75);
    backdrop-filter: blur(2px);
  }}
  /* Custom scrollbar */
  ::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
  }}
  ::-webkit-scrollbar-track {{
    background: #f1f5f9;
  }}
  ::-webkit-scrollbar-thumb {{
    background: #cbd5e1;
    border-radius: 3px;
  }}
  ::-webkit-scrollbar-thumb:hover {{
    background: #94a3b8;
  }}
  @media print {{
    body * {{
      visibility: hidden;
    }}
    #product-modal, #modal-content-printable, #modal-content-printable * {{
      visibility: visible;
    }}
    #modal-content-printable {{
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
      box-shadow: none;
      border: none;
    }}
    .no-print {{
      display: none !important;
    }}
  }}
</style>
</head>
<body class="p-4 md:p-6">

  <!-- Top Header -->
  <header class="mb-6 bg-slate-900 text-white p-5 rounded-lg shadow-md flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
    <div>
      <div class="flex items-center gap-3">
        <span class="bg-blue-600 text-xs font-semibold px-2.5 py-1 rounded tracking-wider uppercase">ICA / DANE / Supersociedades</span>
        <span class="text-xs text-slate-400">Actualización: Agosto 2026</span>
      </div>
      <h1 class="text-xl md:text-2xl font-bold mt-1 tracking-tight">Dashboard de Inteligencia de Mercado: Salud Animal y Fármacos Veterinarios</h1>
      <p class="text-xs md:text-sm text-slate-300 mt-0.5">Consolidación de 8.129 Registros Sanitarios ICA Vigentes, Balances Financieros y Encuesta Anual Manufacturera DANE</p>
    </div>
    <div class="flex items-center gap-2">
      <button onclick="resetFilters()" class="bg-slate-700 hover:bg-slate-600 text-xs font-medium px-3 py-2 rounded transition">Restablecer Filtros</button>
      <button onclick="exportFilteredCSV()" class="bg-blue-600 hover:bg-blue-500 text-xs font-medium px-3 py-2 rounded transition">Descargar CSV Filtrado</button>
    </div>
  </header>

  <!-- KPI Cards -->
  <section class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
    <div class="card p-4 border-l-4 border-blue-600">
      <span class="text-xs text-slate-500 font-semibold uppercase tracking-wider">Registros ICA Vigentes</span>
      <div class="text-2xl font-bold text-slate-900 mt-1" id="kpi-total-regs">{data['summary']['total_registros_vigentes']:,}</div>
      <span class="text-[11px] text-slate-400">Base oficial ICA 2026</span>
    </div>
    <div class="card p-4 border-l-4 border-emerald-600">
      <span class="text-xs text-slate-500 font-semibold uppercase tracking-wider">Fabricación Nacional</span>
      <div class="text-2xl font-bold text-emerald-700 mt-1" id="kpi-nacionales">{data['summary']['fabricados_colombia']:,}</div>
      <span class="text-[11px] text-emerald-600 font-medium">{data['summary']['porc_nacional']}% del portafolio</span>
    </div>
    <div class="card p-4 border-l-4 border-amber-600">
      <span class="text-xs text-slate-500 font-semibold uppercase tracking-wider">Productos Importados</span>
      <div class="text-2xl font-bold text-amber-700 mt-1" id="kpi-importados">{data['summary']['importados_extranjero']:,}</div>
      <span class="text-[11px] text-amber-600 font-medium">{data['summary']['porc_importado']}% del portafolio</span>
    </div>
    <div class="card p-4 border-l-4 border-indigo-600">
      <span class="text-xs text-slate-500 font-semibold uppercase tracking-wider">Empresas Titulares</span>
      <div class="text-2xl font-bold text-indigo-700 mt-1" id="kpi-titulares">{data['summary']['total_titulares_unicos']:,}</div>
      <span class="text-[11px] text-slate-400">Titulares únicos de registro</span>
    </div>
    <div class="card p-4 border-l-4 border-cyan-600">
      <span class="text-xs text-slate-500 font-semibold uppercase tracking-wider">Ventas DANE (Salud Vet.)</span>
      <div class="text-2xl font-bold text-cyan-800 mt-1">${data['summary']['dane_ventas_veterinarias_cpc_cop_b']} B</div>
      <span class="text-[11px] text-cyan-600 font-medium">Exportaciones: ${data['summary']['dane_exportaciones_veterinarias_cop_b']} B</span>
    </div>
    <div class="card p-4 border-l-4 border-purple-600">
      <span class="text-xs text-slate-500 font-semibold uppercase tracking-wider">Producción Fabril CIIU 2100</span>
      <div class="text-2xl font-bold text-purple-800 mt-1">${data['summary']['dane_produccion_fabril_cop_b']} B</div>
      <span class="text-[11px] text-slate-400">31.556 Empleos DANE</span>
    </div>
  </section>

  <!-- Filter Controls Section -->
  <section class="card p-4 mb-6">
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-xs font-bold text-slate-700 uppercase tracking-wider">Filtros y Segmentación de Datos</h2>
      <span class="text-xs text-slate-500" id="filtered-count-label">Mostrando {len(data['products']):,} registros</span>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
      <div>
        <label class="block text-[11px] font-semibold text-slate-600 mb-1 uppercase">Buscar Producto / Activo / Registro</label>
        <input type="text" id="filter-search" oninput="applyFilters()" placeholder="Ej: Traumeel, Ivermectina, 8412-MV..." class="w-full px-3 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500">
      </div>
      <div>
        <label class="block text-[11px] font-semibold text-slate-600 mb-1 uppercase">Tipo de Medicamento</label>
        <select id="filter-tipo" onchange="applyFilters()" class="w-full px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500">
          <option value="">Todos los Tipos</option>
        </select>
      </div>
      <div>
        <label class="block text-[11px] font-semibold text-slate-600 mb-1 uppercase">Origen (Nacional / Importado)</label>
        <select id="filter-origen" onchange="applyFilters()" class="w-full px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500">
          <option value="">Todos los Orígenes</option>
          <option value="COLOMBIA">Fabricado en Colombia</option>
          <option value="EXTRANJERO">Importado del Extranjero</option>
        </select>
      </div>
      <div>
        <label class="block text-[11px] font-semibold text-slate-600 mb-1 uppercase">País de Origen</label>
        <select id="filter-pais" onchange="applyFilters()" class="w-full px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500">
          <option value="">Todos los Países</option>
        </select>
      </div>
      <div>
        <label class="block text-[11px] font-semibold text-slate-600 mb-1 uppercase">Especie de Destino</label>
        <select id="filter-especie" onchange="applyFilters()" class="w-full px-2.5 py-1.5 text-xs bg-slate-50 border border-slate-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500">
          <option value="">Todas las Especies</option>
          <option value="BOVIN">Bovinos</option>
          <option value="CANIN">Caninos (Perros)</option>
          <option value="FELIN">Felinos (Gatos)</option>
          <option value="EQUIN">Equinos (Caballos)</option>
          <option value="PORCIN">Porcinos (Cerdos)</option>
          <option value="AVE">Aves (Avicultura)</option>
          <option value="PEZ">Peces / Acuicultura</option>
        </select>
      </div>
    </div>
  </section>

  <!-- Charts Grid (Row 1) -->
  <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
    <div class="card p-4">
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Distribución por Tipo de Medicamento ICA</h3>
        <span class="text-[11px] text-slate-400">Cantidad de productos</span>
      </div>
      <div class="chart-container">
        <canvas id="chartTipoMed"></canvas>
      </div>
    </div>

    <div class="card p-4">
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Top Países de Origen de Medicamentos Importados</h3>
        <span class="text-[11px] text-slate-400">Registros vigentes</span>
      </div>
      <div class="chart-container">
        <canvas id="chartPaises"></canvas>
      </div>
    </div>
  </section>

  <!-- Charts Grid (Row 2) -->
  <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
    <div class="card p-4">
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Top 15 Titulares con Mayor Número de Registros ICA</h3>
        <span class="text-[11px] text-slate-400">Portafolio autorizado</span>
      </div>
      <div class="chart-container">
        <canvas id="chartTitulares"></canvas>
      </div>
    </div>

    <div class="card p-4">
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Distribución por Especies de Destino</h3>
        <span class="text-[11px] text-slate-400">Menciones en registro sanitario</span>
      </div>
      <div class="chart-container">
        <canvas id="chartEspecies"></canvas>
      </div>
    </div>
  </section>

  <!-- Financial Intelligence Section (Row 3) -->
  <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
    <div class="card p-4">
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Ventas Acumuladas 5 Años: Top Fabricantes Nacionales (CIIU 2100)</h3>
        <span class="text-[11px] text-slate-400">Cifras en COP $ Millones (2020-2024)</span>
      </div>
      <div class="chart-container">
        <canvas id="chartFinFab"></canvas>
      </div>
    </div>

    <div class="card p-4">
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Ventas Acumuladas 5 Años: Top Importadores y Distribuidores</h3>
        <span class="text-[11px] text-slate-400">Cifras en COP $ Millones (2020-2024)</span>
      </div>
      <div class="chart-container">
        <canvas id="chartFinImp"></canvas>
      </div>
    </div>
  </section>

  <!-- Master Data Table Explorer -->
  <section class="card p-4">
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 mb-3">
      <div>
        <h3 class="text-sm font-bold text-slate-900 tracking-tight">Explorador de Registros Sanitarios Oficiales del ICA</h3>
        <p class="text-xs text-slate-500">Haga clic en cualquier fila o en el botón "Ver Ficha" para abrir el detalle técnico completo del registro sanitario</p>
      </div>
      <div class="flex items-center gap-3 text-xs">
        <label>Mostrar: 
          <select id="page-size" onchange="changePageSize()" class="bg-slate-50 border border-slate-300 rounded px-2 py-1">
            <option value="15">15</option>
            <option value="25" selected>25</option>
            <option value="50">50</option>
            <option value="100">100</option>
          </select>
        </label>
        <span id="page-info" class="text-slate-600 font-medium">Página 1 de 1</span>
      </div>
    </div>

    <!-- Table Container -->
    <div class="overflow-x-auto border border-slate-200 rounded">
      <table class="w-full text-left text-xs">
        <thead class="bg-slate-100 text-slate-700 font-semibold border-b border-slate-200 uppercase text-[10px] tracking-wider">
          <tr>
            <th class="p-2.5">Acción</th>
            <th class="p-2.5">Reg. ICA</th>
            <th class="p-2.5">Nombre del Producto</th>
            <th class="p-2.5">Titular del Registro</th>
            <th class="p-2.5">Activos / Composición</th>
            <th class="p-2.5">Tipo Medicamento</th>
            <th class="p-2.5">País Origen</th>
            <th class="p-2.5">Origen</th>
            <th class="p-2.5">Especies</th>
          </tr>
        </thead>
        <tbody id="table-body" class="divide-y divide-slate-100 text-slate-800">
          <!-- Dynamically populated -->
        </tbody>
      </table>
    </div>

    <!-- Pagination Controls -->
    <div class="flex justify-between items-center mt-3 text-xs">
      <button onclick="prevPage()" id="btn-prev" class="bg-slate-100 hover:bg-slate-200 border border-slate-300 px-3 py-1.5 rounded transition disabled:opacity-40 disabled:cursor-not-allowed">Anterior</button>
      <div class="flex gap-1" id="pagination-numbers"></div>
      <button onclick="nextPage()" id="btn-next" class="bg-slate-100 hover:bg-slate-200 border border-slate-300 px-3 py-1.5 rounded transition disabled:opacity-40 disabled:cursor-not-allowed">Siguiente</button>
    </div>
  </section>

  <!-- MODAL: FICHA TÉCNICA DETALLADA DEL REGISTRO SANITARIO ICA -->
  <div id="product-modal" class="fixed inset-0 z-50 flex items-center justify-center p-4 modal-overlay hidden">
    <div id="modal-content-printable" class="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden border border-slate-300">
      
      <!-- Modal Header -->
      <div class="bg-slate-900 text-white p-4 sm:p-5 flex justify-between items-start border-b border-slate-800">
        <div>
          <div class="flex flex-wrap items-center gap-2 mb-1">
            <span id="modal-reg-badge" class="bg-blue-600 text-white text-[11px] font-bold px-2.5 py-0.5 rounded tracking-wide">REG. ICA: 8412-MV</span>
            <span id="modal-estado-badge" class="bg-emerald-600 text-white text-[11px] font-semibold px-2 py-0.5 rounded uppercase">VIGENTE</span>
            <span id="modal-origen-badge" class="bg-amber-500 text-slate-900 text-[11px] font-semibold px-2 py-0.5 rounded uppercase">IMPORTADO (ALEMANIA)</span>
            <span id="modal-tipo-badge" class="bg-slate-700 text-slate-200 text-[11px] font-medium px-2 py-0.5 rounded">BIOLÓGICOS</span>
          </div>
          <h2 id="modal-producto-title" class="text-lg sm:text-xl font-bold text-white tracking-tight mt-1">TRAUMEEL LT AD US. VET.</h2>
          <p id="modal-titular-subtitle" class="text-xs sm:text-sm text-slate-300 mt-0.5">HEEL COLOMBIA LTDA.</p>
        </div>
        <button onclick="closeModal()" class="text-slate-400 hover:text-white p-1 rounded-lg text-2xl font-bold transition no-print">&times;</button>
      </div>

      <!-- Modal Body (Scrollable Content) -->
      <div class="p-5 overflow-y-auto space-y-5 text-xs text-slate-700">
        
        <!-- Section 1: Resumen Regulatorio e Industrial -->
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 bg-slate-50 p-4 rounded-lg border border-slate-200">
          <div>
            <span class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider">Empresa Titular</span>
            <span id="modal-titular" class="font-semibold text-slate-900 text-xs">HEEL COLOMBIA LTDA.</span>
          </div>
          <div>
            <span class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider">Laboratorio Productor</span>
            <span id="modal-productor" class="font-medium text-slate-800 text-xs">BIOLOGISCHE HEILMITTEL HEEL GMBH</span>
          </div>
          <div>
            <span class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider">País de Origen</span>
            <span id="modal-pais" class="font-medium text-slate-800 text-xs">ALEMANIA</span>
          </div>
          <div>
            <span class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider">Empresa Importadora</span>
            <span id="modal-importador" class="font-medium text-slate-800 text-xs">HEEL COLOMBIA LTDA.</span>
          </div>
          <div>
            <span class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider">Categoría / Tipo ICA</span>
            <span id="modal-tipo" class="font-medium text-slate-800 text-xs">Biológicos / Biorregulador</span>
          </div>
          <div>
            <span class="block text-[10px] font-bold text-slate-500 uppercase tracking-wider">Tiempo de Retiro</span>
            <span id="modal-retiro" class="font-medium text-slate-800 text-xs">0 días (No reporta)</span>
          </div>
        </div>

        <!-- Section 2: Formulación y Principios Activos -->
        <div class="border border-slate-200 rounded-lg p-4 bg-white shadow-sm">
          <h4 class="text-xs font-bold text-slate-900 uppercase tracking-wider mb-2 text-blue-900 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-blue-600"></span>
            Composición y Concentración Garantizada
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
            <div class="bg-slate-50 p-3 rounded border border-slate-100">
              <span class="block text-[10px] font-bold text-slate-500 uppercase mb-1">Principios Activos / Fórmulas</span>
              <p id="modal-activos" class="text-slate-800 text-xs leading-relaxed whitespace-pre-line">Arnica montana, Calendula officinalis, Hamamelis virginiana...</p>
            </div>
            <div class="bg-slate-50 p-3 rounded border border-slate-100">
              <span class="block text-[10px] font-bold text-slate-500 uppercase mb-1">Cantidades / Concentraciones</span>
              <p id="modal-cantidades" class="text-slate-800 text-xs leading-relaxed whitespace-pre-line">D2, D4, D6 según farmacopea homeopática oficial...</p>
            </div>
          </div>
        </div>

        <!-- Section 3: Indicaciones de Uso y Especies Autorizadas -->
        <div class="border border-slate-200 rounded-lg p-4 bg-white shadow-sm">
          <h4 class="text-xs font-bold text-slate-900 uppercase tracking-wider mb-2 text-emerald-900 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-600"></span>
            Uso Terapéutico y Especies de Destino
          </h4>
          <div class="space-y-3 mt-2">
            <div class="bg-emerald-50/50 p-3 rounded border border-emerald-100">
              <span class="block text-[10px] font-bold text-emerald-800 uppercase mb-1">Indicaciones Clínicas Aprobadas por el ICA</span>
              <p id="modal-indicaciones" class="text-slate-800 text-xs leading-relaxed">Tratamiento de traumatismos, contusiones, procesos inflamatorios agudos y crónicos del aparato locomotor...</p>
            </div>
            <div class="bg-slate-50 p-3 rounded border border-slate-100">
              <span class="block text-[10px] font-bold text-slate-500 uppercase mb-1">Especies de Destino Autorizadas</span>
              <p id="modal-especies" class="text-slate-800 font-semibold text-xs">Bovinos, Equinos, Caninos, Felinos, Porcinos</p>
            </div>
          </div>
        </div>

        <!-- Section 4: Precauciones y Presentaciones Comerciales -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="border border-slate-200 rounded-lg p-4 bg-white shadow-sm">
            <h4 class="text-xs font-bold text-slate-900 uppercase tracking-wider mb-2 text-amber-900 flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-amber-600"></span>
              Precauciones y Advertencias
            </h4>
            <p id="modal-precauciones" class="text-slate-700 text-xs leading-relaxed bg-amber-50/40 p-3 rounded border border-amber-100">Almacenar en lugar fresco a temperatura inferior a 30°C. Manténgase fuera del alcance de los niños.</p>
          </div>

          <div class="border border-slate-200 rounded-lg p-4 bg-white shadow-sm">
            <h4 class="text-xs font-bold text-slate-900 uppercase tracking-wider mb-2 text-slate-900 flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-slate-600"></span>
              Envases y Presentaciones Aprobadas
            </h4>
            <p id="modal-empaques" class="text-slate-700 text-xs leading-relaxed bg-slate-50 p-3 rounded border border-slate-100">Cajas por 5, 50 y 100 ampollas de 5 ml en vidrio tipo I.</p>
          </div>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="bg-slate-100 p-4 border-t border-slate-200 flex flex-wrap justify-between items-center gap-3 no-print">
        <div class="flex items-center gap-2">
          <button onclick="copyRegIca()" class="bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 font-medium px-3 py-1.5 rounded text-xs transition flex items-center gap-1">
            <span>Copiar Reg. ICA</span>
          </button>
          <button onclick="window.print()" class="bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 font-medium px-3 py-1.5 rounded text-xs transition flex items-center gap-1">
            <span>Imprimir Ficha</span>
          </button>
        </div>
        <button onclick="closeModal()" class="bg-slate-800 hover:bg-slate-700 text-white font-medium px-4 py-1.5 rounded text-xs transition">Cerrar Ficha</button>
      </div>

    </div>
  </div>

  <!-- Script Logic -->
  <script>
    const rawData = {json.dumps(data, ensure_ascii=False)};
    let allProducts = rawData.products;
    let filteredProducts = [...allProducts];

    let currentPage = 1;
    let pageSize = 25;
    let selectedProduct = null;

    // Charts references
    let chartTipoMed, chartPaises, chartTitulares, chartEspecies, chartFinFab, chartFinImp;

    // Init function
    window.onload = function() {{
      populateDropdowns();
      initCharts();
      applyFilters();
      
      // Close modal on Escape key
      document.addEventListener('keydown', function(event) {{
        if (event.key === 'Escape') {{
          closeModal();
        }}
      }});
    }};

    function populateDropdowns() {{
      // Populate Tipo Medicamento
      const tipoSelect = document.getElementById('filter-tipo');
      const tipos = [...new Set(allProducts.map(p => p.Tipo_Medicamento).filter(Boolean))].sort();
      tipos.forEach(t => {{
        const opt = document.createElement('option');
        opt.value = t;
        opt.textContent = t;
        tipoSelect.appendChild(opt);
      }});

      // Populate Pais
      const paisSelect = document.getElementById('filter-pais');
      const paises = [...new Set(allProducts.map(p => p.Pais_Origen).filter(p => p && p !== 'NAN' && p !== 'NO INFORMA.'))].sort();
      paises.forEach(p => {{
        const opt = document.createElement('option');
        opt.value = p;
        opt.textContent = p;
        paisSelect.appendChild(opt);
      }});
    }}

    function initCharts() {{
      // 1. Tipo Medicamento Chart
      const ctxTipo = document.getElementById('chartTipoMed').getContext('2d');
      const tipoLabels = Object.keys(rawData.charts.tipo_medicamento);
      const tipoValues = Object.values(rawData.charts.tipo_medicamento);
      chartTipoMed = new Chart(ctxTipo, {{
        type: 'bar',
        data: {{
          labels: tipoLabels,
          datasets: [{{
            label: 'Productos Registrados',
            data: tipoValues,
            backgroundColor: '#2563eb',
            borderRadius: 4
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          plugins: {{ legend: {{ display: false }} }},
          scales: {{ x: {{ grid: {{ display: false }} }}, y: {{ ticks: {{ font: {{ size: 10 }} }} }} }}
        }}
      }});

      // 2. Paises Importados Chart
      const ctxPaises = document.getElementById('chartPaises').getContext('2d');
      const paisLabels = Object.keys(rawData.charts.paises_importados).filter(p => p !== 'NO INFORMA.');
      const paisValues = paisLabels.map(p => rawData.charts.paises_importados[p]);
      chartPaises = new Chart(ctxPaises, {{
        type: 'bar',
        data: {{
          labels: paisLabels,
          datasets: [{{
            label: 'Productos Importados',
            data: paisValues,
            backgroundColor: '#d97706',
            borderRadius: 4
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{ y: {{ grid: {{ display: false }} }}, x: {{ ticks: {{ font: {{ size: 10 }} }} }} }}
        }}
      }});

      // 3. Top Titulares Chart
      const ctxTit = document.getElementById('chartTitulares').getContext('2d');
      const titLabels = Object.keys(rawData.charts.top_titulares).slice(0, 12).map(t => t.length > 25 ? t.substring(0, 23) + '...' : t);
      const titValues = Object.values(rawData.charts.top_titulares).slice(0, 12);
      chartTitulares = new Chart(ctxTit, {{
        type: 'bar',
        data: {{
          labels: titLabels,
          datasets: [{{
            label: 'Registros Vigentes',
            data: titValues,
            backgroundColor: '#4f46e5',
            borderRadius: 4
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          plugins: {{ legend: {{ display: false }} }},
          scales: {{ x: {{ grid: {{ display: false }} }}, y: {{ ticks: {{ font: {{ size: 10 }} }} }} }}
        }}
      }});

      // 4. Especies Breakdown Chart
      const ctxEsp = document.getElementById('chartEspecies').getContext('2d');
      const espLabels = Object.keys(rawData.charts.species_breakdown);
      const espValues = Object.values(rawData.charts.species_breakdown);
      chartEspecies = new Chart(ctxEsp, {{
        type: 'bar',
        data: {{
          labels: espLabels,
          datasets: [{{
            label: 'Productos por Especie',
            data: espValues,
            backgroundColor: '#059669',
            borderRadius: 4
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{ y: {{ grid: {{ display: false }} }}, x: {{ ticks: {{ font: {{ size: 10 }} }} }} }}
        }}
      }});

      // 5. Finanzas Fabricantes Chart
      const ctxFinFab = document.getElementById('chartFinFab').getContext('2d');
      const fabLabels = rawData.charts.top_fabricantes_finanzas.slice(0, 8).map(f => f.RazonSocial.substring(0, 20));
      const fabValues = rawData.charts.top_fabricantes_finanzas.slice(0, 8).map(f => Math.round(f.Total_5Y_20_24));
      chartFinFab = new Chart(ctxFinFab, {{
        type: 'bar',
        data: {{
          labels: fabLabels,
          datasets: [{{
            label: 'Ventas 5 Años (COP $M)',
            data: fabValues,
            backgroundColor: '#0284c7',
            borderRadius: 4
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{ x: {{ ticks: {{ font: {{ size: 9 }} }} }} }}
        }}
      }});

      // 6. Finanzas Importadores Chart
      const ctxFinImp = document.getElementById('chartFinImp').getContext('2d');
      const impLabels = rawData.charts.top_importadores_finanzas.slice(3, 11).map(i => i.RazonSocial.substring(0, 20));
      const impValues = rawData.charts.top_importadores_finanzas.slice(3, 11).map(i => Math.round(i.Total_5Y_20_24));
      chartFinImp = new Chart(ctxFinImp, {{
        type: 'bar',
        data: {{
          labels: impLabels,
          datasets: [{{
            label: 'Ventas 5 Años (COP $M)',
            data: impValues,
            backgroundColor: '#9333ea',
            borderRadius: 4
          }}]
        }},
        options: {{
          responsive: true,
          maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{ x: {{ ticks: {{ font: {{ size: 9 }} }} }} }}
        }}
      }});
    }}

    function applyFilters() {{
      const search = document.getElementById('filter-search').value.toLowerCase().trim();
      const tipo = document.getElementById('filter-tipo').value;
      const origen = document.getElementById('filter-origen').value;
      const pais = document.getElementById('filter-pais').value;
      const especie = document.getElementById('filter-especie').value;

      filteredProducts = allProducts.filter(p => {{
        if (search) {{
          const match = p.Producto.toLowerCase().includes(search) ||
                        p.Titular.toLowerCase().includes(search) ||
                        p.Activos.toLowerCase().includes(search) ||
                        p.Reg_ICA.toLowerCase().includes(search) ||
                        p.Laboratorio_Productor.toLowerCase().includes(search);
          if (!match) return false;
        }}
        if (tipo && p.Tipo_Medicamento !== tipo) return false;
        if (origen) {{
          if (origen === 'COLOMBIA' && !p.Origen_Clasif.includes('COLOMBIA')) return false;
          if (origen === 'EXTRANJERO' && !p.Origen_Clasif.includes('EXTRANJERO')) return false;
        }}
        if (pais && p.Pais_Origen !== pais) return false;
        if (especie && !p.Especies.toUpperCase().includes(especie)) return false;
        return true;
      }});

      currentPage = 1;
      updateTable();
      updateFilteredKPIs();
    }}

    function updateFilteredKPIs() {{
      document.getElementById('filtered-count-label').textContent = `Mostrando ${{filteredProducts.length.toLocaleString()}} de ${{allProducts.length.toLocaleString()}} registros`;
      document.getElementById('kpi-total-regs').textContent = filteredProducts.length.toLocaleString();
      const nac = filteredProducts.filter(p => p.Origen_Clasif.includes('COLOMBIA')).length;
      const imp = filteredProducts.filter(p => p.Origen_Clasif.includes('EXTRANJERO')).length;
      const tit = new Set(filteredProducts.map(p => p.Titular)).size;
      document.getElementById('kpi-nacionales').textContent = nac.toLocaleString();
      document.getElementById('kpi-importados').textContent = imp.toLocaleString();
      document.getElementById('kpi-titulares').textContent = tit.toLocaleString();
    }}

    function updateTable() {{
      const tbody = document.getElementById('table-body');
      tbody.innerHTML = '';

      const totalPages = Math.ceil(filteredProducts.length / pageSize) || 1;
      const start = (currentPage - 1) * pageSize;
      const pageData = filteredProducts.slice(start, start + pageSize);

      pageData.forEach((p, idx) => {{
        const globalIdx = start + idx;
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-blue-50/60 cursor-pointer transition border-b border-slate-100';
        tr.onclick = function(e) {{
          // If click was not on an action button, still open modal
          openModal(p);
        }};
        const isNac = p.Origen_Clasif.includes('COLOMBIA');
        const badgeClass = isNac ? 'bg-emerald-100 text-emerald-800 border border-emerald-200' : 'bg-amber-100 text-amber-800 border border-amber-200';
        tr.innerHTML = `
          <td class="p-2.5">
            <button onclick="event.stopPropagation(); openModalByReg('${{p.Reg_ICA}}')" class="bg-blue-50 hover:bg-blue-600 hover:text-white text-blue-700 border border-blue-200 font-semibold px-2 py-1 rounded text-[10px] transition">
              Ver Ficha
            </button>
          </td>
          <td class="p-2.5 font-bold text-slate-900 whitespace-nowrap">${{p.Reg_ICA}}</td>
          <td class="p-2.5 font-semibold text-blue-900">${{p.Producto}}</td>
          <td class="p-2.5 text-slate-700">${{p.Titular}}</td>
          <td class="p-2.5 text-slate-500 text-[11px] max-w-xs truncate" title="${{p.Activos}}">${{p.Activos || 'No reporta'}}</td>
          <td class="p-2.5 text-slate-600">${{p.Tipo_Medicamento || 'N/A'}}</td>
          <td class="p-2.5 text-slate-600">${{p.Pais_Origen || 'N/A'}}</td>
          <td class="p-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-semibold ${{badgeClass}}">${{isNac ? 'Nacional' : 'Importado'}}</span></td>
          <td class="p-2.5 text-slate-500 text-[11px] max-w-xs truncate" title="${{p.Especies}}">${{p.Especies || 'N/A'}}</td>
        `;
        tbody.appendChild(tr);
      }});

      document.getElementById('page-info').textContent = `Página ${{currentPage}} de ${{totalPages}} (${{filteredProducts.length.toLocaleString()}} filas)`;
      document.getElementById('btn-prev').disabled = currentPage <= 1;
      document.getElementById('btn-next').disabled = currentPage >= totalPages;
    }}

    // MODAL FUNCTIONS
    function openModalByReg(regIca) {{
      const prod = allProducts.find(p => p.Reg_ICA === regIca);
      if (prod) openModal(prod);
    }}

    function openModal(product) {{
      selectedProduct = product;
      
      // Badges
      document.getElementById('modal-reg-badge').textContent = `REG. ICA: ${{product.Reg_ICA}}`;
      document.getElementById('modal-estado-badge').textContent = product.Estado || 'VIGENTE';
      
      const isNac = product.Origen_Clasif.includes('COLOMBIA');
      const origenBadge = document.getElementById('modal-origen-badge');
      if (isNac) {{
        origenBadge.textContent = 'FABRICACIÓN NACIONAL';
        origenBadge.className = 'bg-emerald-500 text-white text-[11px] font-semibold px-2 py-0.5 rounded uppercase';
      }} else {{
        origenBadge.textContent = `IMPORTADO (${{product.Pais_Origen || 'EXTRANJERO'}})`;
        origenBadge.className = 'bg-amber-500 text-slate-900 text-[11px] font-semibold px-2 py-0.5 rounded uppercase';
      }}

      document.getElementById('modal-tipo-badge').textContent = product.Tipo_Medicamento || 'GENERAL';
      document.getElementById('modal-producto-title').textContent = product.Producto;
      document.getElementById('modal-titular-subtitle').textContent = product.Titular;

      // Section 1: General Info
      document.getElementById('modal-titular').textContent = product.Titular || 'No informado';
      document.getElementById('modal-productor').textContent = product.Laboratorio_Productor || 'No informado';
      document.getElementById('modal-pais').textContent = product.Pais_Origen || 'No informado';
      document.getElementById('modal-importador').textContent = product.Importador || 'No aplica / Titular directo';
      document.getElementById('modal-tipo').textContent = product.Tipo_Medicamento || 'No informado';
      document.getElementById('modal-retiro').textContent = product.Tiempo_Retiro ? `${{product.Tiempo_Retiro}} días` : '0 días / No reporta retiro';

      // Section 2: Activos y Cantidades
      document.getElementById('modal-activos').textContent = product.Activos || 'Información no detallada en registro';
      document.getElementById('modal-cantidades').textContent = product.Cantidades || 'Concentración estándar declarada';

      // Section 3: Indicaciones y Especies
      document.getElementById('modal-indicaciones').textContent = product.Indicaciones || 'Uso prescrito y regulado según ficha de registro ICA';
      document.getElementById('modal-especies').textContent = product.Especies || 'Especies pecuarias y/o de compañía generales';

      // Section 4: Precauciones y Empaques
      document.getElementById('modal-precauciones').textContent = product.Precauciones || 'Almacenar en lugar fresco y seco. Venta bajo fórmula médica veterinaria.';
      document.getElementById('modal-empaques').textContent = product.Empaques || 'Presentación comercial estándar autorizada.';

      // Display Modal
      document.getElementById('product-modal').classList.remove('hidden');
    }}

    function closeModal() {{
      document.getElementById('product-modal').classList.add('hidden');
    }}

    function copyRegIca() {{
      if (selectedProduct) {{
        navigator.clipboard.writeText(selectedProduct.Reg_ICA);
        alert(`Registro ICA "${{selectedProduct.Reg_ICA}}" copiado al portapapeles.`);
      }}
    }}

    function prevPage() {{
      if (currentPage > 1) {{
        currentPage--;
        updateTable();
      }}
    }}

    function nextPage() {{
      const totalPages = Math.ceil(filteredProducts.length / pageSize);
      if (currentPage < totalPages) {{
        currentPage++;
        updateTable();
      }}
    }}

    function changePageSize() {{
      pageSize = parseInt(document.getElementById('page-size').value);
      currentPage = 1;
      updateTable();
    }}

    function resetFilters() {{
      document.getElementById('filter-search').value = '';
      document.getElementById('filter-tipo').value = '';
      document.getElementById('filter-origen').value = '';
      document.getElementById('filter-pais').value = '';
      document.getElementById('filter-especie').value = '';
      applyFilters();
    }}

    function exportFilteredCSV() {{
      let csv = 'Registro_ICA,Producto,Titular,Activos,Cantidades,Indicaciones,Laboratorio_Productor,Pais_Origen,Importador,Empaques,Especies,Tiempo_Retiro,Tipo_Medicamento,Origen_Clasif\\n';
      filteredProducts.forEach(p => {{
        const row = [
          `"${{(p.Reg_ICA || '').replace(/"/g, '""')}}"`,
          `"${{(p.Producto || '').replace(/"/g, '""')}}"`,
          `"${{(p.Titular || '').replace(/"/g, '""')}}"`,
          `"${{(p.Activos || '').replace(/"/g, '""')}}"`,
          `"${{(p.Cantidades || '').replace(/"/g, '""')}}"`,
          `"${{(p.Indicaciones || '').replace(/"/g, '""')}}"`,
          `"${{(p.Laboratorio_Productor || '').replace(/"/g, '""')}}"`,
          `"${{(p.Pais_Origen || '').replace(/"/g, '""')}}"`,
          `"${{(p.Importador || '').replace(/"/g, '""')}}"`,
          `"${{(p.Empaques || '').replace(/"/g, '""')}}"`,
          `"${{(p.Especies || '').replace(/"/g, '""')}}"`,
          `"${{(p.Tiempo_Retiro || '').replace(/"/g, '""')}}"`,
          `"${{(p.Tipo_Medicamento || '').replace(/"/g, '""')}}"`,
          `"${{(p.Origen_Clasif || '').replace(/"/g, '""')}}"`
        ].join(',');
        csv += row + '\\n';
      }});

      const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.setAttribute('download', 'ica_productos_filtrados_completo.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}
  </script>
</body>
</html>
"""

dashboard_file = "/home/camilo-q/.gemini/antigravity/scratch/dashboard_salud_animal_colombia.html"
with open(dashboard_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Updated Dashboard with detailed Fact Sheet Modal: {dashboard_file}")

