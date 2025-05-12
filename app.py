import streamlit as st
import hashlib
import json
from cryptography.fernet import Fernet

# In-memory data storage (load from file if exists)
data_file = "secure_data.json"
try:
    with open(data_file, "r") as f:
        stored_data = json.load(f)
except FileNotFoundError:
    stored_data = {}

# Generate a key (in real app, store this securely and reuse)
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# Global failed attempt tracker
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

# Function to hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Encrypt data
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# Decrypt data
def decrypt_data(encrypted_text, passkey):
    hashed_passkey = hash_passkey(passkey)

    if encrypted_text in stored_data:
        if stored_data[encrypted_text]["passkey"] == hashed_passkey:
            st.session_state.failed_attempts = 0
            return cipher.decrypt(encrypted_text.encode()).decode()

    st.session_state.failed_attempts += 1
    return None

# Save to file
def save_data():
    with open(data_file, "w") as f:
        json.dump(stored_data, f)

# Streamlit UI
st.title("🔒 Secure Data Encryption System")
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("🏠 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")

elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")
    user_data = st.text_area("Enter Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey:
            hashed_passkey = hash_passkey(passkey)
            encrypted_text = encrypt_data(user_data)
            stored_data[encrypted_text] = {"encrypted_text": encrypted_text, "passkey": hashed_passkey}
            save_data()
            st.success("✅ Data stored securely!")
            st.code(encrypted_text, language="text")
        else:
            st.error("⚠️ Both fields are required!")

elif choice == "Retrieve Data":
    if st.session_state.failed_attempts >= 3:
        st.warning("🔒 Too many failed attempts! Please reauthorize.")
        st.stop()

    st.subheader("🔍 Retrieve Your Data")
    encrypted_text = st.text_area("Enter Encrypted Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_text and passkey:
            decrypted_text = decrypt_data(encrypted_text, passkey)
            if decrypted_text:
                st.success(f"✅ Decrypted Data: {decrypted_text}")
            else:
                remaining = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey! Attempts remaining: {remaining}")
        else:
            st.error("⚠️ Both fields are required!")

elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    login_pass = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if login_pass == "admin123":  # Change this for actual usage
            st.session_state.failed_attempts = 0
            st.success("✅ Reauthorized successfully! You may now access Retrieve Data.")
        else:
            st.error("❌ Incorrect password!")
