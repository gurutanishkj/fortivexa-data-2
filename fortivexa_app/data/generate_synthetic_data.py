"""
FORTIVEXA - Synthetic Cybercrime & Mule Account Data Generator
Problem Statement SIH26184 - Ministry of Home Affairs

Generates:
1. 1,000 Cybercrime complaints across Indian metro corridors and feeder cybercrime zones.
2. 10,000 Multi-layer transaction records (Victim -> Layer 1 -> Layer 2 -> Layer 3 -> ATM/POS).
3. Geospatial ATM/Kiosk master directory with past cash-out frequencies and coordinates.
"""

import os
import random
import datetime
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

# Fix random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Metro Corridors & Feeder Hubs with realistic Indian coordinates and pincodes
CORRIDORS = [
    {
        "metro": "Delhi NCR",
        "zones": ["Connaught Place", "Karol Bagh", "Rohini Sector 10", "Gurugram Cyber City", "Noida Sector 18", "Noida Sector 62"],
        "pincodes": ["110001", "110005", "110085", "122002", "201301", "201309"],
        "center_lat": 28.6139,
        "center_lon": 77.2090,
        "lat_range": (28.45, 28.75),
        "lon_range": (77.05, 77.40),
        "police_qrt": "NCR Cyber Cell Special Task Force (Mandir Marg / Cyber City Gurugram)"
    },
    {
        "metro": "Mumbai MMR",
        "zones": ["Bandra Kurla Complex", "Andheri East MIDC", "Lower Parel", "Dadar West", "Thane Naupada", "Vashi Sector 17"],
        "pincodes": ["400051", "400069", "400013", "400028", "400602", "400703"],
        "center_lat": 19.0760,
        "center_lon": 72.8777,
        "lat_range": (19.00, 19.22),
        "lon_range": (72.82, 73.05),
        "police_qrt": "Mumbai Police Cyber Command Unit (BKC Cyber PS)"
    },
    {
        "metro": "Bengaluru",
        "zones": ["Koramangala 5th Block", "Indiranagar 100ft Rd", "Whitefield ITPL", "Electronic City Phase 1", "HSR Layout Sector 1", "MG Road"],
        "pincodes": ["560034", "560038", "560066", "560100", "560102", "560001"],
        "center_lat": 12.9716,
        "center_lon": 77.5946,
        "lat_range": (12.85, 13.05),
        "lon_range": (77.55, 77.75),
        "police_qrt": "CID Cyber Crime Division (Carlton House, Palace Road, Bengaluru)"
    },
    {
        "metro": "Hyderabad",
        "zones": ["Hitec City Phase 2", "Madhapur Police Lines", "Gachibowli Financial Dist", "Banjara Hills Rd 12", "Secunderabad Clock Tower", "Begumpet"],
        "pincodes": ["500081", "500033", "500032", "500034", "500003", "500016"],
        "center_lat": 17.3850,
        "center_lon": 78.4867,
        "lat_range": (17.35, 17.50),
        "lon_range": (78.35, 78.55),
        "police_qrt": "Cyberabad Police Commissionerate Cyber Cell (Gachibowli)"
    },
    {
        "metro": "Kolkata",
        "zones": ["Salt Lake Sector V", "New Town Action Area 1", "Park Street", "Howrah Station South", "Rajarhat Chinar Park"],
        "pincodes": ["700091", "700156", "700016", "700001", "700136"],
        "center_lat": 22.5726,
        "center_lon": 88.3639,
        "lat_range": (22.50, 22.62),
        "lon_range": (88.30, 88.50),
        "police_qrt": "Kolkata Police Cyber Police Station (Lalbazar, Kolkata)"
    },
    {
        "metro": "Ahmedabad",
        "zones": ["SG Highway Bodakdev", "Vastrapur Lake Road", "Navrangpura CG Road", "Gandhinagar Infocity"],
        "pincodes": ["380054", "380015", "380009", "382007"],
        "center_lat": 23.0225,
        "center_lon": 72.5714,
        "lat_range": (23.00, 23.18),
        "lon_range": (72.50, 72.65),
        "police_qrt": "Gujarat CID Crime Cyber Cell (Gandhinagar)"
    }
]

MODUS_OPERANDI_LIST = [
    "Digital Arrest",
    "UPI Phishing",
    "Job Scam",
    "Investment Scam",
    "Credit Card Fraud"
]

BANKS = ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "Punjab National Bank", "Bank of Baroda", "Kotak Mahindra Bank", "Canara Bank"]

