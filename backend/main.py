from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from .rag import rag_system
import uvicorn

app = FastAPI(title="Master SK Academy RAG API")

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    sources: list = []

@app.get("/")
def read_root():
    return {"status": "online", "message": "Master SK Academy AI Backend is Running"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        response_data = rag_system.generate_response(request.message)
        return ChatResponse(
            answer=response_data["answer"],
            sources=response_data["context"]
        )
    except Exception as e:
        print(f"Error: {e}")

class ContactForm(BaseModel):
    name: str
    phone: str
    email: str
    subject: str
    message: str

class AdmissionForm(BaseModel):
    studentName: str
    parentName: str
    phone: str
    email: str = None
    class_applied: str
    message: str = None

def send_email_notification(subject: str, body: str):
    # Retrieve credentials (placeholder logic)
    sender_email = os.getenv("MAIL_USERNAME")
    sender_password = os.getenv("MAIL_PASSWORD")
    recipient_email = "senthil87ks@gmail.com"
    
    if not sender_email or not sender_password:
        print(f"--- SIMULATED EMAIL TO {recipient_email} ---")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        print("---------------------------------------------")
        return True

    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Standard Gmail SMTP port
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@app.post("/submit-contact")
def submit_contact(form: ContactForm):
    subject = f"New Contact Enquiry: {form.subject}"
    body = f"""
    Name: {form.name}
    Phone: {form.phone}
    Email: {form.email}
    Subject: {form.subject}
    Message: {form.message}
    """
    success = send_email_notification(subject, body)
    if success:
        return {"status": "success", "message": "Enquiry submitted successfully"}
    else:
         raise HTTPException(status_code=500, detail="Failed to send email")

@app.post("/submit-admission")
def submit_admission(form: AdmissionForm):
    subject = f"New Admission Enquiry: {form.studentName}"
    body = f"""
    Student Name: {form.studentName}
    Parent Name: {form.parentName}
    Phone: {form.phone}
    Email: {form.email}
    Class: {form.class_applied}
    Message: {form.message}
    """
    success = send_email_notification(subject, body)
    if success:
         return {"status": "success", "message": "Admission enquiry submitted successfully"}
    else:
         raise HTTPException(status_code=500, detail="Failed to send email")


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
