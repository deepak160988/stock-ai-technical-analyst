#!/bin/bash

# Start the backend API on port 8000
npm run start:backend & 

# Start the frontend on port 3000
npm run start:frontend & 

# Wait for all background jobs to finish
wait