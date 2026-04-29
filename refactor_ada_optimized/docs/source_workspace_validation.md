# Validación de workspace real por source (revisión de exactitud)

Fecha: 2026-04-28

## 1) Workspace real de cada source base

| Source base | Workspace real encapsulado |
|---|---|
| `fn_src_mlp_ws_ada` | `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-ADA/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-ada` |
| `fn_src_mlp_ws_dataplatform` | `/subscriptions/0d996eb2-802f-4ef8-8ae6-d385c74da7e6/resourceGroups/ams-dev-dataplatform-rg/providers/Microsoft.OperationalInsights/workspaces/ams-dev-dataplatform-laws` |
| `fn_src_mlp_ws_pisystem` | `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-PISYSTEM/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-pisystem` |
| `fn_src_mlp_ws_ssag` | `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-SSAG/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-ssag` |
| `fn_src_mlp_ws_dispatch` | `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-DISPATCH/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-dispatch` |
| `fn_src_mlp_ws_drillit` | `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-DRILLIT/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-drillit` |
| `fn_src_mlp_ws_blkgrde` | `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-BLKGRDE/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-blkgrde` |
| `fn_src_mlp_ws_meteo` | `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-METEO/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-meteo` |
| `fn_src_mlp_ws_plans` | `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-PLANS/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-plans` |
| `fn_src_mlp_ws_pdmsagi` | `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-PDMSAGI/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-pdmsagi` |
| `fn_src_mlp_ws_notpii_databricksjobs` | DEV: `/subscriptions/0d996eb2-802f-4ef8-8ae6-d385c74da7e6/resourceGroups/ams-dev-dataplatform-rg/providers/Microsoft.OperationalInsights/workspaces/ams-dev-dataplatform-laws`; UAT: `/subscriptions/0d996eb2-802f-4ef8-8ae6-d385c74da7e6/resourceGroups/ams-uat-dataplatform-rg/providers/Microsoft.OperationalInsights/workspaces/ams-uat-dataplatform-laws` |

## 2) Tabla(s) usadas por source (visión funcional)

- `ws_ada`: tablas ADA operativas (`ContainerApp*`, `AppServiceConsoleLogs`, etc.).
- `ws_dataplatform`: `Logs_MLP_ADA_CL` (caso validación `en_mantencion`).
- `ws_notpii_databricksjobs`: `DatabricksJobs` (dev/uat/all).
- `ws_dispatch/ws_drillit/ws_blkgrde`: `AzureDiagnostics` (vía agregador pipelines).
- `ws_meteo/ws_plans/ws_pdmsagi/ws_pisystem/ws_ssag`: `ContainerAppSystemLogs_CL` y/o `ContainerAppConsoleLogs_CL` según consumidor.

## 3) Detección de posibles tablas mal asignadas

### Caso encontrado
- `Logs_MLP_ADA_CL` estaba siendo consultada vía `fn_src_mlp_ws_ada("Logs_MLP_ADA_CL", ...)`, pero el workspace correcto para esa tabla (según requerimiento) es `ams-dev-dataplatform-laws`.

### Impacto potencial
- Riesgo de leer datos desde workspace incorrecto para `en_mantencion`, alterando estado de alertas (falsos OK/ALERT).

## 4) Correcciones aplicadas

1. Se creó `fn_src_mlp_ws_dataplatform(sourceType, startTime, endTime)` en:
   - `law_functions/sources/`
   - `law_functions_body_only/sources/`
2. Se migraron consultas de `Logs_MLP_ADA_CL` a `fn_src_mlp_ws_dataplatform(...)` en:
   - `fn_prd_mlp_ada_dom_blockgrade_status`
   - `fn_prd_mlp_ada_kpi_alert_rows`
   - y espejos `law_functions_body_only`.
3. Se mantuvo la regla de arquitectura:
   - sin acceso directo a tablas fuera de `/sources`.

## 5) Recomendación de naming

- Mantener naming por workspace real (`fn_src_mlp_ws_<workspace_real_o_logico_claro>`).
- Evitar usar un source de producto (`ws_ada`) para tablas hospedadas en otro workspace.
- Cuando un producto depende de más de un workspace, explicitarlo en nombre y catálogo (`ws_dataplatform`, `ws_pisystem`, etc.) para minimizar ambigüedad operativa.

