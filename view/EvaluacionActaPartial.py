import os

import plotly.graph_objects as go
from model.InfoActa import InfoActa
from datetime import datetime
from controller.ControladorPDF import ControladorPdf

# Este archivo contiene las funcionalidades de la vista relacionado con la evaluación de las actas


def agregar_acta(st, controlador):
    st.title("Generación De Actas")
    col1, col2, col3 = st.columns(3)
    col5, col6, col7, col8, col9 = st.columns(5)
    # Objeto que modelará el formulario
    info_acta_obj = InfoActa(controlador.criterios)
    info_acta_obj.fecha_acta = datetime.today().strftime('%Y-%m-%d')
    with col1:
        info_acta_obj.autor = st.text_input("Autor")
    with col2:
        info_acta_obj.nombre_trabajo = st.text_input("Nombre De Trabajo")
    with col3:
        info_acta_obj.tipo_trabajo = st.selectbox('Tipo', ('Aplicado', 'Investigación'))
    with col5:
        info_acta_obj.director = st.selectbox("Director", (controlador.directores()[0],controlador.directores()[1],controlador.directores()[2], controlador.directores()[3],controlador.directores()[4],controlador.directores()[5], controlador.directores()[6],controlador.directores()[7],controlador.directores()[8],))
    with col6:
        info_acta_obj.codirector = st.text_input("Codirector", "N.A")
    with col7:
        info_acta_obj.jurado1 = st.text_input("Jurado #1")
        info_acta_obj.jurado1_1 = st.checkbox("Externo", key="check1")
    with col8:
        info_acta_obj.jurado2 = st.text_input("Jurado #2")
        info_acta_obj.jurado2_2 = st.checkbox("Externo", key="check2")
    with col9:
        info_acta_obj.fecha_presentacion = st.text_input("Fecha de Presentacion")
    enviado_btn = st.button("Enviar")

    # Cuando se oprime el botón se agrega a la lista
    if enviado_btn and info_acta_obj.autor != "" and info_acta_obj.nombre_trabajo != "" and info_acta_obj.director != "" \
            and info_acta_obj.jurado1 != "" and info_acta_obj.jurado2 != "":
        controlador.agregar_evaluacion(info_acta_obj)
        st.success("Acta Agregada Exitosamente.")

        if info_acta_obj.tipo_trabajo == 'Aplicado':
            controlador.proyectos_aplicados += 1
        else:
            controlador.proyectos_investigacion += 1
        if info_acta_obj.jurado1_1 == False or info_acta_obj.jurado2_2 == False:
            controlador.jurados_externos += 1
        if info_acta_obj.jurado1_1 == True or info_acta_obj.jurado2_2 == True:
            controlador.jurados_internos += 1

    elif enviado_btn:
        st.error("Llene Todos Los Campos Vacíos.")
    else:
        st.info("No Deje Ningún Espacio En Blanco En Los Datos")
    # Retorna el controlador pq solo las colecciones se pasan en python por referencia,
    # entonces de esta manera se actualiza el controlador en la vista principal
    return controlador


def ver_historico_acta(st, controlador):
    st.title("Histórico")
    numero = 1
    if [acta.autor for acta in controlador.actas]:
        st.write("Estudiantes registrados en el sistema:")
    else:
        st.warning("Ningún Estudiante Registrado Aún.")
    for acta in controlador.actas:
        st.write("#### Acta #", numero)
        numero += 1
        col1, col2, col3, col4 = st.columns(4)
        col5, col6, col7, col8, col9 = st.columns(5)
        col9, col10, col11 = st.columns(3)
        with col1:
            st.write("**Autor**")
            st.write(acta.autor)
        with col2:
            st.write("**Nombre De Trabajo**")
            st.write(acta.nombre_trabajo)
        with col3:
            st.write("**Tipo De Trabajo**")
            st.write(acta.tipo_trabajo)
        with col4:
            st.write("**Fecha De Creación**")
            st.write(acta.fecha_acta)
        with col5:
            st.write("**Fecha De Presentacion**")
            st.write(acta.fecha_presentacion)
        with col6:
            st.write("**Director**")
            st.write(acta.director)
        with col7:
            st.write("**Codirector**")
            st.write(acta.codirector)
        with col8:
            st.write("**Jurado #1**")
            st.write(acta.jurado1)
        with col9:
            st.write("**Jurado #2**")
            st.write(acta.jurado2)
        with col10:
            st.write("**Nota Final**")
            if not acta.estado:
                st.write("Sin nota")
            elif acta.nota_final > 3.5:
                st.write(acta.nota_final, "Acta Aprobada")
            else:
                st.write(acta.nota_final, "Acta Reprobada")
        with col11:
            st.write("**Estado**")
            if not acta.estado:
                st.write("Acta pendiente por calificar")
            else:
                st.write("Acta calificada")


