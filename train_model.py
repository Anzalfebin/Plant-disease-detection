import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Step 1: Load the dataset
print("Loading dataset...")
df = pd.read_csv('crop_recommendation.csv')

# Step 2: Prepare the data
# Features (input variables)
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
# Target (the thing we want to predict)
y = df['label']

print("Splitting data into training and testing sets...")
# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Train the model
print("Training the Random Forest Classifier model...")
# We use a RandomForestClassifier, which is a powerful and popular choice
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 4: Evaluate the model
print("Evaluating the model...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Step 5: Save the trained model
print("Saving the model to 'model.pkl'...")
with open('model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model training and saving complete!")