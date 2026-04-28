# Source Catalog (KQL)

Este catálogo documenta los `fn_src_mlp_*` activos en `law_functions/sources` y su rol en monitoreo.

## Tabla de catálogo

| Source | Tipo de source | Workspace lógico | Tabla(s) consultadas | Producto asociado | Consumidores directos | Domains/helpers impactados | Criticidad sugerida | Observación funcional | Recomendación de mantenimiento |
|---|---|---|---|---|---|---|---|---|---|
| `fn_src_mlp_ws_ada` | workspace genérico | ada | `tableName` (ej: `ContainerAppConsoleLogs_CL`, `ContainerAppSystemLogs_CL`, `Logs_MLP_ADA_CL`, `AppServiceConsoleLogs`) | ADA (y base para agregador ADA) | `fn_src_mlp_systemlogs_all`, `fn_prd_mlp_ada_dom_blockgrade_status`, `fn_prd_mlp_ada_dom_front_status`, `fn_prd_mlp_ada_alert_from_dispatch_nrt_logs`, `fn_prd_mlp_ada_kpi_alert_rows`, `fn_prd_mlp_ada_lag_helpers` | Blockgrade, Front, KPI, Lag, NRT Dispatch | **Alta** | Source más transversal en ADA; caída impacta múltiples señales. | Mantener; versionar cambios de columnas con pruebas de contratos por tabla. |
| `fn_src_mlp_ws_pisystem` | workspace genérico | pisystem | `tableName` (ej: `ContainerAppSystemLogs_CL`, `ContainerAppConsoleLogs_CL`) | ADA / NOTPII / SIROSAG (vía agregadores) | `fn_src_mlp_systemlogs_all`, `fn_src_mlp_ssag_systemlogs_all`, `fn_prd_mlp_notpii_ingesta_job04_alert` | PI status, SIROSAG evals, ingesta job04 | **Alta** | Fuente compartida por 3 productos. | Mantener; priorizar observabilidad de latencia/calidad de logs de PI. |
| `fn_src_mlp_ws_ssag` | workspace genérico | ssag | `tableName` | SIROSAG | `fn_src_mlp_ssag_systemlogs_all`, `fn_prd_mlp_ssag_eval_desactualizacion` | Desactualización SSAG + resumen SIROSAG | **Media** | Uso principal SIROSAG. | Mantener; revisar schemas usados por helpers SSAG. |
| `fn_src_mlp_ws_dispatch` | workspace genérico | dispatch | `tableName` (actual: `AzureDiagnostics`) | ADA (vía agregador) | `fn_src_mlp_pipeline_runs_all` | Drillit/Blockgrade status (pipeline health) | **Media** | Source de soporte para agregador de pipelines. | Mantener simple; evitar lógica de negocio dentro del source. |
| `fn_src_mlp_ws_drillit` | workspace genérico | drillit | `tableName` (actual: `AzureDiagnostics`) | ADA (vía agregador) | `fn_src_mlp_pipeline_runs_all` | Drillit status | **Media** | Similar a dispatch/blkgrde. | Mantener; documentar tabla mínima esperada (`Category`, `OperationName`). |
| `fn_src_mlp_ws_blkgrde` | workspace genérico | blkgrde | `tableName` (actual: `AzureDiagnostics`) | ADA (vía agregador) | `fn_src_mlp_pipeline_runs_all` | Blockgrade status | **Media** | Similar a dispatch/drillit. | Mantener; considerar checklist de disponibilidad por workspace. |
| `fn_src_mlp_ws_meteo` | workspace genérico | meteo | `tableName` (actual en agregador: `ContainerAppSystemLogs_CL`) | ADA (vía agregador) | `fn_src_mlp_systemlogs_all` | Meteodata status | **Media** | Dependencia única vía agregador ADA systemlogs. | Mantener; validar consistencia de campos `JobName_s`, `Log_s`. |
| `fn_src_mlp_ws_plans` | workspace genérico | plans | `tableName` (actual: `ContainerAppSystemLogs_CL`) | ADA / SIROSAG (vía agregadores) | `fn_src_mlp_systemlogs_all`, `fn_src_mlp_ssag_systemlogs_all` | Plans status ADA + señales SIROSAG | **Alta** | Reutilizado por dos agregadores cross-product. | Mantener; monitorear cambios de formato de logs. |
| `fn_src_mlp_ws_pdmsagi` | workspace genérico | pdmsagi | `tableName` (actual: `ContainerAppSystemLogs_CL`) | SIROSAG (vía agregador) | `fn_src_mlp_ssag_systemlogs_all` | SIROSAG resumen/evaluaciones | **Media** | Dependencia focalizada SIROSAG. | Mantener; revisar frecuencia de datos vs ventana de consulta. |
| `fn_src_mlp_ws_notpii_databricksjobs` | workspace genérico | notpii_databricksjobs (dev/uat/all) | `DatabricksJobs` | NOTPII | `fn_prd_mlp_notpii_autoloader_alert` | Autoloader dev/uat/global | **Alta** | Source clave para alertas de ejecución de jobs. | Mantener; conservar enum de entorno (`dev|uat|all`). |
| `fn_src_mlp_pipeline_runs_all` | agregador product-level | multi (dispatch, drillit, blkgrde) | `AzureDiagnostics` (proyección común) | ADA | `fn_prd_mlp_ada_dom_blockgrade_status`, `fn_prd_mlp_ada_dom_drillit_status` | Blockgrade/Drillit domains | **Alta** | Agregador crítico para salud de pipelines. | Mantener; si crece, separar por dominio manteniendo interfaz estable. |
| `fn_src_mlp_systemlogs_all` | agregador product-level | multi (ada, meteo, pisystem, plans) | `ContainerAppSystemLogs_CL` (proyección común) | ADA | `fn_prd_mlp_ada_dom_dispatch_status`, `fn_prd_mlp_ada_dom_pi_status`, `fn_prd_mlp_ada_dom_alarm_status`, `fn_prd_mlp_ada_dom_meteodata_status`, `fn_prd_mlp_ada_dom_plans_status`, `fn_prd_mlp_ada_dom_kpi_status` | 6 domains ADA | **Alta** | Source más compartido del producto ADA. | Mantener prioritario; definir smoke-checks periódicos. |
| `fn_src_mlp_ssag_systemlogs_all` | agregador product-level | multi (ssag, plans, pdmsagi, pisystem) | `ContainerAppSystemLogs_CL` | SIROSAG | `fn_prd_mlp_ssag_eval_ejecucion`, `fn_prd_mlp_ssag_eval_desfase` | Eje de evaluación SIROSAG | **Alta** | Agregador central SIROSAG para desfase/ejecución. | Mantener; consolidar observabilidad de completitud por workspace. |

## Resumen rápido

- Sources activos: **13**.
- Workspace genéricos: **10**.
- Agregadores product-level: **3**.
- Principales críticos (impacto transversal):
  - `fn_src_mlp_systemlogs_all`
  - `fn_src_mlp_ws_ada`
  - `fn_src_mlp_ws_pisystem`
  - `fn_src_mlp_pipeline_runs_all`

