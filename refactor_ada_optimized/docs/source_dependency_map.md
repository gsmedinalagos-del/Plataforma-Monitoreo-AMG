# Source Dependency Map

## 1) Source → consumidores

- `fn_src_mlp_ws_ada` → `fn_src_mlp_systemlogs_all`, `fn_prd_mlp_ada_dom_front_status`, `fn_prd_mlp_ada_alert_from_dispatch_nrt_logs`, `fn_prd_mlp_ada_kpi_alert_rows`, `fn_prd_mlp_ada_lag_helpers`, `fn_prd_mlp_ada_jobs_status_detail`
- `fn_src_mlp_ws_dataplatform` → `fn_prd_mlp_ada_dom_blockgrade_status`, `fn_prd_mlp_ada_kpi_alert_rows`
- `fn_src_mlp_ws_pisystem` → `fn_src_mlp_systemlogs_all`, `fn_src_mlp_ssag_systemlogs_all`, `fn_prd_mlp_notpii_ingesta_job04_alert`
- `fn_src_mlp_ws_ssag` → `fn_src_mlp_ssag_systemlogs_all`, `fn_prd_mlp_ssag_eval_desactualizacion`
- `fn_src_mlp_ws_dispatch` → `fn_src_mlp_pipeline_runs_all`
- `fn_src_mlp_ws_drillit` → `fn_src_mlp_pipeline_runs_all`
- `fn_src_mlp_ws_blkgrde` → `fn_src_mlp_pipeline_runs_all`
- `fn_src_mlp_ws_meteo` → `fn_src_mlp_systemlogs_all`
- `fn_src_mlp_ws_plans` → `fn_src_mlp_systemlogs_all`, `fn_src_mlp_ssag_systemlogs_all`
- `fn_src_mlp_ws_pdmsagi` → `fn_src_mlp_ssag_systemlogs_all`
- `fn_src_mlp_ws_notpii_databricksjobs` → `fn_prd_mlp_notpii_autoloader_alert`, `fn_prd_mlp_ada_dom_kpi_status`
- `fn_src_mlp_pipeline_runs_all` → `fn_prd_mlp_ada_dom_blockgrade_status`, `fn_prd_mlp_ada_dom_drillit_status`
- `fn_src_mlp_systemlogs_all` → `fn_prd_mlp_ada_dom_pi_status`, `fn_prd_mlp_ada_dom_alarm_status`, `fn_prd_mlp_ada_dom_meteodata_status`, `fn_prd_mlp_ada_dom_plans_status`, `fn_prd_mlp_ada_dom_kpi_status`
- `fn_src_mlp_ssag_systemlogs_all` → `fn_prd_mlp_ssag_eval_ejecucion`, `fn_prd_mlp_ssag_eval_desfase`

## 2) Producto → sources usados

- ADA → `fn_src_mlp_ws_ada`, `fn_src_mlp_ws_dataplatform`, `fn_src_mlp_pipeline_runs_all`, `fn_src_mlp_systemlogs_all`
- NOTPII → `fn_src_mlp_ws_notpii_databricksjobs`, `fn_src_mlp_ws_pisystem`
- SIROSAG → `fn_src_mlp_ws_ssag`, `fn_src_mlp_ssag_systemlogs_all`

## 3) Domain/helper → source utilizado

### ADA
- `fn_prd_mlp_ada_dom_alarm_status` → `fn_src_mlp_systemlogs_all`
- `fn_prd_mlp_ada_dom_dispatch_status` → `fn_src_mlp_ws_ada`
- `fn_prd_mlp_ada_dom_drillit_status` → `fn_src_mlp_pipeline_runs_all`
- `fn_prd_mlp_ada_dom_blockgrade_status` → `fn_src_mlp_pipeline_runs_all`, `fn_src_mlp_ws_dataplatform`
- `fn_prd_mlp_ada_dom_front_status` → `fn_src_mlp_ws_ada`
- `fn_prd_mlp_ada_dom_pi_status` → `fn_src_mlp_systemlogs_all`
- `fn_prd_mlp_ada_dom_plans_status` → `fn_src_mlp_systemlogs_all`
- `fn_prd_mlp_ada_dom_meteodata_status` → `fn_src_mlp_systemlogs_all`
- `fn_prd_mlp_ada_dom_kpi_status` → `fn_src_mlp_systemlogs_all`, `fn_src_mlp_ws_ada`, `fn_src_mlp_ws_notpii_databricksjobs`
- `fn_prd_mlp_ada_alert_from_dispatch_nrt_logs` → `fn_src_mlp_ws_ada`
- `fn_prd_mlp_ada_kpi_alert_rows` → `fn_src_mlp_ws_ada`, `fn_src_mlp_ws_dataplatform`
- `fn_prd_mlp_ada_lag_helpers` → `fn_src_mlp_ws_ada`
- `fn_prd_mlp_ada_jobs_status_detail` → `fn_src_mlp_ws_ada`

### NOTPII
- `fn_prd_mlp_notpii_autoloader_alert` → `fn_src_mlp_ws_notpii_databricksjobs`
- `fn_prd_mlp_notpii_ingesta_job04_alert` → `fn_src_mlp_ws_pisystem`

### SIROSAG
- `fn_prd_mlp_ssag_eval_desactualizacion` → `fn_src_mlp_ws_ssag`
- `fn_prd_mlp_ssag_eval_desfase` → `fn_src_mlp_ssag_systemlogs_all`
- `fn_prd_mlp_ssag_eval_ejecucion` → `fn_src_mlp_ssag_systemlogs_all`

## 4) Sources más compartidos

1. `fn_src_mlp_ws_ada` (6 consumidores)
2. `fn_src_mlp_systemlogs_all` (5 consumidores)
3. `fn_src_mlp_ws_pisystem` (3 consumidores)
4. `fn_src_mlp_pipeline_runs_all` (2 consumidores)
5. `fn_src_mlp_ssag_systemlogs_all` (2 consumidores)
6. `fn_src_mlp_ws_dataplatform` (2 consumidores)

## 5) Sources usados por un solo producto

- Solo ADA: `fn_src_mlp_ws_ada`, `fn_src_mlp_ws_dataplatform`, `fn_src_mlp_ws_dispatch`, `fn_src_mlp_ws_drillit`, `fn_src_mlp_ws_blkgrde`, `fn_src_mlp_ws_meteo`, `fn_src_mlp_pipeline_runs_all`, `fn_src_mlp_systemlogs_all`
- Solo NOTPII: `fn_src_mlp_ws_notpii_databricksjobs`
- Solo SIROSAG: `fn_src_mlp_ws_ssag`, `fn_src_mlp_ws_pdmsagi`, `fn_src_mlp_ssag_systemlogs_all`
- Compartidos multi-producto: `fn_src_mlp_ws_pisystem`, `fn_src_mlp_ws_plans`

## 6) Agregadores que dependen de múltiples workspace sources

- `fn_src_mlp_pipeline_runs_all` ← dispatch + drillit + blkgrde
- `fn_src_mlp_systemlogs_all` ← ada + meteo + pisystem + plans
- `fn_src_mlp_ssag_systemlogs_all` ← ssag + plans + pdmsagi + pisystem
