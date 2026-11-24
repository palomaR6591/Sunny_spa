# -*- coding: utf-8 -*-
"""
Planificador de costos de la jornada para spas
Proyecto final ADMI 1301 · Introducción a la Programación · Universidad de los Andes

Este archivo contiene TODO el cálculo de la aplicación, escrito en Python.
La pantalla (index.html) solo pide los datos y dibuja lo que este archivo devuelve.

IDEA DEL PROYECTO: el código no es de un spa en particular. Cualquier spa escribe sus
propios datos (personal, cabinas, tratamientos, precios, insumos) y obtiene el cálculo de
sus costos. "Sunny Side Luxury Spa" es un spa FICTICIO que usamos como ejemplo de cliente.

IMPORTANTE: las cifras del ejemplo son SUPUESTOS DE SIMULACIÓN propuestos por el grupo.
No son datos reales de ninguna empresa.
"""

import json

# =====================================================================
# 1. DATOS DEL SPA
# =====================================================================

# Datos del spa de ejemplo (ficticio). Cada spa que use la app escribe los suyos.
# El PRIMER tratamiento recibe el resto de los clientes, por eso su porcentaje se calcula solo.
EJEMPLO = {
    "nombre": "Sunny Side Luxury Spa",
    "clientes_por_terapeuta": 3,
    "clientes_por_recepcion": 10,
    "costo_turno_terapeuta": 200000,     # COP por turno
    "costo_turno_recepcion": 120000,     # COP por turno
    "cabinas": 8,
    "tratamientos": [
        {"nombre": "Masaje relajante", "precio": 200000, "insumos": 30000, "porcentaje": 50},
        {"nombre": "Facial hidratante premium", "precio": 260000, "insumos": 50000, "porcentaje": 30},
        {"nombre": "Ritual corporal", "precio": 360000, "insumos": 90000, "porcentaje": 20},
    ],
}

# El spa con el que se está calculando ahora (al empezar, el ejemplo)
spa = EJEMPLO

MAX_TRATAMIENTOS = 6
MAXIMO_DINERO = 100000000
NOMBRES_ESCENARIOS = ["Baja afluencia", "Ocupación media", "Agenda llena"]


# Capacidad máxima planificada: una cabina por terapeuta
def capacidad_maxima():
    return spa["cabinas"] * spa["clientes_por_terapeuta"]