def generate_atm_directory(n_atms: int = 150) -> pd.DataFrame:
    """Generate master directory of 150 ATMs across major metro corridors."""
    atm_records = []
    atm_idx = 1
    
    for corridor in CORRIDORS:
        metro_name = corridor["metro"]
        atms_per_metro = n_atms // len(CORRIDORS)
        
        for _ in range(atms_per_metro):
            atm_id = f"ATM_{metro_name[:3].upper()}_{atm_idx:04d}"
            bank = random.choice(BANKS)
            zone_idx = random.randint(0, len(corridor["zones"]) - 1)
            zone = corridor["zones"][zone_idx]
            pincode = corridor["pincodes"][zone_idx]
            
            lat = round(random.uniform(corridor["lat_range"][0], corridor["lat_range"][1]), 5)
            lon = round(random.uniform(corridor["lon_range"][0], corridor["lon_range"][1]), 5)
            
            # Historical cashout hits (some ATMs are frequent siphon hotspots)
            is_hotspot = random.random() < 0.25
            past_hits = random.randint(12, 48) if is_hotspot else random.randint(0, 11)
            
            # Proximity to branch in meters
            branch_id = f"BR_{bank[:3].upper()}_{pincode[-3:]}"
            branch_distance_m = random.randint(50, 2500)
            
            # ATM daily limit
            daily_limit = random.choice([20000, 40000, 50000, 100000])
            has_biometric_kyc = random.choice([True, False])
            
            atm_records.append({
                "ATM_ID": atm_id,
                "Bank_Name": bank,
                "Metro_Corridor": metro_name,
                "Zone": zone,
                "Target_Pincode": pincode,
                "ATM_Lat": lat,
                "ATM_Lon": lon,
                "Branch_ID": branch_id,
                "Branch_Distance_M": branch_distance_m,
                "Past_Cashout_Hits": past_hits,
                "Daily_Cash_Limit": daily_limit,
                "Has_Biometric_KYC": has_biometric_kyc,
                "QRT_Unit": corridor["police_qrt"]
            })
            atm_idx += 1
            
    df_atms = pd.DataFrame(atm_records)
    return df_atms

def generate_mule_pools():
    """
    Generate synthetic pools of mule accounts with realistic clustering.
    A few 'Hub Mules' connect multiple syndicates, driving high degree/betweenness centrality.
    """
    # 30 Hub Mules (frequently reused across complaints)
    hub_mules = [f"MULE_HUB_{i:04d}" for i in range(101, 131)]
    # 250 Layer-1 Mules
    layer1_pool = [f"MULE_L1_{i:04d}" for i in range(1001, 1251)] + hub_mules[:10]
    # 350 Layer-2 Mules
    layer2_pool = [f"MULE_L2_{i:04d}" for i in range(2001, 2351)] + hub_mules[10:25]
    # 400 Layer-3 Mules (Exit runners / Kiosk withdrawers)
    layer3_pool = [f"MULE_L3_{i:04d}" for i in range(3001, 3401)] + hub_mules[20:30]
    
    return layer1_pool, layer2_pool, layer3_pool, hub_mules

