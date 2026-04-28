# Auditoría técnica de la capa de sources KQL (post-refactor)

Fecha de auditoría: 2026-04-28.

## 1) Resumen ejecutivo

- La capa `fn_src_mlp_*` quedó **funcional y consistente**: la auditoría automática del paquete pasa sin errores (`KQL package audit OK`).
- Actualmente hay **14 sources** en `law_functions/sources`: **10 workspace-genéricos** + **4 agregadores product-level**.
- No hay sources completamente huérfanos (todos tienen al menos un consumidor directo, aunque sea otro source agregador).
- Sí existe al menos **1 wrapper residual claro**: `fn_src_mlp_notpii_databricksjobs_all`, que hoy solo encapsula una llamada con parámetro fijo (`"all"`) a `fn_src_mlp_ws_notpii_databricksjobs`.
- Se detectaron **consultas directas a workspace/tablas fuera de la capa source** en funciones de dominio/helper ADA, lo que rompe parcialmente el objetivo de centralización.
- Con un ajuste adicional (eliminar wrapper residual y mover 2–3 accesos directos a sources), la arquitectura quedaría más simple y uniforme.

## 2) Cantidad total de sources actuales

| Categoría | Cantidad | Funciones |
|---|---:|---|
| Source genérico por workspace | 10 | `fn_src_mlp_ws_ada`, `fn_src_mlp_ws_pisystem`, `fn_src_mlp_ws_ssag`, `fn_src_mlp_ws_dispatch`, `fn_src_mlp_ws_drillit`, `fn_src_mlp_ws_blkgrde`, `fn_src_mlp_ws_meteo`, `fn_src_mlp_ws_plans`, `fn_src_mlp_ws_pdmsagi`, `fn_src_mlp_ws_notpii_databricksjobs` |
| Source agregador / product-level | 4 | `fn_src_mlp_pipeline_runs_all`, `fn_src_mlp_systemlogs_all`, `fn_src_mlp_ssag_systemlogs_all`, `fn_src_mlp_notpii_databricksjobs_all` |
| Source legacy / wrapper residual | 1 (incluido en agregadores) | `fn_src_mlp_notpii_databricksjobs_all` |
| Source no utilizado | 0 | — |
| **Total** | **14** | — |

## 3) Tabla de inventario de sources

| Source | Tipo | Tablas soportadas o consultadas | Consumidores directos | Estado | Recomendación |
|---|---|---|---|---|---|
| `fn_src_mlp_ws_ada` | Genérico workspace | `table(tableName)` (p.ej. `ContainerAppSystemLogs_CL`, `ContainerAppConsoleLogs_CL`) | `fn_src_mlp_systemlogs_all`, helpers ADA (`lag_helpers`, `alert_from_dispatch_nrt_logs`, `kpi_alert_rows`) | Usado | Mantener |
| `fn_src_mlp_ws_pisystem` | Genérico workspace | `table(tableName)` (system/console logs) | `fn_src_mlp_systemlogs_all`, `fn_src_mlp_ssag_systemlogs_all`, helper `notpii_ingesta_job04_alert` | Usado | Mantener |
| `fn_src_mlp_ws_ssag` | Genérico workspace | `table(tableName)` | `fn_src_mlp_ssag_systemlogs_all`, helper `ssag_eval_desactualizacion` | Usado | Mantener |
| `fn_src_mlp_ws_dispatch` | Genérico workspace | `table(tableName)` (hoy: `AzureDiagnostics`) | `fn_src_mlp_pipeline_runs_all` | Usado solo por agregador | Mantener (o fusionar en source multi-workspace de pipelines) |
| `fn_src_mlp_ws_drillit` | Genérico workspace | `table(tableName)` (hoy: `AzureDiagnostics`) | `fn_src_mlp_pipeline_runs_all` | Usado solo por agregador | Mantener (o fusionar en source multi-workspace de pipelines) |
| `fn_src_mlp_ws_blkgrde` | Genérico workspace | `table(tableName)` (hoy: `AzureDiagnostics`) | `fn_src_mlp_pipeline_runs_all` | Usado solo por agregador | Mantener (o fusionar en source multi-workspace de pipelines) |
| `fn_src_mlp_ws_meteo` | Genérico workspace | `table(tableName)` | `fn_src_mlp_systemlogs_all` | Usado solo por agregador | Mantener |
| `fn_src_mlp_ws_plans` | Genérico workspace | `table(tableName)` | `fn_src_mlp_systemlogs_all`, `fn_src_mlp_ssag_systemlogs_all` | Usado | Mantener |
| `fn_src_mlp_ws_pdmsagi` | Genérico workspace | `table(tableName)` | `fn_src_mlp_ssag_systemlogs_all` | Usado solo por agregador | Mantener |
| `fn_src_mlp_ws_notpii_databricksjobs` | Genérico workspace/entorno | `DatabricksJobs` en LAW DEV y UAT (`env=dev|uat|all`) | `fn_src_mlp_notpii_databricksjobs_all` | Usado | Mantener como base |
| `fn_src_mlp_pipeline_runs_all` | Agregador product-level | `AzureDiagnostics` (dispatch + drillit + blkgrde) | `ada_dom_drillit_status`, `ada_dom_blockgrade_status` | Usado | Mantener |
| `fn_src_mlp_systemlogs_all` | Agregador product-level | `ContainerAppSystemLogs_CL` (ada + meteo + pisystem + plans) | 6 domains ADA (`dispatch/pi/alarm/meteodata/plans/kpi status`) | Usado | Mantener |
| `fn_src_mlp_ssag_systemlogs_all` | Agregador product-level | `ContainerAppSystemLogs_CL` (ssag + plans + pdmsagi + pisystem) | helpers SIROSAG (`eval_ejecucion`, `eval_desfase`) | Usado | Mantener |
| `fn_src_mlp_notpii_databricksjobs_all` | Agregador/wrapper residual | Wrapper sobre `fn_src_mlp_ws_notpii_databricksjobs("all", ...)` | helper `notpii_autoloader_alert` | Usado solo por compatibilidad | Candidato a eliminación (reemplazo directo por source base) |

