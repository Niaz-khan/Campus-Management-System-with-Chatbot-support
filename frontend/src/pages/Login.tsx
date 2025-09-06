import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { GraduationCap, BookOpen, Users, Shield, Mail, Lock, Eye, EyeOff } from "lucide-react";

const Login: React.FC = () => {
  // Form state
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  // UI state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      // Send login request - Replace with your actual API call
     
      const response = await axios.post("http://127.0.0.1:8000/api/users/login/", {
        email,
        password,
      });

      // Extract tokens & user info
      const { access, refresh, user } = response.data;

      // Store in localStorage
      localStorage.setItem("accessToken", access);
      localStorage.setItem("refreshToken", refresh);
      localStorage.setItem("user", JSON.stringify(user));

      // Redirect to dashboard
      navigate("/dashboard");
      

      // Demo simulation
      await new Promise(resolve => setTimeout(resolve, 1500));
      // alert(`Login successful! Welcome to EduMax UMS`);
    } catch (err: any) {
      setError("Invalid credentials. Please try again.");
      // setError(err.response?.data?.detail || "Invalid credentials");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Educational Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-indigo-900 via-purple-900 to-blue-900 relative overflow-hidden">
        {/* Animated Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-10 left-10 w-32 h-32 bg-white rounded-full animate-pulse"></div>
          <div className="absolute top-40 right-20 w-24 h-24 bg-white rounded-full animate-pulse delay-1000"></div>
          <div className="absolute bottom-20 left-20 w-40 h-40 bg-white rounded-full animate-pulse delay-2000"></div>
          <div className="absolute top-1/2 right-10 w-20 h-20 bg-white rounded-full animate-pulse delay-500"></div>
          <div className="absolute bottom-40 right-1/3 w-28 h-28 bg-white rounded-full animate-pulse delay-1500"></div>
        </div>
        
        {/* Floating Educational Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-20 right-1/4 text-white opacity-20 animate-bounce">
            <BookOpen size={40} />
          </div>
          <div className="absolute bottom-1/3 left-1/4 text-yellow-400 opacity-30 animate-pulse">
            <Users size={36} />
          </div>
          <div className="absolute top-1/3 left-1/3 text-blue-300 opacity-25 animate-bounce delay-1000">
            <Shield size={32} />
          </div>
        </div>
        
        {/* Content */}
        <div className="relative z-10 flex flex-col justify-center items-start p-16 text-white">
          <div className="mb-8">
            <div className="flex items-center mb-6">
              <GraduationCap size={72} className="text-yellow-400 mr-4" />
              <div>
                <h1 className="text-6xl font-bold leading-none">
                  EduMax
                </h1>
                <div className="text-xl font-light text-indigo-200 mt-2">
                  University Management System
                </div>
              </div>
            </div>
          </div>
          
          <div className="space-y-6 mb-12">
            <div className="flex items-center space-x-4 group">
              <div className="p-3 bg-yellow-400 bg-opacity-20 rounded-full group-hover:bg-opacity-30 transition-all">
                <BookOpen className="text-yellow-400" size={24} />
              </div>
              <span className="text-lg font-medium">Comprehensive Academic Management</span>
            </div>
            <div className="flex items-center space-x-4 group">
              <div className="p-3 bg-blue-400 bg-opacity-20 rounded-full group-hover:bg-opacity-30 transition-all">
                <Users className="text-blue-400" size={24} />
              </div>
              <span className="text-lg font-medium">Student & Faculty Portal</span>
            </div>
            <div className="flex items-center space-x-4 group">
              <div className="p-3 bg-green-400 bg-opacity-20 rounded-full group-hover:bg-opacity-30 transition-all">
                <Shield className="text-green-400" size={24} />
              </div>
              <span className="text-lg font-medium">Secure & Reliable Platform</span>
            </div>
          </div>
          
          <div className="bg-white bg-opacity-10 p-6 rounded-2xl backdrop-blur-sm border border-white border-opacity-20">
            <p className="text-lg italic font-light leading-relaxed">
              "Education is the most powerful weapon which you can use to change the world."
            </p>
            <p className="text-indigo-200 mt-3 text-right font-medium">— Nelson Mandela</p>
          </div>
        </div>
      </div>

      {/* Right Side - Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50 p-8">
        <div className="w-full max-w-md">
          {/* Mobile Header */}
          <div className="lg:hidden text-center mb-10">
            <div className="flex justify-center items-center mb-4">
              <GraduationCap size={48} className="text-indigo-600 mr-3" />
              <div>
                <h1 className="text-3xl font-bold text-gray-800">EduMax</h1>
                <p className="text-gray-600 text-sm">University Management</p>
              </div>
            </div>
          </div>

          {/* Login Card */}
          <div className="bg-white p-10 rounded-3xl shadow-2xl border border-gray-100 backdrop-blur-sm">
            <div className="text-center mb-10">
              <h2 className="text-3xl font-bold text-gray-800 mb-3">Welcome Back!</h2>
              <p className="text-gray-600 text-lg">Sign in to access your academic portal</p>
            </div>

            {error && (
              <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 rounded-r-xl animate-pulse">
                <p className="text-red-700 font-medium">{error}</p>
              </div>
            )}

            <div className="space-y-6">
              {/* Email Field */}
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-3">
                  Email Address
                </label>
                <div className="relative group">
                  <Mail className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 group-focus-within:text-indigo-500 transition-colors" size={20} />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-12 pr-4 py-4 border-2 border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all duration-300 bg-gray-50 focus:bg-white hover:border-gray-300"
                    placeholder="your.email@university.edu"
                    required
                  />
                </div>
              </div>

              {/* Password Field */}
              <div>
                <label className="block text-sm font-bold text-gray-700 mb-3">
                  Password
                </label>
                <div className="relative group">
                  <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 group-focus-within:text-indigo-500 transition-colors" size={20} />
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-12 pr-12 py-4 border-2 border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-all duration-300 bg-gray-50 focus:bg-white hover:border-gray-300"
                    placeholder="••••••••••"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-indigo-500 transition-colors focus:outline-none"
                  >
                    {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                  </button>
                </div>
              </div>

              {/* Remember Me & Forgot Password */}
              <div className="flex items-center justify-between pt-2">
                <label className="flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded transition-colors"
                  />
                  <span className="ml-3 text-sm text-gray-700 font-medium">Remember me</span>
                </label>
                <button className="text-sm text-indigo-600 hover:text-indigo-500 font-semibold transition-colors focus:outline-none focus:underline">
                  Forgot password?
                </button>
              </div>

              {/* Submit Button */}
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-4 px-6 rounded-2xl font-bold text-lg hover:from-indigo-700 hover:to-purple-700 focus:outline-none focus:ring-4 focus:ring-indigo-300 transform transition-all duration-200 hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none shadow-lg hover:shadow-xl"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-6 w-6 border-2 border-white border-t-transparent mr-3"></div>
                    Signing In...
                  </div>
                ) : (
                  <div className="flex items-center justify-center">
                    <span>Sign In to Portal</span>
                    <div className="ml-2 transform group-hover:translate-x-1 transition-transform">→</div>
                  </div>
                )}
              </button>
            </div>

            {/* Additional Links */}
            <div className="mt-10 pt-8 border-t border-gray-200 text-center space-y-4">
              <div className="flex flex-col sm:flex-row justify-center items-center space-y-2 sm:space-y-0 sm:space-x-6">
                <button className="text-sm text-indigo-600 hover:text-indigo-500 font-semibold transition-colors focus:outline-none focus:underline">
                  New Student? Request Access
                </button>
                <button className="text-sm text-indigo-600 hover:text-indigo-500 font-semibold transition-colors focus:outline-none focus:underline">
                  Contact IT Support
                </button>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="mt-8 text-center text-sm text-gray-500 space-y-1">
            <p className="font-medium">© 2025 EduMax University Management System</p>
            <p className="italic">Empowering Education Through Technology</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;