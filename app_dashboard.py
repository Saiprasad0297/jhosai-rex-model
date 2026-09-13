import streamlit as st
import os
import json
import hashlib
from datetime import datetime

# ----------------------------
# Configuration & Data Files
# ----------------------------
DATA_DIR = "data"
IMG_DIR = "img"
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

def init_data_files():
    if not os.path.exists(PRODUCTS_FILE):
        sample_products = [
            {
                "id": 1,
                "name": "Fresh Atlantic Salmon",
                "description": "Premium Norwegian salmon fillet, skin-on, rich in Omega-3.",
                "price": 649.00,
                "original_price": 799.00,
                "discount": 18,
                "delivery": "Delivered in 3 hours",
                "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=500",
                "category": "Fillets & Steaks",
                "filter": "Sea Water",
                "stock": 50,
                "unit": "500g"
            },
            {
                "id": 2,
                "name": "Jumbo Tiger Prawns",
                "description": "Wild-caught, large tiger prawns, peeled and deveined.",
                "price": 529.00,
                "original_price": 649.00,
                "discount": 18,
                "delivery": "Delivered in 3 hours",
                "image": "https://images.unsplash.com/photo-1565680314427-a55bb141c2c2?w=500",
                "category": "Shellfish",
                "filter": "Recommended",
                "stock": 80,
                "unit": "500g"
            },
            {
                "id": 3,
                "name": "Freshwater Rohu Bengali Cut",
                "description": "Cleaned fresh water river rohu pieces, tender and juicy.",
                "price": 349.00,
                "original_price": 420.00,
                "discount": 15,
                "delivery": "Delivered in 3 hours",
                "image": "https://images.unsplash.com/photo-1534939561126-855b8675edd7?w=500",
                "category": "Fresh Water",
                "filter": "Fresh Water",
                "stock": 40,
                "unit": "1 kg"
            },
            {
                "id": 4,
                "name": "Yellowfin Tuna Steaks",
                "description": "Sushi-grade wild tuna steaks, ideal for searing.",
                "price": 699.00,
                "original_price": 849.00,
                "discount": 17,
                "delivery": "Delivered in 3 hours",
                "image": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=500",
                "category": "Fillets & Steaks",
                "filter": "Imported",
                "stock": 35,
                "unit": "500g"
            },
            {
                "id": 5,
                "name": "Alaskan Snow Crab Clusters",
                "description": "Pre-cooked sweet and succulent snow crab legs.",
                "price": 999.00,
                "original_price": 1200.00,
                "discount": 16,
                "delivery": "Delivered in 3 hours",
                "image": "https://images.unsplash.com/photo-1559742811-822873691df8?w=500",
                "category": "Exotic Catch",
                "filter": "No Shell Fish",
                "stock": 20,
                "unit": "1 kg"
            },
            {
                "id": 6,
                "name": "Sea Scallops (Wild)",
                "description": "Tender and sweet sea scallops, wild-harvested.",
                "price": 849.00,
                "original_price": 999.00,
                "discount": 15,
                "delivery": "Delivered in 3 hours",
                "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=500",
                "category": "Shellfish",
                "filter": "Sea Water",
                "stock": 25,
                "unit": "250g"
            },
            {
                "id": 7,
                "name": "Black Pomfret Whole",
                "description": "Whole black pomfret, cleaned and ready to fry or curry.",
                "price": 599.00,
                "original_price": 699.00,
                "discount": 14,
                "delivery": "Delivered in 3 hours",
                "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=500",
                "category": "Whole Fish",
                "filter": "Sea Water",
                "stock": 45,
                "unit": "1 kg"
            },
            {
                "id": 8,
                "name": "Squid Rings (Calamari)",
                "description": "Cleaned tender squid tubes cut into crisp-ready rings.",
                "price": 449.00,
                "original_price": 549.00,
                "discount": 18,
                "delivery": "Delivered in 3 hours",
                "image": "https://images.unsplash.com/photo-1606851094655-b2593a9af63f?w=500",
                "category": "Exotic Catch",
                "filter": "Recommended",
                "stock": 30,
                "unit": "500g"
            }
        ]
        with open(PRODUCTS_FILE, "w") as f:
            json.dump(sample_products, f, indent=2)

    if not os.path.exists(USERS_FILE):
        sample_users = [
            {
                "username": "admin",
                "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
                "email": "admin@seacraves.com",
                "full_name": "Sandeep Admin",
                "address": "12 Ocean Avenue, Coastal Bay",
                "is_admin": True
            },
            {
                "username": "customer",
                "password_hash": hashlib.sha256("customer123".encode()).hexdigest(),
                "email": "customer@seacraves.com",
                "full_name": "Rahul Mariner",
                "address": "45 Harbor View, Sea Town",
                "is_admin": False
            }
        ]
        with open(USERS_FILE, "w") as f:
            json.dump(sample_users, f, indent=2)

    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "w") as f:
            json.dump([], f, indent=2)

