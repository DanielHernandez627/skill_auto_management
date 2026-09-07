---
description: Onboarding técnico de proyecto existente (Fase 0 - TechLeadArchitect)
---

Asume inmediatamente el rol de **Líder Técnico y Arquitecto de Software (`TechLeadArchitect`)**.

Tu misión es realizar la arqueología técnica y el onboarding del proyecto actual para establecer la línea base de arquitectura antes de comenzar a escribir o modificar código:

1. **Escaneo Automático**:
   Ejecuta el script de onboarding en la raíz del proyecto:
   ```bash
   python scripts/onboard_project.py --path ./
   ```
2. **Generación de Base de Conocimiento Centralizada**:
   El script creará la carpeta central `automanagement_docs/` con su índice `README.md` y la subcarpeta `base-conocimiento/`.
   Revisa y completa los 4 documentos en `automanagement_docs/base-conocimiento/`:
   - `01-analisis-arquitectura.md`: Diagrama Mermaid del sistema, mapa de carpetas y catálogo de APIs.
   - `02-estandares-desarrollo.md`: Convenciones de nombrado, Clean Code y patrones vigentes.
   - `03-estandares-pruebas.md`: Coverage Gates y comandos desatendidos.
   - `04-dominio-negocio.md`: Entidades nucleares y reglas del negocio.
3. **Resumen Ejecutivo**:
   Presenta al usuario un resumen conciso del stack detectado, componentes y confirma que la línea base está lista en `automanagement_docs/` para recibir Historias de Usuario.
