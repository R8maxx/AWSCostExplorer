# AWS Cost Report V2 - Análisis Detallado de Costos

Script de Python para extraer y analizar costos de AWS con **desglose completo de EC2** y máxima claridad. Sin categorías genéricas "Others", todo perfectamente identificado.

## 🎯 Características Principales

### ✅ Agrupación por Etiqueta Name
- Cada recurso AWS identificado por su etiqueta **Name**
- Totales y detalles organizados por recurso

### 📋 ServerGroup Informativo
- Muestra la etiqueta **ServerGroup** como información adicional
- Útil para contexto y clasificación visual
- No afecta la agrupación de costos

### 🔍 Desglose Completo de EC2
**Sin "Others" genéricos** - Todo identificado específicamente:
- **Instancias:** `EC2 - Instancia (t3.large)`, `EC2 - Instancia (t2.micro)`
- **Volúmenes:** `EC2 - EBS Volumes (gp3)`, `EC2 - EBS Volumes (gp2)`, `EC2 - EBS Volumes (io1/io2)`
- **Red:** `EC2 - Network Interfaces (ENI)`, `EC2 - Elastic IPs`, `EC2 - Data Transfer (Out)`
- **Snapshots:** `EC2 - EBS Snapshots`
- **NAT Gateway:** `EC2 - NAT Gateway (Hours)`, `EC2 - NAT Gateway (Data Processed)`
- **Load Balancers:** `EC2 - Load Balancer (ALB)`, `EC2 - Load Balancer (NLB)`
- **Otros:** VPN, CloudWatch, IOPS, Throughput, etc.

### 💾 AWS Backup Automático
- Se asocia automáticamente por etiqueta **Name**
- **NO requiere** etiquetas adicionales como `avanza_backup_xxx`
- Aparece como "AWS Backup" en el desglose

---

## 📋 Requisitos

- **Python:** 3.7 o superior
- **AWS CLI:** Configurado con credenciales válidas
- **Permisos IAM:** `ce:GetCostAndUsage` y `ce:GetTags`

---

## 🚀 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar AWS (si no está configurado)

```bash
aws configure
```

Ingresa:
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `us-east-1`
- Default output format: `json`

### 3. Aplicar política IAM

Asigna la política en `iam_policy.json` a tu usuario/rol de AWS.

---

## 💻 Uso

### Ejemplos Básicos

```bash
# Costos del mes actual
python aws_cost_report.py

# Costos de un mes específico
python aws_cost_report.py --mes 10 --anio 2024

# Con nombre de archivo personalizado
python aws_cost_report.py --output costos_octubre_2024.xlsx

# Usando un perfil específico de AWS
python aws_cost_report.py --profile produccion

# Combinando parámetros
python aws_cost_report.py --mes 11 --anio 2024 --output nov_2024.xlsx --profile prod
```

### Parámetros Disponibles

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `--mes` | Mes a consultar (1-12) | `--mes 10` |
| `--anio` | Año a consultar | `--anio 2024` |
| `--output` | Nombre del archivo Excel | `--output mis_costos.xlsx` |
| `--profile` | Perfil de AWS CLI | `--profile produccion` |
| `--region` | Región de AWS | `--region us-east-1` |

---

## 📊 Salida - Excel con 3 Hojas

### Hoja 1: Detalle de Costos

Vista completa con cada recurso y su desglose de servicios:

| Name | ServerGroup | Servicio | Costo (US$) |
|------|-------------|----------|-------------|
| produccion.avanza20rl | PRL | *** TOTAL *** | 834.28 |
| | | EC2 - Instancia (t3.large) | 350.50 |
| | | EC2 - Instancia (t3.medium) | 112.15 |
| | | EC2 - Data Transfer (Out) | 142.97 |
| | | EC2 - EBS Volumes (gp3) | 85.00 |
| | | EC2 - Network Interfaces (ENI) | 25.00 |
| | | EC2 - EBS Snapshots | 14.30 |
| | | AWS Backup | 41.26 |
| | | Amazon S3 | 18.11 |
| | | Amazon VPC | 3.72 |

**Características:**
- ✅ Fila de total por recurso (amarillo claro)
- ✅ Servicios ordenados por costo (mayor a menor)
- ✅ EC2 completamente desglosado
- ✅ Sin "Others" genéricos

### Hoja 2: Resumen

Vista consolidada ordenada por costo total:

| Name | ServerGroup | Costo Total (US$) |
|------|-------------|-------------------|
| produccion.avanza20rl | PRL | 834.28 |
| app-desarrollo | WebServers | 125.50 |
| vpc-principal | Network | 45.80 |
| ... | ... | ... |
| ***** TOTAL GENERAL ***** | | **1,234.56** |

**Características:**
- ✅ Totales por recurso
- ✅ Ordenado de mayor a menor costo
- ✅ Total general (naranja)

### Hoja 3: Por ServerGroup

Análisis agregado por grupo de servidores:

| ServerGroup | Costo Total (US$) |
|-------------|-------------------|
| PRL | 834.28 |
| WebServers | 210.80 |
| Network | 45.80 |
| Sin ServerGroup | 143.68 |

**Características:**
- ✅ Suma de costos por ServerGroup
- ✅ Incluye "Sin ServerGroup" para recursos sin esa etiqueta
- ✅ Encabezado azul

