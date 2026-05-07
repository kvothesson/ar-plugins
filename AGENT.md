# AGENT.md — AR Plugins

Punto de entrada para cualquier agente o desarrollador que trabaje en este ecosistema.
Lee esto completo antes de tocar cualquier archivo.

---

## Indice

1. [Que es esto](#1-que-es-esto)
2. [Arquitectura del ecosistema](#2-arquitectura-del-ecosistema)
3. [El marketplace](#3-el-marketplace)
4. [Plugins](#4-plugins)
5. [Skills](#5-skills)
6. [Workflows de desarrollo](#6-workflows-de-desarrollo)
7. [Principios](#7-principios)
8. [Referencias](#8-referencias)

---

## 1. Que es esto

AR Plugins es un marketplace de plugins de Claude Code para el ecosistema argentino. Cada plugin conecta a Claude con datos reales de Argentina — organismos oficiales, APIs publicas, fuentes primarias — y los expone como skills invocables desde Claude Code.

**Objetivo:** datos reales, fuentes primarias, lenguaje llano. Sin intermediarios, sin hardcodear valores que cambian.

---

## 2. Arquitectura del ecosistema

```
kvothesson/ar-plugins                  <- este repo
  .claude-plugin/
    marketplace.json                   <- indice de todos los plugins publicados
    plugin.json                        <- ar-plugins como plugin instalable (skills de dev)
  skills/
    dev/
      SKILL.md                         <- /dev resolver #N (workflow de desarrollo)
  AGENT.md                             <- este archivo (primer contacto)
  SPEC.md                              <- spec de todos los plugins planificados
  README.md                            <- documentacion publica del marketplace

kvothesson/<nombre>                    <- cada plugin vive en su propio repo
  .claude-plugin/
    plugin.json                        <- metadata del plugin
  skills/
    <nombre>/
      SKILL.md                         <- instrucciones para Claude
  README.md                            <- documentacion para usuarios
  .gitignore
```

**Regla central:** el repo `ar-plugins` es solo el indice y el tooling de desarrollo. El codigo de cada plugin vive en su propio repo bajo `kvothesson/<nombre>`.

---

## 3. El marketplace

`marketplace.json` es el indice central. Lista todos los plugins publicados con nombre, descripcion, repo y version.

Para ver el estado actual:

```bash
gh api repos/kvothesson/ar-plugins/contents/.claude-plugin/marketplace.json --jq '.content' | base64 -d
```

Cada entrada tiene esta forma:

```json
{
  "name": "<nombre>",
  "description": "<descripcion corta>",
  "author": { "name": "kvothesson" },
  "source": {
    "source": "git",
    "url": "https://github.com/kvothesson/<nombre>.git"
  },
  "homepage": "https://github.com/kvothesson/<nombre>"
}
```

Actualizar `marketplace.json` es el ultimo paso al publicar un plugin nuevo o cambiar su version.

---

## 4. Plugins

### Estructura obligatoria

Todo plugin tiene exactamente esta estructura:

```
<nombre>/
  .claude-plugin/
    plugin.json
  skills/
    <nombre>/
      SKILL.md
  README.md
  .gitignore
```

### plugin.json

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

### README.md

Documentacion para humanos. Incluye:
1. Que hace el plugin (2-3 lineas)
2. Instalacion: `claude --plugin-dir /ruta/al/plugin`
3. Un ejemplo real de output por cada comando — con datos del momento, no placeholders
4. Seccion "Fuentes" con URLs

**Los ejemplos deben ser reales.** Antes de escribirlos, hace WebFetch/WebSearch y usa los datos obtenidos. Nunca `$XX.XX` ni `[monto]`.

### .gitignore

```
.DS_Store
*.log
```

### Convencion de versiones

- `1.0.x` — fixes y actualizaciones de URLs/datos
- `1.x.0` — skills nuevas o cambios de comportamiento
- `x.0.0` — refactor estructural o cambio de fuentes principales

### Plugins publicados y pendientes

Ver `SPEC.md` para la descripcion completa de cada plugin — problema que resuelve, skills planificadas y fuentes sugeridas.

```bash
gh api repos/kvothesson/ar-plugins/contents/SPEC.md --jq '.content' | base64 -d
```

---

## 5. Skills

Una skill es un archivo `SKILL.md` que le dice a Claude que hacer cuando el usuario invoca un comando (`/nombre`) o cuando el contexto lo requiere.

### Estructura minima de un SKILL.md

El frontmatter `description` es obligatorio — Claude lo usa para decidir cuando activar la skill automaticamente.

```markdown
---
description: Una oracion. Que hace. Cuando usarlo. Keywords que lo disparan.
---

## Comandos

### /nombre subcomando

Instrucciones para Claude. URL exacta a fetchear. Formato de respuesta esperado.

Fetch: https://api.ejemplo.com/datos

## Manejo de errores

Si la URL principal no responde: [fallback concreto].

## Tono

[Como debe sonar Claude al responder]
```

### Reglas que nunca se violan

- Frontmatter con `description` obligatorio
- Nunca hardcodear montos, fechas ni requisitos — siempre WebFetch/WebSearch a fuente primaria
- URL exacta a fetchear para cada comando
- Formato de respuesta definido con bloque de codigo de ejemplo
- Fallback si la URL principal falla
- Siempre mostrar fuente y fecha del dato en la respuesta

### Referencia oficial de skills

Para el spec completo de frontmatter, argumentos, invocacion, subagents y patrones avanzados:

**https://code.claude.com/docs/en/skills**

Indice de toda la documentacion disponible: https://code.claude.com/docs/llms.txt

---

## 6. Workflows de desarrollo

### Resolver un issue

La skill `/dev resolver #N` implementa el flujo completo: leer el issue, entender que hay que hacer, verificar fuentes, implementar, testear y abrir un PR.

```bash
/dev resolver #5
```

Ver `skills/dev/SKILL.md` para el detalle paso a paso.

### Cargar un issue proactivo

Cuando un agente detecta un caso no cubierto, una fuente caida o una mejora obvia mientras trabaja con un plugin, puede registrarlo como issue en lugar de solo mencionarlo en el chat.

**Estado:** en desarrollo — ver [issue #4](https://github.com/kvothesson/ar-plugins/issues/4).

El criterio de cuando cargar y el formato estandar se esta definiendo iterativamente. Por ahora: si encontras algo que vale registrar, cargalo con titulo descriptivo y contexto suficiente para que otro agente lo resuelva sin esta conversacion.

### Crear un plugin nuevo (paso a paso)

1. Leer SPEC.md para entender que hay que construir
2. Verificar que las URLs/APIs funcionen con WebFetch antes de escribir el SKILL.md
3. Crear el directorio local con la estructura obligatoria
4. Escribir en orden: `plugin.json` -> `SKILL.md` -> `.gitignore` -> `README.md`
5. Testear cada comando del SKILL.md (fetch real, fallback)
6. Crear el repo bajo `kvothesson/<nombre>` y pushear
7. Actualizar `marketplace.json` en este repo

```bash
# Paso 6 — crear repo
cd /tmp/<nombre>
git init && git add -A
git commit -m "feat: plugin <nombre> v1.0.0 — <descripcion corta>"
gh repo create kvothesson/<nombre> --public \
  --description "Plugin de Claude Code — <descripcion>" \
  --source . --remote origin --push

# Paso 7 — actualizar marketplace
gh repo clone kvothesson/ar-plugins /tmp/ar-plugins-mkt
cd /tmp/ar-plugins-mkt
# editar .claude-plugin/marketplace.json — agregar la entrada nueva
git add .claude-plugin/marketplace.json
git commit -m "feat: agrega <nombre> al marketplace"
git push && rm -rf /tmp/ar-plugins-mkt
```

### Actualizar un plugin existente

```bash
gh repo clone kvothesson/<nombre> /tmp/<nombre>
cd /tmp/<nombre>
git checkout -b fix/<descripcion>
# editar lo necesario
git add -A && git commit -m "fix: <descripcion>"
git push origin fix/<descripcion>
gh pr create --repo kvothesson/<nombre> \
  --title "<descripcion>" \
  --body "Describe el cambio y como se teseto"
rm -rf /tmp/<nombre>
```

### Checklist antes de publicar

- [ ] `plugin.json` tiene name, version, description y skills correctos
- [ ] `SKILL.md` tiene frontmatter con `description`
- [ ] Cada URL de fetch verificada y funcional
- [ ] Cada skill tiene formato de respuesta definido en bloque de codigo
- [ ] Cada skill tiene fallback operativo
- [ ] README tiene ejemplos con datos reales (no placeholders)
- [ ] README tiene seccion "Fuentes" con URLs
- [ ] `.gitignore` existe
- [ ] Repo creado bajo `kvothesson/<nombre>` con `--public`
- [ ] `marketplace.json` actualizado

---

## 7. Principios

| Principio | Como aplicarlo |
|-----------|----------------|
| **Sin hardcodear datos que cambian** | Montos, fechas, requisitos: siempre WebFetch/WebSearch a fuente primaria |
| **Fuente primaria siempre** | Sites oficiales (.gob.ar). Medios solo si el organismo no publica algo directamente |
| **Siempre mostrar fecha y fuente** | Cada bloque de respuesta incluye fuente y fecha del dato |
| **Lenguaje llano** | Pasos concretos, sin jerga institucional. El usuario tiene que poder actuar con lo que lee |
| **Privacidad** | No pedir ni transmitir datos del usuario. CUIL, DNI, claves: el usuario los ingresa el solo |
| **Fallback** | Si la URL principal no responde, el skill tiene una alternativa (otra URL o WebSearch) |

---

## 8. Referencias

| Recurso | Donde |
|---------|-------|
| Spec de plugins planificados | `SPEC.md` en este repo |
| Documentacion oficial de skills | https://code.claude.com/docs/en/skills |
| Indice completo de docs de Claude Code | https://code.claude.com/docs/llms.txt |
| Plugin de referencia — economia | https://github.com/kvothesson/arca |
| Plugin de referencia — tramites | https://github.com/kvothesson/tramite |
| Issues y roadmap | https://github.com/kvothesson/ar-plugins/issues |
| Workflow resolver issue | `skills/dev/SKILL.md` en este repo |