def evaluar_criterios(st, controlador):
    st.title("Evaluación de Criterios")
    flag = False
    num = 1
    temp = 0.0
    opcion = st.selectbox('Elija el autor a calificar', [acta.autor for acta in controlador.actas if not acta.estado])
    st.write("#### Criterios")
    for acta in controlador.actas:
        if acta.autor == opcion:
            flag = True
            for criterio in acta.criterios:
                st.write(criterio.descripcion)
                st.write("Valor de:", criterio.porcentaje * 100, "%")
                nota_jurado1 = st.number_input(str(num) + ". Nota Jurado 1", 0.0, 5.0)
                nota_jurado2 = st.number_input(str(num) + ". Nota Jurado 2", 0.0, 5.0)
                criterio.nota = ((nota_jurado1 + nota_jurado2) / 2) * criterio.porcentaje
                criterio.observacion = st.text_input(str(num) + ". Observación", "Sin Comentarios.")
                temp += criterio.nota
                num += 1
            criterio.observacion_adicional = st.text_input(str(num) + ". Observacion adicional", "Sin Comentarios.")
            num += 1
            criterio.restriccion = st.text_input(str(num) + ". Restriccion", "Sin Comentarios.")
            if temp > 3.5:
                st.write("#### Nota Final", temp, "Acta Aprobada.")
                if temp > 4.8:
                    controlador.proyectos_mayor_48 += 1
            else:
                st.write("#### Nota Final", temp, "Acta Reprobada.")

    if not flag:
        st.warning("Sin Estudiantes Por Calificar.")

    enviado_califica = st.button("Enviar")

    for acta in controlador.actas:
        #Actualiza el model con la informacion
        if acta.autor == opcion and enviado_califica:
            acta.nota_final = temp
            acta.estado = True
    if flag:
        nota_min = 3.5
        if enviado_califica and temp > nota_min:
            st.balloons()
            st.success("Evaluación De acta Agregada exitosamente, acta aprobada.")
        elif enviado_califica and temp <= nota_min:
            st.snow()
            st.success("Evaluación De Acta Agregada Exitosamente, acta reprobada.")
        else:
            st.info("Llene Todos Los Campos Vacíos.")


def exportar_acta(st, controlador):
    st.title("Generación de PDF")
    nombre_autor = st.selectbox('Elija el autor ya calificado', [acta.autor for acta in controlador.actas if acta.estado])

    if nombre_autor:
        #Fue seleccionado el autor
        enviado_pdf = st.button("Generar PDF")
        if enviado_pdf:
            controlador_pdf = ControladorPdf()
            controlador_pdf.exportar_acta(st,controlador, nombre_autor)
            st.success("Acta generada en PDF exitosamente, consulte la carpeta de salida 'outputs'.")
    else:
        st.info("Seleccione El Estudiante.")

    if len(controlador.actas) == 0:
        st.warning("No Hay Ningún Estudiante Calificado Actualmente.")

def estadisticas(st, controlador):
    st.title("Estádisticas generales")

    st.metric("Proyectos de Aplicacion", value=controlador.proyectos_aplicados)
    st.metric("Proyectos de Investigación", value=controlador.proyectos_investigacion)
    st.metric("Proyectos con Jurados Externos", value=controlador.jurados_externos)
    st.metric("Proyectos con Jurados Internos", value=controlador.jurados_internos)
    st.metric("Proyectos Superiores a 4.8", value=controlador.proyectos_mayor_48)

    st.title("Estádisticas con Plotly")

    labels = ['Proyectos de Aplicacion', 'Proyectos de Investigación', 'Proyectos con Jurados Externos', 'Proyectos con Jurados Internos', 'Proyectos Superiores a 4.8' ]
    values = [controlador.proyectos_aplicados, controlador.proyectos_investigacion, controlador.jurados_externos, controlador.jurados_internos, controlador.proyectos_mayor_48]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    st.plotly_chart(fig, use_container_width=True)