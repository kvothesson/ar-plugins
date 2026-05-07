---
description: Skill de desarrollo para ar-plugins. Implementa issues con /dev resolver #N. Registra problemas detectados proactivamente con /dev reportar.
---

# Skill: /dev

## Comandos

### `/dev resolver #<número>`

Resolvé el issue indicado de `kvothesson/ar-plugins`, implementá el cambio, verificá que funcione y abrí un PR.

---

#### Paso 0 — Leer el issue y generar el plan

```bash
gh issue view <número> --repo kvothesson/ar-plugins
```

Antes de tocar cualquier archivo, determiná qué tipo de cambio es y generá la todolist con **TodoWrite**. Los ítems deben ser específicos para este issue — no genéricos. Ejemplos según tipo:

**Plugin nuevo:**
- [ ] Leer AGENT.md y SPEC.md
- [ ] Verificar fuentes: [url1], [url2] (una por skill planificada)
- [ ] Crear branch feat/issue-N-nombre
- [ ] Crear estructura: plugin.json, SKILL.md, README, .gitignore
- [ ] Testear cada comando del SKILL.md
- [ ] Verificar checklist completo
- [ ] Commit y push
- [ ] Agregar entrada a marketplace.json
- [ ] Actualizar README de ar-plugins si agrega skills/workflows
- [ ] Abrir PR

**Fix de plugin existente:**
- [ ] Leer AGENT.md
- [ ] Clonar repo kvothesson/<nombre>
- [ ] Crear branch fix/issue-N-descripcion
- [ ] Implementar el fix concreto: [qué hay que cambiar]
- [ ] Verificar que la URL/fuente afectada responde
- [ ] Commit y push
- [ ] Abrir PR

**Cambio en marketplace o docs:**
- [ ] Leer AGENT.md
- [ ] Crear branch y hacer el cambio puntual
- [ ] Commit y push
- [ ] Abrir PR

Marcá cada ítem como completado a medida que avanzás.

---

#### Paso 1 — Leer el contexto

Determiná el tipo de cambio:
- **Plugin nuevo** → seguir flujo completo
- **Fix o actualización de plugin existente** → clonar ese repo y modificar
- **Cambio en marketplace o docs** → modificar directamente en ar-plugins

---

#### Paso 2 — Leer el contexto

Siempre leer AGENT.md antes de tocar archivos:

```bash
gh api repos/kvothesson/ar-plugins/contents/AGENT.md --jq '.content' | base64 -d
```

Si es plugin nuevo, leer también SPEC.md para la descripción completa del plugin:

```bash
gh api repos/kvothesson/ar-plugins/contents/SPEC.md --jq '.content' | base64 -d
```

Para ver un plugin de referencia:

```bash
gh api repos/kvothesson/arca/contents/skills/arca/SKILL.md --jq '.content' | base64 -d
```

---

#### Paso 3 — Verificar fuentes

Para cada skill del plugin, verificá que las URLs funcionen **antes de escribir el SKILL.md**:

- WebFetch a cada URL → ¿responde? ¿datos legibles y útiles?
- Si falla → buscar alternativa con WebSearch `site:<organismo>.gob.ar [tema]`
- Guardar qué URLs funcionaron — son las que van en el SKILL.md y en los ejemplos del README

Sin URLs verificadas no se escribe el SKILL.md.

---

#### Paso 4 — Crear branch y clonar

**Para cambios en ar-plugins directamente:**

```bash
gh repo clone kvothesson/ar-plugins /tmp/ar-plugins-fix-<N>
cd /tmp/ar-plugins-fix-<N>
git checkout -b feat/issue-<N>-<descripción-corta>
```

**Para cambios en el repo de un plugin:**

```bash
gh repo clone kvothesson/<nombre> /tmp/<nombre>-fix-<N>
cd /tmp/<nombre>-fix-<N>
git checkout -b fix/issue-<N>-<descripción-corta>
```

**Para plugin nuevo (repo propio):**

```bash
mkdir -p /tmp/<nombre>/.claude-plugin
mkdir -p /tmp/<nombre>/skills/<nombre>
cd /tmp/<nombre>
git init
```

---

#### Paso 5 — Implementar

**Estructura obligatoria de todo plugin:**

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

**plugin.json:**

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

