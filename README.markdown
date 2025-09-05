# Traceability Blockchain

Traceability Blockchain is a Streamlit-based web application designed to provide end-to-end traceability for agricultural products from farm to consumer. It leverages blockchain technology (mocked with Hyperledger Fabric) to record and verify each step of the supply chain, including farmer registration, sowing, growth monitoring, harvest, transport, retail distribution, and consumer purchase. The app generates QR codes for verification and uses visualizations like maps and charts to track the product journey.

## Features
- **Farmer Registration**: Register farmers with Aadhaar verification and GPS land mapping, generating a unique Farmer ID and QR code.
- **Sowing & Inputs**: Record seed purchase and sowing details with geotagged photos and soil reports, stored on a mock blockchain.
- **Growth Monitoring**: Track fertilizer purchases and applications with verifiable records and QR codes.
- **Harvest & Sale**: Log harvest details (crop, quantity, quality) and sale transactions to buyers, with QR stickers for sacks.
- **Transport Tracking**: Simulate IoT sensor data (temperature, humidity, location) during transport, visualized with maps and charts.
- **Retail Distribution**: Distribute products to retailers, track quantities, and generate QR codes for each retailer.
- **Consumer Purchase**: Provide consumers with a QR code to verify the product’s journey, including farmer, cultivation, and transport details.
- **Visualizations**: Interactive maps (Folium), line charts (temperature trends), pie charts (retailer distribution), and metrics (e.g., transit time).
- **Blockchain Integration**: Mock blockchain transactions (Hyperledger Fabric) and a sample Solidity smart contract for traceability.
- **Interactive UI**: Clean, responsive Streamlit interface with custom styles and real-time feedback.

## Installation

### Prerequisites
- Python 3.8 or higher
- Internet connection for loading external resources (e.g., icons)
- Optional: IPFS client for file storage (mocked in this version)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/traceability-blockchain.git
   cd traceability-blockchain
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Requirements
The following dependencies are listed in `requirements.txt`:
- streamlit==1.25.0
- pandas==2.0.3
- numpy==1.24.3
- qrcode==7.4.2
- Pillow==10.0.0
- matplotlib==3.7.2
- folium==0.14.0
- streamlit-folium==0.15.0
- ipfshttpclient==0.8.0

## Usage
1. **Launch the App**:
   - Run `streamlit run app.py` and open the local URL (e.g., `http://localhost:8501`) in your browser.
2. **Navigate Steps**:
   - Use the sidebar to move through the seven steps: Farmer Registration, Sowing & Inputs, Growth Monitoring, Harvest & Sale, Transport Tracking, Retail Distribution, and Consumer Purchase.
3. **Step-by-Step Process**:
   - **Farmer Registration**: Enter farmer details (name, Aadhaar, location, land coordinates) to generate a Farmer ID and QR code.
   - **Sowing & Inputs**: Record seed purchase and sowing activities with geotagged photos and soil reports.
   - **Growth Monitoring**: Log fertilizer purchases and applications, ensuring traceability with QR codes.
   - **Harvest & Sale**: Enter harvest details and sale transactions, generating QR stickers for product sacks.
   - **Transport Tracking**: View simulated IoT data (temperature, humidity, route) with a Folium map and line charts.
   - **Retail Distribution**: Distribute harvest quantities to retailers and visualize distribution with a pie chart.
   - **Consumer Purchase**: Generate a final QR code for consumers to verify the product’s journey.
4. **Explore Visualizations**:
   - View farm locations on a Folium map, temperature trends, and retailer distribution charts.
   - Download QR codes for verification at each step.
5. **Blockchain Explorer**:
   - View mock blockchain metadata (network, nodes, transactions) and a sample Solidity smart contract.

## Example
- **Input**:
  - Farmer: Vijay Aswal, Uttarkashi, 2.5 acres.
  - Seed: Barnyard millet, purchased from Krishi Seva Kendra.
  - Harvest: 500kg Sharbati Wheat, quality grade A.
  - Transport: 24-hour transit to Mumbai with temperature monitoring.
  - Retail: Distributed to FreshMart (Mumbai) and Organic Bazaar (Pune).
- **Output**:
  - Farmer ID card with QR code.
  - QR codes for seed purchase, sowing, fertilizer, harvest, transport, and retail.
  - Visualizations: Farm location map, temperature trend chart, retailer distribution pie chart.
  - Consumer QR code with full traceability report (farmer, seed, harvest, transport, retailers).
  - Example Insight: "Sharbati Wheat batch traced from Vijay’s farm in Uttarkashi to Mumbai, with 100% organic certification and safe transport conditions."

## Project Structure
```
traceability-blockchain/
├── data/
│   └── sample_photos/  # Geotagged photos and reports (not included in repo)
├── app.py              # Main Streamlit application
├── requirements.txt    # Dependencies
├── README.md           # This file
└── LICENSE             # MIT License file
```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a Pull Request on GitHub.

**Ideas for Improvement**:
- Integrate a real blockchain network (e.g., Ethereum, Hyperledger).
- Add support for actual IPFS file storage.
- Enhance visualizations with interactive features (e.g., Plotly).
- Include additional IoT sensor data (e.g., vibration, light exposure).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For issues or suggestions, open an issue on GitHub or email vaswal919@gmail.com.

## Acknowledgments
- Built with Streamlit, Folium, and Matplotlib for interactive visualizations.
- Inspired by blockchain-based supply chain traceability solutions.