init_data_files()

# ----------------------------
# Helper Functions
# ----------------------------
def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def load_products():
    return load_json(PRODUCTS_FILE)

def save_products(products):
    save_json(PRODUCTS_FILE, products)

def load_users():
    return load_json(USERS_FILE)

def save_users(users):
    save_json(USERS_FILE, users)

def load_orders():
    return load_json(ORDERS_FILE)

def save_orders(filepath, orders):
    save_json(filepath, orders)

def save_uploaded_image(uploaded_file):
    if uploaded_file is not None:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}{file_ext}"
        filepath = os.path.join(IMG_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return filepath.replace("\\", "/")
    return None

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password_hash"] == hash_password(password):
            return user
    return None

def register_user(username, password, email, full_name, address):
    users = load_users()
    for user in users:
        if user["username"] == username:
            return False, "Username already exists."
    new_user = {
        "username": username,
        "password_hash": hash_password(password),
        "email": email,
        "full_name": full_name,
        "address": address,
        "is_admin": False
    }
    users.append(new_user)
    save_users(USERS_FILE, users)
    return True, "Registration successful!"

def get_cart_total(cart):
    return round(sum(item["price"] * item["quantity"] for item in cart), 2)

def add_to_cart(product_id, quantity=1):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return False, "Product not found."
    if product["stock"] < quantity:
        return False, f"Only {product['stock']} left in stock."

    if 'cart' not in st.session_state:
        st.session_state.cart = []

    for item in st.session_state.cart:
        if item["id"] == product_id:
            if item["quantity"] + quantity > product["stock"]:
                return False, "Cannot add more than available stock."
            item["quantity"] += quantity
            return True, "Cart updated."

    st.session_state.cart.append({
        "id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "quantity": quantity,
        "image": product.get("image", ""),
        "discount": product.get("discount", 0),
        "unit": product.get("unit", "500g")
    })
    return True, "Added to cart successfully."

def remove_from_cart(product_id):
    if 'cart' in st.session_state:
        st.session_state.cart = [item for item in st.session_state.cart if item["id"] != product_id]
        return True, "Item removed."
    return False, "Cart is empty."

def update_cart_quantity(product_id, quantity):
    if quantity <= 0:
        return remove_from_cart(product_id)
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return False, "Product not found."
    if product["stock"] < quantity:
        return False, f"Only {product['stock']} left in stock."

    for item in st.session_state.cart:
        if item["id"] == product_id:
            item["quantity"] = quantity
            return True, "Quantity updated."
    return False, "Item not in cart."

def place_order(payment_method):
    if 'cart' not in st.session_state or not st.session_state.cart:
        return False, "Cart is empty."
    if 'user' not in st.session_state or not st.session_state.user:
        return False, "Please log in to place an order."

    user = st.session_state.user
    cart = st.session_state.cart
    total = get_cart_total(cart)

    order = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f")[-8:],
        "user_id": user["username"],
        "user_name": user["full_name"],
        "items": cart.copy(),
        "total": total,
        "payment_method": payment_method,
        "status": "Processing",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "address": user.get("address", "")
    }

    orders = load_orders()
    orders.append(order)
    save_orders(ORDERS_FILE, orders)

    products = load_products()
    for item in cart:
        for product in products:
            if product["id"] == item["id"]:
                product["stock"] -= item["quantity"]
                break
    save_products(products)

    st.session_state.cart = []
    return True, f"Order placed successfully! Order ID: #{order['id']}"

def get_user_orders(username):
    orders = load_orders()
    return [order for order in orders if order["user_id"] == username]

