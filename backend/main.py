from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Thread, Message
from llm import ask_llm

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "AI Chat Backend Running"}


@app.post("/thread")
def create_thread(db: Session = Depends(get_db)):

    thread = Thread(
        title="New Chat"
    )

    db.add(thread)
    db.commit()
    db.refresh(thread)

    return {
        "id": thread.id,
        "title": thread.title
    }


@app.get("/threads")
def get_threads(db: Session = Depends(get_db)):

    threads = db.query(Thread).all()

    return threads


@app.get("/messages/{thread_id}")
def get_messages(thread_id: int, db: Session = Depends(get_db)):

    messages = (
        db.query(Message)
        .filter(Message.thread_id == thread_id)
        .all()
    )

    return messages


@app.post("/chat")
def chat(
    thread_id: int,
    message: str,
    db: Session = Depends(get_db)
):

    # Save user message
    user_message = Message(
        thread_id=thread_id,
        role="user",
        content=message
    )

    db.add(user_message)
    db.commit()

    # Ask AI
    ai_response = ask_llm(message)

    # Save AI response
    assistant_message = Message(
        thread_id=thread_id,
        role="assistant",
        content=ai_response
    )

    db.add(assistant_message)
    db.commit()

    return {
        "response": ai_response
    }