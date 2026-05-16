# Cómo contribuir a AR Plugins

Cualquiera puede agregar un plugin. No hace falta pedir permiso — si el plugin tiene fuentes reales y datos útiles, bienvenido.

---

## Qué es un plugin

Un plugin es una carpeta con un `SKILL.md` que le dice a Claude qué hacer cuando ejecutás su comando. No hay código ejecutable: Claude busca los datos en fuentes oficiales en el momento en que preguntás.

Estructura mínima de un plugin:

```
mi-plugin/
├── plugin.json      # metadatos: name, version, description
├── SKILL.md         # definición del comando y comportamiento
├── README.md        # ejemplos con datos reales
└── .gitignore
```

---

## Proceso para publicar un plugin nuevo

### 1. Leer la especificación

Revisá [SPEC.md](./SPEC.md) para ver qué plugins están planeados o si tu idea ya existe.

### 2. Verificar las fuentes

Antes de escribir nada, confirmá que las URLs/APIs que vas a usar funcionan y devuelven datos reales. Usá WebFetch o curl para testear.

Fuentes aceptadas: sitios `.gob.ar`, APIs del INDEC, BCRA, ANSES, AFIP, datos abiertos nacionales o provinciales, fuentes periodísticas con datos primarios citados.

### 3. Crear el plugin localmente

```bash
mkdir /tmp/mi-plugin && cd /tmp/mi-plugin
```

Escribí en este orden:
1. `plugin.json` — name, version, description
2. `SKILL.md` — frontmatter con `name` y `description` en tercera persona, luego el comportamiento
3. `.gitignore`
4. `README.md` — ejemplos con datos reales (sin placeholders)

Ver [`.agents/plugins.md`](.agents/plugins.md) para la estructura detallada.

### 4. Validar

```bash
claude plugin validate /tmp/mi-plugin
```

### 5. Publicar el repo

```bash
cd /tmp/mi-plugin
git init && git add -A
git commit -m "feat: plugin <nombre> v1.0.0 — <descripcion corta>"
gh repo create <tu-usuario>/<nombre> --public \
  --description "Plugin de Claude Code — <descripcion>" \
  --source . --remote origin --push
```

El plugin puede vivir en tu propia cuenta de GitHub — no necesitás que sea bajo `kvothesson/`.

### 6. Agregar al marketplace

Abrí un PR a este repo modificando `.claude-plugin/marketplace.json` con la entrada de tu plugin.

Formato de la entrada:

```json
{
  "name": "mi-plugin",
  "description": "Qué hace en una línea",
  "source": "github",
  "repo": "tu-usuario/mi-plugin",
  "category": "economia | burocracia | salud | laburo | educacion | legal | medios | finanzas"
}
```

Ver [`.agents/marketplace.md`](.agents/marketplace.md) para el detalle completo.

---

## Checklist antes de abrir el PR

- [ ] `plugin.json` tiene `name`, `version` y `description`
- [ ] `SKILL.md` tiene frontmatter con `name` y `description` en tercera persona
- [ ] Cada URL de fetch verificada y funcional al momento de publicar
- [ ] Cada skill tiene formato de respuesta en bloque de código
- [ ] Cada skill tiene fallback cuando la fuente no responde
- [ ] `claude plugin validate` pasa sin errores
- [ ] README tiene ejemplos con datos reales (no placeholders)
- [ ] README tiene sección "Fuentes" con URLs
- [ ] Repo es público
- [ ] Entrada en `marketplace.json` tiene `category` correcta

---

## Modificar un plugin existente

Si encontrás un bug, una fuente caída o querés mejorar un plugin, el flujo es el mismo que para cualquier repo open source: fork → branch → PR.

```bash
gh repo clone kvothesson/<nombre> /tmp/<nombre>
cd /tmp/<nombre>
git checkout -b fix/<descripcion>
# editá lo necesario
git add -A && git commit -m "fix: <descripcion>"
git push origin fix/<descripcion>
gh pr create --title "<descripcion>" --body "Qué cambió y cómo se probó"
```

---

## Principios del ecosistema

- **Fuentes primarias:** siempre mostrar de dónde viene el dato y cuándo fue obtenido
- **Sin caché:** los datos son actuales porque Claude los busca en el momento
- **Lenguaje llano:** sin tecnicismos innecesarios, para cualquier persona
- **Una responsabilidad por plugin:** cada plugin hace una cosa bien

Ver [`.agents/principios.md`](.agents/principios.md) para el detalle completo.

---

## ¿Dudas?

Abrí un issue o usá el comando `/reportar` desde cualquier plugin del ecosistema.
