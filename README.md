\# 🔥 Hearth – Desktop Chat Application



A modern desktop chat application built using \*\*Python (Tkinter)\*\* and \*\*MySQL\*\*, featuring a clean UI and real-time messaging.



\---



\## ✨ Features



\* 🔐 User Authentication (Login / Register)

\* 💬 Real-time Messaging (Auto-refresh)

\* 👥 Contact List System

\* 🎨 Modern UI with warm theme

\* 📜 Scrollable Chat Interface



\---



\## 🖼️ Preview



!\[App Screenshot](assets/screenshot.png)



\---



\## 🛠️ Tech Stack



\* Python (Tkinter)

\* MySQL

\* PyMySQL



\---



\## ⚙️ Setup Instructions



1\. Clone the repository:



```bash

git clone https://github.com/your-username/hearth-chat-app.git

cd hearth-chat-app

```



2\. Install dependencies:



```bash

pip install -r requirements.txt

```



3\. Setup MySQL database:



```sql

CREATE DATABASE hearth;

```



Create tables:



```sql

CREATE TABLE users (

&#x20;   id INT AUTO\_INCREMENT PRIMARY KEY,

&#x20;   user\_name VARCHAR(255),

&#x20;   password VARCHAR(255)

);



CREATE TABLE messages (

&#x20;   id INT AUTO\_INCREMENT PRIMARY KEY,

&#x20;   sender\_id INT,

&#x20;   receiver\_id INT,

&#x20;   message TEXT,

&#x20;   timestamp TIMESTAMP DEFAULT CURRENT\_TIMESTAMP

);

```



4\. Run the app:



```bash

python main.py

```



\---



\## 🚀 Future Improvements



\* 🔒 Password hashing (bcrypt)

\* 😊 Emoji support

\* 🕒 Message timestamps UI

\* 🌐 Web version (React + Flask)



\---



\## 📌 Author



Your Name

GitHub: https://github.com/Adzz09



