import React from "react";

const Dashboard: React.FC = () => {
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  return (
    <div className="min-h-screen bg-neutral p-6">
      <h1 className="text-3xl font-heading font-bold mb-4">
        Welcome, {user.first_name || "Guest"}!
      </h1>
      <p className="text-lg">
        You are logged in as <span className="font-semibold">{user.role}</span>.
      </p>
    </div>
  );
};

export default Dashboard;
