# 5 noticias mas releventes de seccion Pais & Mundo
with open('jornada.json') as file:
    data = json.load(file)


articulos_globales = []
for articulo in data:
    articulos_globales.append(
        {"titulo": articulo['titulo'], "visitas": articulo['visitas'], "fecha": articulo['fecha'], "seccion": articulo['seccion']})

# seccion Pais & Mundo
articulos_paismundo = []
seccion_paismundo = "PA\u00cdS & MUNDO"
for art in articulos_globales:
    if art['seccion'] == seccion_paismundo:
        articulos_paismundo.append(art)

articulos_paismundo.sort(key=lambda ap: int(ap['visitas']), reverse=True)

print("Sección PAIS & MUNDO\n")
for ag in range(5):
    print("Titulo: {0}. Fecha: {2}. \nVisitas: {1}.\n".format(
        articulos_paismundo[ag]['titulo'], articulos_paismundo[ag]['visitas'], articulos_paismundo[ag]['fecha']))
