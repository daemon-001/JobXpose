# AI Fake Job Detector

An AI-powered web application to detect potentially fraudulent job listings using predefined risk indicators. This project analyzes job descriptions, salaries, emails, and other factors to assess legitimacy and flag suspicious postings.

## 🚀 Features

- 🕵️ Detects unrealistic salaries, vague job descriptions, and high-pressure tactics.
- 📊 Assigns a risk level (Low, Medium, High) to job postings.
- 📩 Flags suspicious contact emails and company legitimacy indicators.
- 🔗 Uses Supabase to store and update risk-related keywords dynamically.
- 🌐 Web-based interface built with Flask and Tailwind CSS.

## 🛠 Tech Stack

- **Backend:** Flask, Supabase (Database)
- **Frontend:** HTML, Tailwind CSS, jQuery
- **APIs:** Supabase API for real-time updates
- **Deployment:** Works on any Flask-compatible hosting

## 📂 Project Structure

```
📝 AI-Fake-Job-Detector
│️— 📄 app.py             # Flask backend handling job analysis
│️— 📄 update_supabase.py # Script to update risk indicators in Supabase
│️— 📄 index.html         # Frontend UI for job submission and results
│️— 📂 static             # (Optional) Place for static assets (CSS, JS, images)
│️— 📂 templates          # Flask template files (if extended)
│️— 📄 README.md          # Project documentation
```

## 🏃‍♂️ How to Run Locally

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/AI-Fake-Job-Detector.git
   cd AI-Fake-Job-Detector
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Flask application**
   ```sh
   python app.py
   ```
   The app will be available at: `http://127.0.0.1:5000/`

4. **(Optional) Update Supabase Data**
   ```sh
   python update_supabase.py
   ```

## 📝 Usage

1. Enter job details on the web interface.
2. Click "Analyze Job Listing."
3. The system evaluates risks and assigns a legitimacy score.
4. View flagged risks, if any.

## 📌 To-Do

- [ ] Add machine learning-based risk prediction.
- [ ] Improve UI for better user experience.
- [ ] Deploy on a cloud platform.

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo, make improvements, and submit a pull request.

## 🐜 License

This project is licensed under the MIT License.

---

💡 **Built for safer job searching!**

