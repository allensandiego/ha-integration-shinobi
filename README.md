# Shinobi Video for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Shinobi Video provides a custom integration for [Shinobi.Video](https://shinobi.video/) to monitor and control your cameras (monitors) directly within Home Assistant.

## Features
- 🎥 View camera streams (monitors)
- 🔔 Motion detection sensors
- 🕹️ Control monitor state (Watch, Record, Stop)

## Prerequisites
Before you begin, ensure you have the following from your Shinobi instance:
1. **Server URL**: The full URL of your Shinobi server (e.g., `http://192.168.1.10:8080`).
2. **API Key**: Generated in the Shinobi dashboard.
3. **Group Key**: Your Shinobi user group key.

## Installation

### HACS (Recommended)
1. Open HACS in Home Assistant.
2. Click on the three dots in the top right corner and select "Custom repositories".
3. Paste the URL of this repository (`https://github.com/allensandiego/ha-integration-shinobi`) and select **Integration** as the category.
4. Click "Add" and then install the **Shinobi Video** integration.
5. Restart Home Assistant.

### Manual
1. Download the latest release.
2. Copy the `custom_components/shinobi` directory into your Home Assistant's `custom_components` directory.
3. Restart Home Assistant.

## Configuration
Go to **Settings** > **Devices & Services** > **Add Integration** and search for **Shinobi Video**. You will be prompted for:
- **Server URL**
- **API Key**
- **Group Key**

## Contributions
Contributions are welcome! Pull requests and issues are the best way to improve this integration.