## 4) Tabla source → consumidores

| Source | Consumidores (domains/helpers/wrappers/agregadores) |
|---|---|
| `fn_src_mlp_ws_ada` | `fn_src_mlp_systemlogs_all`, `fn_prd_mlp_ada_lag_helpers`, `fn_prd_mlp_ada_alert_from_dispatch_nrt_logs`, `fn_prd_mlp_ada_kpi_alert_rows` |
| `fn_src_mlp_ws_pisystem` | `fn_src_mlp_systemlogs_all`, `fn_src_mlp_ssag_systemlogs_all`, `fn_prd_mlp_notpii_ingesta_job04_alert` |
| `fn_src_mlp_ws_ssag` | `fn_src_mlp_ssag_systemlogs_all`, `fn_prd_mlp_ssag_eval_desactualizacion` |
| `fn_src_mlp_ws_dispatch` | `fn_src_mlp_pipeline_runs_all` |
| `fn_src_mlp_ws_drillit` | `fn_src_mlp_pipeline_runs_all` |
| `fn_src_mlp_ws_blkgrde` | `fn_src_mlp_pipeline_runs_all` |
| `fn_src_mlp_ws_meteo` | `fn_src_mlp_systemlogs_all` |
| `fn_src_mlp_ws_plans` | `fn_src_mlp_systemlogs_all`, `fn_src_mlp_ssag_systemlogs_all` |
| `fn_src_mlp_ws_pdmsagi` | `fn_src_mlp_ssag_systemlogs_all` |
| `fn_src_mlp_ws_notpii_databricksjobs` | `fn_src_mlp_notpii_databricksjobs_all` |
| `fn_src_mlp_pipeline_runs_all` | `fn_prd_mlp_ada_dom_drillit_status`, `fn_prd_mlp_ada_dom_blockgrade_status` |
| `fn_src_mlp_systemlogs_all` | `fn_prd_mlp_ada_dom_dispatch_status`, `fn_prd_mlp_ada_dom_pi_status`, `fn_prd_mlp_ada_dom_alarm_status`, `fn_prd_mlp_ada_dom_meteodata_status`, `fn_prd_mlp_ada_dom_plans_status`, `fn_prd_mlp_ada_dom_kpi_status` |
| `fn_src_mlp_ssag_systemlogs_all` | `fn_prd_mlp_ssag_eval_ejecucion`, `fn_prd_mlp_ssag_eval_desfase` |
| `fn_src_mlp_notpii_databricksjobs_all` | `fn_prd_mlp_notpii_autoloader_alert` |

