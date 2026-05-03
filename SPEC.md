# AR Plugins — Spec del Ecosistema

**Visión:** Convertir Claude Code en un mecha para el cerebro argentino. Un conjunto de plugins que le dan a cualquier persona en Argentina acceso instantáneo al contexto, los datos y las herramientas que necesita para navegar la realidad del país.

**Principio:** Cada plugin resuelve un problema real y concreto de vivir, trabajar o pensar en Argentina.

---

## Plugins planificados

### ✅ nodo
**Estado:** Publicado v1.0.0
**Descripción:** Contexto personal persistente entre sesiones.
**Propósito:** Claude arranca sabiendo quién sos y en qué estás trabajando.

---

### 💰 arca
**Descripción:** Economía argentina en tiempo real.
**Problema:** Vivir en Argentina requiere procesar múltiples variables económicas simultáneamente — tipo de cambio, inflación, salario real — para tomar cualquier decisión financiera.
**Skills:**
- `/arca dolar` — todos los tipos de cambio (oficial, blue, MEP, CCL, cripto)
- `/arca inflacion` — IPC último dato, acumulado anual, proyección
- `/arca sueldo [monto]` — convierte un sueldo a dólares en todos los tipos
- `/arca canasta` — costo de la canasta básica actual
- `/arca tarifas` — servicios públicos actualizados

**Fuentes:** BCRA API, bluelytics, INDEC

---

### 📋 tramite
**Descripción:** Navegador de burocracia argentina.
**Problema:** Los trámites argentinos cambian constantemente, tienen requisitos oscuros y procesos no documentados. Perder tiempo y viajes es la norma.
**Skills:**
- `/tramite anses [tipo]` — jubilación, AUH, prestaciones, cómo sacar turno
- `/tramite afip [tipo]` — monotributo, facturación, vencimientos, claves
- `/tramite dni` — renovación, turno, requisitos actualizados
- `/tramite auto` — patente, transferencia, VTV
- `/tramite [cualquier cosa]` — búsqueda libre en el universo de trámites AR

---

### 👨‍💻 laburo
**Descripción:** Mercado laboral argentino para tech y profesionales.
**Problema:** El mercado laboral argentino tiene dinámicas únicas — dolarización de sueldos, freelance internacional, precios en un contexto inflacionario.
**Skills:**
- `/laburo mercado` — state of the market: sueldos promedio por rol, tendencias
- `/laburo tarifa [rol] [senioridad]` — cuánto cobrar en AR / USD / remoto
- `/laburo cv [objetivo]` — adaptar CV al mercado argentino o internacional
- `/laburo propuesta [contexto]` — armar propuesta económica para cliente

---

### 📊 dato
**Descripción:** Datos públicos de Argentina, procesables.
**Problema:** Argentina tiene muchísimos datos públicos (INDEC, elecciones, justicia, catastro) pero son difíciles de acceder y procesar.
**Skills:**
- `/dato indec [indicador]` — cualquier estadística del INDEC
- `/dato elecciones [año] [distrito]` — resultados electorales históricos
- `/dato catastro [provincia]` — datos catastrales y registros de propiedad
- `/dato justicia [tema]` — jurisprudencia y normativa por tema

**Fuentes:** APIs oficiales, datasets.gob.ar

---

### ⚖️ derecho
**Descripción:** Marco legal argentino accesible.
**Problema:** El sistema legal argentino es complejo, cambia frecuentemente y es inaccesible para el ciudadano común. Un abogado para cada consulta es imposible.
**Skills:**
- `/derecho laboral [situacion]` — derechos del trabajador, despidos, ART
- `/derecho consumidor [problema]` — defensa del consumidor, cómo reclamar
- `/derecho contrato [tipo]` — qué debe tener un contrato, qué es inválido
- `/derecho societario [tipo]` — SA, SRL, SAS — diferencias y pasos

---

### 🏥 salud
**Descripción:** Sistema de salud argentino navegable.
**Problema:** El sistema de salud argentino es fragmentado (público / obras sociales / prepagas) y difícil de navegar.
**Skills:**
- `/salud cobertura [obra-social] [prestacion]` — qué cubre, cómo pedirlo
- `/salud pami [tramite]` — jubilados, medicamentos, turnos
- `/salud hospital [provincia]` — hospitales públicos, especialidades, urgencias
- `/salud medicamento [nombre]` — genérico, precio, cobertura, dónde comprarlo

