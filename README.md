# Online Banking System

A comprehensive online banking application built with FastAPI backend, SQLite database, JWT authentication, and Streamlit frontend. This system allows customers to manage their accounts, perform transactions, and administrators to oversee operations.

## Features

### Customer Portal
- **User Registration & Authentication**: Secure registration and login with JWT tokens
- **Account Management**: View personal accounts
- **Transactions**:
  - Deposit money
  - Withdraw money
  - Transfer money between accounts
- **Account Closure**: Close accounts when needed

### Admin Portal
- **Account Overview**: Comprehensive view of all accounts with advanced filtering
- **Filtering Options**:
  - Filter by account status (active/closed)
  - Filter by customer ID
  - Filter by balance range
- **Sorting**: Sort accounts by creation date, balance, or ID
- **Data Visualization**: Bar chart for account balances
- **Secure Access**: Admin registration requires a secret code

### Technical Features
- **RESTful API**: Built with FastAPI for robust backend services
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT-based secure authentication
- **Frontend**: Interactive Streamlit web interface
- **CORS Support**: Cross-origin resource sharing enabled
- **Input Validation**: Email validation and data sanitization

## Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Database**: SQLite, SQLAlchemy
- **Authentication**: Python-JOSE for JWT
- **Frontend**: Streamlit
- **Validation**: Pydantic, Email-Validator
- **HTTP Client**: Requests

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd teamolympus
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements
   ```

3. **Database Setup**:
   The application uses SQLite, and the database file (`banking_app.db`) will be created automatically when the application runs for the first time.

4. **Seed Admin Users**:
   Default admin users are seeded automatically on startup. The admin secret code is `BRANCH-ADMIN-2026`.

## Running the Application

### Backend (FastAPI)
1. Navigate to the banking_app directory:
   ```bash
   cd banking_app
   ```

2. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`

3. API Documentation:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend (Streamlit)
1. From the project root directory:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the provided URL (usually `http://localhost:8501`)

## Usage

### Customer Workflow
1. **Register**: Create a new customer account with username, password, full name, email, and phone
2. **Login**: Authenticate using email and password
3. **Manage Accounts**:
   - View your accounts
   - Deposit money
   - Withdraw money
   - Transfer money between accounts
   - Close accounts

### Admin Workflow
1. **Register**: Register as admin using the secret code `BRANCH-ADMIN-2026`
2. **Login**: Authenticate as admin
3. **Monitor Accounts**: Use filters and sorting to view account information
4. **Analyze Data**: View balance charts for insights

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Customer
- `GET /customer/accounts` - List customer's accounts
- `POST /customer/deposit` - Deposit money
- `POST /customer/withdraw` - Withdraw money
- `POST /customer/transfer` - Transfer money
- `POST /customer/close` - Close account

### Admin
- `GET /admin/accounts` - List all accounts with filters

## Database Schema

The application uses the following main models:
- **User**: Base user information (username, password, role)
- **Customer**: Customer details (full name, email, phone)
- **Staff**: Staff/Admin details
- **Account**: Bank accounts (balance, status, customer_id)
- **Transaction**: Transaction records
- **ServiceRequest**: Service requests (not fully implemented)

## Security

- JWT tokens for authentication
- Password hashing using secure methods
- Admin registration requires secret code
- CORS configured for frontend-backend communication

## Development

### Project Structure
```
teamolympus/
├── app.py                          # Streamlit frontend
├── requirements                    # Python dependencies
├── banking_app.db                  # SQLite database (created on first run)
├── banking_app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application entry point
│   ├── config.py                   # Configuration settings
│   ├── database.py                 # Database connection and setup
│   ├── models/                     # SQLAlchemy models
│   │   ├── user.py
│   │   ├── customer.py
│   │   ├── staff.py
│   │   ├── account.py
│   │   ├── transaction.py
│   │   └── service_request.py
│   ├── routes/                     # API route handlers
│   │   ├── auth.py
│   │   ├── customer.py
│   │   ├── admin.py
│   │   └── staff.py
│   ├── schemas/                    # Pydantic schemas
│   ├── services/                   # Business logic services
│   └── utils/                      # Utility functions (hash, jwt)
```

### Adding New Features
1. Define models in `models/`
2. Create Pydantic schemas in `schemas/`
3. Implement business logic in `services/`
4. Add API routes in `routes/`
5. Update the Streamlit frontend in `app.py`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with FastAPI for the robust backend
- Streamlit for quick and interactive frontend development
- SQLAlchemy for database ORM
- Python-JOSE for JWT handling

## Support

For support, please contact the development team or create an issue in the repository.
