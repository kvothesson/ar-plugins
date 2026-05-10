# Principios y referencias

## Principios

| Principio | Como aplicarlo |
|-----------|----------------|
| **Sin hardcodear datos que cambian** | Montos, fechas, requisitos: siempre WebFetch/WebSearch a fuente primaria |
| **Fuente primaria siempre** | Sites oficiales (.gob.ar). Medios solo si el organismo no publica algo directamente |
| **Siempre mostrar fecha y fuente** | Cada bloque de respuesta incluye fuente y fecha del dato |
| **Lenguaje llano** | Pasos concretos, sin jerga institucional. El usuario tiene que poder actuar con lo que lee |
| **Privacidad** | No pedir ni transmitir datos del usuario. CUIL, DNI, claves: el usuario los ingresa el solo |
| **Fallback** | Si la URL principal no responde, el skill tiene una alternativa (otra URL o WebSearch) |
| **Plataforma agnóstica** | Los skills deben correr en Windows, macOS y Linux sin cambios. Ver reglas abajo. |

---

## Plataforma agnóstica

Todo skill del ecosistema debe poder ejecutarse en cualquier entorno donde corra Claude Code.

**Patrón de detección:**

```python
import platform
os_name = platform.system()  # 'Windows' | 'Darwin' | 'Linux'

if os_name == "Windows":
    ...
elif os_name == "Darwin":
    ...
elif os_name == "Linux":
    ...
else:
    print(f"Plataforma {os_name} no soportada aún.")
```

**Reglas:**
- Nunca hardcodear rutas del sistema (`C:\Windows`, `/usr/local/`, etc.)
- Rutas de usuario: `Path.home()` en Python, `~` en shell
- Usar `psutil`, `pathlib`, `shutil` como capa cross-platform siempre que sea posible
- Para comandos nativos que difieren por OS: branch explícito, una rama por plataforma
- Si una función no existe en un OS dado: decirlo en una línea, no fallar silenciosamente
- Scripts de soporte dentro del skill: referenciar con `${CLAUDE_SKILL_DIR}/script.py`

**Reemplazos canónicos:**

| En vez de... | Usar... |
|---|---|
| `C:\Users\<nombre>\carpeta\` | `Path.home() / "carpeta"` |
| Path a un `.env` personal | `~/.env` o variable de entorno documentada |
| Path hardcodeado a script del plugin | `${CLAUDE_SKILL_DIR}/script.py` |

**Verificar antes de commitear:**

```bash
git diff --cached | grep -iE "Users/|Users\\|/home/[a-z]|\.env|api.key"
```

---

## Referencias

| Recurso | Donde |
|---------|-------|
| Spec de plugins planificados | `SPEC.md` en este repo |
| Documentacion oficial — plugins | https://code.claude.com/docs/en/plugins |
| Documentacion oficial — skills | https://code.claude.com/docs/en/skills |
| Documentacion oficial — marketplaces | https://code.claude.com/docs/en/plugin-marketplaces |
| Indice completo de docs de Claude Code | https://code.claude.com/docs/llms.txt |
| Plugin de referencia — datos (economia) | https://github.com/kvothesson/arca |
| Plugin de referencia — wrapper CLI | https://github.com/kvothesson/facturar |
| Plugin de referencia — cross-platform | https://github.com/kvothesson/bestiario-plugin |
| Issues y roadmap | https://github.com/kvothesson/ar-plugins/issues |
| Workflow resolver issue | `skills/dev/SKILL.md` en este repo |