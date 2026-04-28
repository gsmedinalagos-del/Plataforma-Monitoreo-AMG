# Troubleshooting: `One or more pattern references were not declared`

## Error observado

`One or more pattern references were not declared. Detected pattern references: [workspace resource id]`

## Causa más probable

Las funciones `fn_src_mlp_ws_*` usan referencias cross-resource con resource ids.
Cuando la consulta que invoca esas funciones no declara/adjunta esos recursos de Log Analytics, el motor rechaza la query con ese error.

## Qué validar

1. Que el panel/query incluya en `resources` todos los workspaces requeridos por los sources invocados (directa o indirectamente).
2. Que no estés ejecutando una consulta que llama fuentes cross-workspace desde un contexto que solo adjunta 1 workspace.

## Workspaces requeridos (referencia rápida)

- `fn_src_mlp_ws_ada` → `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-ADA/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-ada`
- `fn_src_mlp_ws_dataplatform` → `/subscriptions/0d996eb2-802f-4ef8-8ae6-d385c74da7e6/resourceGroups/ams-dev-dataplatform-rg/providers/Microsoft.OperationalInsights/workspaces/ams-dev-dataplatform-laws`
- `fn_src_mlp_ws_pisystem` → `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-PISYSTEM/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-pisystem`
- `fn_src_mlp_ws_dispatch` → `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-DISPATCH/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-dispatch`
- `fn_src_mlp_ws_drillit` → `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-DRILLIT/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-drillit`
- `fn_src_mlp_ws_blkgrde` → `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-BLKGRDE/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-blkgrde`
- `fn_src_mlp_ws_meteo` → `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-METEO/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-meteo`
- `fn_src_mlp_ws_plans` → `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-PLANS/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-plans`
- `fn_src_mlp_ws_pdmsagi` → `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-PDMSAGI/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-pdmsagi`
- `fn_src_mlp_ws_ssag` → `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-SSAG/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-ssag`
- `fn_src_mlp_ws_notpii_databricksjobs` →
  - DEV: `/subscriptions/0d996eb2-802f-4ef8-8ae6-d385c74da7e6/resourceGroups/ams-dev-dataplatform-rg/providers/Microsoft.OperationalInsights/workspaces/ams-dev-dataplatform-laws`
  - UAT: `/subscriptions/0d996eb2-802f-4ef8-8ae6-d385c74da7e6/resourceGroups/ams-uat-dataplatform-rg/providers/Microsoft.OperationalInsights/workspaces/ams-uat-dataplatform-laws`

## Recomendación operativa

- Mantener los sources como están (correctos por workspace real).
- Ajustar la configuración de ejecución (lista de `resources`) para incluir todos los workspaces que pueda tocar el source llamado.
- Para facilitar soporte, usar `python refactor_ada_optimized/analyze_source_catalog.py` y revisar la nueva sección `Required workspace references by source`.

