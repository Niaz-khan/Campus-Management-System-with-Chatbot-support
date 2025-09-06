// Import React hook and axios for API calls
import { useState } from "react";
import axios from "axios";

// The Register component
export default function Register() {
  // useState for form fields (email, first name, etc.)
  const [form, setForm] = useState({
    email: "",
    first_name: "",
    last_name: "",
    password: "",
    role: "STUDENT" // default role
  });

  const [message, setMessage] = useState(""); // Store success or error message

  // Handles input field changes for all form fields
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    // [e.target.name] dynamically updates the correct field (email, password, etc.)
  };

  // Handles the registration form submission
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevents page reload
    try {
      // Send POST request to Django register API
      const response = await axios.post("http://127.0.0.1:8000/api/users/register/", form);

      // If success, show message
      setMessage("User registered successfully!");
      console.log(response.data); // For debugging

    } catch (err: any) {
      // Show error message from backend or fallback
      setMessage(err.response?.data?.detail || "Registration failed");
    }
  };

  return (
    <div>
      <h1>Register</h1>

      {/* Show message (success or error) */}
      {message && <p>{message}</p>}

      {/* Registration form */}
      <form onSubmit={handleRegister}>
        <input name="email" type="email" placeholder="Email" onChange={handleChange} required />
        <br />

        <input name="first_name" type="text" placeholder="First Name" onChange={handleChange} />
        <br />

        <input name="last_name" type="text" placeholder="Last Name" onChange={handleChange} />
        <br />

        <input name="password" type="password" placeholder="Password" onChange={handleChange} required />
        <br />

        <input name="role" type="text" placeholder="Role" onChange={handleChange} />
        <br />

        <button type="submit">Register</button>
      </form>
    </div>
  );
}
