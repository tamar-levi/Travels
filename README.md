# 🌍 TravelMate – Smart Travel Management Platform

> 🚧 *The site is currently under development – thank you for your patience!* 👌

---

## ✨ Overview

**TravelMate** is an intelligent **travel planning and brokerage platform** that offers users a seamless way to design, manage, and optimize their journeys. Built with cutting-edge technologies like **React** and **Node.js**, it connects directly with **Google Maps** to deliver accurate, real-time routing that integrates public transport, private trips, and custom itineraries — all in one place.

---

## 🧭 Key Features

✅ **Interactive Map Integration** – Built on Google Maps API for live, location-aware routing and visualization.
✅ **Smart Route Planner** – Combine public transportation and internal trip segments effortlessly.
✅ **User & Trip Management** – Full-featured dashboard for managing profiles, saved trips, history, and preferences.
✅ **Broker Mode** – Allow travel brokers to manage routes and recommend travel packages.
✅ **Responsive & Mobile-Friendly UI** – Optimized for devices of all sizes using modern React design principles.
✅ **Authentication & Security** – Secure login and role-based access powered by Node.js + Express.

## 🛠️ Tech Stack

* **Frontend**: React, Tailwind CSS, Axios, Google Maps API
* **Backend**: Node.js, Express.js, MongoDB
* **Authentication**: JWT-based login & role management
* **Deployment**: (Optional) Vercel/Netlify for frontend, Render/Heroku for backend

## 🚀 Getting Started

To run this project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/TravelMate.git
cd TravelMate
```

### 2. Setup the Backend

```bash
cd server
npm install
npm run dev
```

### 3. Setup the Frontend

```bash
cd client
npm install
npm start
```

> Make sure to configure your `.env` files for both frontend and backend (e.g., Google Maps API key, MongoDB URI, JWT secrets).

## 📸 Preview

![Home Page](./docs/home_preview.png)
![Trip Planner](./docs/route_planner.png)

## 🎯 Use Cases

* Plan custom trips using public transportation & walking paths
* Save favorite routes & travel preferences
* Manage bookings through the broker dashboard
* Explore optimized, eco-friendly travel routes

## 📦 Project Structure

```bash
📦 TravelMate
├── client (React frontend)
│   ├── src
│   └── ...
├── server (Node backend)
│   ├── routes
│   ├── controllers
│   └── ...
├── docs (images + planning)
├── .env.example
└── README.md
```

## 🔒 Security Notes

* All user data is encrypted and securely stored
* Routes are protected using JWT authentication middleware

## 🧱 Roadmap

* [x] User login, registration, and role handling
* [x] Google Maps integration with live routing
* [ ] Admin analytics dashboard (Coming Soon!)
* [ ] AI-based travel recommendations (Planned)

## 🤝 Contributing

We welcome feedback, suggestions, and pull requests. To contribute:

1. Fork the repo
2. Create your branch (`git checkout -b feature/yourFeature`)
3. Commit and push your changes
4. Open a pull request and describe your changes

## 📜 License

This project is licensed under the MIT License.

---

### ✨ Built with vision, passion, and code.