---

### 🚀 startup
**Descripción:** Ecosistema emprendedor argentino.
**Problema:** El ecosistema startup argentino tiene sus propias reglas, fondos, aceleradoras y regulaciones — y está desconectado de los recursos globales.
**Skills:**
- `/startup fondos` — grants, VC activos, FONTAR, FIDE, aceleradoras
- `/startup legal [tipo]` — cómo constituir una empresa tech, SAS, opciones
- `/startup equity [contexto]` — estructuras de equity para el contexto argentino
- `/startup pitch [idea]` — framework de pitch adaptado al ecosistema local

---

### 📰 medios
**Descripción:** Síntesis del ecosistema informativo argentino.
**Problema:** El ecosistema mediático argentino es ruidoso, polarizado y difícil de procesar. Distinguir información de narrativa requiere mucho tiempo y contexto.
**Skills:**
- `/medios agenda` — qué está pasando hoy, desde múltiples fuentes
- `/medios tema [tema]` — cómo cubren distintos medios el mismo tema
- `/medios verificar [afirmacion]` — fact-check con fuentes primarias
- `/medios historia [tema]` — contexto histórico de una noticia actual

---

### 🎓 educacion
**Descripción:** Sistema educativo argentino + oportunidades.
**Problema:** Las oportunidades educativas en Argentina son amplias pero poco conocidas — becas, programas, acceso a universidades públicas gratuitas de calidad mundial.
**Skills:**
- `/educacion becas [perfil]` — becas disponibles según carrera, situación, nivel
- `/educacion universidad [carrera]` — dónde estudiarla, ranking, modalidad
- `/educacion certificaciones [area]` — certificaciones tech reconocidas, cómo prepararlas
- `/educacion ingles` — recursos gratuitos, caminos para aprender

---

## Principios de diseño

### 1. Offline-first donde sea posible
Los argentinos tienen conectividad variable. Los plugins deben funcionar con datos en caché cuando las APIs fallen.

### 2. Sin pagar para lo básico
Todo lo que el Estado ya ofrece gratis tiene que ser accesible gratis. Los plugins no intermedian con costo.

### 3. Agnóstico a la coyuntura
Los datos cambian todo el tiempo en Argentina. Los plugins deben apuntar a fuentes primarias y oficiales, no hardcodear valores.

### 4. Lenguaje llano
Sin tecnicismos innecesarios. El objetivo es que una persona sin formación específica pueda usar el resultado directamente.

### 5. Privacidad
Ningún plugin envía datos personales a terceros. Las consultas son locales o van a APIs públicas sin identificación.

---

## Roadmap

| Prioridad | Plugin | Impacto | Complejidad |
|-----------|--------|---------|-------------|
| 🔥 Alta | **arca** | Masivo, se usa todos los días | Media — APIs existentes |
| 🔥 Alta | **tramite** | Masivo, ahorra tiempo real | Alta — datos cambian mucho |
| 🟡 Media | **laburo** | Alto en tech | Media |
| 🟡 Media | **derecho** | Alto, sin alternativa accesible | Alta |
| 🟡 Media | **dato** | Multiplicador para periodistas/analistas | Media |
| 🟢 Normal | **salud** | Alto en vulnerables | Alta |
| 🟢 Normal | **startup** | Nicho pero estratégico | Media |
| 🟢 Normal | **medios** | Ciudadanía informada | Alta |
| 🟢 Normal | **educacion** | Alto impacto a largo plazo | Media |

---

## Próximo paso: arca

`arca` es el primer plugin a desarrollar después de `nodo` porque:
1. Se usa a diario — cualquier argentino lo necesita
2. Las APIs existen y son estables (BCRA, bluelytics, INDEC)
3. El caso de uso es simple y verificable
4. Genera adopción inmediata del ecosistema

**Estructura de `arca`:**
```
ar-plugins/
  arca/
    .claude-plugin/plugin.json
    skills/
      arca/SKILL.md
    memory/          # datos en caché opcionales
    README.md
```
