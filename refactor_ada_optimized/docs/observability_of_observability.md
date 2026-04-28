# Observability of Observability (versión estática)

> Alcance: análisis estático del repositorio (`law_functions`), sin consultas a Azure.

## 1) Métricas base

- **Total de sources**: **13**
- **Total de sources workspace-genéricos**: **10**
- **Total de sources agregadores**: **3**
- **Total de domains/helpers que consumen sources**: **17**

## 2) Sources con más consumidores

1. `fn_src_mlp_systemlogs_all` → 6 consumidores directos
2. `fn_src_mlp_ws_ada` → 6 consumidores directos
3. `fn_src_mlp_ws_pisystem` → 3 consumidores directos
4. `fn_src_mlp_pipeline_runs_all` → 2 consumidores directos
5. `fn_src_mlp_ssag_systemlogs_all` → 2 consumidores directos

## 3) Sources con mayor impacto transversal

### Alta transversalidad técnica
- `fn_src_mlp_ws_pisystem`: cruza NOTPII + ADA + SIROSAG (directa o vía agregadores).
- `fn_src_mlp_ws_plans`: participa en agregadores ADA y SIROSAG.

### Alta transversalidad funcional dentro de un producto
- `fn_src_mlp_systemlogs_all`: concentra gran parte del monitoreo ADA.
- `fn_src_mlp_ws_ada`: soporta múltiples helpers/domains críticos de ADA.

## 4) Productos con más dependencias

- **ADA**: mayor dependencia total (3 sources de alto uso + mayor número de domains conectados).
- **NOTPII**: dependencia focalizada en 2 sources (`ws_notpii_databricksjobs`, `ws_pisystem`).
- **SIROSAG**: dependencia en 2 sources principales (`ws_ssag`, `ssag_systemlogs_all`) + dependencia indirecta de `ws_plans/ws_pisystem/ws_pdmsagi` por agregador.

## 5) Posibles puntos críticos de falla

1. **`fn_src_mlp_systemlogs_all`**
   - Un fallo impacta al menos 6 domains ADA.
2. **`fn_src_mlp_ws_ada`**
   - Degradación afecta varios helpers/domains ADA y además un agregador.
3. **`fn_src_mlp_ws_pisystem`**
   - Falla transversal entre productos (NOTPII + ADA + SIROSAG).
4. **Agregadores multi-workspace** (`pipeline_runs_all`, `systemlogs_all`, `ssag_systemlogs_all`)
   - Más puntos de falla por dependencia en múltiples sources base.

## 6) Candidatos a optimización futura (sin governance automática aún)

- Definir **SLO internos de datos** por source crítico (latencia, completitud, error rate de consulta).
- Publicar un **runbook por source crítico** con:
  - síntomas,
  - consumers afectados,
  - workspace/tablas de diagnóstico.
- Añadir reporte periódico (manual o script local) de:
  - cambios en número de consumidores por source,
  - aparición de nuevos sources no catalogados,
  - cambios de criticidad sugerida.
- Homologar convención de “campos mínimos esperados” por tipo de source (p.ej. pipeline/systemlogs).

## 7) Estado actual recomendado

- Arquitectura centrada en `fn_src_mlp_*`: **vigente**.
- Sin wrappers legacy activos en sources: **vigente**.
- Próximo paso recomendado: mantener este documento como baseline de soporte/onboarding y revisarlo ante cada refactor de monitoreo.

