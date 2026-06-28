import React from "react";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import ReactDOM from "react-dom/client";
import "./index.css";
import { TopicPage, RoadmapPage, QuizPage, ProfilePage } from "./pages/index";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import Landing from "./logins/Landing";
import UserLogin from "./logins/UserLogin";
import RegisterUser from "./logins/RegisterUser";
import AdminLogin from "./logins/AdminLogin";
import AdminDashboard from "./logins/admin-dashboard/AdminDashboard";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Landing />,
  },
  {
    path: "/test",
    element: <App></App>,
  },
  {
    path: "/roadmap/",
    element: <RoadmapPage />,
  },
  {
    path: "/quiz/",
    element: <QuizPage />,
  },
  {
    path: "/topic/",
    element: <TopicPage />,
  },
  {
    path: "/login",
    element: <UserLogin />,
  },
  {
    path: "/register",
    element: <RegisterUser />,
  },
  {
    path: "/admin-login",
    element: <AdminLogin />,
  },
  {
    path: "/profile",
    element: <ProfilePage />, // profile.js
  },
  {
    path: "/admin",
    element: <AdminDashboard />,
  },
]);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();