# Los tres escenarios: un tercio, dos tercios y el total de la capacidad máxima
def clientes_escenarios():
    capacidad = capacidad_maxima()
    return [capacidad // 3, capacidad * 2 // 3, capacidad]


# =====================================================================
# 2. VALIDACIÓN DE LOS DATOS QUE ESCRIBE EL SPA
# =====================================================================

# Convierte un texto en número entero. Si no es un número válido devuelve None.
# En los campos de dinero acepta "$200.000" o "200 000" (quita $, puntos y espacios).
def leer_entero(texto, es_dinero):
    texto = str(texto).strip()
    if es_dinero:
        texto = texto.replace("$", "").replace(".", "").replace(" ", "")
    # isdecimal() es True solo si son únicamente dígitos (rechaza letras, negativos y decimales)
    if texto.isdecimal() == False or len(texto) > 12:
        return None
    return int(texto)


# Revisa los datos del formulario. Devuelve (errores, datos limpios, advertencias).
# Si la lista de errores está vacía, los datos se pueden usar.
def validar_configuracion(datos):
    errores = []
    advertencias = []
    limpio = {}

    # Nombre del spa
    nombre = str(datos.get("nombre", "")).strip()
    if nombre == "":
        errores.append("Escriba el nombre del spa.")
    elif len(nombre) > 40:
        errores.append("El nombre del spa es muy largo (máximo 40 letras).")
    limpio["nombre"] = nombre

    # Personal, costos y cabinas: (clave, nombre en pantalla, mínimo, máximo, es dinero)
    campos = [
        ("clientes_por_terapeuta", "Clientes por terapeuta por turno", 1, 20, False),
        ("clientes_por_recepcion", "Clientes por persona de recepción/apoyo", 1, 200, False),
        ("costo_turno_terapeuta", "Costo del turno de un terapeuta", 1, MAXIMO_DINERO, True),
        ("costo_turno_recepcion", "Costo del turno de recepción/apoyo", 1, MAXIMO_DINERO, True),
        ("cabinas", "Cabinas del spa", 1, 100, False),
    ]
    for clave, etiqueta, minimo, maximo, es_dinero in campos:
        valor = leer_entero(datos.get(clave, ""), es_dinero)
        if valor == None or valor < minimo or valor > maximo:
            errores.append(f"{etiqueta}: escriba un número entero entre {minimo} y {maximo}"
                           + (" (en pesos, sin decimales)." if es_dinero else "."))
            valor = minimo
        limpio[clave] = valor

    # Tratamientos
    lista = datos.get("tratamientos", [])
    if type(lista) != list or len(lista) < 1:
        errores.append("Agregue al menos un tratamiento.")
        lista = []
    if len(lista) > MAX_TRATAMIENTOS:
        errores.append(f"La app admite hasta {MAX_TRATAMIENTOS} tratamientos.")
        lista = lista[:MAX_TRATAMIENTOS]

    tratamientos = []
    nombres_usados = []
    suma_resto = 0                      # suma de los porcentajes del tratamiento 2 en adelante
    for i in range(len(lista)):
        t = lista[i]
        if type(t) != dict:
            errores.append(f"Tratamiento {i + 1}: los datos no se pudieron leer.")
            continue
        titulo = f"Tratamiento {i + 1}"

        nombre_t = str(t.get("nombre", "")).strip()
        if nombre_t == "":
            errores.append(f"{titulo}: escriba el nombre.")
        elif len(nombre_t) > 40:
            errores.append(f"{titulo}: el nombre es muy largo (máximo 40 letras).")
        elif nombre_t.lower() in nombres_usados:
            errores.append(f"{titulo}: el nombre «{nombre_t}» está repetido.")
        nombres_usados.append(nombre_t.lower())
        if nombre_t != "":
            titulo = f"{titulo} ({nombre_t})"

        precio = leer_entero(t.get("precio", ""), True)
        if precio == None or precio < 1 or precio > MAXIMO_DINERO:
            errores.append(f"{titulo}: el precio debe ser un número entero de pesos mayor que 0.")
            precio = 1
        insumos = leer_entero(t.get("insumos", ""), True)
        if insumos == None or insumos > MAXIMO_DINERO:
            errores.append(f"{titulo}: el costo de insumos debe ser un número entero de pesos (puede ser 0).")
            insumos = 0

        # El primer tratamiento recibe el resto; los demás indican su porcentaje
        if i == 0:
            porcentaje = 0
        else:
            porcentaje = leer_entero(t.get("porcentaje", ""), False)
            if porcentaje == None or porcentaje > 100:
                errores.append(f"{titulo}: el porcentaje de clientes debe ser un entero entre 0 y 100.")
                porcentaje = 0
            suma_resto = suma_resto + porcentaje

        if insumos >= precio and precio > 1:
            advertencias.append(f"{titulo}: el costo de insumos es igual o mayor que el precio; "
                                "cada cliente de ese tratamiento genera pérdida.")
        tratamientos.append({"nombre": nombre_t, "precio": precio, "insumos": insumos, "porcentaje": porcentaje})

    if suma_resto > 100:
        errores.append(f"Los porcentajes de los tratamientos 2 en adelante suman {suma_resto} %. "
                       "No pueden pasar de 100 %.")
    elif len(tratamientos) > 0:
        tratamientos[0]["porcentaje"] = 100 - suma_resto     # el primero recibe el resto
    limpio["tratamientos"] = tratamientos

    # Hace falta capacidad para armar los tres escenarios
    if limpio["cabinas"] * limpio["clientes_por_terapeuta"] < 3:
        errores.append("La capacidad máxima (cabinas × clientes por terapeuta) debe ser de al menos 3 clientes.")

    return errores, limpio, advertencias


# Estado del spa activo, para que la pantalla lo muestre
def estado_spa():
    capacidad = capacidad_maxima()
    return {
        "nombre": spa["nombre"],
        "es_ejemplo": spa == EJEMPLO,
        "capacidad": capacidad,
        "atajos": [capacidad // 3, capacidad * 2 // 3, capacidad, capacidad + capacidad // 4],
    }


# Recibe los datos del formulario (en texto JSON), los valida y, si están bien, los activa
def configurar_spa(texto_json):
    global spa
    try:
        datos = json.loads(texto_json)
    except ValueError:
        return {"estado": "error", "mensajes": ["Los datos del spa no se pudieron leer."]}
    if type(datos) != dict:
        return {"estado": "error", "mensajes": ["Los datos del spa no se pudieron leer."]}

    errores, limpio, advertencias = validar_configuracion(datos)
    if len(errores) > 0:
        return {"estado": "error", "mensajes": errores}

    spa = limpio
    resultado = estado_spa()
    resultado["estado"] = "ok"
    resultado["advertencias"] = advertencias
    return resultado


# Vuelve al spa de ejemplo
def usar_ejemplo():
    global spa
    spa = EJEMPLO
    return estado_spa()


# Datos del spa activo, para llenar el formulario "Mi spa"
def datos_del_spa():
    return spa


# Datos del ejemplo, para mostrarlos en el formulario
def datos_del_ejemplo():
    return EJEMPLO


# =====================================================================
# 3. FUNCIONES DE CÁLCULO
# =====================================================================

# Convierte un número en pesos colombianos. Ejemplo: formato_cop(2040000) -> "$2.040.000"
def formato_cop(valor):
    texto = f"{abs(valor):,.0f}"       # separa los miles con coma: 2,040,000
    texto = texto.replace(",", ".")    # cambia la coma por punto: 2.040.000
    if valor < 0:
        return "-$" + texto
    return "$" + texto


# Convierte un porcentaje en texto con coma decimal. Ejemplo: formato_porcentaje(45.07) -> "45,1 %"
def formato_porcentaje(valor):
    texto = f"{valor:.1f}"
    texto = texto.replace(".", ",")
    return texto + " %"


# Cuántos trabajadores se necesitan (siempre redondeando hacia arriba)
def personal_necesario(clientes, capacidad):
    personal = clientes // capacidad          # división entera: cuántos grupos completos hay
    if clientes % capacidad > 0:              # % da el resto: si sobran clientes...
        personal = personal + 1               # ...hace falta un trabajador más
    return personal


# Reparte los clientes entre los tratamientos del spa
def repartir_clientes(clientes):
    tratamientos = spa["tratamientos"]
    reparto = [0] * len(tratamientos)
    restantes = clientes
    for i in range(1, len(tratamientos)):
        # (2 * clientes * porcentaje + 100) // 200 es "clientes * porcentaje / 100" redondeado
        # al entero más cercano (los .5 suben), usando solo números enteros
        cantidad = (2 * clientes * tratamientos[i]["porcentaje"] + 100) // 200
        if cantidad > restantes:                 # nunca repartir más clientes de los que hay
            cantidad = restantes
        reparto[i] = cantidad
        restantes = restantes - cantidad
    reparto[0] = restantes                       # el primer tratamiento recibe el resto
    return reparto                               # mismo orden que spa["tratamientos"]


# Calcula todos los resultados de una jornada y los devuelve en un diccionario
def calcular_jornada(clientes):
    # Si la demanda supera la capacidad, la operación no es viable: no se calcula nada más
    if clientes > capacidad_maxima():
        return {
            "clientes": clientes,
            "viable": False,
            "clientes_sin_atender": clientes - capacidad_maxima(),
        }

    # Personal
    terapeutas = personal_necesario(clientes, spa["clientes_por_terapeuta"])
    recepcion = personal_necesario(clientes, spa["clientes_por_recepcion"])
    costo_personal = terapeutas * spa["costo_turno_terapeuta"] + recepcion * spa["costo_turno_recepcion"]

    # Ingresos e insumos, tratamiento por tratamiento
    clientes_servicio = repartir_clientes(clientes)
    ingresos_servicio = []
    ingresos_total = 0
    costo_insumos_total = 0
    for i in range(len(spa["tratamientos"])):
        t = spa["tratamientos"][i]
        ingreso = clientes_servicio[i] * t["precio"]
        insumos = clientes_servicio[i] * t["insumos"]
        ingresos_servicio.append(ingreso)
        ingresos_total = ingresos_total + ingreso
        costo_insumos_total = costo_insumos_total + insumos

    # Costos totales y ganancia
    costos_totales = costo_personal + costo_insumos_total
    ganancia = ingresos_total - costos_totales

    # Margen (evita dividir por cero si no hay clientes)
    if ingresos_total > 0:
        margen = ganancia / ingresos_total * 100
    else:
        margen = 0

    # Utilización de los terapeutas (evita dividir por cero)
    capacidad_contratada = terapeutas * spa["clientes_por_terapeuta"]
    if capacidad_contratada > 0:
        utilizacion = clientes / capacidad_contratada * 100
    else:
        utilizacion = 0

    resultado = {
        "clientes": clientes,
        "viable": True,
        "clientes_sin_atender": 0,
        "terapeutas": terapeutas,
        "recepcion": recepcion,
        "clientes_servicio": clientes_servicio,
        "ingresos_servicio": ingresos_servicio,
        "costo_personal": costo_personal,
        "costo_insumos": costo_insumos_total,
        "costos_totales": costos_totales,
        "ingresos_total": ingresos_total,
        "ganancia": ganancia,
        "margen": margen,
        "utilizacion": utilizacion,
    }
    return resultado


# =====================================================================
# 4. FUNCIONES QUE PREPARAN LO QUE MUESTRA LA PANTALLA
# =====================================================================

# Convierte el resultado de una jornada viable en textos listos para mostrar
def preparar_resultado(r):
    tratamientos = []
    for i in range(len(spa["tratamientos"])):
        tratamientos.append({
            "nombre": spa["tratamientos"][i]["nombre"],
            "clientes": r["clientes_servicio"][i],
            "ingresos": formato_cop(r["ingresos_servicio"][i]),
            "ingresos_num": r["ingresos_servicio"][i],
        })

    return {
        "estado": "ok",
        "clientes": r["clientes"],
        "terapeutas": r["terapeutas"],
        "recepcion": r["recepcion"],
        "utilizacion": formato_porcentaje(r["utilizacion"]),
        "tratamientos": tratamientos,
        "ingresos_total": formato_cop(r["ingresos_total"]),
        "ingresos_total_num": r["ingresos_total"],
        "costo_personal": formato_cop(r["costo_personal"]),
        "costo_personal_num": r["costo_personal"],
        "costo_insumos": formato_cop(r["costo_insumos"]),
        "costo_insumos_num": r["costo_insumos"],
        "costos_totales": formato_cop(r["costos_totales"]),
        "ganancia": formato_cop(r["ganancia"]),
        "ganancia_num": r["ganancia"],
        "margen": formato_porcentaje(r["margen"]),
    }


# Lo que usa el administrador: recibe el texto escrito en la pantalla, lo valida y calcula
def consultar_jornada(texto):
    texto = texto.strip()

    # isdecimal() es True solo si el texto son únicamente dígitos (rechaza letras, negativos y decimales)
    if texto == "":
        return {"estado": "error", "mensaje": "Escriba cuántos clientes espera para la jornada."}
    if texto.isdecimal() == False or len(texto) > 9:
        return {"estado": "error", "mensaje": "Escriba un número entero positivo (por ejemplo: 10)."}

    clientes = int(texto)
    if clientes == 0:
        return {"estado": "error", "mensaje": "Sin clientes no hace falta abrir turnos: no hay ingresos ni costos de la jornada."}

    r = calcular_jornada(clientes)
    if r["viable"] == False:
        return {
            "estado": "no_viable",
            "clientes": clientes,
            "capacidad_maxima": capacidad_maxima(),
            "cabinas": spa["cabinas"],
            "clientes_por_terapeuta": spa["clientes_por_terapeuta"],
            "sin_atender": r["clientes_sin_atender"],
        }
    return preparar_resultado(r)


# Calcula los tres escenarios con la misma función
def comparar_escenarios():
    lista = []
    escenarios = clientes_escenarios()
    for i in range(len(NOMBRES_ESCENARIOS)):
        r = calcular_jornada(escenarios[i])
        datos = preparar_resultado(r)
        datos["escenario"] = NOMBRES_ESCENARIOS[i]
        lista.append(datos)
    return lista


# Los datos del spa activo, para mostrarlos en pantalla
def obtener_supuestos():
    filas_personal = [
        ["Clientes por terapeuta por turno", str(spa["clientes_por_terapeuta"])],
        ["Clientes por persona de recepción/apoyo", str(spa["clientes_por_recepcion"])],
        ["Turno de terapeuta", formato_cop(spa["costo_turno_terapeuta"])],
        ["Turno de recepción/apoyo", formato_cop(spa["costo_turno_recepcion"])],
        ["Cabinas del spa", str(spa["cabinas"])],
        ["Capacidad máxima", str(capacidad_maxima()) + " clientes"],
    ]
    filas_tratamientos = []
    for t in spa["tratamientos"]:
        filas_tratamientos.append([
            t["nombre"],
            formato_cop(t["precio"]),
            formato_cop(t["insumos"]),
            str(t["porcentaje"]) + " %",
        ])
    return {"nombre": spa["nombre"], "personal": filas_personal, "tratamientos": filas_tratamientos}
