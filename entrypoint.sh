#!/bin/bash
set -e

echo "==================================="
echo "Document AI API - Starting..."
echo "==================================="

# Function to wait for PostgreSQL
wait_for_postgres() {
    echo "Waiting for PostgreSQL to be ready..."
    while ! pg_isready -h postgres -U user > /dev/null 2>&1; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 1
    done
    echo "PostgreSQL is up and running!"
}

# Function to run migrations
run_migrations() {
    echo "Running Alembic migrations..."
    alembic upgrade head
    if [ $? -eq 0 ]; then
        echo "Migrations completed successfully!"
    else
        echo "ERROR: Migrations failed!"
        exit 1
    fi
}

# Function to create admin user
create_admin_user() {
    echo "Checking/creating admin user..."
    python setup_db.py
    if [ $? -eq 0 ]; then
        echo "Admin user setup completed!"
    else
        echo "WARNING: Admin user setup failed, but continuing..."
    fi
}

# Main execution
echo ""
echo "Step 1: Waiting for PostgreSQL..."
wait_for_postgres

echo ""
echo "Step 2: Running database migrations..."
run_migrations

echo ""
echo "Step 3: Setting up admin user..."
create_admin_user

echo ""
echo "==================================="
echo "Starting FastAPI application..."
echo "==================================="
echo ""

# Start the application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
