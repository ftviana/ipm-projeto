# InsideView - Airbnb Data Analytics Dashboard

A Vue.js application for exploring and analyzing Airbnb listing data across Porto, Lisbon, and Barcelona. Built with Vue 3, Vite, and Leaflet maps.

## Features

- **Explore Data**: Interactive heatmaps and trend charts for Airbnb listings
- **Compare Cities**: Side-by-side comparison of metrics across cities and time periods
- **Anomalies Detection**: Identify suspicious listings (multi-host, high occupancy, price spikes, etc.)
- **Export Reports**: Generate PDF reports with filtered data
- **Multi-currency Support**: View prices in EUR, USD, or GBP
- **Historical Data**: Analyze data across multiple time periods (Mar/Jun/Sep 2025)

## Prerequisites

- **Node.js** v20.19.0+ or v22.12.0+
- **npm** (comes with Node.js)

## Installation

1. Clone the repository:

```sh
git clone <repository-url>
cd ipm-projeto
```

2. Install dependencies:

```sh
npm install
```

3. Build the database from CSV files:

```sh
python build_jsondb.py
```

## Running the Application

You need to run **both** the backend server and the frontend dev server:

### 1. Start the JSON Server (Backend API)

```sh
npm run server
```

This starts the API server at `http://localhost:3000`

### 2. Start the Vue Development Server (Frontend)

In a new terminal:

```sh
npm run dev
```

This starts the app at `http://localhost:5173`

## Build for Production

```sh
npm run build
```

The built files will be in the `dist/` folder.

## Tech Stack

### Frontend

- **Vue 3** (^3.5.22) - Frontend framework
- **Vite** (^7.1.7) - Build tool
- **Vue Router** (^4.6.3) - Client-side routing

### Maps & Geospatial

- **Leaflet** (^1.9.4) - Interactive maps
- **@vue-leaflet/vue-leaflet** (^0.10.1) - Vue 3 Leaflet components
- **leaflet.heat** (^0.2.0) - Heatmap layer for Leaflet
- **@fawmi/vue-google-maps** (^0.9.79) - Google Maps integration

### Data Visualization

- **Chart.js** (^4.5.1) - Charts and graphs
- **vue-chartjs** (^5.3.3) - Vue 3 wrapper for Chart.js

### PDF Export

- **jsPDF** (^2.5.1) - PDF generation
- **jspdf-autotable** (^3.8.3) - Table plugin for jsPDF

### Backend

- **JSON Server** (^1.0.0-beta.3) - Mock REST API

## Project Structure

```
src/
├── components/     # Reusable components (HeatmapMap, TrendChart, etc.)
├── views/          # Page components (Home, ExploreData, Compare, etc.)
├── layouts/        # Layout wrappers
├── router/         # Route definitions
├── store.js        # Global state (currency, period)
└── main.js         # App entry point

db/                 # Source CSV data files
├── porto/
├── lisbon/
└── barcelona/
```

## Data Source

Listing data sourced from [Inside Airbnb](http://insideairbnb.com/).
