# Shinobi Video for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![paypal](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://paypal.me/aldsandiego)

Shinobi Video provides a custom integration for [Shinobi.Video](https://shinobi.video/) to monitor your cameras (monitors) directly within Home Assistant.

## Features
- 🎥 **Live Camera Streams**: Supports HLS (Recommended), MP4 and MJPEG streaming (automatically detected based on your Shinobi monitor settings).
- 📸 **Instant Snapshots**: View high-quality still images directly in your Home Assistant dashboard.
- 🔴 **Control Recordings**: Toggle recording on/off for each camera with dedicated switch entities.
- 🔔 **Monitor Status**: Real-time sensors showing the current status of each monitor.
- 🔗 **Rich Metadata**: Access direct stream URLs and Monitor IDs through entity attributes.
- 🛠️ **Seamless Connection**: Built-in support for SSL verification toggles and automatic URL protocol resolution.

## Prerequisites
Before you begin, ensure you have the following from your Shinobi instance:
1. **Server URL**: The full URL or IP of your Shinobi server (e.g., `http://192.168.1.10:8080`).
2. **API Key**: Generated in the Shinobi dashboard with "Read" and "Stream" permissions.
3. **Group Key**: Your Shinobi user group key.

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

The integration will automatically detect all active monitors and create corresponding Camera and Sensor entities.

## Troubleshooting

### Setup dialog asks for Host, Port, Username, and Password
If adding the integration presents a form with **Host**, **Path**, **Port**, **Username**, and **Password** (and potentially an *"Invalid server details"* error) instead of **Server URL**, **API Key**, and **Group Key**:
- You have the default HACS integration (`elad-bar/ha-shinobi`) loaded. Because both integrations use the `shinobi` integration domain, Home Assistant will continue running the previously loaded integration until it is replaced and restarted.
- **Resolution**:
  1. In **HACS**, uninstall any existing Shinobi integration (and delete `custom_components/shinobi` if it was manually copied).
  2. **Restart Home Assistant** so cached component definitions are removed.
  3. In **HACS** > **Custom repositories**, add `https://github.com/allensandiego/ha-integration-shinobi` (Category: **Integration**).
  4. Download and install **Shinobi Video** from this custom repository.
  5. **Restart Home Assistant**.
  6. Go to **Settings** > **Devices & Services** > **Add Integration** > search for **Shinobi Video**. The prompt will now show the correct fields (**Server URL**, **API Key**, and **Group Key**).

