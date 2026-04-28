# Observability of Observability (estático)

Alcance: análisis estático del repositorio, sin consultar Azure.

## Métricas estáticas actuales

- Total de sources: **14**
- Sources workspace-genéricos: **11**
- Sources agregadores: **3**
- Domains/helpers que consumen sources: **17**

## Sources más consumidos

1. `fn_src_mlp_ws_ada` (6)
2. `fn_src_mlp_systemlogs_all` (5)
3. `fn_src_mlp_ws_pisystem` (3)
4. `fn_src_mlp_pipeline_runs_all` (2)
5. `fn_src_mlp_ssag_systemlogs_all` (2)
6. `fn_src_mlp_ws_dataplatform` (2)

## Impacto transversal

- Alto transversal multi-producto:
  - `fn_src_mlp_ws_pisystem`
  - `fn_src_mlp_ws_plans` (vía agregadores)
- Alto transversal intra-producto (ADA):
  - `fn_src_mlp_systemlogs_all`
  - `fn_src_mlp_ws_ada`
  - `fn_src_mlp_ws_dataplatform` (por impacto en señal `en_mantencion`)

## Productos con más dependencias

- ADA: 4 sources directos (`ws_ada`, `ws_dataplatform`, `pipeline_runs_all`, `systemlogs_all`)
- NOTPII: 2 sources directos
- SIROSAG: 2 sources directos

## Puntos críticos de falla sugeridos

1. `fn_src_mlp_ws_ada` (helpers/domains ADA + agregador)
2. `fn_src_mlp_systemlogs_all` (afecta 5 domains ADA)
3. `fn_src_mlp_ws_dataplatform` (afecta lógica `en_mantencion` en blockgrade/KPI)
4. `fn_src_mlp_ws_pisystem` (impacto transversal ADA/NOTPII/SIROSAG)

## Candidatos de optimización futura

- Definir SLO de datos por source crítico (latencia/completitud/errores).
- Runbook por source crítico con “síntoma → consumidor impactado → diagnóstico”.
- Snapshot periódico del mapa de dependencias para detectar cambios de criticidad.
- Mantener naming explícito por workspace real cuando una tabla no pertenece al workspace lógico principal del producto.

