# -*- coding: utf-8 -*-
"""
Sunny Side Luxury Spa · Planificador de costos de la jornada
Proyecto final ADMI 1301 · Introducción a la Programación · Universidad de los Andes

Este archivo contiene TODO el cálculo de la aplicación, escrito en Python.
La pantalla (index.html) solo pide el dato y dibuja lo que este archivo devuelve.

IMPORTANTE: todas las cifras son SUPUESTOS DE SIMULACIÓN propuestos por el grupo.
No son datos reales de ninguna empresa.
"""

# =====================================================================
# 1. SUPUESTOS (se pueden cambiar aquí)
# =====================================================================

# Personal
clientes_por_terapeuta = 3
clientes_por_recepcion = 10
costo_turno_terapeuta = 200000      # COP por turno
costo_turno_recepcion = 120000      # COP por turno

# Capacidad máxima planificada: una cabina por terapeuta
cabinas = 8
capacidad_maxima = cabinas * clientes_por_terapeuta

# Tratamientos: listas paralelas (posición 0 = masaje, 1 = facial, 2 = ritual)
nombres_servicios = ["Masaje relajante", "Facial hidratante premium", "Ritual corporal"]
nombres_cortos = ["Masaje", "Facial", "Ritual"]
precios = [200000, 260000, 360000]          # COP por cliente
costos_insumos = [30000, 50000, 90000]      # COP por cliente

# Mezcla de tratamientos (el masaje recibe el resto)
proporcion_facial = 0.30
proporcion_ritual = 0.20
proporcion_masaje = 1 - proporcion_facial - proporcion_ritual

# Escenarios: un tercio, dos tercios y el total de la capacidad máxima
nombres_escenarios = ["Baja afluencia", "Ocupación media", "Agenda llena"]
clientes_escenarios = [capacidad_maxima // 3, capacidad_maxima * 2 // 3, capacidad_maxima]


# =====================================================================
# 2. FUNCIONES DE CÁLCULO (las mismas del notebook)
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


# Reparte los clientes entre los tres tratamientos
def repartir_clientes(clientes):
    facial = int(clientes * proporcion_facial + 0.5)    # int(x + 0.5): todo .5 sube
    ritual = int(clientes * proporcion_ritual + 0.5)
    masaje = clientes - facial - ritual                 # el masaje recibe el resto
    return [masaje, facial, ritual]                     # mismo orden que nombres_servicios


# Calcula todos los resultados de una jornada y los devuelve en un diccionario
def calcular_jornada(clientes):
    # Si la demanda supera la capacidad, la operación no es viable: no se calcula nada más
    if clientes > capacidad_maxima:
        return {
            "clientes": clientes,
            "viable": False,
            "clientes_sin_atender": clientes - capacidad_maxima,
        }

    # Personal
    terapeutas = personal_necesario(clientes, clientes_por_terapeuta)
    recepcion = personal_necesario(clientes, clientes_por_recepcion)
    costo_personal = terapeutas * costo_turno_terapeuta + recepcion * costo_turno_recepcion

    # Ingresos e insumos, tratamiento por tratamiento
    clientes_servicio = repartir_clientes(clientes)
    ingresos_servicio = []
    ingresos_total = 0
    costo_insumos_total = 0
    for i in range(len(nombres_servicios)):
        ingreso = clientes_servicio[i] * precios[i]
        insumos = clientes_servicio[i] * costos_insumos[i]
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
    capacidad_contratada = terapeutas * clientes_por_terapeuta
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
# 3. FUNCIONES QUE PREPARAN LO QUE MUESTRA LA PANTALLA
# =====================================================================

# Convierte el resultado de una jornada viable en textos listos para mostrar
def preparar_resultado(r):
    tratamientos = []
    for i in range(len(nombres_servicios)):
        tratamientos.append({
            "nombre": nombres_servicios[i],
            "nombre_corto": nombres_cortos[i],
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

    # isdigit() es True solo si el texto son únicamente dígitos (rechaza letras, negativos y decimales)
    if texto == "":
        return {"estado": "error", "mensaje": "Escriba cuántos clientes espera para la jornada."}
    if texto.isdigit() == False:
        return {"estado": "error", "mensaje": "Escriba un número entero positivo (por ejemplo: 10)."}

    clientes = int(texto)
    if clientes == 0:
        return {"estado": "error", "mensaje": "Sin clientes no hace falta abrir turnos: no hay ingresos ni costos de la jornada."}

    r = calcular_jornada(clientes)
    if r["viable"] == False:
        return {
            "estado": "no_viable",
            "clientes": clientes,
            "capacidad_maxima": capacidad_maxima,
            "cabinas": cabinas,
            "clientes_por_terapeuta": clientes_por_terapeuta,
            "sin_atender": r["clientes_sin_atender"],
        }
    return preparar_resultado(r)


# Calcula los tres escenarios con la misma función
def comparar_escenarios():
    lista = []
    for i in range(len(nombres_escenarios)):
        r = calcular_jornada(clientes_escenarios[i])
        datos = preparar_resultado(r)
        datos["escenario"] = nombres_escenarios[i]
        lista.append(datos)
    return lista


# Los supuestos, para mostrarlos en pantalla
def obtener_supuestos():
    filas_personal = [
        ["Clientes por terapeuta por turno", str(clientes_por_terapeuta)],
        ["Clientes por persona de recepción/apoyo", str(clientes_por_recepcion)],
        ["Turno de terapeuta", formato_cop(costo_turno_terapeuta)],
        ["Turno de recepción/apoyo", formato_cop(costo_turno_recepcion)],
        ["Cabinas del spa", str(cabinas)],
        ["Capacidad máxima", str(capacidad_maxima) + " clientes"],
    ]
    demanda = [proporcion_masaje, proporcion_facial, proporcion_ritual]
    filas_tratamientos = []
    for i in range(len(nombres_servicios)):
        filas_tratamientos.append([
            nombres_servicios[i],
            formato_cop(precios[i]),
            formato_cop(costos_insumos[i]),
            f"{demanda[i] * 100:.0f} %",
        ])
    return {"personal": filas_personal, "tratamientos": filas_tratamientos}
