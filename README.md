# Shinobi Video for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![paypal](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://paypal.me/aldsandiego)

Shinobi Video provides a custom integration for [Shinobi.Video](https://shinobi.video/) to monitor your cameras (monitors) directly within Home Assistant.

## Features
- 🎥 **Live Camera Streams**: Supports both HLS and MJPEG streaming (automatically detected based on your Shinobi monitor settings).
- 📸 **Instant Snapshots**: View high-quality still images directly in your Home Assistant dashboard.
- 🔔 **Monitor Status**: Real-time sensors showing the current status of each monitor.
- 🔗 **Rich Metadata**: Access direct stream URLs and Monitor IDs through entity attributes.
- 🛠️ **Seamless Connection**: Built-in support for SSL verification toggles and automatic URL protocol resolution.

## Prerequisites
Before you begin, ensure you have the following from your Shinobi instance:
1. **Server URL**: The full URL or IP of your Shinobi server (e.g., `http://192.168.1.10:8080`).
2. **API Key**: Generated in the Shinobi dashboard with "Read" and "Stream" permissions.
3. **Group Key**: Your Shinobi user group key.

### Shinobi Monitor Configuration
For the best experience, ensure each monitor in Shinobi is configured as follows:
- **JPEG API**: Must be **Enabled** to show previews and snapshots.
- **Streamer**: To use HLS, ensure the "Stream Type" is set to HLS in the monitor's "Streamer" section. The integration will automatically use the best available stream URL provided by Shinobi.

## Installation

### HACS (Recommended)
1. Open **HACS** in Home Assistant.
2. Click on the three dots in the top right corner and select **Custom repositories**.
3. Paste the URL of this repository: `https://github.com/allensandiego/ha-integration-shinobi`
4. Select **Integration** as the category and click **Add**.
5. Install the **Shinobi Video** integration and restart Home Assistant.

### Manual
1. Download the latest release.
2. Copy the `custom_components/shinobi` directory into your Home Assistant's `custom_components` directory.
3. Restart Home Assistant.

## Configuration
Go to **Settings** > **Devices & Services** > **Add Integration** and search for **Shinobi Video**. 

You will be prompted for:
- **Server URL**: IP or Domain (http/https is handled automatically).
- **API Key**
- **Group Key**
- **Verify SSL**: Uncheck this if you are using self-signed certificates on your local Shinobi server.

The integration will automatically detect all monitors and create corresponding Camera and Sensor entities.

## Contributions
Contributions are welcome! Pull requests and issues are the best way to improve this integration.
