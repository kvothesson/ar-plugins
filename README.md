# AR Plugins

Plugins de Claude Code para vivir, trabajar y pensar en Argentina.
Datos reales, fuentes primarias, lenguaje llano.

---

## Plugins disponibles

| Plugin | Que hace |
|--------|----------|
| [arca](https://github.com/kvothesson/arca) | Dólar, inflación, sueldos en tiempo real |
| [tramite](https://github.com/kvothesson/tramite) | ANSES, ARCA/AFIP, DNI, registro automotor |
| [laburo](https://github.com/kvothesson/laburo) | Sueldos, paritarias, SMVM, tarifas freelance, CV |
| [derecho](https://github.com/kvothesson/derecho) | Marco legal: laboral, consumidor, contratos |
| [dato](https://github.com/kvothesson/dato) | INDEC, elecciones, catastro, jurisprudencia |
| [nodo](https://github.com/kvothesson/nodo) | Contexto personal persistente entre sesiones |
| [guita](https://github.com/kvothesson/guita) | Ingreso neto real, gastos con inflacion y runway por situacion laboral |

---

## Instalación

### 1. Clonar el plugin que necesitás

```bash
git clone https://github.com/kvothesson/arca ~/plugins/arca
```

Reemplazá `arca` con el nombre del plugin que quieras.

### 2. Abrir Claude Code apuntando a ese directorio

```bash
claude --plugin-dir ~/plugins/arca
```

Para usar varios plugins a la vez, pasá múltiples `--plugin-dir`:

```bash
claude --plugin-dir ~/plugins/arca --plugin-dir ~/plugins/tramite
```

### 3. Usar el comando del plugin

```
/arca dolar
/tramite anses jubilacion
/laburo sueldo desarrollador
```

---

## Ejemplos rápidos

### arca — economía en tiempo real

```
/arca

💵 Dólar — 3 may 2026

Oficial     $1.365  / $1.415
Blue        $1.380  / $1.400
MEP         $1.437  / $1.448
CCL         $1.492  / $1.494
Tarjeta     $1.774  / $1.839

Brecha blue vs oficial: +1,9%
```

```
/arca inflacion

📈 Inflación — IPC Nacional

Último mes (mar 2026):   3,38%
Últimos 12 meses:       32,61%
Acumulado 2026:          9,44%

Fuente: INDEC — apis.datos.gob.ar
```

### laburo — mercado laboral

```
/laburo sueldo desarrollador

## Sueldos — Desarrollador de Software (Argentina)

Junior (0–2 años):   $1.200.000 – $1.800.000 bruto/mes
Semi Senior (2–4):   $1.800.000 – $2.800.000 bruto/mes
Senior (4+):         $2.800.000 – $4.500.000+ bruto/mes

En dólares (blue):   u$s 850 – u$s 3.200/mes

Fuente: encuesta SysArg, encuesta Openqube — mayo 2026
```

### tramite — burocracia argentina

```
/tramite anses jubilacion

## Jubilación — ANSES

Requisitos:
- Mujeres: 60 años + 30 años de aportes
- Hombres: 65 años + 30 años de aportes

Haber mínimo vigente: $...  (se actualiza trimestralmente)
Turno online: mi.anses.gob.ar

Fuente: anses.gob.ar
```

### guita — finanzas personales

```
/guita repartidor

## Ingreso neto real — Repartidor de plataforma

Ingreso bruto:               $80.000/mes (4 semanas x $20.000)
  Combustible:               -$14.000/mes
  Mantenimiento moto:         -$6.000/mes
  Cuota unipersonal:         -$10.000/mes
  Internet celular:           -$2.000/mes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Neto estimado:               $48.000/mes
En dolares blue:             u$s 34/mes

Canasta basica:              $417.680 (INDEC, dic 2025)
SMVM vigente:                $363.000 (mayo 2026)

Fuente: INDEC / Secretaria de Trabajo / dolarapi.com — mayo 2026
```

```
/guita runway

Ahorros:     u$s 3.000 = $4.200.000 al blue
Gastos:      $688.000/mes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Runway nominal:   6.1 meses (hasta noviembre 2026)
Runway real:      5.6 meses (hasta octubre 2026)

La inflacion (3.05%/mes) te quita 0.5 meses de runway real.

Fuente: INDEC IPC / dolarapi.com — mayo 2026
```

---

## Cómo funcionan

Cada plugin es una carpeta con un `SKILL.md` que le dice a Claude qué hacer cuando usás su comando. No hay código ejecutable — es Claude el que busca los datos en fuentes oficiales en el momento en que preguntás.

Eso significa:
- Los datos son siempre actuales (no hay caché)
- Las fuentes son primarias (sitios .gob.ar, APIs del INDEC, etc.)
- Claude siempre muestra de dónde viene el dato y cuándo fue obtenido

---

## Agregar un plugin nuevo al marketplace

Ver [AGENT.md](./AGENT.md) — es el runbook completo para agentes y desarrolladores que quieran crear o actualizar plugins.

Resumen del flujo:

1. Leer el `SPEC.md` para entender qué plugin construir
2. Verificar que las fuentes (URLs/APIs) funcionen
3. Crear el plugin con la estructura estándar
4. Publicar en `kvothesson/<nombre>` como repo público
5. Agregar la entrada al `marketplace.json` de este repo

---

## Estado del marketplace

```bash
gh api repos/kvothesson/ar-plugins/contents/marketplace.json \
  | node -e "let d=''; process.stdin.on('data',c=>d+=c); process.stdin.on('end',()=>{const j=JSON.parse(d); console.log(Buffer.from(j.content,'base64').toString())})"
```
