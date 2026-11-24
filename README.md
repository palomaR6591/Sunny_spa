# Sunny Side Luxury Spa · Planificador de costos de la jornada

Proyecto final de **ADMI 1301 · Introducción a la Programación** (Universidad de los Andes, 2026-2).

> **Aviso:** Sunny Side Luxury Spa es un spa **ficticio**. Todas las cifras (precios, costos, capacidades) son **supuestos de simulación propuestos por el grupo**. No son datos reales de ninguna empresa.

## Abrir la app

**https://jdespinosa2008.github.io/Sunny_spa/**

### Agregarla al celular

- **Android (Chrome):** menú ⋮ → *Instalar app* o *Añadir a la pantalla de inicio*.
- **iPhone (Safari):** botón Compartir → *Añadir a pantalla de inicio*.

Después de abrirla una vez con internet, también funciona sin conexión.

## ¿Qué hace?

El administrador escribe cuántos clientes espera para la jornada y la app calcula:

1. Terapeutas necesarios.
2. Personal de recepción y apoyo.
3. Costo de los turnos de trabajo.
4. Costo de los insumos.
5. Ingresos por cada tratamiento (masaje, facial y ritual corporal).
6. Ganancia operativa estimada.
7. Comparación de tres escenarios: baja afluencia (8 clientes), ocupación media (16) y agenda llena (24).

Si la demanda supera la capacidad máxima (24 clientes con 8 cabinas), la app avisa que no se puede atender y **no muestra cifras financieras**.

La ganancia es **operativa**: no incluye arriendo, servicios públicos ni impuestos.

## ¿Cómo funciona por dentro?

- **`app.py`** contiene todo el cálculo, escrito en Python: `personal_necesario`, `repartir_clientes`, `calcular_jornada`, entre otras. Son las mismas funciones del notebook del proyecto.
- **`index.html`** es la pantalla. Solo pide el dato y dibuja lo que devuelve Python.
- El Python se ejecuta **dentro del navegador** con [Pyodide](https://pyodide.org) (carpeta `pyodide/`, licencia MPL-2.0), así que no hay servidor y nada sale del dispositivo.
- `manifest.webmanifest`, `sw.js` e `icons/` permiten instalarla en el celular y usarla sin conexión.

### Cambiar un supuesto

Editar los valores al inicio de `app.py` (por ejemplo, los precios o las cabinas). Después, cambiar el número de `VERSION` en `sw.js` para que los celulares descarguen la versión nueva.

## Probarla en el computador

```
python -m http.server 8000
```

y abrir `http://localhost:8000`. (Abrir `index.html` con doble clic no funciona, porque el navegador bloquea la carga de archivos locales.)

## Uso de inteligencia artificial

Se usó Claude (Anthropic) como apoyo para diseñar y generar un borrador de la aplicación. El grupo verificó los cálculos contra cuentas hechas a mano. La nota completa está en el notebook del proyecto.

## Integrantes

Matias Galeano · Emily Rojas · Paloma Restrepo · Valeria Nuncio

Profesor: Gustavo Niño · ADMI 1301 · Facultad de Administración, Universidad de los Andes.
