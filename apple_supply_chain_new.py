import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
import qrcode
from io import BytesIO
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from PIL import Image
import hashlib
import ipfshttpclient
import random

# Set page config
st.set_page_config(
    page_title="Farm-to-Consumer Blockchain Traceability",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .css-1aumxhk {
        background-color: #f0f2f6;
        background-image: none;
    }
    .css-1v3fvcr {
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .st-b7 {
        color: #4CAF50;
    }
    .farmer-card {
        border: 1px solid #4CAF50;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        background-color: #f8fff8;
    }
    .step-card {
        border-left: 4px solid #4CAF50;
        padding-left: 15px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'farmer_data' not in st.session_state:
    st.session_state.farmer_data = {}
if 'batch_data' not in st.session_state:
    st.session_state.batch_data = {}
if 'transport_data' not in st.session_state:
    st.session_state.transport_data = pd.DataFrame()
if 'retailers_data' not in st.session_state:
    st.session_state.retailers_data = []
if 'farmer_registered' not in st.session_state:
    st.session_state.farmer_registered = False
if 'sowing_data' not in st.session_state:
    st.session_state.sowing_data = {}
if 'fertilizer_data' not in st.session_state:
    st.session_state.fertilizer_data = {}
if 'harvest_data' not in st.session_state:
    st.session_state.harvest_data = {}

# Mock IPFS client
class MockIPFSClient:
    def add_bytes(self, data):
        return f"IPFS_{hashlib.sha256(data).hexdigest()[:10]}"

# Initialize mock IPFS client
ipfs = MockIPFSClient()

# Helper function to generate QR code
def generate_qr_code(data, size=200):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    if isinstance(data, dict):
        qr.add_data(json.dumps(data))
    else:
        qr.add_data(str(data))
    qr.make(fit=True)
    img = qr.make_image(fill_color="green", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# App header
st.title("Blockchain Traceability Journey")
st.subheader("From seed to sale - Complete digital traceability with blockchain")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2785/2785818.png", width=100)
    st.title("Traceability Steps")
    
    steps = {
        1: "1. Farmer Registration",
        2: "2. Sowing & Inputs",
        3: "3. Growth Monitoring",
        4: "4. Harvest & Sale",
        5: "5. Transport Tracking",
        6: "6. Retail Distribution",
        7: "7. Consumer Purchase"
    }
    
    for step_num, step_name in steps.items():
        if st.button(step_name, key=f"step_{step_num}", use_container_width=True):
            st.session_state.current_step = step_num
    
    st.divider()
    st.markdown("**Blockchain Explorer**")
    st.code("Network: Hyperledger Fabric", language="plaintext")
    st.code("Nodes: 7", language="plaintext")
    st.code("Transactions: 84", language="plaintext")
    
    if st.button("View Smart Contract", key="view_contract"):
        st.session_state.show_contract = True

# Step 1: Farmer Registration
if st.session_state.current_step == 1:
    st.header("📝 Farmer Registration")
    st.markdown("""
    Farmers register with Aadhaar verification and GPS land mapping to create a permanent digital identity.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("farmer_registration"):
            st.subheader("Farmer Details")
            farmer_name = st.text_input("Full Name", value="Vijay Aswal")
            aadhaar_number = st.text_input("Aadhaar Number", value="1234 5678 9012")
            phone_number = st.text_input("Phone Number", value="+91 9876543210")
            village = st.text_input("Village", value="Harsill")
            district = st.text_input("District", value="Uttarkashi")
            state = st.text_input("State", value="Uttarakhand")
            
            st.subheader("Land Details")
            land_area = st.number_input("Land Area (acres)", min_value=0.1, value=2.5)
            land_lat = st.number_input("Latitude", value=31.0383)
            land_lon = st.number_input("Longitude", value=78.7377)
            
            submitted = st.form_submit_button("Register Farmer")
            
            if submitted:
                # Hash Aadhaar number for privacy
                aadhaar_hash = hashlib.sha256(aadhaar_number.encode()).hexdigest()
                
                # Generate Farmer ID
                farmer_id = f"FARM{random.randint(1000, 9999)}"
                
                # Store farmer data
                st.session_state.farmer_data = {
                    "FarmerID": farmer_id,
                    "Name": farmer_name,
                    "AadhaarHash": aadhaar_hash,
                    "Phone": phone_number,
                    "Location": {
                        "Village": village,
                        "District": district,
                        "State": state
                    },
                    "LandDetails": {
                        "Area": f"{land_area} acres",
                        "Coordinates": f"{land_lat}°N, {land_lon}°E"
                    },
                    "RegistrationDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "BlockchainTx": f"0x{hashlib.sha256(farmer_id.encode()).hexdigest()[:20]}"
                }
                
                st.session_state.farmer_registered = True
                st.success("Farmer registered successfully on blockchain!")
    
    with col2:
        if st.session_state.farmer_registered:
            st.subheader("Farmer ID Card")
            with st.container():
                st.markdown(f"""
                <div class="farmer-card">
                    <h3 style="color: #4CAF50;">🌾 Farmer Digital ID</h3>
                    <p><strong>ID:</strong> {st.session_state.farmer_data['FarmerID']}</p>
                    <p><strong>Name:</strong> {st.session_state.farmer_data['Name']}</p>
                    <p><strong>Location:</strong> {st.session_state.farmer_data['Location']['Village']}, {st.session_state.farmer_data['Location']['District']}</p>
                    <p><strong>Land:</strong> {st.session_state.farmer_data['LandDetails']['Area']} @ {st.session_state.farmer_data['LandDetails']['Coordinates']}</p>
                    <p><strong>Registered:</strong> {st.session_state.farmer_data['RegistrationDate']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate and display QR code
                qr_img = generate_qr_code(st.session_state.farmer_data)
                st.image(qr_img, caption="Farmer ID QR Code", width=200)
                
                st.download_button(
                    label="Download Farmer ID Card",
                    data=qr_img,
                    file_name=f"{st.session_state.farmer_data['FarmerID']}_card.png",
                    mime="image/png"
                )
            
            st.subheader("Farm Location")
            m = folium.Map(location=[land_lat, land_lon], zoom_start=14)
            folium.Marker(
                [land_lat, land_lon],
                popup=f"{farmer_name}'s Farm",
                tooltip=f"{land_area} acres",
                icon=folium.Icon(color="green", icon="tree-conifer")
            ).add_to(m)
            folium_static(m)
        else:
            st.info("Please complete the registration form to generate Farmer ID and QR code")

# Step 2: Sowing & Inputs
elif st.session_state.current_step == 2:
    st.header("🌱 Sowing & Input Management")
    st.markdown("""
    Record seed purchase and sowing details with geotagged verification.
    """)
    
    if not st.session_state.farmer_registered:
        st.warning("Please complete Farmer Registration first")
        st.button("Go to Step 1", on_click=lambda: setattr(st.session_state, 'current_step', 1))
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Seed Purchase")
            with st.form("seed_purchase"):
                seed_type = st.selectbox("Seed Type", ["Hybrid", "Organic", "GM", "Traditional"])
                seed_variety = st.text_input("Seed Variety", value="Barnyard millet")
                seed_batch = st.text_input("Seed Batch Number", value=f"SEED{random.randint(1000, 9999)}")
                purchase_date = st.date_input("Purchase Date", datetime.date.today())
                seller_name = st.text_input("Seller Name", value="Krishi Seva Kendra")
                
                submitted = st.form_submit_button("Record Seed Purchase")
                if submitted:
                    st.session_state.sowing_data["SeedPurchase"] = {
                        "Type": seed_type,
                        "Variety": seed_variety,
                        "Batch": seed_batch,
                        "PurchaseDate": purchase_date.strftime("%Y-%m-%d"),
                        "Seller": seller_name,
                        "BlockchainTx": f"0x{hashlib.sha256(seed_batch.encode()).hexdigest()[:20]}"
                    }
                    st.success("Seed purchase recorded on blockchain!")
        
        with col2:
            if "SeedPurchase" in st.session_state.sowing_data:
                st.subheader("Seed Purchase QR")
                qr_img = generate_qr_code(st.session_state.sowing_data["SeedPurchase"])
                st.image(qr_img, width=200)
                
                st.json(st.session_state.sowing_data["SeedPurchase"])
        
        st.divider()
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Sowing Activity")
            with st.form("sowing_activity"):
                sowing_date = st.date_input("Sowing Date", datetime.date.today())
                sowing_method = st.selectbox("Sowing Method", ["Manual", "Machine", "Drones"])
                field_photo = st.file_uploader("Field Photo (Geotagged)", type=["jpg", "png"])
                soil_report = st.file_uploader("Soil Test Report", type=["pdf", "jpg", "png"])
                
                submitted = st.form_submit_button("Record Sowing Activity")
                if submitted:
                    # Mock IPFS upload for photos
                    field_photo_hash = ipfs.add_bytes(field_photo.read()) if field_photo else "Not provided"
                    soil_report_hash = ipfs.add_bytes(soil_report.read()) if soil_report else "Not provided"
                    
                    st.session_state.sowing_data["Sowing"] = {
                        "FarmerID": st.session_state.farmer_data["FarmerID"],
                        "SeedBatch": st.session_state.sowing_data["SeedPurchase"]["Batch"],
                        "Date": sowing_date.strftime("%Y-%m-%d"),
                        "Method": sowing_method,
                        "FieldPhoto": field_photo_hash,
                        "SoilReport": soil_report_hash,
                        "Location": st.session_state.farmer_data["LandDetails"]["Coordinates"],
                        "BlockchainTx": f"0x{hashlib.sha256(str(sowing_date).encode()).hexdigest()[:20]}"
                    }
                    st.success("Sowing activity recorded on blockchain!")
        
        with col4:
            if "Sowing" in st.session_state.sowing_data:
                st.subheader("Sowing Record QR")
                qr_img = generate_qr_code(st.session_state.sowing_data["Sowing"])
                st.image(qr_img, width=200)
                
                st.json(st.session_state.sowing_data["Sowing"])
                
                if st.button("Proceed to Growth Monitoring"):
                    st.session_state.current_step = 3

# Step 3: Growth Monitoring
elif st.session_state.current_step == 3:
    st.header("🌿 Crop Growth Monitoring")
    st.markdown("""
    Track fertilizer use and crop growth with verifiable records.
    """)
    
    if not st.session_state.sowing_data:
        st.warning("Please complete Sowing & Inputs first")
        st.button("Go to Step 2", on_click=lambda: setattr(st.session_state, 'current_step', 2))
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Fertilizer Purchase")
            with st.form("fertilizer_purchase"):
                fert_type = st.selectbox("Fertilizer Type", ["Organic", "Urea", "DAP", "NPK", "Compost"])
                fert_batch = st.text_input("Fertilizer Batch", value=f"FERT{random.randint(1000, 9999)}")
                purchase_date = st.date_input("Purchase Date", datetime.date.today())
                seller_name = st.text_input("Seller Name", value="Krishi Seva Kendra")
                quantity = st.number_input("Quantity (kg)", min_value=1, value=50)
                
                submitted = st.form_submit_button("Record Purchase")
                if submitted:
                    st.session_state.fertilizer_data["Purchase"] = {
                        "Type": fert_type,
                        "Batch": fert_batch,
                        "Date": purchase_date.strftime("%Y-%m-%d"),
                        "Seller": seller_name,
                        "Quantity": f"{quantity}kg",
                        "BlockchainTx": f"0x{hashlib.sha256(fert_batch.encode()).hexdigest()[:20]}"
                    }
                    st.success("Fertilizer purchase recorded on blockchain!")
        
        with col2:
            if "Purchase" in st.session_state.fertilizer_data:
                st.subheader("Fertilizer Purchase QR")
                qr_img = generate_qr_code(st.session_state.fertilizer_data["Purchase"])
                st.image(qr_img, width=200)
                
                st.json(st.session_state.fertilizer_data["Purchase"])
        
        st.divider()
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Fertilizer Application")
            if "Purchase" not in st.session_state.fertilizer_data:
                st.warning("Record fertilizer purchase first")
            else:
                with st.form("fertilizer_application"):
                    application_date = st.date_input("Application Date", datetime.date.today())
                    quantity_used = st.number_input("Quantity Used (kg)", 
                                                  min_value=1, 
                                                  max_value=int(st.session_state.fertilizer_data["Purchase"]["Quantity"].replace("kg", "")), 
                                                  value=10)
                    field_photo = st.file_uploader("Application Photo (Geotagged)", type=["jpg", "png"])
                    notes = st.text_area("Application Notes")
                    
                    submitted = st.form_submit_button("Record Application")
                    if submitted:
                        # Mock IPFS upload for photo
                        field_photo_hash = ipfs.add_bytes(field_photo.read()) if field_photo else "Not provided"
                        
                        st.session_state.fertilizer_data["Application"] = {
                            "PurchaseTx": st.session_state.fertilizer_data["Purchase"]["BlockchainTx"],
                            "Date": application_date.strftime("%Y-%m-%d"),
                            "QuantityUsed": f"{quantity_used}kg",
                            "FieldPhoto": field_photo_hash,
                            "Notes": notes,
                            "Location": st.session_state.farmer_data["LandDetails"]["Coordinates"],
                            "BlockchainTx": f"0x{hashlib.sha256(str(application_date).encode()).hexdigest()[:20]}"
                        }
                        st.success("Fertilizer application recorded on blockchain!")
        
        with col4:
            if "Application" in st.session_state.fertilizer_data:
                st.subheader("Application Record QR")
                qr_img = generate_qr_code(st.session_state.fertilizer_data["Application"])
                st.image(qr_img, width=200)
                
                st.json(st.session_state.fertilizer_data["Application"])
                
                if st.button("Proceed to Harvest"):
                    st.session_state.current_step = 4

# Step 4: Harvest & Sale
elif st.session_state.current_step == 4:
    st.header("🌾 Harvest & Sale")
    st.markdown("""
    Record harvest details and connect with buyers through verified transactions.
    """)
    
    if not st.session_state.fertilizer_data:
        st.warning("Please complete Growth Monitoring first")
        st.button("Go to Step 3", on_click=lambda: setattr(st.session_state, 'current_step', 3))
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Harvest Details")
            with st.form("harvest_details"):
                harvest_date = st.date_input("Harvest Date", datetime.date.today())
                crop_variety = st.text_input("Crop Variety", value="Sharbati Wheat")
                quantity = st.number_input("Harvest Quantity (kg)", min_value=1, value=500)
                quality = st.select_slider("Quality Grade", options=["A", "B", "C"], value="A")
                last_spray = st.date_input("Last Pesticide Spray Date", datetime.date.today() - datetime.timedelta(days=20))
                
                submitted = st.form_submit_button("Record Harvest")
                if submitted:
                    if (harvest_date - last_spray).days < 15:
                        st.error("Harvest must be at least 15 days after last pesticide spray")
                    else:
                        st.session_state.harvest_data = {
                            "FarmerID": st.session_state.farmer_data["FarmerID"],
                            "Date": harvest_date.strftime("%Y-%m-%d"),
                            "Crop": crop_variety,
                            "Quantity": f"{quantity}kg",
                            "Quality": quality,
                            "LastSpray": last_spray.strftime("%Y-%m-%d"),
                            "BlockchainTx": f"0x{hashlib.sha256(str(harvest_date).encode()).hexdigest()[:20]}"
                        }
                        st.success("Harvest recorded on blockchain!")
        
        with col2:
            if st.session_state.harvest_data:
                st.subheader("Harvest QR Code")
                qr_img = generate_qr_code(st.session_state.harvest_data)
                st.image(qr_img, width=200)
                
                st.json(st.session_state.harvest_data)
        
        st.divider()
        
        # Sale Transaction (separate from the form)
        if st.session_state.harvest_data:
            st.subheader("Sale Transaction")
            
            # Input fields for sale
            buyer_name = st.text_input("Buyer Name", value="AgriMarkt Pvt Ltd", key="buyer_name")
            buyer_id = st.text_input("Buyer ID", value="BUYER123", key="buyer_id")
            price = st.number_input("Price per kg (₹)", min_value=1, value=25, key="price_per_kg")
            payment_method = st.selectbox("Payment Method", ["UPI", "Bank Transfer", "Cash"], key="payment_method")
            
            # Button outside any form
            if st.button("Record Sale"):
                total = price * int(st.session_state.harvest_data["Quantity"].replace("kg", ""))
                st.session_state.harvest_data["Sale"] = {
                    "Buyer": buyer_name,
                    "BuyerID": buyer_id,
                    "Price": f"₹{price}/kg",
                    "Total": f"₹{total}",
                    "PaymentMethod": payment_method,
                    "PaymentStatus": "Completed",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "BlockchainTx": f"0x{hashlib.sha256(buyer_id.encode()).hexdigest()[:20]}"
                }
                st.success(f"Sale recorded successfully! ₹{total} transferred to farmer.")
                
                # Generate QR stickers for each sack (mock)
                st.session_state.harvest_data["QR_Stickers"] = [
                    f"QR_{random.randint(1000, 9999)}" for _ in range(int(quantity/50))
                ]
                
            # Proceed button (only shown after sale is recorded)
            if "Sale" in st.session_state.harvest_data:
                if st.button("Proceed to Transport"):
                    st.session_state.current_step = 5

# Step 5: Transport Tracking
elif st.session_state.current_step == 5:
    st.header("🚚 Transport Tracking")
    st.markdown("""
    IoT sensors monitor temperature, humidity, and location during transport.
    Data is recorded on blockchain for immutable tracking.
    """)
    
    if not st.session_state.harvest_data or "Sale" not in st.session_state.harvest_data:
        st.warning("Please complete Harvest & Sale first")
        st.button("Go to Step 4", on_click=lambda: setattr(st.session_state, 'current_step', 4))
    else:
        if 'transport_data' not in st.session_state or st.session_state.transport_data.empty:
            # Generate simulated transport data
            timestamps = pd.date_range(
                start=pd.Timestamp(st.session_state.harvest_data["Date"]) + pd.Timedelta(hours=1),
                periods=24,
                freq="H"
            )
            
            base_temp = np.random.normal(4, 0.5, 24)
            if np.random.random() > 0.7:
                spike_pos = np.random.randint(8, 18)
                base_temp[spike_pos] += np.random.uniform(2, 5)
            
            transport_df = pd.DataFrame({
                "Timestamp": timestamps,
                "Temperature (°C)": np.clip(base_temp, 2, 10),
                "Humidity (%)": np.random.normal(65, 5, 24),
                "Location": [
                    f"{18.5 - i*0.02:.4f}°N, {73.8 + i*0.1:.4f}°E" 
                    for i in range(24)
                ]
            })
            st.session_state.transport_data = transport_df
        
        st.subheader("Transport Simulation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.line_chart(
                st.session_state.transport_data.set_index("Timestamp")["Temperature (°C)"],
                height=300
            )
            
            max_temp = st.session_state.transport_data["Temperature (°C)"].max()
            if max_temp > 5:
                st.error(f"ALERT: Temperature reached {max_temp:.1f}°C (Above safe threshold)")
            else:
                st.success("Temperature maintained within safe range (2-5°C)")
            
            st.subheader("Route Tracking")
            m = folium.Map(location=[18.5, 73.8], zoom_start=8)
            
            route_locations = [
                [18.5204, 73.8567],  # Farm location
                [18.5, 74.0],
                [18.4, 74.2],
                [18.3, 74.5],
                [18.2, 74.8],
                [18.1, 75.0],
                [18.0, 75.5],
                [19.0, 72.8],  # Mumbai
            ]
            folium.PolyLine(route_locations, color="blue", weight=2.5, opacity=1).add_to(m)
            
            folium.Marker(
                route_locations[0],
                popup="Farm (Origin)",
                icon=folium.Icon(color="green")
            ).add_to(m)
            
            folium.Marker(
                route_locations[-1],
                popup="Mumbai (Destination)",
                icon=folium.Icon(color="red")
            ).add_to(m)
            
            folium_static(m, width=400, height=300)
        
        with col2:
            st.dataframe(st.session_state.transport_data)
            
            st.subheader("Transport Metadata")
            transport_time = st.session_state.transport_data["Timestamp"].iloc[-1] - st.session_state.transport_data["Timestamp"].iloc[0]
            st.metric("Total Transit Time", f"{transport_time.seconds/3600:.1f} hours")
            st.metric("Average Temperature", f"{st.session_state.transport_data['Temperature (°C)'].mean():.1f}°C")
            st.metric("Average Humidity", f"{st.session_state.transport_data['Humidity (%)'].mean():.1f}%")
            
            # Generate transport QR
            transport_summary = {
                "BatchID": st.session_state.harvest_data.get("BlockchainTx", ""),
                "From": st.session_state.farmer_data["Location"]["Village"],
                "To": "Mumbai",
                "StartTime": str(st.session_state.transport_data["Timestamp"].iloc[0]),
                "EndTime": str(st.session_state.transport_data["Timestamp"].iloc[-1]),
                "AvgTemp": f"{st.session_state.transport_data['Temperature (°C)'].mean():.1f}°C",
                "Alerts": "None" if max_temp <= 5 else "High temperature detected"
            }
            
            st.subheader("Transport QR Code")
            qr_img = generate_qr_code(transport_summary)
            st.image(qr_img, width=200)
            
            if st.button("Complete Transport"):
                st.session_state.current_step = 6

# Step 6: Retail Distribution
elif st.session_state.current_step == 6:
    st.header("🏪 Retail Distribution")
    st.markdown("""
    Products are distributed to retailers who verify the batch and record their receipt on blockchain.
    """)
    
    if 'transport_data' not in st.session_state or st.session_state.transport_data.empty:
        st.warning("Please complete Transport Tracking first")
        st.button("Go to Step 5", on_click=lambda: setattr(st.session_state, 'current_step', 5))
    else:
        st.subheader("Retailer Distribution Network")
        
        if not st.session_state.retailers_data:
            st.session_state.retailers_data = [
                {"name": "FreshMart", "location": "Mumbai", "quantity": 0},
                {"name": "Organic Bazaar", "location": "Pune", "quantity": 0},
                {"name": "Farm2Table", "location": "Delhi", "quantity": 0}
            ]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribute to Retailers")
            total_quantity = int(st.session_state.harvest_data['Quantity'].replace('kg', ''))
            distributed = sum(r['quantity'] for r in st.session_state.retailers_data)
            remaining = total_quantity - distributed
            
            st.metric("Total Batch Quantity", f"{total_quantity} kg")
            st.metric("Already Distributed", f"{distributed} kg")
            st.metric("Remaining Quantity", f"{remaining} kg")
            
            st.progress(distributed / total_quantity)
            
            if remaining > 0:
                selected_retailer = st.selectbox(
                    "Select Retailer", 
                    [r['name'] for r in st.session_state.retailers_data],
                    key="selected_retailer"
                )
                retailer_quantity = st.number_input(
                    "Quantity (kg)", 
                    min_value=1, 
                    max_value=remaining, 
                    key="retailer_quantity"
                )
                
                if st.button("Record Distribution"):
                    for retailer in st.session_state.retailers_data:
                        if retailer['name'] == selected_retailer:
                            retailer['quantity'] += retailer_quantity
                    
                    st.success(f"Distributed {retailer_quantity}kg to {selected_retailer}")
                    st.rerun()
        
        with col2:
            st.subheader("Distribution Records")
            
            distributed = sum(r['quantity'] for r in st.session_state.retailers_data)
            if distributed > 0:
                active_retailers = [r for r in st.session_state.retailers_data if r['quantity'] > 0]
                
                if active_retailers:
                    fig, ax = plt.subplots()
                    ax.pie(
                        [r['quantity'] for r in active_retailers],
                        labels=[r['name'] for r in active_retailers],
                        autopct='%1.1f%%',
                        colors=['#4CAF50', '#8BC34A', '#CDDC39']
                    )
                    st.pyplot(fig)
                    
                    # Generate retailer QR codes
                    for retailer in active_retailers:
                        retailer_data = {
                            "Retailer": retailer['name'],
                            "Location": retailer['location'],
                            "Quantity": f"{retailer['quantity']}kg",
                            "BatchID": st.session_state.harvest_data.get("BlockchainTx", ""),
                            "Farmer": st.session_state.farmer_data["Name"],
                            "HarvestDate": st.session_state.harvest_data["Date"]
                        }
                        
                        st.image(
                            generate_qr_code(retailer_data), 
                            caption=f"{retailer['name']} QR", 
                            width=150
                        )
                else:
                    st.info("No products distributed yet")
            else:
                st.info("No products distributed yet")
            
            if remaining == 0 and st.button("Complete Distribution"):
                st.session_state.current_step = 7

# Step 7: Consumer Purchase
elif st.session_state.current_step == 7:
    st.header("🛒 Consumer Purchase")
    st.markdown("""
    Consumers can scan the QR code to verify the product's journey from farm to store.
    """)
    
    if not st.session_state.retailers_data or sum(r['quantity'] for r in st.session_state.retailers_data) == 0:
        st.warning("Please complete Retail Distribution first")
        st.button("Go to Step 6", on_click=lambda: setattr(st.session_state, 'current_step', 6))
    else:
        st.subheader("Product Traceability")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Prepare final traceability data
            traceability_data = {
                "Product": st.session_state.harvest_data["Crop"],
                "BatchID": st.session_state.harvest_data.get("BlockchainTx", ""),
                "Farmer": {
                    "Name": st.session_state.farmer_data["Name"],
                    "ID": st.session_state.farmer_data["FarmerID"],
                    "Location": st.session_state.farmer_data["Location"]["Village"]
                },
                "Seed": st.session_state.sowing_data["SeedPurchase"]["Batch"],
                "Harvest": {
                    "Date": st.session_state.harvest_data["Date"],
                    "Quantity": st.session_state.harvest_data["Quantity"],
                    "Quality": st.session_state.harvest_data["Quality"]
                },
                "Transport": {
                    "From": st.session_state.farmer_data["Location"]["Village"],
                    "To": "Mumbai",
                    "Duration": "24 hours",
                    "AvgTemp": f"{st.session_state.transport_data['Temperature (°C)'].mean():.1f}°C"
                },
                "Retailers": [
                    {"Name": r["name"], "Quantity": r["quantity"]} 
                    for r in st.session_state.retailers_data if r["quantity"] > 0
                ],
                "Blockchain": {
                    "Transactions": [
                        st.session_state.farmer_data["BlockchainTx"],
                        st.session_state.sowing_data["SeedPurchase"]["BlockchainTx"],
                        st.session_state.sowing_data["Sowing"]["BlockchainTx"],
                        st.session_state.fertilizer_data["Purchase"]["BlockchainTx"],
                        st.session_state.fertilizer_data["Application"]["BlockchainTx"],
                        st.session_state.harvest_data["BlockchainTx"],
                        st.session_state.harvest_data["Sale"]["BlockchainTx"]
                    ]
                }
            }
            
            # Generate QR code
            try:
                qr_img = generate_qr_code(traceability_data)
                st.image(qr_img, width=300)
                
                st.download_button(
                    label="Download Traceability QR",
                    data=qr_img,
                    file_name="product_traceability_qr.png",
                    mime="image/png"
                )
            except Exception as e:
                st.error(f"Error generating QR code: {str(e)}")
                st.warning("Showing simplified version due to data size")
                st.json({
                    "Product": traceability_data["Product"],
                    "BatchID": traceability_data["BatchID"],
                    "Farmer": traceability_data["Farmer"]["Name"],
                    "HarvestDate": traceability_data["Harvest"]["Date"]
                })
        
        with col2:
            st.subheader("Traceability Report")
            
            st.markdown(f"""
            ### 🌾 Farm-to-Table Journey
            **Product:** {traceability_data["Product"]}  
            **Batch ID:** {traceability_data["BatchID"]}
            
            ### 👨‍🌾 Farmer Details
            **Name:** {traceability_data["Farmer"]["Name"]}  
            **ID:** {traceability_data["Farmer"]["ID"]}  
            **Location:** {traceability_data["Farmer"]["Location"]}
            
            ### 🌱 Cultivation
            **Seed Batch:** {traceability_data["Seed"]}  
            **Organic Certified:** ✅ Yes  
            **Fertilizer Used:** {st.session_state.fertilizer_data["Purchase"]["Type"]}
            
            ### 🚜 Harvest
            **Date:** {traceability_data["Harvest"]["Date"]}  
            **Quantity:** {traceability_data["Harvest"]["Quantity"]}  
            **Quality Grade:** {traceability_data["Harvest"]["Quality"]}
            
            ### 🚚 Transport
            **From:** {traceability_data["Transport"]["From"]}  
            **To:** {traceability_data["Transport"]["To"]}  
            **Duration:** {traceability_data["Transport"]["Duration"]}  
            **Temperature:** {traceability_data["Transport"]["AvgTemp"]}
            
            ### 🏪 Retail Availability
            """)
            
            for retailer in traceability_data["Retailers"]:
                st.markdown(f"- {retailer['Name']}: {retailer['Quantity']}kg")
            
            st.markdown("""
            ### 🔗 Blockchain Verification
            All steps verified and recorded on blockchain
            """)
        
        st.divider()
        st.subheader("Impact Metrics")
        
        cols = st.columns(3)
        cols[0].metric("Farmer Income", "₹25/kg", "+25% vs traditional")
        cols[1].metric("Supply Chain Efficiency", "3 days", "60% faster")
        cols[2].metric("Food Safety", "100% Traceable", "0 recalls")

# Show smart contract if requested
if st.session_state.get('show_contract', False):
    with st.expander("Smart Contract Code", expanded=True):
        st.markdown("""
        ```solidity
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.8.0;
        
        contract FarmTraceability {
            address public admin;
            
            struct Farmer {
                string name;
                string aadhaarHash;
                string location;
                string landCoordinates;
                bool registered;
            }
            
            struct Batch {
                string farmerId;
                string seedBatch;
                string fertilizerBatch;
                uint256 harvestDate;
                uint256 quantity;
                string quality;
                address buyer;
                bool sold;
            }
            
            mapping(string => Farmer) public farmers;
            mapping(string => Batch) public batches;
            
            event FarmerRegistered(string farmerId, string name);
            event BatchCreated(string batchId, string farmerId);
            event BatchSold(string batchId, address buyer);
            
            constructor() {
                admin = msg.sender;
            }
            
            function registerFarmer(
                string memory farmerId,
                string memory name,
                string memory aadhaarHash,
                string memory location,
                string memory landCoordinates
            ) public {
                require(msg.sender == admin, "Only admin can register farmers");
                require(!farmers[farmerId].registered, "Farmer already registered");
                
                farmers[farmerId] = Farmer({
                    name: name,
                    aadhaarHash: aadhaarHash,
                    location: location,
                    landCoordinates: landCoordinates,
                    registered: true
                });
                
                emit FarmerRegistered(farmerId, name);
            }
            
            function createBatch(
                string memory batchId,
                string memory farmerId,
                string memory seedBatch,
                string memory fertilizerBatch,
                uint256 harvestDate,
                uint256 quantity,
                string memory quality
            ) public {
                require(farmers[farmerId].registered, "Farmer not registered");
                require(batches[batchId].harvestDate == 0, "Batch already exists");
                
                batches[batchId] = Batch({
                    farmerId: farmerId,
                    seedBatch: seedBatch,
                    fertilizerBatch: fertilizerBatch,
                    harvestDate: harvestDate,
                    quantity: quantity,
                    quality: quality,
                    buyer: address(0),
                    sold: false
                });
                
                emit BatchCreated(batchId, farmerId);
            }
            
            function purchaseBatch(string memory batchId) public payable {
                require(batches[batchId].harvestDate != 0, "Batch doesn't exist");
                require(!batches[batchId].sold, "Batch already sold");
                
                // In a real contract, you would include payment logic here
                batches[batchId].buyer = msg.sender;
                batches[batchId].sold = true;
                
                emit BatchSold(batchId, msg.sender);
            }
            
            function getBatchDetails(string memory batchId) public view returns (
                string memory farmerId,
                string memory seedBatch,
                string memory fertilizerBatch,
                uint256 harvestDate,
                uint256 quantity,
                string memory quality,
                address buyer,
                bool sold
            ) {
                Batch memory batch = batches[batchId];
                return (
                    batch.farmerId,
                    batch.seedBatch,
                    batch.fertilizerBatch,
                    batch.harvestDate,
                    batch.quantity,
                    batch.quality,
                    batch.buyer,
                    batch.sold
                );
            }
        }
        ```
        """)
        st.button("Close", on_click=lambda: setattr(st.session_state, 'show_contract', False))