**Reglas del SKILL.md (nunca violarlas):**
- Frontmatter con `description` obligatorio
- Nunca hardcodear montos, fechas ni requisitos — siempre WebFetch/WebSearch a fuente primaria
- URL exacta a fetchear para cada comando
- Formato de respuesta con bloque de código de ejemplo
- Fallback si la URL principal falla
- Sección de tono al final
- Siempre mostrar fuente y fecha del dato en la respuesta

**Para fix/actualización:** solo modificar lo pedido. Sin refactors no solicitados.

---

#### Paso 6 — Testear

Para cada comando del SKILL.md, ejecutá las búsquedas/fetches que el skill haría en producción y verificá resultados. Usá esos datos reales para escribir los ejemplos del README — sin placeholders.

Checklist antes de continuar:

- [ ] `plugin.json` tiene name, version, description y skills correctos
- [ ] `SKILL.md` tiene frontmatter con `description`
- [ ] Cada URL de fetch verificada y funcional
- [ ] Cada skill tiene formato de respuesta definido en bloque de código
- [ ] Cada skill tiene fallback
- [ ] README del plugin tiene ejemplos con datos reales (no `$XX.XX` ni `[monto]`)
- [ ] README del plugin tiene sección "Fuentes" con URLs
- [ ] `.gitignore` existe
- [ ] Si el cambio agrega skills o workflows nuevos: README de ar-plugins actualizado

---

#### Paso 7 — Commit y push

**Para plugin existente (fix):**

```bash
git add -A
git commit -m "fix: <descripción corta> (closes #<N>)"
git push origin <branch>
```

**Para plugin nuevo:**

```bash
git add -A
git commit -m "feat: plugin <nombre> v1.0.0"
gh repo create kvothesson/<nombre> --public \
  --description "Plugin de Claude Code — <descripción>" \
  --source . --remote origin --push
```

---

#### Paso 8 — Actualizar marketplace.json (si aplica)

Si el cambio agrega un plugin nuevo o modifica su versión, actualizar `.claude-plugin/marketplace.json` en ar-plugins:

```bash
# Editar .claude-plugin/marketplace.json en el branch actual:
# - Plugin nuevo: agregar entrada al array "plugins"
# - Versión actualizada: cambiar "version" en la entrada existente
git add .claude-plugin/marketplace.json
git commit -m "feat: agrega <nombre> al marketplace"
```

---

#### Paso 9 — Abrir el PR

```bash
gh pr create \
  --repo kvothesson/ar-plugins \
  --title "<descripción corta>" \
  --body "Closes #<N>

## Qué hace
<descripción del cambio>

## Cómo se testeó
<URLs verificadas, datos obtenidos, fallbacks probados>"
```

---

### `/dev reportar`

Registrá un issue accionable en el repo correcto cuando detectás un problema mientras trabajás con un plugin o con el ecosistema.

Usalo explícitamente (`/dev reportar`) o dejá que el agente lo proponga solo cuando detecte algo que vale la pena registrar.

---

#### Paso 1 — Decidir si vale la pena abrir un issue

Abrí un issue si y solo si el problema cumple las tres condiciones:

1. **Es accionable**: otro agente puede resolverlo solo con la info del issue, sin contexto de esta sesión.
2. **Es concreto**: no "podría mejorarse", sino "la URL X retorna 404" o "el comando Y no cubre el caso Z".
3. **Tiene impacto real**: afecta a un usuario que intente usar el plugin/ecosistema hoy.

No abras un issue si el problema es vago, trivial (typo menor, preferencia de estilo) o si ya lo mencionaste en el chat y el usuario lo va a resolver en esta misma sesión.

**Casos típicos que justifican abrir:**
- Una URL del SKILL.md no responde o cambió de dominio
- El usuario pidió algo que el plugin casi cubre pero le falta un caso concreto
- Hay un edge case que el SKILL.md no contempla y que va a aparecer frecuentemente
- Falta un subcomando que sería evidente para cualquier usuario del plugin
- El AGENT.md o SPEC.md tiene información desactualizada o contradictoria

**Casos que NO justifican abrir:**
- "Sería bueno mejorar el tono de la respuesta"
- Un problema que ya se resolvió en esta sesión
- Algo que el usuario no pidió y cuyo valor es discutible

---

#### Paso 2 — Determinar dónde va el issue

El ecosistema tiene dos destinos posibles:

| Repo destino | Cuándo |
|---|---|
| `kvothesson/<nombre-del-plugin>` | El problema es específico de un plugin: SKILL.md roto, fuente caída, edge case de ese plugin, mejora de comportamiento de ese plugin |
| `kvothesson/ar-plugins` | El problema es del ecosistema: AGENT.md desactualizado, SPEC.md incorrecto, tooling de dev (`/dev resolver`), marketplace.json, estructura del sistema |

**Cómo detectar de cuál es:**
- ¿Estabas usando o analizando un plugin específico cuando detectaste el problema? → repo del plugin
- ¿El problema afecta a cómo se desarrolla o publica cualquier plugin? → `ar-plugins`
- ¿El problema es una URL o comportamiento de una skill específica? → repo del plugin
- ¿No está claro? → `ar-plugins` con un label de triage

```bash
# Para identificar el nombre del plugin activo:
# Si estás en el repo clonado: el nombre es el directorio
# Si estás en conversación: el plugin que el usuario invocó o mencionó
```

---

#### Paso 3 — Verificar que no existe un issue similar

```bash
# Buscar en el repo destino
gh issue list --repo kvothesson/<repo-destino> --state open --search "<palabras clave del problema>"

# Si aparece algo parecido: mencionarlo al usuario y preguntar si igual querés abrir uno nuevo
# Si no aparece nada: continuar
```

No dupliques issues. Si existe uno abierto que cubre el mismo problema, mencioná el número en el chat y no abras uno nuevo.

---

#### Paso 4 — Redactar el issue

Formato estándar — siempre seguirlo:

**Título:** `[tipo]: descripción concreta en una línea`

Tipos válidos:
- `fix` — algo roto (URL caída, comportamiento incorrecto)
- `feat` — algo que falta y tiene valor claro
- `source` — fuente de datos cambió o dejó de responder
- `edge-case` — caso no cubierto por el SKILL.md actual

**Body:**

```markdown
## Contexto

<Una o dos oraciones: en qué situación se detectó el problema. Sin datos personales del usuario.>

## Problema

<Qué falla o qué falta. Específico y accionable.>

## Cómo reproducir / evidencia

<URL que falló, comando que se intentó, respuesta que se obtuvo vs la esperada. Si aplica.>

## Propuesta (opcional)

<Solo si tenés una idea concreta de cómo resolverlo. No es obligatorio.>
```

No incluyas nombres ni datos del usuario. No incluyas especulaciones. No incluyas info que solo tenga sentido en esta sesión.

---

#### Paso 5 — Mostrárselo al usuario y pedir aprobación

Antes de abrir cualquier issue, mostrar el borrador completo en el chat:

```
Detecté algo que vale registrar como issue. ¿Lo abro?

Repo: kvothesson/<repo-destino>
Título: [tipo]: descripción
Body:
---
[contenido del body]
---
```

Esperá una respuesta afirmativa antes de continuar. Si el usuario dice que no, o pide ajustes, incorporalos antes de abrir.

---

#### Paso 6 — Abrir el issue

Solo después de la aprobación del usuario:

```bash
gh issue create \
  --repo kvothesson/<repo-destino> \
  --title "[tipo]: descripción concreta" \
  --body "$(cat <<'EOF'
## Contexto

<contexto>

## Problema

<problema>

## Cómo reproducir / evidencia

<evidencia>
EOF
)"
```

Compartí el link del issue abierto en el chat.

---

## Tono del proceso

- Seguir AGENT.md al pie de la letra — es el contrato de calidad del ecosistema
- Resolver con sentido común ante ambigüedad, sin preguntar lo obvio
- Si algo está bloqueado (URL caída, permisos), informar el blocker concretamente antes de seguir

---

## Referencias

Recursos a consultar según lo que pida el issue — no son siempre necesarios, usarlos cuando aplique:

| Cuándo | Recurso |
|---|---|
| El issue involucra crear o modificar una skill | [Documentación de skills](https://code.claude.com/docs/en/skills) |
| Necesitás descubrir otras páginas de docs | [Índice completo de docs](https://code.claude.com/docs/llms.txt) |
| El issue involucra la estructura de un plugin | AGENT.md del repo (Paso 2) |
| El issue involucra un plugin específico | SPEC.md del repo (Paso 2) |
