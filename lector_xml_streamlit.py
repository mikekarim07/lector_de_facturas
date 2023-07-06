import os
import time
import pandas as pd
import xml.etree.ElementTree as ET
import streamlit as st
from streamlit_option_menu import option_menu
import io
import base64

import time
import pandas as pd
import xml.etree.ElementTree as ET
import streamlit as st
import io
import base64
import zipfile

st.set_page_config(
    page_title="CDFI Lector archivos xml - webapp",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

def parse_xml4(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    namespaces = {
        'cfdi': 'http://www.sat.gob.mx/cfd/4',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
        'pago10': 'http://www.sat.gob.mx/Pagos'
    }

    version = root.attrib.get('Version', '')
    forma_de_pago = root.attrib.get('FormaPago', '')
    regimen = root.find('cfdi:Emisor', namespaces=namespaces).attrib.get('RegimenFiscal', '')
    tipo_de_comprobante = root.attrib.get('TipoDeComprobante', '')
    rfc_emisor = root.find('cfdi:Emisor', namespaces=namespaces).attrib.get('Rfc', '')
    nombre_emisor = root.find('cfdi:Emisor', namespaces=namespaces).attrib.get('Nombre', '')
    rfc_receptor = root.find('cfdi:Receptor', namespaces=namespaces).attrib.get('Rfc', '')
    nombre_receptor = root.find('cfdi:Receptor', namespaces=namespaces).attrib.get('Nombre', '')
    subtotal = root.attrib.get('SubTotal', '')
    total = root.attrib.get('Total', '')
    uuid = root.find('cfdi:Complemento/tfd:TimbreFiscalDigital', namespaces=namespaces).attrib.get('UUID', '')
    fecha_emision = root.attrib.get('Fecha', '')

    return {
        'version': version,
        'forma_de_pago': forma_de_pago,
        'regimen': regimen,
        'tipo_de_comprobante': tipo_de_comprobante,
        'rfc_emisor': rfc_emisor,
        'nombre_emisor': nombre_emisor,
        'rfc_receptor': rfc_receptor,
        'nombre_receptor': nombre_receptor,
        'subtotal': subtotal,
        'total': total,
        'uuid': uuid,
        'fecha_emision': fecha_emision
    }

def parse_xml33(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    namespaces = {
        'cfdi': 'http://www.sat.gob.mx/cfd/3',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
        'pago10': 'http://www.sat.gob.mx/Pagos'
    }

    version = root.attrib.get('Version', '')
    forma_de_pago = root.attrib.get('FormaPago', '')
    regimen = root.find('cfdi:Emisor', namespaces=namespaces).attrib.get('RegimenFiscal', '')
    tipo_de_comprobante = root.attrib.get('TipoDeComprobante', '')
    rfc_emisor = root.find('cfdi:Emisor', namespaces=namespaces).attrib.get('Rfc', '')
    nombre_emisor = root.find('cfdi:Emisor', namespaces=namespaces).attrib.get('Nombre', '')
    rfc_receptor = root.find('cfdi:Receptor', namespaces=namespaces).attrib.get('Rfc', '')
    nombre_receptor = root.find('cfdi:Receptor', namespaces=namespaces).attrib.get('Nombre', '')
    subtotal = root.attrib.get('SubTotal', '')
    total = root.attrib.get('Total', '')
    uuid = root.find('cfdi:Complemento/tfd:TimbreFiscalDigital', namespaces=namespaces).attrib.get('UUID', '')
    fecha_emision = root.attrib.get('Fecha', '')
    
    return {
        'version': version,
        'forma_de_pago': forma_de_pago,
        'regimen': regimen,
        'tipo_de_comprobante': tipo_de_comprobante,
        'rfc_emisor': rfc_emisor,
        'nombre_emisor': nombre_emisor,
        'rfc_receptor': rfc_receptor,
        'nombre_receptor': nombre_receptor,
        'subtotal': subtotal,
        'total': total,
        'uuid': uuid,
        'fecha_emision': fecha_emision
    }


def parse_xmlcomp33(xml_file):
    # Parse the XML string
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Namespace dictionary
    ns = {
        "cfdi": "http://www.sat.gob.mx/cfd/3",
        "pago10": "http://www.sat.gob.mx/Pagos",
        "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital"
    }

    # Get the payment element
    pago_element = root.find("cfdi:Complemento/pago10:Pagos/pago10:Pago", ns)

    fecha_pago = pago_element.attrib.get("FechaPago")
    forma_pago = pago_element.attrib.get("FormaDePagoP")
    moneda_pago = pago_element.attrib.get("MonedaP")
    monto = pago_element.attrib.get("Monto")

    doc_relacionado_element = pago_element.find("pago10:DoctoRelacionado", ns)
    id_documento = doc_relacionado_element.attrib.get("IdDocumento")
    moneda_dr = doc_relacionado_element.attrib.get("MonedaDR")
    metodo_pago_dr = doc_relacionado_element.attrib.get("MetodoDePagoDR")
    num_parcialidad = doc_relacionado_element.attrib.get("NumParcialidad")
    imp_saldo_ant = doc_relacionado_element.attrib.get("ImpSaldoAnt")
    imp_pagado = doc_relacionado_element.attrib.get("ImpPagado")
    imp_saldo_insoluto = doc_relacionado_element.attrib.get("ImpSaldoInsoluto")

    return {
        "version": root.attrib.get("Version"),
        "Fecha": root.attrib.get("Fecha"),
        "RFC emisor": root.find("cfdi:Emisor", ns).attrib.get("Rfc"),
        "Nombre emisor": root.find("cfdi:Emisor", ns).attrib.get("Nombre"),
        "RFC receptor": root.find("cfdi:Receptor", ns).attrib.get("Rfc"),
        "Nombre receptor": root.find("cfdi:Receptor", ns).attrib.get("Nombre"),
        "uso_cfdi": root.find("cfdi:Receptor", ns).attrib.get("UsoCFDI"),
        "UUID": root.find("cfdi:Complemento/tfd:TimbreFiscalDigital", ns).attrib.get("UUID"),
        "FechaPago": fecha_pago,
        "FormaDePagoP": forma_pago,
        "MonedaP": moneda_pago,
        "Monto": monto,
        "IdDocumento": id_documento,
        "MonedaDR": moneda_dr,
        "MetodoDePagoDR": metodo_pago_dr,
        "NumParcialidad": num_parcialidad,
        "ImpSaldoAnt": imp_saldo_ant,
        "ImpPagado": imp_pagado,
        "ImpSaldoInsoluto": imp_saldo_insoluto
    }

def parse_xmlcomp40(xml_file):
    # Parse the XML string
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Namespace dictionary
    ns = {
        "cfdi": "http://www.sat.gob.mx/cfd/4",
        "pago20": "http://www.sat.gob.mx/Pagos20",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital"
    }

    # Get the payment element
    pago_element = root.find("cfdi:Complemento/pago20:Pagos/pago20:Pago", ns)

    fecha_pago = pago_element.attrib.get("FechaPago")
    forma_pago = pago_element.attrib.get("FormaDePagoP")
    moneda_pago = pago_element.attrib.get("MonedaP")
    monto = pago_element.attrib.get("Monto")

    doc_relacionado_element = pago_element.find("pago20:DoctoRelacionado", ns)
    id_documento = doc_relacionado_element.attrib.get("IdDocumento")
    moneda_dr = doc_relacionado_element.attrib.get("MonedaDR")
    metodo_pago_dr = doc_relacionado_element.attrib.get("MetodoDePagoDR")
    num_parcialidad = doc_relacionado_element.attrib.get("NumParcialidad")
    imp_saldo_ant = doc_relacionado_element.attrib.get("ImpSaldoAnt")
    imp_pagado = doc_relacionado_element.attrib.get("ImpPagado")
    imp_saldo_insoluto = doc_relacionado_element.attrib.get("ImpSaldoInsoluto")

    return {
        "version": root.attrib.get("Version"),
        "Fecha": root.attrib.get("Fecha"),
        "RFC emisor": root.find("cfdi:Emisor", ns).attrib.get("Rfc"),
        "Nombre emisor": root.find("cfdi:Emisor", ns).attrib.get("Nombre"),
        "RFC receptor": root.find("cfdi:Receptor", ns).attrib.get("Rfc"),
        "Nombre receptor": root.find("cfdi:Receptor", ns).attrib.get("Nombre"),
        "uso_cfdi": root.find("cfdi:Receptor", ns).attrib.get("UsoCFDI"),
        "UUID": root.find("cfdi:Complemento/tfd:TimbreFiscalDigital", ns).attrib.get("UUID"),
        "FechaPago": fecha_pago,
        "FormaDePagoP": forma_pago,
        "MonedaP": moneda_pago,
        "Monto": monto,
        "IdDocumento": id_documento,
        "MonedaDR": moneda_dr,
        "MetodoDePagoDR": metodo_pago_dr,
        "NumParcialidad": num_parcialidad,
        "ImpSaldoAnt": imp_saldo_ant,
        "ImpPagado": imp_pagado,
        "ImpSaldoInsoluto": imp_saldo_insoluto
    }


def parse_xml32(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    namespaces = {
        'cfdi': 'http://www.sat.gob.mx/cfd/3',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
    }

    version = root.attrib.get('version', '')
    forma_de_pago = root.attrib.get('formaDePago', '')
    regimen = root.find('cfdi:Emisor', namespaces=namespaces).find('cfdi:RegimenFiscal', namespaces=namespaces).attrib.get('Regimen', '')
    tipo_de_comprobante = root.attrib.get('tipoDeComprobante', '')
    rfc_emisor = root.find('cfdi:Emisor', namespaces=namespaces).attrib.get('rfc', '')
    nombre_emisor = root.find('cfdi:Emisor', namespaces=namespaces).attrib.get('nombre', '')
    rfc_receptor = root.find('cfdi:Receptor', namespaces=namespaces).attrib.get('rfc', '')
    nombre_receptor = root.find('cfdi:Receptor', namespaces=namespaces).attrib.get('nombre', '')
    subtotal = root.attrib.get('subTotal', '')
    total = root.attrib.get('total', '')
    uuid = root.find('cfdi:Complemento/tfd:TimbreFiscalDigital', namespaces=namespaces).attrib.get('UUID', '')
    fecha_emision = root.attrib.get('fecha', '')

    return {
        'version': version,
        'forma_de_pago': forma_de_pago,
        'regimen': regimen,
        'tipo_de_comprobante': tipo_de_comprobante,
        'rfc_emisor': rfc_emisor,
        'nombre_emisor': nombre_emisor,
        'rfc_receptor': rfc_receptor,
        'nombre_receptor': nombre_receptor,
        'subtotal': subtotal,
        'total': total,
        'uuid': uuid,
        'fecha_emision': fecha_emision
    }

def search_xml_files(zip_file):
    xml_files = []

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('.xml'):
                xml_files.append(zip_ref.read(file))

    return xml_files

def main():
    uploaded_files = st.file_uploader('Cargar archivos ZIP', accept_multiple_files=True, type='zip')

    if st.button('Procesar') and uploaded_files:
        xml_files = []

        for uploaded_file in uploaded_files:
            with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    if file.endswith('.xml'):
                        xml_files.append(zip_ref.read(file))

        total_archivos = len(xml_files)
        st.info(f'Total de archivos cargados: {total_archivos}')

        start_time = time.time()
        
        data_parse_xml4 = []
        data_parse_xml33 = []
        data_parse_xml32 = []
        data_parse_xmlcomp33 = []
        data_parse_xmlcomp40 = []
        xml_files_not_processed_parse_xml4 = []
        xml_files_not_processed_parse_xml33 = []
        xml_files_not_processed_parse_xml32 = []
        xml_files_not_processed_parse_xmlcomp33 = []
        xml_files_not_processed_parse_xmlcomp40 = []
        
        df_parse_xml32 = pd.DataFrame()  # Inicializar df_parse_xml32 como un DataFrame vacío
        df_parse_xml33 = pd.DataFrame()  # Inicializar df_parse_xml33 como un DataFrame vacío
        df_parse_xml4 = pd.DataFrame()  # Inicializar df_parse_xml4 como un DataFrame vacío
        df_parser_xmlcomp33 = pd.DataFrame()  # Inicializar df_parse_xmlcomp33 como un DataFrame vacío
        df_parser_xmlcomp40 = pd.DataFrame()  # Inicializar df_parse_xmlcomp40 como un DataFrame vacío
        for xml_path in xml_files:
            try:
                xml_data_parse_xml4 = parse_xml4(xml_path)
                data_parse_xml4.append(xml_data_parse_xml4)
            except Exception as e:
                xml_files_not_processed_parse_xml4.append(xml_path)
        
            try:
                xml_data_parse_xml33 = parse_xml33(xml_path)
                data_parse_xml33.append(xml_data_parse_xml33)
            except Exception as e:
                xml_files_not_processed_parse_xml33.append(xml_path)

            try:
                xml_data_parse_xml32 = parse_xml32(xml_path)
                data_parse_xml32.append(xml_data_parse_xml32)
            except Exception as e:
                xml_files_not_processed_parse_xml32.append(xml_path)

            try:
                xml_data_parse_xmlcomp33 = parse_xmlcomp33(xml_path)
                data_parse_xmlcomp33.append(xml_data_parse_xmlcomp33)
            except Exception as e:
                xml_files_not_processed_parse_xmlcomp33.append(xml_path)

            try:
                xml_data_parse_xmlcomp40 = parse_xmlcomp40(xml_path)
                data_parse_xmlcomp40.append(xml_data_parse_xmlcomp40)
            except Exception as e:
                xml_files_not_processed_parse_xmlcomp40.append(xml_path)

        end_time = time.time()
        processing_time = end_time - start_time
        processing_time_formatted = "{:.4f}".format(processing_time)
        st.info(f'Se encontraron un total de {total_archivos} archivos, los cuales fueron procesados en un tiempo total de: {processing_time_formatted} segundos')

        df_parse_xml4 = pd.DataFrame(data_parse_xml4)
        df_parse_xml33 = pd.DataFrame(data_parse_xml33)
        df_parse_xml32 = pd.DataFrame(data_parse_xml32)
        df_parse_xmlcomp33 = pd.DataFrame(data_parse_xmlcomp33)
        df_parser_xmlcomp40 = pd.DataFrame(data_parse_xmlcomp40)

        if xml_files_not_processed_parse_xml4:
            df_not_processed_parse_xml4 = pd.DataFrame({'Archivo no procesado': xml_files_not_processed_parse_xml4})
            # st.warning(f'Archivos XML version 3.3 no procesados en la función 4.0: {len(df_not_processed_parse_xml4)}')
            #st.dataframe(df_not_processed_parse_xml4)
        
        if xml_files_not_processed_parse_xml33:
            df_not_processed_parse_xml33 = pd.DataFrame({'Archivo no procesado': xml_files_not_processed_parse_xml33})
            # st.warning(f'Archivos XML version 4.0 no procesados en la función 3.0: {len(df_not_processed_parse_xml33)}')
            #st.dataframe(df_not_processed_parse_xml33)

        if xml_files_not_processed_parse_xml32:
            df_not_processed_parse_xml32 = pd.DataFrame({'Archivo no procesado': xml_files_not_processed_parse_xml32})
            # st.warning(f'Archivos XML version 4.0 no procesados en la función : {len(df_not_processed_parse_xml32)}')
            #st.dataframe(df_not_processed_parse_xml33)
        
        
        df_parse_xml33 = df_parse_xml33[df_parse_xml33['rfc_emisor']!='']
        CFDIs = pd.concat([df_parse_xml33, df_parse_xml4, df_parse_xml32], ignore_index=True)
        CFDIs[['fecha_emision', 'hora_emision']] = CFDIs['fecha_emision'].str.split('T', n=1, expand=True)
        CFDIs[['fecha_emision']] = CFDIs[['fecha_emision']].apply(pd.to_datetime)
        CFDIs[['subtotal', 'total']] = CFDIs[['subtotal', 'total']].apply(pd.to_numeric)
        CFDIs['tipo_de_comprobante'] = CFDIs['tipo_de_comprobante'].replace(['I'],'ingreso')
        CFDIs['tipo_de_comprobante'] = CFDIs['tipo_de_comprobante'].replace(['E'],'egreso')
        CFDIs['tipo_de_comprobante'] = CFDIs['tipo_de_comprobante'].replace(['P'],'pago')
        CFDIs['tipo_de_comprobante'] = CFDIs['tipo_de_comprobante'].str.capitalize()
        CFDIs['Año'] = CFDIs['fecha_emision'].dt.year
        CFDIs['Mes'] = CFDIs['fecha_emision'].dt.month
        CFDIs['Día'] = CFDIs['fecha_emision'].dt.day
        CFDIs[['Año', 'Mes', 'Día']] = CFDIs[['Año', 'Mes', 'Día']].astype('string')
        
        Summary = CFDIs.groupby(by=['Año', 'Mes'], as_index=False)['subtotal'].sum()
        # formadepago = CFDIs[['forma_de_pago']].drop_duplicates()
        
        # st.write(len(df_parse_xml33))
        # st.dataframe(df_parse_xml33)

        # st.write(df_parse_xml32.shape)
        # st.dataframe(df_parse_xml32)
        # st.write(df_parse_xml33.shape)
        # st.dataframe(df_parse_xml33)
        # st.write(df_parse_xml4.shape)
        # st.dataframe(df_parse_xml4)
        
        
            

        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["CFDIs", "Ingresos", "Egresos", "Complementos Pago", "Conciliacion Pagos"])

        with tab1:
            st.subheader("Total de CFDIs")
            st.caption('Detalle de los CFDIs procesados')
            st.write(CFDIs.shape)
            st.dataframe(CFDIs, height=600)
            # st.selectbox('selecciona la fecha', ['Ene', 'Feb'])


        with tab2:
            st.subheader("Ingresos")
            if rfc_busqueda:
                CFDIs_rfc_emisor = CFDIs[(CFDIs['rfc_emisor'] == rfc_busqueda) & (CFDIs['tipo_de_comprobante'] != 'Pago') ] 
                # Customer = Customer[(Customer['Tx'] == 'EG') | (Customer['Tx'] == 'OK')]
                st.caption('Detalle de CFDIs de Ingresos')
                st.caption(f'Resultados filtrados por el RFC: {rfc_busqueda}')
                st.write(CFDIs_rfc_emisor.shape)
                st.dataframe(CFDIs_rfc_emisor)
                st.divider()
                st.caption('Resumen por periodo de Ingresos')
                summary_rfc_emisor = CFDIs_rfc_emisor.groupby(by=['rfc_emisor', 'Año', 'Mes'], as_index=False)['subtotal'].sum()
                st.dataframe(summary_rfc_emisor)
                st.bar_chart(CFDIs_rfc_emisor, x='fecha_emision', y='subtotal')

        with tab3:
            st.subheader("Egresos")
            if rfc_busqueda:
                # CFDIs_rfc_receptor = CFDIs[CFDIs['rfc_receptor'] == rfc_busqueda]
                CFDIs_rfc_receptor = CFDIs[(CFDIs['rfc_receptor'] == rfc_busqueda) & (CFDIs['tipo_de_comprobante'] != 'Pago') ] 
                st.caption('Detalle de CFDIs de Egresos')
                st.caption(f'Resultados filtrados por el RFC: {rfc_busqueda}')
                st.write(CFDIs_rfc_receptor.shape)
                st.dataframe(CFDIs_rfc_receptor)
                st.divider()
                st.subheader('Resumen por periodo de Egresos')
                summary_rfc_receptor = CFDIs_rfc_receptor.groupby(by=['rfc_receptor', 'Año', 'Mes'], as_index=False)['subtotal'].sum()
                st.dataframe(summary_rfc_receptor)

        with tab4:
            st.subheader("Complementos de Pago")
            if rfc_busqueda and not df_parse_xmlcomp33.empty and not df_parser_xmlcomp40.empty:
                # CFDIs_rfc_receptor = CFDIs[CFDIs['rfc_receptor'] == rfc_busqueda]
                # comp_pago = df_parse_xmlcomp33[CFDIs['rfc_receptor'] == rfc_busqueda] 
                st.caption('Detalle de los complementos de pago recibidos')
                st.caption(f'Resultados filtrados por el RFC: {rfc_busqueda}')
                # conciliacion = CFDIs.merge('UUID', left_on=)
                st.write(df_parse_xmlcomp33.shape) 
                df_parse_xmlcomp33 = pd.concat([df_parse_xmlcomp33, df_parser_xmlcomp40], ignore_index=True)
                df_parse_xmlcomp33[['fecha_emision', 'hora_emision']] = df_parse_xmlcomp33['Fecha'].str.split('T', n=1, expand=True)
                df_parse_xmlcomp33[['fecha_emision']] = df_parse_xmlcomp33[['fecha_emision']].apply(pd.to_datetime)
                df_parse_xmlcomp33[['Monto', 'ImpSaldoAnt', 'ImpPagado', 'ImpSaldoInsoluto', 'NumParcialidad']] = df_parse_xmlcomp33[['Monto', 'ImpSaldoAnt', 'ImpPagado', 'ImpSaldoInsoluto', 'NumParcialidad']].apply(pd.to_numeric)
                df_parse_xmlcomp33['Año'] = df_parse_xmlcomp33['fecha_emision'].dt.year
                df_parse_xmlcomp33['Mes'] = df_parse_xmlcomp33['fecha_emision'].dt.month
                df_parse_xmlcomp33['Día'] = df_parse_xmlcomp33['fecha_emision'].dt.day
                df_parse_xmlcomp33[['Año', 'Mes', 'Día']] = df_parse_xmlcomp33[['Año', 'Mes', 'Día']].astype('string')
        

                
                st.dataframe(df_parse_xmlcomp33)
        
        with tab5:
            st.subheader("Conciliacion de Pagos")
            if rfc_busqueda and not df_parse_xmlcomp33.empty:
                # CFDIs_rfc_receptor = CFDIs[CFDIs['rfc_receptor'] == rfc_busqueda]
                # comp_pago = df_parse_xmlcomp33[CFDIs['rfc_receptor'] == rfc_busqueda] 
                st.caption('Conciliacion de los complementos de pago vs CFDIs de Egresos')
                st.caption(f'Resultados filtrados por el RFC: {rfc_busqueda}')
                #agrupar los comprobantes de pago por: rfc_emisor, rfc_receptor, fecha de pago (split column by delimiter to datetime), convertir a numero las columnas de numeros, 
                #agregar tambien estructura de comprobante de pago 4.0
                resumen_comppagos = df_parse_xmlcomp33.groupby(by=['RFC emisor', 'Nombre emisor', 'RFC receptor', 'IdDocumento'], as_index=False)['ImpPagado'].sum()
                
                # conciliacion = CFDIs.merge('UUID', left_on=)
                # conciliacion = df_FBL3N.merge(df_parametros, left_on='Account', right_on='GL_Account', how='left')
                st.write(resumen_comppagos.shape)
                st.dataframe(resumen_comppagos)

        if st.button('Descargar Excel'):
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                # Escribir los DataFrames en hojas de Excel
                CFDIs.to_excel(writer, sheet_name='CFDIs')
                CFDIs_rfc_emisor.to_excel(writer, sheet_name='Ingresos')
                CFDIs_rfc_receptor.to_excel(writer, sheet_name='Egresos')
                df_parse_xmlcomp33.to_excel(writer, sheet_name='Comp Pago')
                resumen_comppagos.to_excel(writer, sheet_name='Conciliacion')

                # Cerrar el escritor de Excel y guardar el archivo en el buffer
                writer.save()

            # Establecer enlace de descarga
            b64 = base64.b64encode(buffer.getvalue()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Descargar Excel</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
    

