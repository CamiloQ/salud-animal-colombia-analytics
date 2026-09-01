# Colombia Veterinary Market Intelligence & Analytics (Salud Animal Colombia)

Plataforma de inteligencia de mercado, analítica regulatoria y observatorio económico de la industria farmacéutica y de salud animal en Colombia.

El proyecto integra los registros sanitarios oficiales del **Instituto Colombiano Agropecuario (ICA)**, las series macroeconómicas e industriales del **Departamento Administrativo Nacional de Estadística (DANE)** y los estados financieros auditados de la **Superintendencia de Sociedades**.

---

## Características Principales

1. **Dashboard Interactivo Web (`index.html`):**
   * Desplegable directamente en **GitHub Pages** sin servidores ni configuraciones complejas.
   * KPIs en tiempo real (8.129 Registros Vigentes, Cuota Nacional vs. Importada, Titulares, Ventas DANE).
   * 6 Gráficos analíticos dinámicos (Categorías terapéuticas, Países de origen, Ranking de titulares, Especies, Finanzas).
   * Explorador maestro de registros sanitarios con búsqueda instantánea y paginación.
   * **Ficha Técnica Oficial por Producto (Modal):** Despliegue de los 15 atributos regulatorios (titular, laboratorio fabricante, principios activos, concentraciones, indicaciones, especies, empaques y tiempo de retiro).
   * Exportación instantánea de consultas filtradas a CSV.

2. **Fuentes de Datos Consolidadas (`/data`):**
   * `ica_medicamentos_vigentes_agosto_2026.csv`: Padrón nacional depurado de 8.129 productos con registro ICA vigente.
   * `ica_laboratorios_registrados.csv`: Censo de 5.000 registros analíticos y técnicos de laboratorios autorizados ante el ICA.
   * `ica_registros_heel_colombia.csv`: Catálogo oficial de 23 medicamentos de homotoxicología y biorregulación (Heel Colombia / Alemania).
   * `ranking_consolidado_importadores_distribuidores.csv`: Ranking de ventas quinquenales (2020-2024) de filiales multinacionales y distribuidores.
   * `directorio_laboratorios_veterinarios_ciiu_2100.csv`: Directorio financiero de laboratorios farmacéuticos nacionales.
   * `dane_eam_productos_farmaceuticos_veterinarios.csv`: Microdatos de producción, ventas y exportaciones por producto (CPC Ver. 2.1).
   * `dane_emmet_mensual_ciiu_2100.csv`: Serie temporal mensual continua (2018-2026) de la industria farmacéutica.

3. **Informes Ejecutivos (`/reports`):**
   * `informe_mercado_veterinario_ciiu_2100.pdf`: Informe ejecutivo en alta resolución.

---

## Cómo Publicar en GitHub Pages

Para publicar el dashboard de manera gratuita y pública en la web mediante GitHub Pages:

1. Subir este repositorio a su cuenta de GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Colombia Veterinary Market Intelligence Dashboard"
   git branch -M main
   git remote add origin https://github.com/<SU_USUARIO>/<NOMBRE_DEL_REPO>.git
   git push -u origin main
   ```
2. En GitHub, ir a la pestaña **Settings** del repositorio.
3. En el menú lateral izquierdo, hacer clic en **Pages**.
4. En **Build and deployment > Source**, seleccionar **Deploy from a branch**.
5. En **Branch**, seleccionar `main` y la carpeta `/ (root)`. Hacer clic en **Save**.
6. En un par de minutos, el dashboard estará disponible públicamente en: `https://<SU_USUARIO>.github.io/<NOMBRE_DEL_REPO>/`

---

## Estructura del Repositorio

```
colombia-veterinary-market-intelligence/
├── index.html                     # Aplicación Dashboard interactiva (GitHub Pages ready)
├── README.md                      # Documentación completa del proyecto
├── .gitignore                     # Archivos ignorados por Git
├── data/                          # Datasets consolidados en CSV y JSON
│   ├── dashboard_data.json
│   ├── ica_medicamentos_vigentes_agosto_2026.csv
│   ├── ica_laboratorios_registrados.csv
│   ├── ica_registros_heel_colombia.csv
│   ├── ranking_consolidado_importadores_distribuidores.csv
│   ├── directorio_laboratorios_veterinarios_ciiu_2100.csv
│   ├── dane_eam_productos_farmaceuticos_veterinarios.csv
│   └── dane_emmet_mensual_ciiu_2100.csv
├── scripts/                       # Scripts Python de extracción y procesamiento
└── reports/                       # Documentos e informes ejecutivos en PDF
```

---

## Licencia y Transparencia

Los datos utilizados provienen de fuentes oficiales públicas de la República de Colombia bajo los principios de la Ley 1712 de 2014 (Transparencia y del Derecho de Acceso a la Información Pública Nacional).