# ----------------------------
# Streamlit App Configuration
# ----------------------------
st.set_page_config(
    page_title="SEACRAVES | Premium Oceanic Market",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Oceanic Deep Teal & Coral Brand Theme + Scrolling Banner Styles
st.markdown("""
<style>
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .ocean-banner {
        background: linear-gradient(90deg, #0284C7 0%, #0369A1 100%);
        color: #FFFFFF;
        text-align: center;
        padding: 10px;
        font-size: 0.95rem;
        font-weight: 500;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    .ocean-ticker {
        background-color: #065F46;
        color: #6EE7B7;
        text-align: center;
        padding: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    
    /* Scrolling Banner Styles */
    .hero-slider-container {
        display: flex;
        overflow-x: auto;
        scroll-snap-type: x mandatory;
        gap: 20px;
        padding-bottom: 15px;
        scrollbar-width: none; /* Firefox */
    }
    .hero-slider-container::-webkit-scrollbar {
        display: none; /* Safari and Chrome */
    }
    .hero-slide-card {
        flex: 0 0 100%;
        scroll-snap-align: start;
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
    }
    .hero-text-content {
        flex: 1;
    }
    .hero-image-wrapper {
        flex: 1;
        text-align: right;
    }
    .hero-image-wrapper img {
        max-height: 220px;
        border-radius: 10px;
        object-fit: cover;
        width: 100%;
    }

    .product-card {
        background: #1E293B;
        padding: 18px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid #334155;
        text-align: left;
        margin-bottom: 20px;
    }
    .badge-discount {
        background-color: #7F1D1D;
        color: #FCA5A5;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #0EA5E9;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.45rem 1rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #0284C7;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State Variables
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = "All Seafood"
if 'selected_filter' not in st.session_state:
    st.session_state.selected_filter = "All"
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# ----------------------------
# Top Oceanic Announcement Bar
# ----------------------------
st.markdown('<div class="ocean-banner">🌊 Welcome to SeaCraves by Sandeep — Premium Sustainably Sourced Seafood Delivered Fresh!</div>', unsafe_allow_html=True)

# ----------------------------
# Header Container Layout
# ----------------------------
with st.container():
    h_col1, h_col2, h_col3, h_col4 = st.columns([2, 3, 2, 2])
    with h_col1:
        st.markdown("### ⚓ **SEACRAVES** <span style='font-size:0.6rem; color:#38BDF8;'>BY SANDEEP</span>", unsafe_allow_html=True)
    with h_col2:
        search_input = st.text_input("Search", placeholder="Search salmon, prawns, tuna...", value=st.session_state.search_query, label_visibility="collapsed")
        if search_input != st.session_state.search_query:
            st.session_state.search_query = search_input
    with h_col3:
        st.markdown("📍 **Hub:** Coastal Port 01")
    with h_col4:
        user_btn_label = f"👤 {st.session_state.user['full_name'].split()[0]}" if st.session_state.user else "👤 Account"
        cart_count = sum(item['quantity'] for item in st.session_state.cart)
        
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button(user_btn_label, key="nav_signin"):
                st.session_state.page = "Account"
                st.rerun()
        with c_btn2:
            if st.button(f"🛒 Cart ({cart_count})", key="nav_cart"):
                st.session_state.page = "Cart"
                st.rerun()

# ----------------------------
# Category Navigation Bar (Including Admin Panel Link if Admin)
# ----------------------------
seafood_categories = [
    "All Seafood", "Best Sellers", "New Arrivals", "Fillets & Steaks", 
    "Shellfish", "Fresh Water", "Whole Fish", "Exotic Catch"
]

if st.session_state.user and st.session_state.user.get("is_admin", False):
    seafood_categories.append("⚙️ Admin Panel")

cat_cols = st.columns(len(seafood_categories))
for idx, cat_name in enumerate(seafood_categories):
    with cat_cols[idx]:
        is_active = (st.session_state.selected_category == cat_name)
        button_label = f"⚓ {cat_name}" if is_active else cat_name
        if st.button(button_label, key=f"cat_btn_{idx}"):
            if cat_name == "⚙️ Admin Panel":
                st.session_state.page = "Admin"
            else:
                st.session_state.selected_category = cat_name
                st.session_state.page = "Home"
            st.rerun()

# ----------------------------
# Delivery Ticker
# ----------------------------
st.markdown('<div class="ocean-ticker">⚡ Express Cold-Chain Delivery: Guaranteed fresh catch at your doorstep within 3 hours!</div>', unsafe_allow_html=True)

# ----------------------------
# Page Router & Content
# ----------------------------
page = st.session_state.page

if page == "Home":
    # ----------------------------
    # Scrolling Hero Slider with Seafood Banners
    # ----------------------------
    st.markdown("""
        <div class="hero-slider-container">
            <div class="hero-slide-card">
                <div class="hero-text-content">
                    <h1 style="color: #38BDF8; margin: 0; font-size: 1.8rem;">Claiming We're Fresh isn't Enough Anymore!</h1>
                    <p style="font-size: 0.95rem; color: #94A3B8; margin-top: 8px;">Swipe horizontally to discover why SeaCraves catch is 100% wild-caught, chemical-free, and instantly chilled.</p>
                    <div style="font-weight: 600; color: #38BDF8; margin-top: 12px; font-size: 0.85rem;">Swipe ⟶</div>
                </div>
                <div class="hero-image-wrapper">
                    <img src="https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=500" alt="Fresh Salmon">
                </div>
            </div>
            
            <div class="hero-slide-card">
                <div class="hero-text-content">
                    <h1 style="color: #38BDF8; margin: 0; font-size: 1.8rem;">Jumbo Prawns & Exotic Shellfish</h1>
                    <p style="font-size: 0.95rem; color: #94A3B8; margin-top: 8px;">Directly sourced from certified coastal marine harbors, cleaned, vacuum-sealed, and delivered in 3 hours.</p>
                    <div style="font-weight: 600; color: #38BDF8; margin-top: 12px; font-size: 0.85rem;">Swipe ⟶</div>
                </div>
                <div class="hero-image-wrapper">
                    <img src="https://images.unsplash.com/photo-1565680314427-a55bb141c2c2?w=500" alt="Tiger Prawns">
                </div>
            </div>

            <div class="hero-slide-card">
                <div class="hero-text-content">
                    <h1 style="color: #38BDF8; margin: 0; font-size: 1.8rem;">Pristine Freshwater Catch Daily</h1>
                    <p style="font-size: 0.95rem; color: #94A3B8; margin-top: 8px;">Tender cuts of river fish and steaks, cut fresh to order with zero preservatives added.</p>
                    <div style="font-weight: 600; color: #38BDF8; margin-top: 12px; font-size: 0.85rem;">Explore Below ↓</div>
                </div>
                <div class="hero-image-wrapper">
                    <img src="https://images.unsplash.com/photo-1534939561126-855b8675edd7?w=500" alt="Freshwater Catch">
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    f_col1, f_col2 = st.columns([4, 1])
    with f_col1:
        filter_options = ["All", "Recommended", "No Shell Fish", "Imported", "Fresh Water", "Sea Water"]
        chosen_filter = st.selectbox("Quick filters", filter_options, index=filter_options.index(st.session_state.selected_filter) if st.session_state.selected_filter in filter_options else 0, label_visibility="collapsed")
        if chosen_filter != st.session_state.selected_filter:
            st.session_state.selected_filter = chosen_filter
            st.rerun()
    with f_col2:
        sort_by = st.selectbox("Sort By", ["Sort By: Popular", "Price: Low to High", "Price: High to Low"], label_visibility="collapsed")

    st.markdown(f"### 🌊 {st.session_state.selected_category.upper()}")
    st.caption("Directly sourced from certified marine harbors and crystal-clear freshwater fisheries.")

    products = load_products()

    filtered = products
    cat = st.session_state.selected_category
    if cat in ["Fillets & Steaks", "Shellfish", "Fresh Water", "Whole Fish", "Exotic Catch"]:
        filtered = [p for p in filtered if p["category"] == cat]
    elif cat == "New Arrivals":
        filtered = products[-4:]
    elif cat == "Best Sellers":
        filtered = products[:4]
    
    if st.session_state.search_query:
        q = st.session_state.search_query.lower()
        filtered = [p for p in filtered if q in p["name"].lower() or q in p["description"].lower()]
        
    if st.session_state.selected_filter != "All" and cat not in ["New Arrivals", "Best Sellers"]:
        filtered = [p for p in filtered if p.get("filter") == st.session_state.selected_filter]

    if sort_by == "Price: Low to High":
        filtered.sort(key=lambda x: x["price"])
    elif sort_by == "Price: High to Low":
        filtered.sort(key=lambda x: x["price"], reverse=True)

    if not filtered:
        st.info("No seafood items found matching your criteria.")

    cols = st.columns(4)
    for idx, product in enumerate(filtered):
        with cols[idx % 4]:
            with st.container():
                st.markdown("""
                <div class="product-card">
                """, unsafe_allow_html=True)
                
                if product.get('image'):
                    st.image(product['image'], use_container_width=True)

                unit_str = product.get('unit', '500g')
                st.markdown(f"""
                    <div style="font-size:0.75rem; color:#38BDF8; font-weight:600;">{product['delivery']}</div>
                    <div style="font-weight:700; font-size:1rem; color:#F8FAFC; height: 45px; overflow: hidden; margin: 5px 0;">{product['name']}</div>
                    <div style="font-size:0.8rem; color:#94A3B8; height: 38px; overflow: hidden; margin-bottom: 10px;">{product['description']}</div>
                    <div style="font-size:0.8rem; color:#38BDF8; margin-bottom: 5px;">📦 Pack Size: <b>{unit_str}</b></div>
                """, unsafe_allow_html=True)
                
                p_c1, p_c2 = st.columns(2)
                with p_c1:
                    st.markdown(f"**₹{product['price']:.2f}**")
                with p_c2:
                    if product.get("discount", 0) > 0:
                        st.markdown(f"<span class='badge-discount'>{product['discount']}% OFF</span>", unsafe_allow_html=True)

                if st.button("ADD TO CART", key=f"prod_{product['id']}"):
                    if not st.session_state.user:
                        st.warning("Please sign in first.")
                    else:
                        success, message = add_to_cart(product["id"])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                st.markdown("</div>", unsafe_allow_html=True)

elif page == "Cart":
    st.markdown("## 🛒 Your Seafood Cart")
    if not st.session_state.cart:
        st.info("Your cart is currently empty.")
        if st.button("Explore Catch"):
            st.session_state.page = "Home"
            st.rerun()
    else:
        for item in st.session_state.cart:
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            with c1:
                st.markdown(f"**{item['name']}**")
                st.caption(f"₹{item['price']:.2f} each ({item.get('unit', '500g')})")
            with c2:
                st.markdown(f"₹{item['price'] * item['quantity']:.2f}")
            with c3:
                new_qty = st.number_input("Qty", min_value=1, max_value=20, value=item['quantity'], key=f"cart_qty_{item['id']}", label_visibility="collapsed")
                if new_qty != item['quantity']:
                    update_cart_quantity(item['id'], new_qty)
                    st.rerun()
            with c4:
                if st.button("Remove", key=f"remove_{item['id']}"):
                    remove_from_cart(item['id'])
                    st.rerun()
            st.divider()

        total = get_cart_total(st.session_state.cart)
        st.markdown(f"### Total Amount: ₹{total:.2f}")
        
        st.markdown("### Select Payment Method")
        payment_method = st.radio(
            "Choose a payment option:", 
            ["Cash on Delivery (COD)", "UPI / Google Pay / PhonePe", "Credit / Debit Card"],
            label_visibility="collapsed"
        )
        
        if st.button("Proceed to Checkout 🚀", type="primary"):
            success, msg = place_order(payment_method)
            if success:
                st.success(msg)
                st.balloons()
                st.session_state.page = "Orders"
                st.rerun()
            else:
                st.error(msg)

elif page == "Orders":
    st.markdown("## 📦 Order History")
    if not st.session_state.user:
        st.warning("Please sign in to view your orders.")
    else:
        orders = get_user_orders(st.session_state.user["username"])
        if not orders:
            st.info("No orders found.")
        else:
            for order in orders:
                with st.expander(f"Order #{order['id']} — {order['date']} — ₹{order['total']:.2f}"):
                    st.markdown(f"**Status:** {order['status']}")
                    st.markdown(f"**Payment Method:** {order.get('payment_method', 'COD')}")
                    st.markdown(f"**Delivery Address:** {order['address']}")
                    for item in order["items"]:
                        unit_str = item.get('unit', '500g')
                        st.markdown(f"- {item['name']} ({unit_str}) x {item['quantity']} @ ₹{item['price']:.2f}")

elif page == "Admin":
    if not st.session_state.user or not st.session_state.user.get("is_admin", False):
        st.error("Access Denied. Only the administrator can manage products.")
        if st.button("Return Home"):
            st.session_state.page = "Home"
            st.rerun()
    else:
        st.markdown("## ⚙️ Admin Product Management Panel")
        st.caption("Add, edit, or remove items from the SeaCraves inventory.")
        
        tab_add, tab_edit, tab_del = st.tabs(["➕ Add New Product", "✏️ Edit Product", "🗑️ Remove Product"])
        
        with tab_add:
            with st.form("add_product_form"):
                p_name = st.text_input("Product Name")
                p_desc = st.text_area("Description")
                p_price = st.number_input("Price (₹)", min_value=1.0, value=499.0)
                p_orig = st.number_input("Original Price (₹)", min_value=1.0, value=599.0)
                p_disc = st.slider("Discount (%)", 0, 50, 15)
                p_unit = st.text_input("Pack Size / Unit (e.g., 500g, 1 kg, 250g)", value="500g")
                p_stock = st.number_input("Stock Quantity", min_value=1, value=50)
                p_category = st.selectbox("Category", ["Fillets & Steaks", "Shellfish", "Fresh Water", "Whole Fish", "Exotic Catch"])
                p_filter = st.selectbox("Filter Type", ["Recommended", "No Shell Fish", "Imported", "Fresh Water", "Sea Water"])
                
                p_image_file = st.file_uploader("Upload Product Image", type=["jpg", "jpeg", "png"], key="add_img_upload")
                
                submitted = st.form_submit_button("Add Product to Store")
                if submitted:
                    image_url = save_uploaded_image(p_image_file)
                    if not image_url:
                        image_url = "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=500"
                    
                    products = load_products()
                    new_id = max([p["id"] for p in products], default=0) + 1
                    new_prod = {
                        "id": new_id,
                        "name": p_name,
                        "description": p_desc,
                        "price": p_price,
                        "original_price": p_orig,
                        "discount": p_disc,
                        "delivery": "Delivered in 3 hours",
                        "image": image_url,
                        "category": p_category,
                        "filter": p_filter,
                        "stock": int(p_stock),
                        "unit": p_unit
                    }
                    products.append(new_prod)
                    save_products(products)
                    st.success(f"Successfully added '{p_name}' to inventory!")
                    st.rerun()

        with tab_edit:
            products = load_products()
            if not products:
                st.info("No products available to edit.")
            else:
                edit_options = {f"{p['id']} - {p['name']}": p for p in products}
                selected_label = st.selectbox("Select product to edit", list(edit_options.keys()), key="edit_select_box")
                prod_to_edit = edit_options[selected_label]
                
                with st.form("edit_product_form"):
                    e_name = st.text_input("Product Name", value=prod_to_edit["name"])
                    e_desc = st.text_area("Description", value=prod_to_edit["description"])
                    e_price = st.number_input("Price (₹)", min_value=1.0, value=float(prod_to_edit["price"]))
                    e_orig = st.number_input("Original Price (₹)", min_value=1.0, value=float(prod_to_edit.get("original_price", prod_to_edit["price"])))
                    e_disc = st.slider("Discount (%)", 0, 50, int(prod_to_edit.get("discount", 0)))
                    e_unit = st.text_input("Pack Size / Unit (e.g., 500g, 1 kg)", value=prod_to_edit.get("unit", "500g"))
                    e_stock = st.number_input("Stock Quantity", min_value=0, value=int(prod_to_edit.get("stock", 10)))
                    
                    cat_list = ["Fillets & Steaks", "Shellfish", "Fresh Water", "Whole Fish", "Exotic Catch"]
                    e_category = st.selectbox("Category", cat_list, index=cat_list.index(prod_to_edit["category"]) if prod_to_edit["category"] in cat_list else 0)
                    
                    filter_list = ["Recommended", "No Shell Fish", "Imported", "Fresh Water", "Sea Water"]
                    e_filter = st.selectbox("Filter Type", filter_list, index=filter_list.index(prod_to_edit.get("filter", "Recommended")) if prod_to_edit.get("filter") in filter_list else 0)
                    
                    st.markdown(f"**Current Image Path:** {prod_to_edit.get('image', 'None')}")
                    e_image_file = st.file_uploader("Upload New Image (Optional)", type=["jpg", "jpeg", "png"], key="edit_img_upload")
                    
                    update_submitted = st.form_submit_button("Save Changes")
                    if update_submitted:
                        new_image_url = save_uploaded_image(e_image_file)
                        final_image_url = new_image_url if new_image_url else prod_to_edit.get("image", "")

                        for p in products:
                            if p["id"] == prod_to_edit["id"]:
                                p["name"] = e_name
                                p["description"] = e_desc
                                p["price"] = e_price
                                p["original_price"] = e_orig
                                p["discount"] = e_disc
                                p["stock"] = int(e_stock)
                                p["category"] = e_category
                                p["filter"] = e_filter
                                p["image"] = final_image_url
                                p["unit"] = e_unit
                                break
                        save_products(products)
                        st.success(f"Successfully updated '{e_name}'!")
                        st.rerun()
                    
        with tab_del:
            products = load_products()
            if not products:
                st.info("No products available to remove.")
            else:
                prod_options = {f"{p['id']} - {p['name']} (₹{p['price']})": p['id'] for p in products}
                selected_to_delete = st.selectbox("Select product to remove", list(prod_options.keys()))
                
                if st.button("Delete Selected Product", type="primary"):
                    target_id = prod_options[selected_to_delete]
                    updated_products = [p for p in products if p["id"] != target_id]
                    save_products(updated_products)
                    st.success("Product successfully removed from inventory.")
                    st.rerun()

elif page == "Account":
    st.markdown("## 👤 User Account & Authentication")
    if st.session_state.user is None:
        tab_login, tab_reg = st.tabs(["Sign In", "Register"])
        with tab_login:
            l_user = st.text_input("Username", key="l_user_input")
            l_pass = st.text_input("Password", type="password", key="l_pass_input")
            if st.button("Login"):
                user = authenticate_user(l_user, l_pass)
                if user:
                    st.session_state.user = user
                    st.success(f"Welcome back, {user['full_name']}!")
                    st.session_state.page = "Home"
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        with tab_reg:
            r_user = st.text_input("Username", key="r_user_input")
            r_pass = st.text_input("Password", type="password", key="r_pass_input")
            r_email = st.text_input("Email", key="r_email_input")
            r_name = st.text_input("Full Name", key="r_name_input")
            r_addr = st.text_area("Delivery Address", key="r_addr_input")
            if st.button("Register Account"):
                success, msg = register_user(r_user, r_pass, r_email, r_name, r_addr)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
    else:
        user = st.session_state.user
        st.markdown(f"**Name:** {user['full_name']}")
        st.markdown(f"**Email:** {user['email']}")
        st.markdown(f"**Address:** {user['address']}")
        if user.get("is_admin", False):
            st.info("🔑 Role: Administrator (Full Access)")
        else:
            st.info("🛍️ Role: Customer (Browse & Online Checkout)")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📦 View My Orders"):
                st.session_state.page = "Orders"
                st.rerun()
        with col_b:
            if st.button("🚪 Logout"):
                st.session_state.user = None
                st.session_state.cart = []
                st.session_state.page = "Home"
                st.rerun()

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown("""
<div style="font-size: 0.85rem; background: #0B0F19; color: #94A3B8; padding: 25px; border-radius: 8px; margin-top: 40px; border: 1px solid #1E293B;">
    <p><b>Express Delivery Hubs:</b> Coastal Mumbai • Chennai Port • Vizag Harbor • Kolkata Docks • Kochi Waters • Goa Coast</p>
    <p><b>Featured Varieties:</b> Atlantic Salmon • Tiger Prawns • Freshwater Rohu • Yellowfin Tuna • Snow Crab • Sea Scallops • Black Pomfret • Calamari</p>
    <hr style="border-color: #334155;">
    <p style="text-align: center; margin-bottom: 0;">SeaCraves by Sandeep | Marine Harvest & Logistics Ltd. | FSSAI Lic. No. 22299900011223</p>
</div>
""", unsafe_allow_html=True)