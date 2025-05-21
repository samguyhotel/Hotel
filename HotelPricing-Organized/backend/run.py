import uvicorn
import os
from app.db.init_db import init_db

if __name__ == "__main__":
    # Initialize the database with sample data
    init_db()
    
    # Run the FastAPI application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