def generate_synthetic_data(num_complaints: int = 1000, num_transactions: int = 10000) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Generates 1,000 complaints and multi-layer transactions with realistic cybercrime patterns.
    """
    df_atms = generate_atm_directory(n_atms=150)
    layer1_pool, layer2_pool, layer3_pool, hub_mules = generate_mule_pools()
    
    complaint_records = []
    transaction_records = []
    
    txn_counter = 1
    base_time = datetime.datetime.now() - datetime.timedelta(days=45)
    
    for c_idx in range(1, num_complaints + 1):
        complaint_id = f"CMP-2026-{c_idx:05d}"
        victim_id = f"VIC_{c_idx:05d}"
        modus = random.choice(MODUS_OPERANDI_LIST)
        
        # Financial loss amounts based on Modus Operandi
        if modus == "Digital Arrest":
            amount_lost = round(random.uniform(500000, 7500000), 2)
        elif modus == "Investment Scam":
            amount_lost = round(random.uniform(200000, 4500000), 2)
        elif modus == "Job Scam":
            amount_lost = round(random.uniform(50000, 850000), 2)
        elif modus == "UPI Phishing":
            amount_lost = round(random.uniform(25000, 350000), 2)
        else: # Credit Card Fraud
            amount_lost = round(random.uniform(30000, 400000), 2)
            
        # Timestamp offset
        time_offset_days = random.uniform(0, 44)
        c_time = base_time + datetime.timedelta(days=time_offset_days, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        timestamp_str = c_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Corridors and target ATMs
        corridor = random.choice(CORRIDORS)
        metro_name = corridor["metro"]
        
        # Select matching ATMs for this corridor
        corridor_atms = df_atms[df_atms["Metro_Corridor"] == metro_name]
        selected_atm = corridor_atms.sample(1).iloc[0]
        
        target_pincode = selected_atm["Target_Pincode"]
        atm_id = selected_atm["ATM_ID"]
        atm_lat = selected_atm["ATM_Lat"]
        atm_lon = selected_atm["ATM_Lon"]
        branch_id = selected_atm["Branch_ID"]
        past_cashout_hits = selected_atm["Past_Cashout_Hits"]
        
        # Time lag in minutes from fraud execution to attempted cash-out
        # Siphoning chains operate in rapid 15 to 240 minute windows
        time_lag_mins = int(np.random.lognormal(mean=3.8, sigma=0.6))
        time_lag_mins = max(15, min(time_lag_mins, 480))
        
        # Suspected Crypto / POS redirection flag (common in investment scams)
        is_crypto_pos = 1 if (modus == "Investment Scam" and random.random() < 0.55) or (random.random() < 0.12) else 0
        
        # Mule Chain Assignment
        # Some complaints connect to common hub mules (ring syndicates)
        use_shared_hub = random.random() < 0.40
        if use_shared_hub:
            l1_mule = random.choice(hub_mules[:10])
            l2_mule = random.choice(hub_mules[10:20])
            l3_mule = random.choice(hub_mules[20:30])
        else:
            l1_mule = random.choice(layer1_pool)
            l2_mule = random.choice(layer2_pool)
            l3_mule = random.choice(layer3_pool)
            
        # Ground truth cashout success (high risk target)
        # Higher past hits, shorter time lag, and hub mules strongly correlate with imminent cash-out success
        risk_score_latent = (
            (0.35 * (past_cashout_hits / 50.0)) +
            (0.30 * (1.0 / (1.0 + (time_lag_mins / 60.0)))) +
            (0.20 * (1.0 if l1_mule in hub_mules or l2_mule in hub_mules else 0.2)) +
            (0.15 * (1.0 if amount_lost > 500000 else 0.4))
        )
        cashout_success = 1 if risk_score_latent > 0.48 else 0
        
        complaint_records.append({
            "Complaint_ID": complaint_id,
            "Victim_ID": victim_id,
            "Modus_Operandi": modus,
            "Amount_Lost": amount_lost,
            "Timestamp": timestamp_str,
            "Layer1_Mule": l1_mule,
            "Layer2_Mule": l2_mule,
            "Layer3_Mule": l3_mule,
            "Time_Lag_Mins": time_lag_mins,
            "Metro_Corridor": metro_name,
            "Branch_ID": branch_id,
            "Target_Pincode": target_pincode,
            "ATM_ID": atm_id,
            "ATM_Lat": atm_lat,
            "ATM_Lon": atm_lon,
            "Past_Cashout_Hits": past_cashout_hits,
            "Is_Crypto_POS": is_crypto_pos,
            "Cashout_Success": cashout_success
        })
        
        # Generate Multi-Layer Transactions for this complaint
        # Hop 0 -> 1: Victim to Layer 1 Mule
        t1_time = c_time + datetime.timedelta(minutes=random.randint(1, 10))
        t1_amount = round(amount_lost * random.uniform(0.95, 1.0), 2)
        transaction_records.append({
            "Txn_ID": f"TXN_{txn_counter:07d}",
            "Complaint_ID": complaint_id,
            "Source_Account": victim_id,
            "Destination_Account": l1_mule,
            "Layer": 1,
            "Amount": t1_amount,
            "Timestamp": t1_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Channel": random.choice(["UPI", "IMPS", "RTGS"]),
            "Status": "COMPLETED"
        })
        txn_counter += 1
        
        # Hop 1 -> 2: Layer 1 Mule splits / forwards to Layer 2 Mule (and possibly secondary accounts)
        t2_time = t1_time + datetime.timedelta(minutes=random.randint(4, 25))
        t2_amount = round(t1_amount * random.uniform(0.85, 0.98), 2)
        transaction_records.append({
            "Txn_ID": f"TXN_{txn_counter:07d}",
            "Complaint_ID": complaint_id,
            "Source_Account": l1_mule,
            "Destination_Account": l2_mule,
            "Layer": 2,
            "Amount": t2_amount,
            "Timestamp": t2_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Channel": "IMPS",
            "Status": "COMPLETED"
        })
        txn_counter += 1
        
        # Additional diversion splits to obscure trail
        for _ in range(random.randint(1, 3)):
            extra_l2 = random.choice(layer2_pool)
            extra_amt = round(t1_amount * random.uniform(0.05, 0.15), 2)
            transaction_records.append({
                "Txn_ID": f"TXN_{txn_counter:07d}",
                "Complaint_ID": complaint_id,
                "Source_Account": l1_mule,
                "Destination_Account": extra_l2,
                "Layer": 2,
                "Amount": extra_amt,
                "Timestamp": (t1_time + datetime.timedelta(minutes=random.randint(5, 30))).strftime("%Y-%m-%d %H:%M:%S"),
                "Channel": "UPI",
                "Status": "COMPLETED"
            })
            txn_counter += 1
            
        # Hop 2 -> 3: Layer 2 Mule forwards to Layer 3 Mule (Withdrawal runner)
        t3_time = t2_time + datetime.timedelta(minutes=random.randint(6, 40))
        t3_amount = round(t2_amount * random.uniform(0.80, 0.95), 2)
        transaction_records.append({
            "Txn_ID": f"TXN_{txn_counter:07d}",
            "Complaint_ID": complaint_id,
            "Source_Account": l2_mule,
            "Destination_Account": l3_mule,
            "Layer": 3,
            "Amount": t3_amount,
            "Timestamp": t3_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Channel": "IMPS",
            "Status": "COMPLETED"
        })
        txn_counter += 1
        
        # Hop 3 -> Cash-out Exit: Layer 3 Mule to ATM/POS
        t4_time = t3_time + datetime.timedelta(minutes=time_lag_mins)
        exit_channel = "CRYPTO_OTC_POS" if is_crypto_pos else "ATM_CASH_WITHDRAWAL"
        transaction_records.append({
            "Txn_ID": f"TXN_{txn_counter:07d}",
            "Complaint_ID": complaint_id,
            "Source_Account": l3_mule,
            "Destination_Account": atm_id,
            "Layer": 4,
            "Amount": min(t3_amount, 50000.0 if not is_crypto_pos else t3_amount),
            "Timestamp": t4_time.strftime("%Y-%m-%d %H:%M:%S"),
            "Channel": exit_channel,
            "Status": "FLAGGED_CASHOUT" if cashout_success else "PENDING_INVESTIGATION"
        })
        txn_counter += 1
        
    # Supplement remaining transactions up to num_transactions
    while txn_counter <= num_transactions:
        c = random.choice(complaint_records)
        src = random.choice([c["Layer1_Mule"], c["Layer2_Mule"]])
        dst = random.choice(layer3_pool)
        transaction_records.append({
            "Txn_ID": f"TXN_{txn_counter:07d}",
            "Complaint_ID": c["Complaint_ID"],
            "Source_Account": src,
            "Destination_Account": dst,
            "Layer": random.choice([2, 3]),
            "Amount": round(random.uniform(5000, 75000), 2),
            "Timestamp": c["Timestamp"],
            "Channel": random.choice(["UPI", "IMPS"]),
            "Status": "COMPLETED"
        })
        txn_counter += 1
        
    df_complaints = pd.DataFrame(complaint_records)
    df_transactions = pd.DataFrame(transaction_records[:num_transactions])
    
    return df_complaints, df_transactions, df_atms

def save_synthetic_dataset():
    """Generates and persists the dataset files."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    print("[FORTIVEXA Data Gen] Synthesizing 1,000 Cybercrime Complaints and 10,000 Multi-Layer Transactions...")
    df_complaints, df_transactions, df_atms = generate_synthetic_data(num_complaints=1000, num_transactions=10000)
    
    complaints_file = os.path.join(DATA_DIR, "complaints.csv")
    transactions_file = os.path.join(DATA_DIR, "transactions.csv")
    atms_file = os.path.join(DATA_DIR, "atm_locations.csv")
    
    df_complaints.to_csv(complaints_file, index=False)
    df_transactions.to_csv(transactions_file, index=False)
    df_atms.to_csv(atms_file, index=False)
    
    print(f"  [OK] Complaints Dataset saved to: {complaints_file} (Records: {len(df_complaints)})")
    print(f"  [OK] Transactions Dataset saved to: {transactions_file} (Records: {len(df_transactions)})")
    print(f"  [OK] ATM Locations Master saved to: {atms_file} (Records: {len(df_atms)})")
    
    return df_complaints, df_transactions, df_atms

if __name__ == "__main__":
    save_synthetic_dataset()
