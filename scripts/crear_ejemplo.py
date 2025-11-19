#!/usr/bin/env python3
"""
Script de ejemplo/demo para mostrar la estructura de salida
sin necesidad de credenciales de AWS
"""

import pandas as pd
from datetime import datetime

def crear_excel_demo():
    """Crea un archivo Excel de ejemplo con datos simulados"""
    
    # Datos de ejemplo basados en las imágenes proporcionadas
    datos_ejemplo = [
        {'Etiqueta Name': 'servidor-web-prod', 'Servicio': 'TOTAL', 'Costo (US$)': 250.50},
        {'Etiqueta Name': '', 'Servicio': 'Amazon Elastic Compute Cloud - Compute', 'Costo (US$)': 180.30},
        {'Etiqueta Name': '', 'Servicio': 'Amazon Elastic Block Store', 'Costo (US$)': 45.20},
        {'Etiqueta Name': '', 'Servicio': 'AWS Backup (avanza_backup_daily)', 'Costo (US$)': 25.00},
        {'Etiqueta Name': '', 'Servicio': '', 'Costo (US$)': ''},
        
        {'Etiqueta Name': 'db-produccion', 'Servicio': 'TOTAL', 'Costo (US$)': 450.75},
        {'Etiqueta Name': '', 'Servicio': 'Amazon Relational Database Service', 'Costo (US$)': 380.50},
        {'Etiqueta Name': '', 'Servicio': 'Amazon Elastic Block Store', 'Costo (US$)': 60.25},
        {'Etiqueta Name': '', 'Servicio': 'AWS Backup (avanza_backup_weekly)', 'Costo (US$)': 10.00},
        {'Etiqueta Name': '', 'Servicio': '', 'Costo (US$)': ''},
        
        {'Etiqueta Name': 'bucket-archivos-s3', 'Servicio': 'TOTAL', 'Costo (US$)': 89.50},
        {'Etiqueta Name': '', 'Servicio': 'Amazon Simple Storage Service', 'Costo (US$)': 75.30},
        {'Etiqueta Name': '', 'Servicio': 'AWS Backup (avanza-backup-monthly)', 'Costo (US$)': 14.20},
        {'Etiqueta Name': '', 'Servicio': '', 'Costo (US$)': ''},
        
        {'Etiqueta Name': 'vpc-principal', 'Servicio': 'TOTAL', 'Costo (US$)': 11.04},
        {'Etiqueta Name': '', 'Servicio': 'Amazon Virtual Private Cloud', 'Costo (US$)': 11.04},
        {'Etiqueta Name': '', 'Servicio': '', 'Costo (US$)': ''},
        
        {'Etiqueta Name': 'Sin etiqueta', 'Servicio': 'TOTAL', 'Costo (US$)': 125.68},
        {'Etiqueta Name': '', 'Servicio': 'Amazon Elastic Compute Cloud - Compute', 'Costo (US$)': 98.44},
        {'Etiqueta Name': '', 'Servicio': 'AWS Lambda', 'Costo (US$)': 15.24},
        {'Etiqueta Name': '', 'Servicio': 'Amazon CloudWatch', 'Costo (US$)': 12.00},
    ]
    
    df = pd.DataFrame(datos_ejemplo)
    
    # Resumen
    resumen_data = [
        ['Periodo', '2024-11-01 a 2024-12-01'],
        [''],
        ['Resumen por Etiqueta Name', 'Costo Total (US$)'],
        ['servidor-web-prod', 250.50],
        ['db-produccion', 450.75],
        ['Sin etiqueta', 125.68],
        ['bucket-archivos-s3', 89.50],
        ['vpc-principal', 11.04],
        [''],
        ['COSTO TOTAL GENERAL', 927.47]
    ]
    
    nombre_archivo = 'aws_costos_ejemplo.xlsx'
    
    with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Costos por Etiqueta', index=False)
        
        workbook = writer.book
        worksheet = writer.sheets['Costos por Etiqueta']
        
        # Ajustar anchos
        worksheet.column_dimensions['A'].width = 35
        worksheet.column_dimensions['B'].width = 50
        worksheet.column_dimensions['C'].width = 15
        
        # Aplicar formato
        from openpyxl.styles import Font, PatternFill
        
        fill_total = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
        font_bold = Font(bold=True)
        
        for row_idx, row in enumerate(worksheet.iter_rows(min_row=2, max_row=worksheet.max_row), start=2):
            if row[1].value == 'TOTAL':
                for cell in row:
                    cell.fill = fill_total
                    cell.font = font_bold
        
        # Hoja de resumen
        df_resumen = pd.DataFrame(resumen_data)
        df_resumen.to_excel(writer, sheet_name='Resumen', index=False, header=False)
        
        worksheet_resumen = writer.sheets['Resumen']
        worksheet_resumen.column_dimensions['A'].width = 30
        worksheet_resumen.column_dimensions['B'].width = 20
        
        # Formato para el total
        fill_total_general = PatternFill(start_color='FFA500', end_color='FFA500', fill_type='solid')
        for cell in worksheet_resumen[len(resumen_data) + 1]:
            cell.fill = fill_total_general
            cell.font = Font(bold=True, size=12)
    
    print("✅ Archivo de ejemplo creado: aws_costos_ejemplo.xlsx")
    print(f"Este archivo muestra la estructura de salida del script principal")
    print(f"Total de ejemplo: $927.47 US$")

if __name__ == '__main__':
    crear_excel_demo()
