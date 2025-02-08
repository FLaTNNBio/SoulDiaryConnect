# SoulDiaryConnect

**SoulDiaryConnect** is an AI-powered system designed to support patients in their **psychotherapeutic journey** by enabling journaling with **personalized AI feedback**, while keeping the **therapist connected and in control**. 
The platform allows patients to **log daily experiences**, receive **AI-generated motivational and clinical feedback**, and stay in touch with their physician.
The AI used is [Mistral 7B OpenOrca](https://huggingface.co/mistralai/Mistral-7B-v0.1).
<p align="center">
  <img src="https://github.com/FLaTNNBio/SoulDiaryConnect/blob/e029cedbdc8da70dbec7e5fe89edf20dfc26bb97/media/logo-blu.png" width="250" alt="Logo SoulDiaryConnect">
</p>

---

## Features

- **AI-Assisted Journaling** – Patients can document their daily experiences and receive **motivational feedback** from an LLM.
- **Personalized AI** – Doctors can **configure AI responses** to provide **clinical insights** and tailor support to each patient.
- **Intuitive User Interface** – A web application with **dedicated patient and doctor dashboards**.
- **Secure Data Management** – Uses **PostgreSQL** for structured data storage.
- **Advanced NLP Processing** – Powered by **Mistral-7B**, running locally with **llama_cpp**.
- **Multi-User Access** – Patients and doctors have separate roles and functionalities.

---

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **NLP**: Mistral-7B (Quantized GGUF) via llama_cpp
- **Database**: PostgreSQL

---

## Installation Guide

### **1️. Clone the repository**
```sh
git clone https://github.com/FLaTNNBio/SoulDiaryConnect.git
cd SoulDiaryConnect
```

### **2. Set up a virtual environment**
```sh
python3 -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

### **3. Install dependencies**
```sh
pip install -r requirements.txt
```

## **4. Configure the database**

Install PostgreSQL following the [official guideline](https://www.postgresql.org/download/).
To exectute the queries:
```sh
python manage.py dbshell
```

Then:
```sql
\i souldiaryconnect.sql
```

Now edit **setting.py** to configure PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'souldiaryconnect',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Make database migrations:
```sh
python manage.py makemigrations
```

Run database migrations:
```sh
python manage.py migrate
```

## **5. Load the NLP model (Mistral-7B)**

Download the [Mistral-7B (quantized GGUF)](https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF) model and place it in the 'models/mistral/' directory.

Update the model path in **views.py** and edit the *context size* (**n_ctx** value):
```python
model_path = "./models/mistral/your_mistral-7b-openorca.Q8_0.gguf"
llama_model = Llama(model_path=model_path, n_ctx=2048)
```

## **6. Start the server**
```sh
python manage.py runserver
```
## **Roles & Functionality**
### Doctor
- **Manage patients** – Access and review patient journal entries.
- **Customize AI responses** – Configure the AI to tailor feedback generation.
- **Monitor therapy progress** – View clinical trends and intervene when necessary.
### Patient
- **Write personal journal entries** – Document daily thoughts and emotions.
- **Receive AI-generated feedback** – Get motivational and therapeutic insights.
- **View therapist's comments** – See personalized feedback from the doctor.
