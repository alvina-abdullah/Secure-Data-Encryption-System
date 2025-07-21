import streamlit as st
from cryptography.fernet import Fernet

# Generate or use a key
def generate_key():
    return Fernet.generate_key().decode()

# Encrypt text
def encrypt_message(message, key):
    try:
        f = Fernet(key.encode())
        encrypted = f.encrypt(message.encode())
        return encrypted.decode()
    except Exception as e:
        return f"Error: {str(e)}"

# Decrypt text
def decrypt_message(token, key):
    try:
        f = Fernet(key.encode())
        decrypted = f.decrypt(token.encode())
        return decrypted.decode()
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit App UI
st.set_page_config(page_title="🔐 Secure Data Encryption", layout="centered")
st.title("🔐 Secure Data Encryption System")

st.markdown("Encrypt or decrypt any message securely using a **Fernet key**.")

# Sidebar: Generate Key
st.sidebar.header("🔑 Key Generator")
if st.sidebar.button("Generate New Key"):
    st.sidebar.code(generate_key(), language="text")

# User Inputs
mode = st.radio("Choose Mode:", ["Encrypt", "Decrypt"])
key = st.text_input("Enter your Fernet Key:")
text = st.text_area("Enter your Message:")

# Process
if st.button("Submit"):
    if not key or not text:
        st.warning("Please enter both key and message.")
    else:
        if mode == "Encrypt":
            result = encrypt_message(text, key)
            st.success("🔒 Encrypted Text:")
            st.code(result, language="text")
        else:
            result = decrypt_message(text, key)
            st.success("🔓 Decrypted Text:")
            st.code(result, language="text")

st.markdown("---")
st.caption("Built with ❤️ using Python & Streamlit")
