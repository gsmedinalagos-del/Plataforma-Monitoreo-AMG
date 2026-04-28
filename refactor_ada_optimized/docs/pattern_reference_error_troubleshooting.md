# Troubleshooting: `One or more pattern references were not declared`

## Error observado

`One or more pattern references were not declared. Detected pattern references: [workspace resource id]`

## Causa más probable

Las funciones `fn_src_mlp_ws_*` usan referencias cross-resource con resource IDs.
Si el caller (Grafana / API / Scheduled Query / portal) **no adjunta esos resources**, el motor rechaza la consulta.

## Cómo arreglarlo (paso a paso)

1. Identifica qué función estás llamando (`fn_prd_*` o `fn_src_*`).
2. Obtén la lista de workspaces requeridos por sus sources.
3. Agrega esos workspaces en el caller:
   - En Grafana Azure Monitor: `targets[].azureLogAnalytics.resources`.
   - En API de Azure Monitor Logs: `workspaces` / `additionalWorkspaces` según endpoint.
   - En reglas/alertas: incluye todos los scopes/workspaces necesarios.
4. Vuelve a ejecutar la query.

## Caso específico: `fn_prd_mlp_ada_dom_dispatch_status`

Con el estado actual del repo, la ruta Dispatch usa `fn_src_mlp_ws_ada(...)` para revisar job17.
Por lo tanto el caller debe incluir al menos este resource ID:

- `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-ADA/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-ada`

## Workspaces requeridos por source base (referencia rápida)

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

- Usa `python refactor_ada_optimized/analyze_source_catalog.py` para revisar dependencias y workspaces asociados.
- Si un panel falla por pattern reference, primero revisa `resources` antes de tocar lógica KQL.



## Ejemplo directo de tu caso (`fn_src_mlp_ws_plans`)

Si ejecutas:

`fn_src_mlp_ws_plans("ContainerAppConsoleLogs_CL", ago(6h), now())`

y aparece el error de pattern references, debes adjuntar este resource en el caller:

- `/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-PLANS/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-plans`

> Nota: el tercer parámetro debe ser `datetime` (usa `now()`), no `1m` (timespan).

## Resolver resources de forma automática (script)

Ejecuta:

- `python refactor_ada_optimized/resolve_required_resources.py fn_src_mlp_ws_plans`
- `python refactor_ada_optimized/resolve_required_resources.py fn_prd_mlp_ada_dom_dispatch_status`

El script imprime los resource IDs de workspace requeridos por cierre de dependencias.

## Verificación puntual `ws_plans` vs `ws_ssag`

- `fn_src_mlp_ws_plans` apunta a `MLP-PRD-RG-PLANS / mlp-prd-law-plans`.
- `fn_src_mlp_ws_ssag` apunta a `MLP-PRD-RG-SSAG / mlp-prd-law-ssag`.
- Si en ejecución aparece `...RG-SSAG...` al llamar `fn_src_mlp_ws_plans`, probablemente se está llamando otra función (`fn_src_mlp_ws_ssag`) o una versión no actualizada/publicada de la función.


## ¿Es por la definición o porque “no toma la tabla”?

En este error concreto, **no** es porque la tabla no exista ni por el `where TimeGenerated`.
El motor falla **antes** de ejecutar la lectura de datos, porque falta declarar el workspace en el caller.

Checklist rápido:

1. `endTime` debe ser `datetime` (usar `now()`, no `1m`).
2. El caller debe incluir el resource de PLANS en `resources`.
3. Recién después de eso, si aparece otro error, revisar existencia de tabla/columnas.

Ejemplo correcto de llamada:

`fn_src_mlp_ws_plans("ContainerAppConsoleLogs_CL", ago(6h), now())`

Si quieres probar solo estructura mínima:

`fn_src_mlp_ws_plans("ContainerAppConsoleLogs_CL", ago(30m), now()) | take 1`


## Aclaración importante: `print strcat(...)` no ejecuta la consulta

Si haces algo como:

- `print query_text = strcat('workspace("...").table("...')`

eso **solo construye e imprime texto**. No ejecuta el `workspace(...).table(...)`.
Por eso puede "funcionar" aunque falten `resources` en el caller: estás validando formato de string, no ejecución real de la query.

Para validar ejecución real usa directamente la función/source, por ejemplo:

- `fn_src_mlp_ws_plans("ContainerAppConsoleLogs_CL", ago(6h), now()) | take 1`

Si ahí aparece `pattern references were not declared`, el problema sigue siendo `resources` faltantes en el caller.


## ¿Cómo hacer que ejecute correctamente? (receta rápida)

### Opción A — Grafana (Azure Monitor datasource)

En el target de la query agrega en `azureLogAnalytics.resources` el workspace requerido.

Ejemplo para `fn_src_mlp_ws_plans(...)`:

```json
{
  "azureLogAnalytics": {
    "query": "fn_src_mlp_ws_plans("ContainerAppConsoleLogs_CL", ago(6h), now()) | take 1",
    "resources": [
      "/subscriptions/c68213bf-7453-4ba4-9aaa-56b822af4c20/resourceGroups/MLP-PRD-RG-PLANS/providers/Microsoft.OperationalInsights/workspaces/mlp-prd-law-plans"
    ]
  }
}
```

### Opción B — Validador previo (recomendado)

Antes de ejecutar, obtén la lista exacta de resources con:

- `python refactor_ada_optimized/resolve_required_resources.py fn_src_mlp_ws_plans`
- `python refactor_ada_optimized/resolve_required_resources.py fn_prd_mlp_ada_dom_dispatch_status`

### Opción C — Prueba mínima en Logs

Prueba mínima de ejecución real:

- `fn_src_mlp_ws_plans("ContainerAppConsoleLogs_CL", ago(30m), now()) | take 1`

Si falla con `pattern references were not declared`, todavía falta adjuntar resources en el caller.
