# ADA Refactor Final (implementación por familias de fuente)

Este paquete queda en formato final:
- **LAW:** 1 archivo `.kql` = 1 función.
- **Grafana:** 1 archivo `.kql` = 1 wrapper.
- **LAW UI:** carpeta `law_functions_body_only/` con solo body (sin `let ... { }`).

## Estructura final
- `law_functions/sources/` *(sources compartidos por familia)*
- `law_functions/helpers_cross_product/`
- `law_functions/helpers_ada/`
- `law_functions/domains/`
- `law_functions_body_only/` *(espejo de `law_functions/` con body-only)*
- `grafana_wrappers/`

---

## LAW — archivos a crear

### Sources compartidos (familia de fuente)
1. `law_functions/sources/fn_src_pipeline_runs_all.kql`
2. `law_functions/sources/fn_src_systemlogs_all.kql`
3. `law_functions/sources/fn_src_ada_consolelogs.kql`

### Cross-product helpers
4. `law_functions/helpers_cross_product/fn_mon_status_to_color.kql`
5. `law_functions/helpers_cross_product/fn_mon_global_from_color_set.kql`

### ADA-only helper
6. `law_functions/helpers_ada/fn_prd_ada_lag_helpers.kql`

### Domain functions
7. `law_functions/domains/fn_prd_ada_dom_dispatch_status.kql`
8. `law_functions/domains/fn_prd_ada_dom_drillit_status.kql`
9. `law_functions/domains/fn_prd_ada_dom_blockgrade_status.kql`
10. `law_functions/domains/fn_prd_ada_dom_pi_status.kql`
11. `law_functions/domains/fn_prd_ada_dom_plans_status.kql`
12. `law_functions/domains/fn_prd_ada_dom_meteodata_status.kql`
13. `law_functions/domains/fn_prd_ada_dom_alarm_status.kql`
14. `law_functions/domains/fn_prd_ada_dom_front_status.kql`
15. `law_functions/domains/fn_prd_ada_dom_kpi_status.kql`
16. `law_functions/domains/fn_prd_ada_dom_kpi_detalle_html.kql`
17. `law_functions/domains/fn_prd_ada_dom_global_status.kql`

---

## Grafana — wrappers
1. `grafana_wrappers/var_mlp_ada_dispatch.kql`
2. `grafana_wrappers/var_mlp_ada_drillit.kql`
3. `grafana_wrappers/var_mlp_ada_blockgrade.kql`
4. `grafana_wrappers/var_mlp_ada_pi.kql`
5. `grafana_wrappers/var_mlp_ada_plans.kql`
6. `grafana_wrappers/var_mlp_ada_meteodata.kql`
7. `grafana_wrappers/var_mlp_ada_alarm.kql`
8. `grafana_wrappers/var_mlp_ada_front.kql`
9. `grafana_wrappers/var_mlp_ada_kpi.kql`
10. `grafana_wrappers/var_mlp_ada_global.kql`

---

## Firmas (Function parameters) en LAW

### Sources compartidos
- `fn_src_pipeline_runs_all(startTime:datetime, endTime:datetime)`
- `fn_src_systemlogs_all(startTime:datetime, endTime:datetime)`
- `fn_src_ada_consolelogs(startTime:datetime, endTime:datetime)`

### Cross-product helpers
- `fn_mon_status_to_color(status:string)`
- `fn_mon_global_from_color_set(colors:dynamic, alert_color:string = "#E53935", ok_color:string = "#EAF4EA")`

### ADA-only helper
- `fn_prd_ada_alert_from_tables_lag(tables:dynamic, startTime:datetime, endTime:datetime)`

### Domain functions
- `fn_prd_ada_dom_dispatch_status(startTime:datetime, endTime:datetime)`
- `fn_prd_ada_dom_drillit_status(startTime:datetime, endTime:datetime)`
- `fn_prd_ada_dom_blockgrade_status(startTime:datetime, endTime:datetime)`
- `fn_prd_ada_dom_pi_status(startTime:datetime, endTime:datetime)`
- `fn_prd_ada_dom_plans_status(startTime:datetime, endTime:datetime)`
- `fn_prd_ada_dom_meteodata_status(startTime:datetime, endTime:datetime)`
- `fn_prd_ada_dom_alarm_status(startTime:datetime, endTime:datetime)`
- `fn_prd_ada_dom_front_status(startTime:datetime, endTime:datetime)`
- `fn_prd_ada_dom_kpi_status(startTime:datetime, endTime:datetime)`
- `fn_prd_ada_dom_kpi_detalle_html(startTime:datetime, endTime:datetime)`
- `fn_prd_ada_dom_global_status(startTime:datetime, endTime:datetime)`

---

## Mapa de consumo de sources por dominio

### Usa `fn_src_pipeline_runs_all`
- `fn_prd_ada_dom_dispatch_status`
- `fn_prd_ada_dom_drillit_status`
- `fn_prd_ada_dom_blockgrade_status`

### Usa `fn_src_systemlogs_all`
- `fn_prd_ada_dom_pi_status`
- `fn_prd_ada_dom_plans_status`
- `fn_prd_ada_dom_meteodata_status`
- `fn_prd_ada_dom_alarm_status`
- `fn_prd_ada_dom_kpi_status`

### Usa `fn_src_ada_consolelogs`
- `fn_prd_ada_dom_alarm_status`
- `fn_prd_ada_dom_kpi_status`
- `fn_prd_ada_dom_kpi_detalle_html`
- `fn_prd_ada_alert_from_tables_lag`

### Quedan directas en dominio (uso único)
- `fn_prd_ada_dom_front_status` mantiene `AppServiceConsoleLogs` directo.
- `fn_prd_ada_dom_kpi_detalle_html` mantiene `Logs_MLP_ADA_CL` directo.

---

## Regla de performance aplicada
En dominios que consumen source helper compartido, se aplica **filtro temprano** por identificadores de dominio:
- `ResourceGroup`
- `JobName_s`
- `ContainerJobName_s`
- u otro equivalente.

Esto evita sobrecálculo por filtrar tarde después del `union`.

---

## Orden recomendado de implementación en LAW
1. Crear `sources/` (3 funciones).
2. Crear helpers cross-product (2 funciones).
3. Crear helper ADA-only (1 función).
4. Crear dominios (11 funciones), dejando `fn_prd_ada_dom_global_status` al final.
5. Reemplazar variables en Grafana por wrappers.

---

## Importante para LAW UI (body-only)
Los archivos en `law_functions_body_only/` contienen solo el body de cada función.
Al crear funciones en LAW UI, pega ese contenido en **Body** para evitar errores de guardado.
