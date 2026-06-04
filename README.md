# 🏠 Real Estate Backend API

A comprehensive, production-ready REST API backend for a real estate platform, built with **Django 5.1** and **Django REST Framework**. This project provides a robust foundation for managing property listings, agent profiles, user authentication, and customer inquiries — everything needed to power a modern real estate marketplace.

## 🚀 About The Project

The Real Estate Backend API is designed to serve as the backbone for any real estate application, whether it's a web platform, mobile app, or a combination of both. It follows industry best practices in API design, security, and data modeling to deliver a scalable and maintainable solution.

At its core, the system revolves around four key modules. The **Accounts** module handles user registration, login, logout, and profile management using token-based authentication, ensuring secure access across all endpoints. The **Properties** module is the heart of the platform, offering full CRUD operations on property listings with support for multiple property types including houses, apartments, condos, land, and commercial spaces. It features advanced filtering capabilities, allowing users to search by price range, number of bedrooms, area, city, property type, and listing type (sale or rent). Each property can have multiple images with primary image designation.

The **Agents** module manages real estate agent profiles linked to user accounts, tracking license numbers, agency affiliations, years of experience, and specializations. Agents can be verified by administrators and are the only users authorized to create and manage property listings. The **Inquiries** module enables potential buyers or renters to send inquiries about specific properties, with a status workflow that tracks each inquiry from new to responded to closed.

The API implements role-based access control, ensuring that agents can only modify their own listings while buyers can browse freely and submit inquiries. Built-in pagination, search functionality, and ordering make it effortless to handle large datasets. The project uses SQLite for development simplicity but can easily be configured for PostgreSQL or MySQL in production environments.

## 🛠️ Tech Stack

- **Framework:** Django 5.1
- **API:** Django REST Framework 3.15
- **Authentication:** Token-based Authentication
- **Filtering:** django-filter
- **CORS:** django-cors-headers
- **Image Handling:** Pillow
- **Database:** SQLite (development) / PostgreSQL (production-ready)

## 📦 Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd real-estates

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/accounts/register/` | User registration |
| POST | `/api/v1/accounts/login/` | Login (returns token) |
| POST | `/api/v1/accounts/logout/` | Logout (invalidate token) |
| GET/PUT | `/api/v1/accounts/profile/` | View/update profile |

### Properties
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/properties/` | List properties (with filters) |
| POST | `/api/v1/properties/` | Create property (agents only) |
| GET | `/api/v1/properties/{id}/` | Property details |
| PUT/PATCH | `/api/v1/properties/{id}/` | Update property |
| DELETE | `/api/v1/properties/{id}/` | Delete property |
| GET | `/api/v1/properties/featured/` | Featured listings |
| POST | `/api/v1/properties/{id}/images/` | Upload images |

### Agents
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/agents/` | List all agents |
| POST | `/api/v1/agents/` | Create agent profile |
| GET | `/api/v1/agents/{id}/` | Agent details |
| GET | `/api/v1/agents/{id}/properties/` | Agent's listings |
| GET | `/api/v1/agents/top-agents/` | Top verified agents |

### Inquiries
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/inquiries/` | Send an inquiry |
| GET | `/api/v1/inquiries/` | List inquiries |
| PATCH | `/api/v1/inquiries/{id}/` | Update inquiry status |

## 🔍 Property Filters

Filter properties using query parameters:

```
/api/v1/properties/?property_type=apartment&listing_type=rent&city=Mumbai
/api/v1/properties/?price_min=500000&price_max=2000000&bedrooms_min=2
/api/v1/properties/?search=luxury&ordering=-price
```

## 🔑 Authentication

Use token-based authentication by including the token in request headers:

```
Authorization: Token your-auth-token-here
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
