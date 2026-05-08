# Skills

Una skill es un `SKILL.md` que le dice a Claude que hacer cuando el usuario invoca un comando o el contexto lo requiere.

## Frontmatter obligatorio

```markdown
---
name: nombre-skill
description: "Obtiene cotizacion del dolar". "Consulta el precio oficial y blue". Activar cuando el usuario pregunta por el tipo de cambio o el valor del dolar.
---
```

`name` y `description` son obligatorios. Sin ellos Claude no puede auto-activar la skill.

## Formato del description

Tercera persona. Frases de activacion entre comillas dobles que imitan lo que diria el usuario. Terminar con una oracion explicando cuando activar.

| Aspecto | Correcto | Incorrecto |
|---------|----------|------------|
| Persona | "Obtiene...", "Consulta..." | "Debes obtener...", "Te ayudo a..." |
| Frases de activacion | Entre comillas dobles | Sin comillas |
| Instrucciones en el body | Imperativo: "Fetchear la URL", "Mostrar el resultado" | Segunda persona: "Debes fetchear" |

## Estructura del body

```markdown
## Comandos

### /nombre subcomando

Instrucciones para Claude. URL exacta a fetchear. Formato de respuesta esperado.

Fetch: https://api.ejemplo.com/datos

## Manejo de errores

Si la URL principal no responde: [fallback concreto — otra URL o WebSearch].

## Tono

[Como debe sonar Claude al responder]
```

## Progressive disclosure — subdirectorios opcionales

```
skills/<nombre>/
  SKILL.md
  references/    <- specs, docs, schemas que Claude carga bajo demanda
  examples/      <- ejemplos de uso real
  scripts/       <- scripts bash o Python que el skill puede ejecutar
```

La mayoria de plugins de este ecosistema no necesitan estos subdirectorios.

## Reglas que nunca se violan

- Frontmatter con `name` y `description` obligatorio
- Nunca hardcodear montos, fechas ni requisitos — siempre WebFetch/WebSearch a fuente primaria
- URL exacta a fetchear para cada comando
- Formato de respuesta definido con bloque de codigo de ejemplo
- Fallback si la URL principal falla
- Siempre mostrar fuente y fecha del dato en la respuesta

## Tipos de plugins

**Plugins de datos** (mayoria): WebFetch/WebSearch a APIs y fuentes publicas. Reglas estandar.

**Plugins wrapper de CLI** (ej: `facturar`): traducen lenguaje natural a comandos Bash.
- No hay WebFetch a APIs propias — el skill construye y ejecuta el comando
- Documentar prerequisitos de instalacion claramente
- Detectar si la herramienta esta disponible antes de ejecutar
- Confirmar acciones destructivas o irreversibles antes de ejecutar
