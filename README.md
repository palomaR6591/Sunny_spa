# Planificador de costos para spas

Proyecto final de **ADMI 1301 · Introducción a la Programación** (Universidad de los Andes, 2026-2).

Es una aplicación en Python que **cualquier spa** puede usar para calcular los costos y la ganancia operativa de su jornada. El escenario del proyecto es ofrecerla a spas de Bogotá: cada spa escribe sus propios datos (personal, cabinas, tratamientos, precios e insumos) y la app hace el cálculo con ellos.

> **Aviso:** **Sunny Side Luxury Spa** es un spa **ficticio** que usamos como *cliente de ejemplo*, para mostrar cómo se ve la app ya aplicada. Todas sus cifras (precios, costos, capacidades) son **supuestos de simulación propuestos por el grupo**. No son datos reales de ninguna empresa, y este proyecto no incluye información de mercado real.

## Abrir la app

**https://jdespinosa2008.github.io/Sunny_spa/**

### Agregarla al celular

- **Android (Chrome):** menú ⋮ → *Instalar app* o *Añadir a la pantalla de inicio*.
- **iPhone (Safari):** botón Compartir → *Añadir a pantalla de inicio*.

Después de abrirla una vez con internet, también funciona sin conexión.

## Cómo la usa un spa

1. Abrir la pestaña **Mi spa** y escribir: nombre del spa, clientes que atiende un terapeuta por turno, clientes por persona de recepción/apoyo, costo de cada turno, cabinas, y de 1 a 6 tratamientos (nombre, precio, costo de insumos y porcentaje de clientes que lo piden).
2. Pulsar **Guardar y calcular**. Los datos se guardan **solo en ese dispositivo** (no hay servidor ni cuentas).
3. En **Jornada**, escribir cuántos clientes espera y ver: terapeutas necesarios, personal de recepción y apoyo, costo de turnos, costo de insumos, ingresos por tratamiento y ganancia operativa.
4. En **Escenarios**, comparar tres jornadas: baja afluencia (un tercio de la capacidad), ocupación media (dos tercios) y agenda llena (la capacidad completa).
5. En **Datos**, revisar con qué números se está calculando.

Al abrirla por primera vez, la app muestra el spa de ejemplo (Sunny Side). El botón **Ver datos del ejemplo** copia sus datos al formulario como guía, y **Borrar mis datos** vuelve al ejemplo.

## Reglas del cálculo

- **Capacidad máxima** = cabinas × clientes por terapeuta. Si la demanda la supera, la app avisa que no se puede atender y **no muestra cifras financieras**.
- **Personal:** se contrata siempre redondeando hacia arriba (`clientes // capacidad`, y uno más si sobra resto).
- **Reparto de clientes:** el primer tratamiento recibe el resto; los demás reciben su porcentaje, redondeado al entero más cercano.
- **Ganancia operativa** = ingresos − costo de personal − costo de insumos. **No incluye** arriendo, servicios públicos ni impuestos.
- Los porcentajes de demanda, los precios y los costos son **datos que escribe cada spa**; la app no los estima.

Si un dato no es válido (letras, negativos, decimales, porcentajes que suman más de 100 %, nombres repetidos…), la app lo indica y no calcula hasta corregirlo.

## ¿Cómo funciona por dentro?

- **`app.py`** contiene todo el cálculo, escrito en Python: `validar_configuracion`, `personal_necesario`, `repartir_clientes`, `calcular_jornada`, entre otras. Los datos del spa viven en un diccionario (`spa`); el ejemplo está en `EJEMPLO`. Con los datos de Sunny Side da los mismos resultados que el notebook del proyecto.
- **`index.html`** es la pantalla. Solo recoge los datos y dibuja lo que devuelve Python.
- El Python se ejecuta **dentro del navegador** con [Pyodide](https://pyodide.org) (carpeta `pyodide/`, licencia MPL-2.0), así que no hay servidor y nada sale del dispositivo.
- `manifest.webmanifest`, `sw.js` e `icons/` permiten instalarla en el celular y usarla sin conexión.

### Cambiar el código

Si se modifica algún archivo, cambiar el número de `VERSION` en `sw.js` para que los celulares descarguen la versión nueva.

## Probarla en el computador

```
python -m http.server 8000
```

y abrir `http://localhost:8000`. (Abrir `index.html` con doble clic no funciona, porque el navegador bloquea la carga de archivos locales.)

## Limitaciones

- Es un modelo simple de **una jornada**: no incluye arriendo, servicios, impuestos, nómina mensual ni demanda por horas.
- Supone que cada terapeuta usa una cabina y que la mezcla de tratamientos es la que escribe el spa.
- Los resultados son estimaciones para planear, no contabilidad.
- Los datos quedan en el navegador del dispositivo: si se borran los datos del navegador, hay que volver a escribirlos.

## Uso de inteligencia artificial

Se usó Claude (Anthropic) como apoyo para diseñar y generar un borrador de la aplicación. El grupo verificó los cálculos contra cuentas hechas a mano. La nota completa está en el notebook del proyecto.

## Integrantes

Matias Galeano · Emily Rojas · Paloma Restrepo · Valeria Nuncio

Profesor: Gustavo Niño · ADMI 1301 · Facultad de Administración, Universidad de los Andes.