## 5) Tabla consumidor → source

| Consumidor | Tipo consumidor | Source(s) utilizado(s) |
|---|---|---|
| `fn_prd_mlp_ada_dom_alarm_status` | Domain ADA | `fn_src_mlp_systemlogs_all` |
| `fn_prd_mlp_ada_dom_dispatch_status` | Domain ADA | `fn_src_mlp_systemlogs_all` |
| `fn_prd_mlp_ada_dom_kpi_status` | Domain ADA | `fn_src_mlp_systemlogs_all` |
| `fn_prd_mlp_ada_dom_meteodata_status` | Domain ADA | `fn_src_mlp_systemlogs_all` |
| `fn_prd_mlp_ada_dom_pi_status` | Domain ADA | `fn_src_mlp_systemlogs_all` |
| `fn_prd_mlp_ada_dom_plans_status` | Domain ADA | `fn_src_mlp_systemlogs_all` |
| `fn_prd_mlp_ada_dom_drillit_status` | Domain ADA | `fn_src_mlp_pipeline_runs_all` |
| `fn_prd_mlp_ada_dom_blockgrade_status` | Domain ADA | `fn_src_mlp_pipeline_runs_all` (+ acceso directo residual a `Logs_MLP_ADA_CL`) |
| `fn_prd_mlp_ada_lag_helpers` | Helper ADA | `fn_src_mlp_ws_ada` |
| `fn_prd_mlp_ada_alert_from_dispatch_nrt_logs` | Helper ADA | `fn_src_mlp_ws_ada` |
| `fn_prd_mlp_ada_kpi_alert_rows` | Helper ADA | `fn_src_mlp_ws_ada` (+ acceso directo residual a `Logs_MLP_ADA_CL`) |
| `fn_prd_mlp_notpii_autoloader_alert` | Helper NOTPII | `fn_src_mlp_notpii_databricksjobs_all` |
| `fn_prd_mlp_notpii_ingesta_job04_alert` | Helper NOTPII | `fn_src_mlp_ws_pisystem` |
| `fn_prd_mlp_ssag_eval_ejecucion` | Helper SIROSAG | `fn_src_mlp_ssag_systemlogs_all` |
| `fn_prd_mlp_ssag_eval_desfase` | Helper SIROSAG | `fn_src_mlp_ssag_systemlogs_all` |
| `fn_prd_mlp_ssag_eval_desactualizacion` | Helper SIROSAG | `fn_src_mlp_ws_ssag` |

## 6) Sources no usados o candidatos a eliminación

### No usados
- Ninguno (0).

### Usados solo por compatibilidad / candidatos a eliminación
- `fn_src_mlp_notpii_databricksjobs_all`: wrapper de una línea con `env="all"`; no agrega semántica adicional ni proyección/filtro.

## 7) Duplicidades detectadas

1. **Duplicidad estructural de sources workspace**
   - `fn_src_mlp_ws_ada`, `fn_src_mlp_ws_pisystem`, `fn_src_mlp_ws_ssag`, `fn_src_mlp_ws_dispatch`, `fn_src_mlp_ws_drillit`, `fn_src_mlp_ws_blkgrde`, `fn_src_mlp_ws_meteo`, `fn_src_mlp_ws_plans`, `fn_src_mlp_ws_pdmsagi` repiten el mismo patrón:
     - `workspace("...").table(tableName)` + filtro `TimeGenerated`.
   - Esto es intencional para claridad por workspace, pero es duplicidad de plantilla.

2. **Wrapper residual en NOTPII**
   - `fn_src_mlp_notpii_databricksjobs_all` no aporta lógica más allá de fijar `env=all`.

3. **Accesos directos fuera de sources (duplican responsabilidad de acceso a datos)**
   - `fn_prd_mlp_ada_kpi_alert_rows` consulta directo `workspace(...).Logs_MLP_ADA_CL` para `en_mantencion`.
   - `fn_prd_mlp_ada_dom_blockgrade_status` consulta directo `workspace(...).Logs_MLP_ADA_CL` para `en_mantencion`.
   - `fn_prd_mlp_ada_dom_front_status` consulta directo `workspace(...).table("AppServiceConsoleLogs")`.

