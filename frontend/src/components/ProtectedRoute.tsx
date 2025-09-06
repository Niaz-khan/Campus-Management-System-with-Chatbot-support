import React from "react";
import { Navigate } from "react-router-dom";

// Props definition: the component accepts child components to protect
interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  // Retrieve access token from localStorage (saved after login)
  const accessToken = localStorage.getItem("accessToken");

  // If no token found, redirect user to the login page
  if (!accessToken) {
    return <Navigate to="/login" replace />;
  }

  // If token exists, allow access to the protected page
  return <>{children}</>;
};

export default ProtectedRoute;
