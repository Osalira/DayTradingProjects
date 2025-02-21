# DayTradingProjects

This project serves as the main repository for the Day Trading system project, which is composed of several microservices organized as Git submodules.

## Repository Structure

The project includes the following submodules:

- **backend/api-gateway** – API Gateway for routing requests
- **backend/auth-service** – Authentication service
- **backend/logging-service** – Logging and monitoring service
- **backend/matching-engine** – Order matching engine
- **backend/trading-service** – Trading service
- **frontend-monolith** – Frontend application

## Cloning the Repository

To clone the repository along with all submodules, run:

```bash
git clone --recurse-submodules https://github.com/Osalira/DayTradingProjects.git