## 8) Recomendación final de arquitectura

### Estado actual
- La refactorización **sí mejoró** centralización para la mayoría de productos (ADA/SIROSAG/NOTPII consumen sources explícitos).
- Aun así, la arquitectura no está totalmente cerrada porque existen queries directas a workspaces en capa de dominio/helper.

### Propuesta objetivo (más simple y mantenible)

1. **Mantener**
   - `fn_src_mlp_systemlogs_all`, `fn_src_mlp_pipeline_runs_all`, `fn_src_mlp_ssag_systemlogs_all`.
   - `fn_src_mlp_ws_ada`, `fn_src_mlp_ws_pisystem`, `fn_src_mlp_ws_ssag`, `fn_src_mlp_ws_plans`, `fn_src_mlp_ws_meteo`, `fn_src_mlp_ws_pdmsagi`, `fn_src_mlp_ws_dispatch`, `fn_src_mlp_ws_drillit`, `fn_src_mlp_ws_blkgrde`, `fn_src_mlp_ws_notpii_databricksjobs`.

2. **Eliminar**
   - `fn_src_mlp_notpii_databricksjobs_all`.

3. **Fusionar (opcional, fase 2)**
   - Considerar un source genérico único por identificador de workspace (ej. `fn_src_mlp_ws(workspaceKey, tableName, startTime, endTime)`) para evitar duplicidad de nueve funciones casi idénticas.
   - Si se prioriza legibilidad sobre abstracción, mantener los 9 workspace sources actuales.

4. **Reemplazar accesos directos por source genérico existente**
   - Migrar en ADA cualquier `workspace(...).Logs_MLP_ADA_CL` o `.table(...)` a `fn_src_mlp_ws_ada(...)`.
   - Para `AppServiceConsoleLogs`, reutilizar `fn_src_mlp_ws_ada("AppServiceConsoleLogs", startTime, endTime)`.

## 9) Lista concreta de cambios sugeridos (no implementados en esta auditoría)

1. En `fn_prd_mlp_notpii_autoloader_alert`, reemplazar:
   - `fn_src_mlp_notpii_databricksjobs_all(startTime - 2d, endTime)`
   - por `fn_src_mlp_ws_notpii_databricksjobs("all", startTime - 2d, endTime)`.
2. Eliminar source wrapper `fn_src_mlp_notpii_databricksjobs_all` tras validar despliegue.
3. En `fn_prd_mlp_ada_kpi_alert_rows` y `fn_prd_mlp_ada_dom_blockgrade_status`, reemplazar acceso directo a `Logs_MLP_ADA_CL` por `fn_src_mlp_ws_ada("Logs_MLP_ADA_CL", ...)`.
4. En `fn_prd_mlp_ada_dom_front_status`, reemplazar acceso directo a `AppServiceConsoleLogs` por `fn_src_mlp_ws_ada("AppServiceConsoleLogs", ...)`.
5. Re-ejecutar auditoría automática y verificación estática tras aplicar cambios.

## 10) Validación técnica ejecutada

- Comando ejecutado: `python refactor_ada_optimized/validate_kql_references.py`.
- Resultado: `KQL package audit OK`.
- Métricas del script: `Defined functions: 39`, `Checked files: 54`, wrappers/helpers/domains requeridos OK.

## 11) Chequeos estáticos ejecutados

1. Búsqueda de referencias a sources y consumidores:
   - `rg -n "fn_src_mlp_"`
   - script Python de mapeo source→consumidores y consumidor→source.
2. Búsqueda de acceso directo a workspace fuera de capa source:
   - `rg -n "workspace\s*\(" refactor_ada_optimized/law_functions --glob '!**/sources/**'`
3. Búsqueda de `.table(...)` fuera de capa source:
   - `rg -n "\.table\s*\(" refactor_ada_optimized/law_functions --glob '!**/sources/**'`
4. Búsqueda de tablas concretas relevantes fuera de sources:
   - `rg -n "\b[A-Za-z0-9_]+_CL\b|AzureDiagnostics|DatabricksJobs|AppServiceConsoleLogs" refactor_ada_optimized/law_functions --glob '!**/sources/**'`

