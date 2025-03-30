import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
import os
import pickle
import json

# Load dataset
df = pd.read_csv('fake_job_postings.csv')  # Update with actual path

# Fill NaN values with empty strings
df.fillna("", inplace=True)

# Combine relevant text fields
df['combined_text'] = df['title'] + ' ' + df['company_profile'] + ' ' + df['description'] + ' ' + df['requirements'] + ' ' + df['benefits']

# Convert salary_range to numerical values
def process_salary(salary_range):
    try:
        # Check if the salary range contains a dash (e.g., "5000-7000")
        if '-' in salary_range:
            values = salary_range.split('-')
            # Ensure both parts are numeric
            if values[0].strip().isdigit() and values[1].strip().isdigit():
                return (float(values[0]) + float(values[1])) / 2  # Average salary
        
        # If it's a single numeric value, convert it to float
        if salary_range.strip().isdigit():
            return float(salary_range)
    except Exception as e:
        print(f"Error processing salary: {salary_range} - {e}")
    
    # Return NaN for invalid or non-numeric salary ranges
    return np.nan

# Apply the updated function
df['salary'] = df['salary_range'].apply(process_salary)
df['salary'].fillna(df['salary'].median(), inplace=True)

# Tokenization
MAX_WORDS = 20000
MAX_LEN = 300

tokenizer = Tokenizer(num_words=MAX_WORDS)
tokenizer.fit_on_texts(df['combined_text'])
sequences = tokenizer.texts_to_sequences(df['combined_text'])
X_text = pad_sequences(sequences, maxlen=MAX_LEN)

# Normalize salary
scaler = MinMaxScaler()
X_salary = scaler.fit_transform(df[['salary']])

# Target variable
y = df['fraudulent'].values

# Train-test split
X_text_train, X_text_test, X_salary_train, X_salary_test, y_train, y_test = train_test_split(
    X_text, X_salary, y, test_size=0.2, random_state=42)

# Model definition
text_input = keras.layers.Input(shape=(MAX_LEN,), name='text_input')
salary_input = keras.layers.Input(shape=(1,), name='salary_input')

embedding = keras.layers.Embedding(input_dim=MAX_WORDS, output_dim=128, input_length=MAX_LEN)(text_input)
bi_lstm = keras.layers.Bidirectional(keras.layers.LSTM(64, return_sequences=True))(embedding)
global_pooling = keras.layers.GlobalMaxPooling1D()(bi_lstm)

concatenated = keras.layers.concatenate([global_pooling, salary_input])
dense1 = keras.layers.Dense(64, activation='relu')(concatenated)
dropout = keras.layers.Dropout(0.5)(dense1)
output = keras.layers.Dense(1, activation='sigmoid')(dropout)

model = keras.Model(inputs=[text_input, salary_input], outputs=output)

# Compile model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train model with history
history = model.fit(
    [X_text_train, X_salary_train], y_train,
    validation_data=([X_text_test, X_salary_test], y_test),
    epochs=10, batch_size=32, verbose=1
)

# Evaluate model
loss, accuracy = model.evaluate([X_text_test, X_salary_test], y_test)
print(f'Test Accuracy: {accuracy * 100:.2f}%')

# Make predictions
y_pred_proba = model.predict([X_text_test, X_salary_test])
y_pred = (y_pred_proba > 0.5).astype(int)

# Create directory for saving model artifacts
save_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
os.makedirs(save_dir, exist_ok=True)

# Save model in .keras format
model_path = os.path.join(save_dir, 'fake_job_detection_model.keras')
model.save(model_path, save_format='keras')
print(f"Model saved to {model_path}")

# Save preprocessors
tokenizer_path = os.path.join(save_dir, 'tokenizer.pickle')
with open(tokenizer_path, 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
print(f"Tokenizer saved to {tokenizer_path}")

scaler_path = os.path.join(save_dir, 'salary_scaler.pickle')
with open(scaler_path, 'wb') as handle:
    pickle.dump(scaler, handle, protocol=pickle.HIGHEST_PROTOCOL)
print(f"Scaler saved to {scaler_path}")

# Save model configuration
config = {
    'MAX_WORDS': MAX_WORDS,
    'MAX_LEN': MAX_LEN,
    'model_version': '1.0.0'
}
config_path = os.path.join(save_dir, 'model_config.json')
with open(config_path, 'w') as f:
    json.dump(config, f)
print(f"Model configuration saved to {config_path}")

# Visualize training history
plt.figure(figsize=(12, 4))

# Plot accuracy
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# Plot loss
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(save_dir, 'training_history.png'))
plt.show()

# Plot confusion matrix
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.savefig(os.path.join(save_dir, 'confusion_matrix.png'))
plt.show()

# Plot ROC curve
fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend()
plt.savefig(os.path.join(save_dir, 'roc_curve.png'))
plt.show()

# Print classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
