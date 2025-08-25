# 🏥 Public Health Management System (PHMS)

A modular, Django-based web application designed to serve as the foundational backend for a modern healthcare ecosystem. This project successfully implements the core models and authentication system for managing hospitals, clinics, doctors, and patients, providing a solid base for future development of advanced features like Electronic Health Records (EHR).

[![Django](https://img.shields.io/badge/Django-4.2.7-092E20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Status](https://img.shields.io/badge/Status-Core%20Complete%20%E2%80%93%20WIP%20Ready-brightgreen?style=for-the-badge)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

## 📖 Overview

PHMS is a robust and well-structured backend system built with Django. It lays the groundwork for a comprehensive healthcare management platform by solving the core data organization challenges. The system features a multi-role authentication system and expertly designed data models, making it an ideal starting point for developers, students, and organizations to build a fully-featured Healthcare IT solution.

**The Vision:** To evolve into a full-fledged system with EHR, patient portals, telemedicine, and data analytics, specifically designed to address the challenges and opportunities in healthcare management within regions like Pakistan.

---

## ⚙️ **What's Built & Stable (Core Foundation)**

### ✅ Completed & Functional
- **🔐 Secure Authentication System:** Role-based login for System Admins, Hospital Admins, and Doctors.
- **🗂️ Core Data Models:** Well-defined Django models for:
  - `Hospital` & `Clinic` management
  - `Doctor` profiles with specialization tracking
  - `Patient` registration and demographic data
  - `PatientRecord` for storing medical visit data (symptoms, diagnosis, prescription)
- **🏠 Admin Dashboard:** A powerful Django Admin interface for full data oversight and management.
- **🧱 Scalable Architecture:** A clean, modular codebase that follows Django best practices, making it easy to extend and maintain.

---

## 🚧 **Future Roadmap & Opportunities (Ideal for Contributors!)**

This project is purpose-built for growth. The solid foundation is complete; now it's time to build upon it. Here are the planned next phases:

### 🎯 Phase 1: Enhanced Features (Next Steps)
- **📊 Electronic Health Records (EHR) Dashboard:** A dedicated UI for doctors to view and manage patient medical histories.
- **📅 Appointment Scheduling System:** Functionality for patients to book and manage visits.
- **🔐 Advanced Permission Layers:** Fine-grained control over who can view and edit sensitive patient data.

### 🌟 Phase 2: Advanced Modules
- **🤖 Telemedicine Integration:** Live video consultation capabilities using WebRTC.
- **📱 RESTful API:** A full API using Django REST Framework (DRF) for mobile app development.
- **📈 Data Analytics Dashboard:** Visual insights into hospital performance, patient demographics, and common diagnoses.
- **🌐 Patient Portal:** A secure frontend for patients to view their own history and reports.

### 🧠 Phase 3: AI & Innovation
- **💡 Clinical Decision Support System (CDSS):** Basic alerts for drug interactions based on patient history.
- **🗣️ Multi-language Support (Urdu):** UI localization to improve accessibility.

---

## 🛠️ **Technology Stack**

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | Django 4.2.7 |
| **Frontend (Current)** | HTML5, Bootstrap 5, Django Templates |
| **Database** | SQLite (Development) / PostgreSQL (Production-ready) |
| **Authentication** | Django's built-in auth system |
| **Deployment** | Docker-ready, can be deployed on Heroku, AWS, or any VPS. |

---

## 🚀 **Getting Started**

Follow these steps to set up a development environment and explore the core functionality.

### Prerequisites
- Python 3.10+
- pip

### Installation & Setup
1.  **Clone the repository**
    ```bash
    git clone https://github.com/usman-razzaq/public-health-management-system.git
    cd public-health-management-system
    ```

2.  **Create and activate a virtual environment**
    ```bash
    # On Windows
    python -m venv venv
    .\venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser account to access the admin panel**
    ```bash
    python manage.py createsuperuser
    # Follow the prompts to create an admin account.
    ```

6.  **Run the development server**
    ```bash
    python manage.py runserver
    ```

7.  **Explore the application:**
    - **Admin Interface:** Navigate to `http://127.0.0.1:8000/admin` and log in with your superuser credentials. Here you can manage all data.
    - **Main Site:** The base URL `http://127.0.0.1:8000` will show the main site structure.

---

## 🤝 **Contributing**

This project is a living codebase and contributions are highly welcome! It's a perfect opportunity for developers to contribute to a meaningful project and gain experience with Django and healthcare IT.

We are looking for help with all items on the [Roadmap](#-future-roadmap--opportunities-ideal-for-contributors).

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

Please read our `CONTRIBUTING.md` (to be created) for detailed guidelines.

---

## 📜 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. This means you are free to use, modify, and distribute the code for any purpose.

---

## 📞 **Contact & Connect**

**Usman Razzaq** - [@usmanxrazzaq](https://twitter.com/usmanxrazzaq) - usmanrazzaq114@gmail.com

**Project Link:** [https://github.com/usman-razzaq/public-health-management-system](https://github.com/usman-razzaq/public-health-management-system)

- **LinkedIn:** [https://linkedin.com/in/usmanrazzaq]

---

## 🙏 **Acknowledgments**

* Django for the incredible framework.
* The open-source community for endless learning resources.
* This project was initially developed as a Final Year Project for a Computer Science degree.