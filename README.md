# LuzIA 👁️🤖

LuzIA es un proyecto de arte generativo y visión artificial diseñado para ejecutarse en una Raspberry Pi. Utiliza una cámara para analizar el entorno y detectar personas, estimando su edad y género para generar patrones visuales dinámicos en una matriz de LEDs NeoPixel.

Este es un **proyecto personal de solo lectura**.

## 🚀 Características
- **Detección Facial:** Utiliza OpenCV y modelos Caffe para identificar rostros en tiempo real.
- **Análisis Demográfico:** Estimación de edad y género mediante redes neuronales profundas (DNN).
- **Visualización Dinámica:** Control de matrices de LEDs WS2812 (NeoPixel) con efectos de transición.
- **Interacción con Hardware:** Integración con sensores de distancia Sharp IR y botones físicos via Arduino.

## 🛠️ Requisitos de Hardware
- **Computadora Base:** Raspberry Pi (3B+ o superior recomendada).
- **Cámara:** Cámara USB o módulo de cámara oficial.
- **Microcontrolador:** Arduino (Nano/Uno/Leonardo) para lectura de sensores.
- **Sensores:**
    - Sensor de distancia Sharp IR (GP2Y0A02YK0F).
    - Botón momentáneo.
- **Pantalla:** Tira de LEDs WS2812B (NeoPixel) organizada en matriz.

## 📋 Requisitos de Software
- Python 3.x
- Bibliotecas de sistema: `gstreamer-1.0`

## ⚙️ Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/luzia.git
   cd luzia
   ```

2. **Instalar dependencias de Python:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar el Arduino:**
   - Cargar el archivo `luzia.ino` en tu placa mediante el IDE de Arduino.
   - Conectar el Arduino a la Raspberry Pi vía USB.

## 🏃 Ejecución

Puedes iniciar el proyecto usando el script de ayuda:
```bash
chmod +x run.sh
./run.sh
```

O directamente ejecutando el script principal:
```bash
cd luzia
python3 luzia.py
```

### Configuración (Variables de Entorno)
Puedes ajustar los parámetros sin modificar el código:
- `ARDUINO_PORT`: Ruta al puerto serie (por defecto: `/dev/ttyACM0`).
- `LUZIA_DATA_PATH`: Ruta donde se guardan los datos analizados.

## ⚖️ Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
*Desarrollado como un proyecto personal de exploración técnica en Visión Artificial y Hardware.*
