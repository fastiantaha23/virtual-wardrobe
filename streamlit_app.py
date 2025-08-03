import streamlit as st
import pandas as pd
import os
from PIL import Image
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Constants ---
DATA_PATH = "wardrobe.csv"
IMAGE_FOLDER = "images"
CATEGORIES = ["Shirt", "Pants", "Shoes"]

# --- Page Config ---
st.set_page_config(page_title="Virtual Wardrobe Stylist", layout="wide")
st.title("👕 Virtual Wardrobe Stylist")

# --- Load wardrobe data ---
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    df['tags'] = df['tags'].apply(lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else x.split(','))
else:
    df = pd.DataFrame(columns=["filename", "category", "tags"])

# --- Save wardrobe data ---
def save_df():
    df.to_csv(DATA_PATH, index=False)

# --- Add New Item ---
st.sidebar.header("➕ Add New Item")
with st.sidebar.form("add_form"):
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    category = st.selectbox("Category", CATEGORIES)
    tags_input = st.text_input("Tags (comma-separated)", "")
    add_submit = st.form_submit_button("Add to Wardrobe")

    if add_submit and uploaded_file:
        filename = uploaded_file.name
        filepath = os.path.join(IMAGE_FOLDER, filename)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        new_item = {
            "filename": filename,
            "category": category,
            "tags": [t.strip() for t in tags_input.split(",") if t.strip()]
        }
        df.loc[len(df)] = new_item
        save_df()
        st.sidebar.success(f"{filename} added!")

# --- Show Wardrobe ---
st.subheader("🧥 Your Wardrobe")

for cat in CATEGORIES:
    cat_df = df[df["category"] == cat]
    st.markdown(f"### {cat}")
    if cat_df.empty:
        st.info("No items found.")
    else:
        for i, row in cat_df.iterrows():
            cols = st.columns([1, 3, 2])
            with cols[0]:
                img_path = os.path.join(IMAGE_FOLDER, row["filename"])
                if os.path.exists(img_path):
                    st.image(img_path, width=100)
            with cols[1]:
                st.markdown(f"Filename: {row['filename']}")
                st.markdown(f"Tags: {', '.join(row['tags'])}")
            with cols[2]:
                if st.button("📝 Edit", key=f"edit_{i}"):
                    st.session_state["edit_mode"] = True
                    st.session_state["editing_index"] = i
                if st.button("❌ Delete", key=f"delete_{i}"):
                    df.drop(i, inplace=True)
                    df.reset_index(drop=True, inplace=True)
                    save_df()
                    st.experimental_rerun()

# --- Edit Form (rendered only once) ---
if st.session_state.get("edit_mode", False):
    edit_index = st.session_state.get("editing_index", None)
    if edit_index is not None and edit_index < len(df):
        row = df.iloc[edit_index]
        st.markdown("---")
        st.markdown("### ✏ Edit Item")
        with st.form(f"edit_form_{edit_index}"):
            new_category = st.selectbox("Edit Category", CATEGORIES, index=CATEGORIES.index(row["category"]))
            new_tags = st.text_input("Edit Tags", value=", ".join(row["tags"]))
            save_button = st.form_submit_button("Save Changes")
            if save_button:
                df.at[edit_index, "category"] = new_category
                df.at[edit_index, "tags"] = [t.strip() for t in new_tags.split(",") if t.strip()]
                save_df()
                st.success("Item updated successfully.")
                st.session_state["edit_mode"] = False
                st.session_state["editing_index"] = None
                st.rerun()



# --- Outfit Predictor ---
st.subheader("🎯 Outfit Predictor")

with st.form("predict_form"):
    st.markdown("👤 Select your preferred style tags (e.g., summer, formal, office, casual)")
    all_tags = sorted(list({tag for tags in df["tags"] for tag in tags}))
    user_tags = st.multiselect("Preferred Tags", all_tags)
    predict_submit = st.form_submit_button("Suggest Outfit")

# --- AI Outfit Logic ---
if predict_submit:
    if not user_tags:
        st.warning("Please select at least one tag.")
    else:
        def recommend(df_cat, user_tags):
            if df_cat.empty:
                return None
            tag_texts = [" ".join(tags) for tags in df_cat["tags"]]
            user_input = [" ".join(user_tags)] * len(df_cat)
            vec = CountVectorizer().fit(tag_texts + user_input)
            item_vecs = vec.transform(tag_texts)
            user_vec = vec.transform(user_input)
            scores = cosine_similarity(user_vec, item_vecs).flatten()
            best_idx = scores.argmax()
            return df_cat.iloc[best_idx]

        shirt = recommend(df[df["category"] == "Shirt"], user_tags)
        pants = recommend(df[df["category"] == "Pants"], user_tags)
        shoes = recommend(df[df["category"] == "Shoes"], user_tags)

        if shirt is not None and pants is not None and shoes is not None:
            st.success("✅ Recommended Outfit")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(os.path.join(IMAGE_FOLDER, shirt["filename"]), caption="👕 Shirt", use_column_width=True)
            with col2:
                st.image(os.path.join(IMAGE_FOLDER, pants["filename"]), caption="👖 Pants", use_column_width=True)
            with col3:
                st.image(os.path.join(IMAGE_FOLDER, shoes["filename"]), caption="👟 Shoes", use_column_width=True)
        else:
            st.error("Some wardrobe items are missing in one or more categories.")