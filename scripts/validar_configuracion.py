#!/usr/bin/env python3
"""
Script para validar la configuración de AWS y permisos necesarios
"""

import boto3
import sys
from botocore.exceptions import ClientError, NoCredentialsError

def validar_credenciales():
    """Valida que las credenciales de AWS estén configuradas"""
    print("🔍 Validando credenciales de AWS...")
    try:
        session = boto3.Session()
        sts = session.client('sts')
        identity = sts.get_caller_identity()
        
        print("✅ Credenciales válidas")
        print(f"   Account ID: {identity['Account']}")
        print(f"   ARN: {identity['Arn']}")
        print(f"   User ID: {identity['UserId']}")
        return True
    except NoCredentialsError:
        print("❌ No se encontraron credenciales de AWS")
        print("   Ejecuta: aws configure")
        return False
    except Exception as e:
        print(f"❌ Error al validar credenciales: {e}")
        return False

def validar_permisos_cost_explorer():
    """Valida que el usuario tenga permisos para Cost Explorer"""
    print("\n🔍 Validando permisos de Cost Explorer...")
    try:
        from datetime import datetime, timedelta
        
        ce = boto3.client('ce', region_name='us-east-1')
        
        # Intentar una consulta simple
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost']
        )
        
        print("✅ Permisos de Cost Explorer configurados correctamente")
        
        # Mostrar un ejemplo de costo
        if response['ResultsByTime']:
            ultimo_dia = response['ResultsByTime'][-1]
            costo = float(ultimo_dia['Total']['UnblendedCost']['Amount'])
            fecha = ultimo_dia['TimePeriod']['Start']
            print(f"   Último costo registrado: ${costo:.2f} US$ ({fecha})")
        
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            print("❌ No tienes permisos para acceder a Cost Explorer")
            print("   Necesitas los permisos: ce:GetCostAndUsage")
            print("   Ver archivo: iam_policy.json")
        else:
            print(f"❌ Error: {e.response['Error']['Message']}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def validar_etiquetas():
    """Verifica si hay recursos con etiquetas Name"""
    print("\n🔍 Verificando recursos con etiqueta Name...")
    try:
        from datetime import datetime, timedelta
        
        ce = boto3.client('ce', region_name='us-east-1')
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        response = ce.get_tags(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            TagKey='Name'
        )
        
        if response['Tags']:
            print(f"✅ Se encontraron {len(response['Tags'])} etiquetas Name activas")
            print("   Ejemplos:")
            for tag in response['Tags'][:5]:
                print(f"   - {tag}")
            if len(response['Tags']) > 5:
                print(f"   ... y {len(response['Tags']) - 5} más")
        else:
            print("⚠️  No se encontraron recursos con etiqueta Name")
            print("   Asegúrate de etiquetar tus recursos con la clave 'Name'")
        
        return True
    except Exception as e:
        print(f"⚠️  No se pudieron verificar las etiquetas: {e}")
        return False

def validar_backup_tags():
    """Verifica si hay recursos con etiquetas AWSBackup"""
    print("\n🔍 Verificando recursos con etiquetas AWS Backup...")
    try:
        from datetime import datetime, timedelta
        
        ce = boto3.client('ce', region_name='us-east-1')
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        
        response = ce.get_tags(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            TagKey='AWSBackup'
        )
        
        if response['Tags']:
            print(f"✅ Se encontraron {len(response['Tags'])} etiquetas AWSBackup")
            valores_esperados = ['BackupDia', 'BackupSemana', 'BackupMes']
            for valor in response['Tags']:
                if valor in valores_esperados:
                    print(f"   ✓ {valor}")
        else:
            print("⚠️  No se encontraron etiquetas AWSBackup")
            print("   Valores esperados: BackupDia, BackupSemana, BackupMes")
        
        return True
    except Exception as e:
        print(f"⚠️  No se pudieron verificar las etiquetas de Backup: {e}")
        return False

def main():
    print("=" * 70)
    print("AWS Cost Report - Validación de Configuración")
    print("=" * 70)
    print()
    
    validaciones = [
        validar_credenciales(),
        validar_permisos_cost_explorer(),
        validar_etiquetas(),
        validar_backup_tags()
    ]
    
    print("\n" + "=" * 70)
    if all(validaciones[:2]):  # Las dos primeras son críticas
        print("✅ CONFIGURACIÓN VÁLIDA - El script aws_cost_report.py está listo para usar")
    else:
        print("❌ CONFIGURACIÓN INCOMPLETA - Revisa los errores anteriores")
        sys.exit(1)
    
    if not all(validaciones[2:]):  # Las otras son advertencias
        print("⚠️  Hay algunas advertencias, pero el script funcionará")
    
    print("=" * 70)
    print("\n💡 Siguiente paso: Ejecutar el script principal")
    print("   python aws_cost_report.py")
    print("   python aws_cost_report.py --mes 10 --anio 2024")

if __name__ == '__main__':
    main()
