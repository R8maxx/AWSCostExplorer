# AWS Cost Report - Costos por Etiqueta Name

Script de Python para extraer y analizar costos de AWS organizados por la etiqueta "Name". Incluye todos los servicios (EC2, S3, RDS, VPC, etc.) y costos específicos de AWS Backup.

## 📋 Requisitos

- Python 3.7 o superior
- Credenciales de AWS configuradas
- Permisos IAM necesarios:
  - `ce:GetCostAndUsage`
  - `ce:GetTags`

## 🚀 Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar credenciales de AWS (si no lo has hecho):
```bash
aws configure
```

## 💻 Uso

### Ejemplos básicos:

**Obtener costos del mes actual:**
```bash
python aws_cost_report.py
```

**Obtener costos de un mes específico:**
```bash
python aws_cost_report.py --mes 10 --anio 2024
```

**Especificar nombre de archivo de salida:**
```bash
python aws_cost_report.py --mes 11 --anio 2024 --output costos_noviembre_2024.xlsx
```

**Usar un perfil específico de AWS:**
```bash
python aws_cost_report.py --profile mi-perfil --mes 1 --anio 2025
```

**Cambiar región:**
```bash
python aws_cost_report.py --region eu-west-1
```

### Parámetros disponibles:

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `--mes` | Mes a consultar (1-12) | `--mes 10` |
| `--anio` | Año a consultar | `--anio 2024` |
| `--output` | Nombre del archivo Excel | `--output costos.xlsx` |
| `--profile` | Perfil de AWS CLI | `--profile produccion` |
| `--region` | Región de AWS | `--region us-east-1` |

## 📊 Salida

El script genera un archivo Excel con dos hojas:

### 1. Costos por Etiqueta
Detalle completo de costos organizados por etiqueta Name y servicio:
- Agrupación por etiqueta Name
- Total por recurso (resaltado en amarillo)
- Desglose por cada servicio de AWS
- Costos de AWS Backup asociados a cada plan

### 2. Resumen
Vista consolidada con:
- Periodo consultado
- Total por etiqueta Name (ordenado de mayor a menor)
- Costo total general (resaltado en naranja)

## 🔄 AWS Backup

El script identifica automáticamente los costos de AWS Backup basándose en:

| Etiqueta AWSBackup | Plan de Backup |
|-------------------|----------------|
| `BackupDia` | avanza_backup_daily |
| `BackupSemana` | avanza_backup_weekly |
| `BackupMes` | avanza-backup-monthly |

Los costos de backup se asocian a la etiqueta Name del recurso respaldado.

## 🔐 Permisos IAM necesarios

Crear una política con estos permisos:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ce:GetCostAndUsage",
                "ce:GetTags"
            ],
            "Resource": "*"
        }
    ]
}
```

## 📝 Notas importantes

1. **Etiquetas Name**: Los recursos deben tener la etiqueta "Name" para aparecer correctamente agrupados
2. **Recursos sin etiqueta**: Los recursos sin la etiqueta Name aparecerán como "Sin etiqueta"
3. **Moneda**: Todos los costos se muestran en dólares estadounidenses (US$)
4. **Delay de AWS**: Los costos pueden tardar hasta 24 horas en aparecer en Cost Explorer
5. **Región**: Cost Explorer es un servicio global, pero se accede desde us-east-1

## 🐛 Solución de problemas

### Error: "Unable to locate credentials"
```bash
aws configure
# O especificar perfil:
export AWS_PROFILE=mi-perfil
```

### Error: "Access Denied"
Verificar que el usuario/rol tiene permisos `ce:GetCostAndUsage`

### No aparecen costos de AWS Backup
- Verificar que los recursos tengan la etiqueta `AWSBackup` con valores: BackupDia, BackupSemana o BackupMes
- Los planes de backup deben estar activos y respaldando recursos

### Los costos no coinciden con Cost Explorer
- Asegurarse de usar el mismo periodo de tiempo
- Los costos son "UnblendedCost" (sin descuentos de RI/Savings Plans)

## 📧 Soporte

Para problemas o preguntas, contactar al equipo de DevOps o Cloud.

## 🔄 Actualizaciones

**Versión 1.0** - Características:
- ✅ Costos por etiqueta Name
- ✅ Todos los servicios de AWS
- ✅ Integración con AWS Backup
- ✅ Exportación a Excel con formato
- ✅ Hoja de resumen
- ✅ Soporte para periodos personalizados