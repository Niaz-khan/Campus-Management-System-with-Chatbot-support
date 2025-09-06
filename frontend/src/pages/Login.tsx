// Importing React hooks and axios for API requests
import { useState } from "react";
import axios from "axios";

// The Login component (function component)
export default function Login() {
  // useState creates state variables: these store input values and errors
  const [email, setEmail] = useState("");        // Stores the email input
  const [password, setPassword] = useState("");  // Stores the password input
  const [error, setError] = useState("");        // Stores any login error message

  // Function that runs when the user submits the login form
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevents page refresh when form is submitted

    try {
      // Sending POST request to your Django login API
      const response = await axios.post("http://127.0.0.1:8000/api/users/login/", {
        email,      // sending email from state
        password    // sending password from state
      });

      // Extracting data from API response
      const { access, refresh, user } = response.data;

      // Storing JWT tokens and user info in localStorage (browser storage)
      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);
      localStorage.setItem("user", JSON.stringify(user)); // save user object as JSON string

      // For now, just show a welcome message (later we will redirect)
      alert(`Welcome ${user.first_name}!`);

    } catch (err: any) {
      // If login fails, set error message from backend or a default one
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  // JSX = the UI of this page
  return (
    <div>
      <h1>Login</h1>

      {/* Show error message if exists */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Login form */}
      <form onSubmit={handleLogin}>
        {/* Email input field */}
        <input
          type="email"
          placeholder="Email"
          value={email}                        // connects input value to state
          onChange={(e) => setEmail(e.target.value)} // updates state when user types
          required
        />
        <br />

        {/* Password input field */}
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <br />

        {/* Submit button */}
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
