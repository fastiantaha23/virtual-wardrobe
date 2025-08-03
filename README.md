# 👗 Virtual Wardrobe Stylist

An interactive **AI-powered virtual stylist** built with **Python** and **Streamlit**, designed to help users upload, view, and match wardrobe items for smart outfit suggestions. This app is a practical example of combining data, UI design, and basic AI logic to create a personalized experience.

## 🔍 Features

✅ **Upload & Manage Wardrobe**
- Add images of your shirts, pants, and shoes
- Auto-categorized by type (e.g., Shirt, Pants, Shoes)
- Tag items by color, season, and style (e.g., "formal", "casual", "winter")

🎯 **AI-Powered Outfit Suggestions**
- Uses tag-matching logic to suggest outfits
- Only shows compatible combinations (e.g., formal shirt with formal shoes)

📷 **Aesthetic Image Display**
- Neatly organized wardrobe grid with small thumbnails
- Responsive layout to show multiple items in one row

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** for UI
- **Pandas** for data handling
- **CSV** as local storage for wardrobe and saved outfits

---

## 🧠 How Outfit Suggestion Works

Each item (shirt, pants, shoes) has associated tags like:
"formal", "casual", "summer", "winter", "black", "white", etc.

The app finds compatible combinations based on:
- Shared tags (e.g., all items are “formal” or “winter”)
- Avoids mismatched items (e.g., casual shoes with formal shirts)

---

## 📂 Project Structure

virtual-wardrobe/
├── streamlit_app.py # Main application
├── wardrobe.csv # Stores wardrobe data
├── images/ # Folder for uploaded item images
│ ├── shirt_blue.jpg
│ ├── pants_black.jpg
│ └── ...
├── requirements.txt # Required Python packages
└── README.md # This file

## 🚀 How to Run

1. **Install dependencies**
```bash
pip install -r requirements.txt
Run the Streamlit app

streamlit run streamlit_app.py
Upload images
Place your clothing images inside the images/ folder before running the app or upload them during use.

🎯 What I Learned
This project helped me explore:

Real-world UI building with Streamlit

Basic AI decision-making via tag-matching

State management and CSV-based data persistence

Designing user-centric tools with a mix of form and function

🔗 Connect with Me
Made with ❤️ by Taha Malik

🌐 LinkedIn

💻 GitHub

✉️ Email

⭐️ Star This Repo
If you liked this project, consider starring ⭐ it — it helps others discover it too!

📜 License
This project is open-source under the MIT License.


Let me know if you want me to:
- Generate the screenshots automatically from your app
- Help you create a `LICENSE` file
- Create the `requirements.txt` from your local environment
- Deploy to Streamlit Cloud for live sharing

Happy uploading!
