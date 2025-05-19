#!/bin/bash

# Start the Django backend
echo "Starting Django backend on port 9000..."
cd backend
python manage.py runserver 9000 &
BACKEND_PID=$!

# Wait a moment for the backend to start
sleep 3

# Start the Chainlit frontend
echo "Starting Chainlit frontend on port 8000..."
cd ../chainlit_app
chainlit run app.py --port 8000 &
FRONTEND_PID=$!

# Handle SIGINT (Ctrl+C) to gracefully shut down both servers
trap 'echo "Shutting down servers..."; kill $BACKEND_PID; kill $FRONTEND_PID; exit' SIGINT

echo "Both servers are running. Press Ctrl+C to stop."
wait