---

## 🏷️ Etiquetas Requeridas

### Name (Requerida)
- **Propósito:** Identificar cada recurso
- **Ejemplos:** `servidor-web-prod`, `db-produccion`, `vpc-principal`
- **Importante:** Sin esta etiqueta, los recursos aparecen como "Sin etiqueta"

### ServerGroup (Opcional)
- **Propósito:** Agrupar recursos por función o tipo
- **Ejemplos:** `WebServers`, `Database`, `Network`, `Storage`
- **Nota:** Solo informativa, no afecta la agrupación de costos

---

## 🔍 Desglose de EC2 Detallado

El script categoriza automáticamente todos los componentes de EC2:

### Instancias y Compute
- `EC2 - Instancia (tipo)` - Con tipo específico (t3.large, t2.micro, etc.)
- `EC2 - Spot Instances` - Instancias Spot
- `EC2 - Reserved Instances` - Instancias reservadas

### Almacenamiento EBS
- `EC2 - EBS Volumes (gp3)` - SSD propósito general
- `EC2 - EBS Volumes (gp2)` - SSD propósito general anterior
- `EC2 - EBS Volumes (io1/io2)` - SSD alto rendimiento
- `EC2 - EBS Volumes (st1)` - HDD throughput optimizado
- `EC2 - EBS Volumes (sc1)` - HDD cold storage
- `EC2 - EBS Snapshots` - Copias de seguridad
- `EC2 - EBS IOPS` - IOPS provisionadas
- `EC2 - EBS Throughput` - Throughput provisionado

### Red
- `EC2 - Network Interfaces (ENI)` - Interfaces de red elásticas
- `EC2 - Elastic IPs` - Direcciones IP elásticas
- `EC2 - Data Transfer (Out)` - Transferencia de datos saliente
- `EC2 - Data Transfer (Regional/In)` - Transferencia regional o entrante

### Infraestructura
- `EC2 - NAT Gateway (Hours)` - Horas de NAT Gateway
- `EC2 - NAT Gateway (Data Processed)` - Datos procesados por NAT
- `EC2 - Load Balancer (ALB)` - Application Load Balancer
- `EC2 - Load Balancer (NLB)` - Network Load Balancer
- `EC2 - VPN Connection` - Conexión VPN

### Otros
- `EC2 - CloudWatch Monitoring` - Monitoreo detallado
- `EC2 - EBS Optimized` - Instancias optimizadas para EBS

---

## 💾 AWS Backup

El script detecta automáticamente los costos de AWS Backup asociados a cada recurso:

- **Detección:** Por etiqueta **Name**
- **NO requiere:** Etiquetas adicionales (`avanza_backup_daily`, etc.)
- **Aparece como:** "AWS Backup" en el desglose de servicios

---

## ⏱️ Rendimiento

- **Consultas a AWS:** 5-6 consultas a Cost Explorer
- **Tiempo de ejecución:** ~30-40 segundos
- **Costo AWS:** ~$0.05-0.06 USD por ejecución ($0.01 por consulta)

---

## 🔐 Permisos IAM Necesarios

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

Ver archivo `iam_policy.json` incluido.

---

## 📝 Ejemplo de Salida en Consola

```
======================================================================
AWS COST REPORT - Desglose Completo por Name
======================================================================
✅ Conectado a AWS (us-east-1)
📊 Obteniendo costos base por Name y Servicio...
🏷️  Obteniendo etiquetas ServerGroup...
🔍 Desglosando EC2 en detalle...
   → Amazon Elastic Compute Cloud - Compute
   → EC2 - Other
   → Amazon Elastic Block Store
💾 Obteniendo costos de AWS Backup...
⚙️  Procesando datos...
📝 Creando Excel...

✅ Excel creado: aws_costos_detallados.xlsx
💰 Costo total: $1,234.56 USD
📊 Recursos: 15
======================================================================
✨ Completado exitosamente
======================================================================
```

---

## 💡 Casos de Uso

### 1. Análisis Mensual de Costos
```bash
python aws_cost_report.py --mes 10 --anio 2024 --output octubre_2024.xlsx
```

### 2. Comparación Mes a Mes
```bash
python aws_cost_report.py --mes 9 --anio 2024 --output sep_2024.xlsx
python aws_cost_report.py --mes 10 --anio 2024 --output oct_2024.xlsx
python aws_cost_report.py --mes 11 --anio 2024 --output nov_2024.xlsx
```

### 3. Auditoría por Recurso
Abre el Excel y revisa la hoja "Detalle de Costos" para ver el desglose completo de cada recurso.

### 4. Optimización de Costos EC2
Identifica componentes costosos:
- ¿Muchos snapshots? → Implementa lifecycle policies
- ¿Alto Data Transfer? → Considera CloudFront
- ¿EBS caro? → Cambia de gp2 a gp3
- ¿Network Interfaces sin usar? → Elimínalas

---

## 📧 Soporte

Para problemas o preguntas, contacta a tu equipo de DevOps o Cloud.

---

## 📄 Licencia

Script interno para gestión de costos AWS.

---

**Desarrollado para:** Máxima claridad y detalle en costos AWS  
**Versión:** 2.0  
**Fecha:** Noviembre 2024  
**Compatible con:** Todos los servicios de AWS