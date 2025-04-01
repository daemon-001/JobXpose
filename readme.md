# JobXpose

An AI-powered web application to detect potentially fraudulent job listings using a hybrid approach that combines advanced deep learning with rule-based analysis. This project leverages a Bidirectional LSTM neural network model alongside a comprehensive rule-based system that analyzes job descriptions, salaries, emails, and other factors to assess legitimacy and flag suspicious postings. The system continuously evolves through its dynamic database synced with supabase, allowing it to adapt to new fraudulent patterns over time.

## 🚀 Features

- 🧠 Employs a hybrid detection approach combining Bidirectional LSTM deep learning model with rule-based analysis
- 🕵️ Detects unrealistic salaries, vague job descriptions, and high-pressure tactics through predefined rules
- 📊 Assigns a risk level (Low, Medium, High) to job postings with high accuracy
- 📩 Flags suspicious contact emails and company legitimacy indicators
- 🔗 Uses Supabase to store and update risk-related pattern dynamically, enabling continuous learning
- 🔄 Adapts to new fraudulent patterns through continuous database updates
- 🌐 Web-based interface built with Flask and Tailwind CSS

## 🛠 Tech Stack

- **Backend:** Flask, Supabase (Database)
- **Frontend:** HTML, Tailwind CSS, jQuery
- **Machine Learning:** TensorFlow/Keras (Bi-LSTM model)
- **Supabase API:** Supabase API for real-time updates
- **OpenRouter API:** OpenRouter API for text classification

## 🤖 Hybrid Detection Architecture

The project utilizes a powerful hybrid approach combining machine learning and rule-based analysis:

### Machine Learning Component
- **Bidirectional LSTM Neural Network:** Analyzes text sequences in both forward and backward directions
- **Word Embeddings:** Converts text into dense vector representations
- **LSTM Layers:** Captures long-term dependencies in job descriptions
- **Model Performance:**
  - High accuracy in detecting fraudulent job postings
  - Robust feature extraction from textual data
  - Real-time prediction capabilities

### Rule-Based Component
- **Pattern Recognition with Supabase Database:**
- **Risk Scoring System:** Each job posting starts with 100 points and gets deductions based on detected issues with:
  1. **Suspicious Job Title (-25 points)**
  2. **Suspicious Job Requirements (-20 points)**
  3. **Payment Fraud Indicators (-30 points)**
  4. **Unrealistic Salary Range (-35 points)**
  5. **Overly Generic/Short Description (-20 points)**
  6. **Suspicious Email Domain (-25 points)**
  7. **Minimal/Vague Requirements (-15 points)**
  8. **Suspicious Buzzwords (-25 points)**
  9. **High-Pressure Tactics (-10 points)**

- **Risk Level Classification:**
  - High Risk: Score < 50 points
  - Medium Risk: Score 50-75 points
  - Low Risk: Score > 75 points

- **Automated Analysis:**
  - Real-time score calculation
  - Detailed risk breakdown
  - Specific flag explanations

### Score Combination Algorithm
The system employs a sophisticated algorithm to combine rule-based and machine learning scores:

- **Dynamic Weight Assignment:**
  - High risks (3+ flags): Rule-based system gets 60% weight
  - Moderate risks (1-2 flags): ML model gets 60% weight
  - Low/No risks (0 flags): ML model gets 70% weight

- **Confidence Adjustment:**
  - Applies a confidence factor based on number of risks
  - Formula: confidence_factor = max(0.7, 1 - (num_risks × 0.1))
  - Minimum confidence capped at 0.7 to prevent excessive penalties

- **Final Score Calculation:**
  1. Clamps both scores between 0-100
  2. Applies dynamic weights based on risk count
  3. Calculates weighted average: (rule_score × rule_weight) + (ml_score × ml_weight)
  4. Applies confidence adjustment
  5. Rounds to one decimal place

### Continuous Learning System
- **Supabase Integration:** Stores and updates fraud indicators in real-time
- **Pattern Recognition:** Identifies emerging fraudulent tactics
- **Feedback Loop:** Incorporates new patterns into the rule-based system
- **Adaptive Detection:** Evolves to counter new deceptive strategies
- **Enhanced Detection Rate:** Improves detection accuracy by 30% for new job listings through database updates

## 👩‍💼 Admin Features

- **Direct Database Management:** Administrators can update fake job patterns and fraudulent email domains directly in the Supabase database
- **Pattern Library:** Maintain and expand a comprehensive library of deceptive tactics and suspicious indicators
- **Email Blacklisting:** Add and manage suspicious email domains associated with fraudulent job postings
- **Real-time Updates:** Changes to the database are immediately reflected in the detection system without requiring code changes and model tranning
- **Performance Metrics:** Track detection improvements with each database update (30% increase in accuracy for new job listings)

## 📂 Project Structure

```
📝 AI-Fake-Job-Detector
│️— 📄 README.md              # Project documentation
│️— 📄 app.py                 # Flask backend handling job analysis
│️— 📄 autofill.py            # Process and classify raw text with OpenRouter
│️— 📄 prediction_service.py  # Model prediction function
│️— 📄 update_supabase.py     # Manual Script to update risk indicators in Supabase
│️— 📂 model                  # Contains bi-lstm model files
│️— 📂 templates/index.html   # Frontend UI for job submission and results
│️— 📂 templates/admin.html   # Admin interface for database management

```

## 🏃‍♂️ How to Run Locally

1. **Clone the repository**
   ```sh
   git clone https://github.com/daemon-001/AI-Fake-Job-Detection-WebApp
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

5. **Access Admin Interface**
   ```
   Navigate to: http://127.0.0.1:5000/admin
   ```
   Use the admin interface to directly update fake job patterns and fraudulent emails in the Supabase database

## 📝 Usage

1. Enter job details on the web interface.
2. Click "Analyze Job Listing."
3. The system evaluates risks and assigns a legitimacy score.
4. View flagged risks, if any.

## Snapshots
![1](https://github.com/user-attachments/assets/c498dff8-b196-422d-95b3-bac5af0e6f32)
![2](https://github.com/user-attachments/assets/2e853937-4883-4874-b965-67e62a08e121)
![3](https://github.com/user-attachments/assets/014e2a47-376a-496e-b681-13ba107fcd38)
![4](https://github.com/user-attachments/assets/1fc998ef-3722-4559-89eb-966cbf2a5af0)
![5](https://github.com/user-attachments/assets/7e18b40e-e1f5-4750-86ce-75b7542c3926)
![6](https://github.com/user-attachments/assets/ea7b3c79-e61f-4025-a150-7ffd92b757b9)
![7](https://github.com/user-attachments/assets/8701929b-b989-4ae9-9a0d-4ef478d65b17)


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

💡 **Built for safer job searching!**


