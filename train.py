import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# Training dataset samples
data = [
    ("char buf[10]; gets(buf);", "Buffer Overflow"),
    ("char dest[8]; strcpy(dest, src);", "Buffer Overflow"),
    ("void test(char *input) { char b[16]; sprintf(b, \"%s\", input); }", "Buffer Overflow"),
    ("char target[5]; strcat(target, large_input);", "Buffer Overflow"),
    
    ("query = f\"SELECT * FROM users WHERE user='{user}' AND pass='{password}'\"", "SQL Injection"),
    ("cursor.execute(\"SELECT * FROM accounts WHERE id = \" + account_id)", "SQL Injection"),
    ("db.execute(f\"DELETE FROM items WHERE name = '{item_name}'\")", "SQL Injection"),
    ("query = \"SELECT * FROM staff WHERE email = '\" + email + \"'\"", "SQL Injection"),
    
    ("os.system('ping -c 1 ' + user_ip)", "Command Injection"),
    ("subprocess.Popen('cat ' + file_name, shell=True)", "Command Injection"),
    ("import subprocess; subprocess.call(user_input, shell=True)", "Command Injection"),
    ("os.popen('ls ' + user_folder)", "Command Injection"),
    
    ("char dest[10]; strncpy(dest, src, sizeof(dest) - 1); dest[sizeof(dest)-1] = '\\0';", "Safe"),
    ("std::string s; std::cin >> s;", "Safe"),
    ("cursor.execute(\"SELECT * FROM users WHERE user=%s AND pass=%s\", (user, password))", "Safe"),
    ("import sqlite3; cur.execute(\"SELECT * FROM items WHERE id=?\", (item_id,))", "Safe"),
    ("import subprocess; subprocess.run(['ping', '-c', '1', safe_ip], shell=False)", "Safe"),
    ("with open('file.txt', 'r') as f: data = f.read()", "Safe"),
    ("safe_val = int(input_data)", "Safe")
]

df = pd.DataFrame(data, columns=["code", "label"])

if not os.path.exists("dataset"):
    os.makedirs("dataset")
df.to_csv("dataset/code_snippets.csv", index=False)

# Tokenize keywords and syntax operators
vectorizer = TfidfVectorizer(
    token_pattern=r"(?u)\b\w+\b|[!$%^&*()_+|~=`{}\[\]:\";'<>?,.\/\\]",
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(df['code'])
y = df['label']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

if not os.path.exists("models"):
    os.makedirs("models")

joblib.dump(model, "models/model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("Training finished. Artifacts saved in models directory.")