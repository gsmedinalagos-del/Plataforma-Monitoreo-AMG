# Análisis técnico ADA (variables de dashboard)

Fuente inspeccionada: `Plataforma_Monitoreo_AMG.json` (único JSON model encontrado en el repo).

## Inventario de variables ADA

| Variable | Largo KQL (chars) | joins | summarize | where | Extracción final |
|---|---:|---:|---:|---:|---|
| `var_mlp_ada_ingestas_global` | 38959 | 8 | 9 | 41 | `(ALERT)` |
| `var_mlp_ada_global` | 41973 | 8 | 9 | 39 | `(ALERT)` |
| `var_mlp_ada_pi` | 37301 | 8 | 9 | 34 | `PI:(\w+)` |
| `var_mlp_ada_meteodata` | 37480 | 8 | 9 | 34 | `Meteodata:(\w+)` |
| `var_mlp_ada_kpi` | 11638 | 0 | 2 | 6 | `(sin extract final / lógica propia)` |
| `var_mlp_ada_alarm` | 37654 | 8 | 9 | 30 | `Alarmas:(\w+)` |
| `var_mlp_ada_front` | 37368 | 8 | 9 | 34 | `Front:(\w+)` |
| `var_mlp_ada_dispatch` | 41330 | 8 | 9 | 39 | `Dispatch:(\w+)` |
| `var_mlp_ada_drillit` | 34979 | 8 | 9 | 30 | `Drillit:(\w+)` |
| `var_mlp_ada_blockgrade` | 41026 | 8 | 9 | 42 | `Blockgrade:(\w+)` |
| `var_mlp_ada_plans` | 41922 | 8 | 9 | 39 | `Plans:(\w+)` |

## Hallazgos de duplicación

- Se observaron dos familias de KQL casi idénticas:
  - Familia A (ingestas + agregación completa): `var_mlp_ada_global`, `var_mlp_ada_dispatch`, `var_mlp_ada_blockgrade`, `var_mlp_ada_plans`.
  - Familia B (ingestas + agregación completa simplificada): `var_mlp_ada_pi`, `var_mlp_ada_meteodata`, `var_mlp_ada_front`, `var_mlp_ada_alarm`.
- En ambas familias, la diferencia principal está al final (regex en `extract()` sobre `mapa`) para quedarse con un subconjunto específico.
- `var_mlp_ada_kpi` sí es una query separada y más corta, enfocada en KPIs sin datos y no replica toda la familia de ingestas.
- `var_mlp_ada_ingestas_global` calcula la misma base de estado transversal y termina con estado global (ALERT/OK), pero no está activo visualmente (referencia comentada).

## Evidencia de uso en el dashboard (HTML/text panel)

- Se usa `${var_mlp_ada_global:raw}` para el chip ADA global.
- Se usan `${var_mlp_ada_dispatch:raw}`, `${var_mlp_ada_drillit:raw}`, `${var_mlp_ada_pi:raw}`, `${var_mlp_ada_plans:raw}`, `${var_mlp_ada_blockgrade:raw}`, `${var_mlp_ada_meteodata:raw}`, `${var_mlp_ada_kpi:raw}`, `${var_mlp_ada_alarm:raw}`, `${var_mlp_ada_front:raw}` en el resumen ADA.
- `${var_mlp_ada_ingestas_global:raw}` aparece comentada (no activa) dentro del HTML.

## Estrategia de optimización propuesta

1. Crear una sola variable base ADA (ej. `var_mlp_ada_base`) que devuelva en una fila todos los estados (`Dispatch`, `PI`, `Drillit`, `Blockgrade`, `Plans`, `KPIs`, `Alarmas`, `Front`) y opcionalmente el `mapa` serializado.
2. Reemplazar variables específicas por expresiones livianas derivadas de esa base (si el dashboard lo permite) o por una sola query adicional muy corta que lea la salida base y proyecte cada color (evitando recalcular joins/summarize pesados).
3. Mantener compatibilidad gradual:
   - Fase 1: introducir nueva base sin eliminar variables actuales.
   - Fase 2: migrar chips uno a uno.
   - Fase 3: eliminar variables duplicadas cuando se confirme paridad visual/funcional.

## Riesgos a validar

- Dependencia del panel de texto con interpolación `${var:raw}`.
- Orden de evaluación/refresh de variables (evitar cambios de timing).
- Diferencias de regex finales (`Dispatch` vs `NRT Dispatch` en ciertos mapas) antes de consolidar.
- Validar exactitud comparando color viejo vs nuevo durante al menos 1 semana operativa.
