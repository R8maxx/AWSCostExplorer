#!/usr/bin/env python3
"""
Script de ejemplo/demo para mostrar la estructura de salida
sin necesidad de credenciales de AWS
"""

import pandas as pd
from datetime import datetime


def crear_excel_demo():
    """Crea un archivo Excel de ejemplo con datos simulados"""

    # Datos de ejemplo con Name y ServerGroup
    datos_ejemplo = [
        {'Name': 'servidor-web-prod', 'ServerGroup': 'WebServers', 'Servicio': 'TOTAL', 'Costo (US$)': 250.50},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'Amazon Elastic Compute Cloud - Compute', 'Costo (US$)': 180.30},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'Amazon Elastic Block Store', 'Costo (US$)': 45.20},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'AWS Backup (avanza_backup_daily)', 'Costo (US$)': 25.00},
        {'Name': '', 'ServerGroup': '', 'Servicio': '', 'Costo (US$)': ''},

        {'Name': 'db-produccion', 'ServerGroup': 'Database', 'Servicio': 'TOTAL', 'Costo (US$)': 450.75},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'Amazon Relational Database Service', 'Costo (US$)': 380.50},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'Amazon Elastic Block Store', 'Costo (US$)': 60.25},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'AWS Backup (avanza_backup_weekly)', 'Costo (US$)': 10.00},
        {'Name': '', 'ServerGroup': '', 'Servicio': '', 'Costo (US$)': ''},

        {'Name': 'bucket-archivos-s3', 'ServerGroup': 'Storage', 'Servicio': 'TOTAL', 'Costo (US$)': 89.50},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'Amazon Simple Storage Service', 'Costo (US$)': 75.30},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'AWS Backup (avanza-backup-monthly)', 'Costo (US$)': 14.20},
        {'Name': '', 'ServerGroup': '', 'Servicio': '', 'Costo (US$)': ''},

        {'Name': 'app-desarrollo', 'ServerGroup': 'WebServers', 'Servicio': 'TOTAL', 'Costo (US$)': 85.30},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'Amazon Elastic Compute Cloud - Compute', 'Costo (US$)': 65.30},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'Amazon Elastic Block Store', 'Costo (US$)': 20.00},
        {'Name': '', 'ServerGroup': '', 'Servicio': '', 'Costo (US$)': ''},

        {'Name': 'vpc-principal', 'ServerGroup': 'Network', 'Servicio': 'TOTAL', 'Costo (US$)': 11.04},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'Amazon Virtual Private Cloud', 'Costo (US$)': 11.04},
        {'Name': '', 'ServerGroup': '', 'Servicio': '', 'Costo (US$)': ''},

        {'Name': 'Sin etiqueta', 'ServerGroup': '', 'Servicio': 'TOTAL', 'Costo (US$)': 125.68},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'Amazon Elastic Compute Cloud - Compute', 'Costo (US$)': 98.44},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'AWS Lambda', 'Costo (US$)': 15.24},
        {'Name': '', 'ServerGroup': '', 'Servicio': 'Amazon CloudWatch', 'Costo (US$)': 12.00},
    ]

    df = pd.DataFrame(datos_ejemplo)

    # Resumen
    resumen_data = [
        ['Periodo', '2024-11-01 a 2024-12-01'],
        [''],
        ['Name', 'ServerGroup', 'Costo Total (US$)'],
        ['db-produccion', 'Database', 450.75],
        ['servidor-web-prod', 'WebServers', 250.50],
        ['Sin etiqueta', '', 125.68],
        ['bucket-archivos-s3', 'Storage', 89.50],
        ['app-desarrollo', 'WebServers', 85.30],
        ['vpc-principal', 'Network', 11.04],
        [''],
        ['COSTO TOTAL GENERAL', '', 1012.77]
    ]

    nombre_archivo = 'aws_costos_ejemplo.xlsx'

    with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Costos por Etiqueta', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Costos por Etiqueta']

        # Ajustar anchos
        worksheet.column_dimensions['A'].width = 35  # Name
        worksheet.column_dimensions['B'].width = 25  # ServerGroup
        worksheet.column_dimensions['C'].width = 50  # Servicio
        worksheet.column_dimensions['D'].width = 15  # Costo

        # Aplicar formato
        from openpyxl.styles import Font, PatternFill

        fill_total = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
        font_bold = Font(bold=True)

        for row_idx, row in enumerate(worksheet.iter_rows(min_row=2, max_row=worksheet.max_row), start=2):
            if row[2].value == 'TOTAL':  # Columna "Servicio"
                for cell in row:
                    cell.fill = fill_total
                    cell.font = font_bold

        # Hoja de resumen
        df_resumen = pd.DataFrame(resumen_data)
        df_resumen.to_excel(writer, sheet_name='Resumen', index=False, header=False)

        worksheet_resumen = writer.sheets['Resumen']
        worksheet_resumen.column_dimensions['A'].width = 35
        worksheet_resumen.column_dimensions['B'].width = 25
        worksheet_resumen.column_dimensions['C'].width = 20

        # Formato para el total
        fill_total_general = PatternFill(start_color='FFA500', end_color='FFA500', fill_type='solid')
        for cell in worksheet_resumen[len(resumen_data) + 1]:
            cell.fill = fill_total_general
            cell.font = Font(bold=True, size=12)

        # Agregar hoja de análisis por ServerGroup
        analisis_sg = [
            ['ServerGroup', 'Costo Total (US$)'],
            ['Database', 450.75],
            ['WebServers', 335.80],
            ['Sin ServerGroup', 125.68],
            ['Storage', 89.50],
            ['Network', 11.04]
        ]
        df_sg = pd.DataFrame(analisis_sg[1:], columns=analisis_sg[0])
        df_sg.to_excel(writer, sheet_name='Por ServerGroup', index=False)

        ws_sg = writer.sheets['Por ServerGroup']
        ws_sg.column_dimensions['A'].width = 35
        ws_sg.column_dimensions['B'].width = 20
        for cell in ws_sg[1]:
            cell.fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
            cell.font = Font(color='FFFFFF', bold=True)

    print("✅ Archivo de ejemplo creado: aws_costos_ejemplo.xlsx")
    print(f"Este archivo muestra la estructura de salida del script principal")
    print(f"Total de ejemplo: $1,012.77 US$")
    print(f"Incluye 3 hojas: Detalle, Resumen, Por ServerGroup")


if __name__ == '__main__':
    crear_excel_demo()