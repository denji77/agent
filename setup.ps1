# Multi-Agent Debate System - Setup Script
# Run this script to set up your environment

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Multi-Agent Debate System - Setup Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found. Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}

Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists" -ForegroundColor Gray
} else {
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
}

Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green

Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray
pip install -r requirements.txt --quiet
Write-Host "  ✓ Dependencies installed" -ForegroundColor Green

Write-Host ""

# Check for .env file
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host "  Creating .env file from template..." -ForegroundColor Gray
    Copy-Item ".env.example" ".env"
    Write-Host "  ⚠ Please edit .env and add your OpenAI API key" -ForegroundColor Yellow
}

Write-Host ""

# Create logs directory
Write-Host "Creating logs directory..." -ForegroundColor Yellow
if (Test-Path "logs") {
    Write-Host "  Logs directory already exists" -ForegroundColor Gray
} else {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "  ✓ Logs directory created" -ForegroundColor Green
}

Write-Host ""

# Run tests
Write-Host "Running system tests..." -ForegroundColor Yellow
python test_system.py

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Edit .env and add your OpenAI API key" -ForegroundColor White
Write-Host "  2. Run: python main.py" -ForegroundColor White
Write-Host ""
Write-Host "For more information, see README.md" -ForegroundColor Gray
Write-Host ""
