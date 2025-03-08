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
│️— 📄 README.md            # Project documentation
│️— 📄 app.py               # Flask backend handling job analysis
│️— 📄 update_supabase.py   # Script to update risk indicators in Supabase
│️— 📂 templates/index.html # Frontend UI for job submission and results
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

## Snapshots
![1](https://github.com/user-attachments/assets/c1a4fc3a-fe16-483c-b5f1-fe65cefa3367)
![2](https://github.com/user-attachments/assets/9b099018-e6d2-4391-81df-ed66f8e7888b)
![3](https://github.com/user-attachments/assets/8c18b10a-1a8c-4ec1-9dfe-19d915eea52c)
![4](https://github.com/user-attachments/assets/255939c4-1a62-4860-b6df-80228f44d948)
![5](https://github.com/user-attachments/assets/cc0f8de1-aa68-4438-9c80-147ebfc4342d)
![6](https://github.com/user-attachments/assets/f7d20c58-b483-49aa-a6cc-380152a958b8)
![7](https://github.com/user-attachments/assets/43e87743-bd89-4b0b-a70c-46c92f22be84)
![8](https://github.com/user-attachments/assets/10e0e9a3-bcac-4394-91fe-0ee6144479fd)


---

💡 **Built for safer job searching!**


