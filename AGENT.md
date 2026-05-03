# AGENT.md — AR Plugins: Runbook para agentes

Este archivo es el punto de entrada para cualquier agente que necesite **crear un plugin nuevo**, **actualizar uno existente** o **hacer cambios al marketplace**. Leé esto antes de tocar cualquier archivo.

---

## 0. Contexto del ecosistema

AR Plugins es un conjunto de plugins de Claude Code para el contexto argentino. El objetivo: datos reales, fuentes primarias, lenguaje llano.

- **Marketplace:** `kvothesson/ar-plugins` — `marketplace.json` lista todos los plugins publicados
- **SPEC:** `SPEC.md` en este mismo repo — describe todos los plugins planificados, su propósito y skills
- **Plugins publicados:** cada uno vive en su propio repo `kvothesson/<nombre>`
- **Modelos de referencia:** [`kvothesson/arca`](https://github.com/kvothesson/arca) y [`kvothesson/tramite`](https://github.com/kvothesson/tramite)

---

## 1. Estructura de un plugin

Todo plugin tiene esta estructura exacta:

```
<nombre>/
  .claude-plugin/
    plugin.json       <- metadata del plugin
  skills/
    <nombre>/
      SKILL.md        <- instrucciones para Claude: que hacer con cada comando
  README.md           <- documentacion para humanos con ejemplos reales de output
  .gitignore
```

### `plugin.json`

```json
{
  "name": "<nombre>",
  "version": "1.0.0",
  "description": "<descripcion corta sin emojis>",
  "skills": [
    {
      "name": "<nombre>",
      "path": "skills/<nombre>/SKILL.md"
    }
  ]
}
```

### `SKILL.md`

Empieza con frontmatter:

```markdown
---
description: <Una oracion. Que hace el plugin. Cuando usarlo. Que keywords lo disparan.>
---
```

Luego el cuerpo: comandos con su formato de respuesta, URLs a fetchear, manejo de errores, tono.

**Reglas para el SKILL.md:**
- Nunca hardcodear montos, fechas ni requisitos — siempre WebFetch o WebSearch a fuente primaria
- Especificar la URL exacta a fetchear para cada comando
- Definir el formato de respuesta con un bloque de codigo de ejemplo
- Incluir fallback si la URL principal falla
- Seccion de tono al final
- Siempre mostrar fuente y fecha del dato en la respuesta al usuario

### `README.md`

Documentacion para humanos. Incluye:
1. Que hace el plugin (2-3 lineas)
2. Instalacion (`claude --plugin-dir /ruta`)
3. Un ejemplo real de output por cada comando — con datos actuales, no placeholders
4. Seccion de fuentes con URLs

**Los ejemplos del README deben ser reales.** Antes de escribirlos, hace WebSearch o WebFetch para obtener datos del momento. No uses `$XX.XX` ni `[monto]`.

### `.gitignore`

```
.DS_Store
*.log
```

---

## 2. Como crear un plugin nuevo

### Paso 1 — Leer el SPEC

```bash
gh api repos/kvothesson/ar-plugins/contents/SPEC.md \
  | python -c "import sys,json,base64; d=json.load(sys.stdin); print(base64.b64decode(d['content']).decode())"
```

Identifica el plugin a construir. El SPEC tiene: descripcion, problema que resuelve, skills y fuentes sugeridas.

### Paso 2 — Explorar fuentes

Antes de escribir el SKILL.md, verifica que las URLs/APIs funcionen. Para cada skill:

- **Si hay API publica:** hace WebFetch a la URL y comprueba que devuelve datos utiles
- **Si no hay API:** hace WebSearch con `site:<organismo>.gob.ar [tema]` y verifica resultados
- **Anota** que URLs funcionaron — las vas a usar en el SKILL.md y en los ejemplos del README

### Paso 3 — Crear directorio local y escribir archivos

```bash
mkdir -p /tmp/<nombre>/.claude-plugin
mkdir -p /tmp/<nombre>/skills/<nombre>
```

Orden de escritura: `plugin.json` -> `SKILL.md` -> `.gitignore` -> `README.md` (despues de testear fuentes).

### Paso 4 — Testear cada skill

Para cada comando del SKILL.md, ejecuta las busquedas/fetches que el skill haria en produccion:
- La URL responde?
- Los datos son legibles y utiles?
- El fallback funciona si la URL principal falla?

Usa los datos reales obtenidos para escribir los ejemplos del README.

### Paso 5 — Crear repo y publicar

```bash
cd /tmp/<nombre>
git init
git add -A
git commit -m "feat: plugin <nombre> v1.0.0 — <descripcion corta>"
gh repo create kvothesson/<nombre> --public \
  --description "Plugin de Claude Code — <descripcion>" \
  --source . --remote origin --push
```

### Paso 6 — Actualizar el marketplace

```bash
# Clonar en directorio temporal
gh repo clone kvothesson/ar-plugins /tmp/ar-plugins

# Editar /tmp/ar-plugins/marketplace.json:
# Agregar al array "plugins":
# {
#   "name": "<nombre>",
#   "description": "<descripcion>",
#   "repository": "https://github.com/kvothesson/<nombre>",
#   "version": "1.0.0"
# }

cd /tmp/ar-plugins
git add marketplace.json
git commit -m "feat: agrega <nombre> al marketplace"
git push

rm -rf /tmp/ar-plugins
```

---

## 3. Como actualizar un plugin existente

### Actualizar un skill o corregir URLs

```bash
gh repo clone kvothesson/<nombre> /tmp/<nombre>
# editar los archivos necesarios
cd /tmp/<nombre>
git add -A
git commit -m "fix: <descripcion del cambio>"
git push
rm -rf /tmp/<nombre>
```

### Convencion de versiones

- `1.0.x` — fixes y actualizaciones de URLs/datos
- `1.x.0` — skills nuevas o cambios de comportamiento
- `x.0.0` — refactor estructural o cambio de fuentes principales

Si el cambio es significativo, actualiza `version` en `plugin.json` y luego en `marketplace.json`:

```bash
gh repo clone kvothesson/ar-plugins /tmp/ar-plugins
# editar marketplace.json: cambiar "version" del plugin correspondiente
cd /tmp/ar-plugins
git add marketplace.json
git commit -m "chore: bumps <nombre> a v<nueva-version>"
git push
rm -rf /tmp/ar-plugins
```

---

## 4. Principios que nunca se negocian

| Principio | Como aplicarlo |
|-----------|----------------|
| **Sin hardcodear datos que cambian** | Montos, fechas, requisitos: siempre WebFetch/WebSearch a fuente primaria |
| **Fuente primaria siempre** | Sites oficiales (.gob.ar). Medios solo si el organismo no publica algo directamente |
| **Siempre mostrar fecha y fuente** | Cada bloque de respuesta incluye `Fuente: [organismo] — [url]` y fecha del dato |
| **Lenguaje llano** | Pasos concretos, sin jerga institucional. El usuario tiene que poder actuar con lo que lee |
| **Privacidad** | No pedir ni transmitir datos del usuario. CUIL, DNI, claves: el usuario los ingresa el solo |
| **Fallback** | Si la URL principal no responde, el skill tiene una alternativa (otra URL o WebSearch) |

---

## 5. Plugins pendientes (por prioridad)

Ver `SPEC.md` para descripcion completa y skills de cada uno.

| Plugin | Prioridad | Fuentes sugeridas |
|--------|-----------|-------------------|
| `laburo` | Media | Encuesta sueldos SysArg, LinkedIn, remotar.com |
| `derecho` | Media | infoleg.gob.ar, saij.gob.ar, mpd.gov.ar |
| `dato` | Media | apis.datos.gob.ar, datasets.gob.ar, INDEC |
| `salud` | Normal | sssalud.gob.ar, pami.org.ar |
| `startup` | Normal | agencia.gob.ar, FONTAR |
| `medios` | Normal | multiples fuentes, requiere WebSearch |
| `educacion` | Normal | becas.gob.ar, universidades nacionales |

---

## 6. Checklist antes de publicar un plugin nuevo

- [ ] `plugin.json` tiene `name`, `version`, `description` y `skills` correctos
- [ ] `SKILL.md` tiene frontmatter con `description`
- [ ] Cada skill tiene su URL de fetch verificada y funcional
- [ ] Cada skill tiene formato de respuesta definido en bloque de codigo
- [ ] Cada skill tiene fallback si la URL principal falla
- [ ] README tiene ejemplos con datos reales (no placeholders)
- [ ] README tiene seccion "Fuentes" con URLs
- [ ] `.gitignore` existe
- [ ] Repo creado bajo `kvothesson/<nombre>` con `--public`
- [ ] `marketplace.json` actualizado con el nuevo plugin

---

## 7. Comandos de referencia rapida

```bash
# Ver plugins actuales en marketplace
gh api repos/kvothesson/ar-plugins/contents/marketplace.json \
  | python -c "import sys,json,base64; d=json.load(sys.stdin); print(base64.b64decode(d['content']).decode())"

# Ver SPEC completo
gh api repos/kvothesson/ar-plugins/contents/SPEC.md \
  | python -c "import sys,json,base64; d=json.load(sys.stdin); print(base64.b64decode(d['content']).decode())"

# Ver SKILL.md de tramite (referencia)
gh api repos/kvothesson/tramite/contents/skills/tramite/SKILL.md \
  | python -c "import sys,json,base64; d=json.load(sys.stdin); print(base64.b64decode(d['content']).decode())"

# Ver SKILL.md de arca (referencia)
gh api repos/kvothesson/arca/contents/skills/arca/SKILL.md \
  | python -c "import sys,json,base64; d=json.load(sys.stdin); print(base64.b64decode(d['content']).decode())"

# Ver README de cualquier plugin
gh api repos/kvothesson/<nombre>/contents/README.md \
  | python -c "import sys,json,base64; d=json.load(sys.stdin); print(base64.b64decode(d['content']).decode())"
```
