import "../styles/login_page.css";
import { FcGoogle } from "react-icons/fc";
import { FaGithub } from "react-icons/fa";
import { FiMail, FiLock, FiEye, FiArrowRight , FiEyeOff } from "react-icons/fi";
import { useNavigate } from "react-router-dom";
import type { LoginFormData } from "../types/login_schema";
import { useState } from "react";

const LoginPage = () => {

  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onSubmit = async (data: LoginFormData) => {
    try {
        const response = await fetch("http://127.0.0.1:8000/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error("Invalid email or password");
        }

        const result = await response.json();

        localStorage.setItem(
            "access_token",
            result.access_token
        );

        navigate("/chat");

    } catch (error) {
        alert("Invalid email or password");
    }
};
  
  return (
    <div className="login-page">
      {/* Left Side */}
      <div className="login-left">
        <div className="brand">
          <img src="/logo.svg" alt="Logo" className="logo" />

          <h1>AI Assistant</h1>

          <p>
            Chat smarter with your own AI-powered assistant. Secure, fast,
            and always ready to help.
          </p>
        </div>
      </div>

      {/* Right Side */}

      <div className="login-right">
        <div className="login-card">

          <h2>Welcome Back 👋</h2>

          <p className="subtitle">
            Sign in to continue to your workspace.
          </p>

          <form onSubmit={(e) => {
            e.preventDefault();
            onSubmit({
              email: "",
              password: ""
            });
          }}>

            {/* Email */}

            <div className="input-group">
              <label>Email</label>

              <div className="input-box">
                <FiMail className="input-icon" />

                <input
                  type="email"
                  placeholder="Enter your email"
                />
              </div>
            </div>

            {/* Password */}

            <div className="input-group">
              <label>Password</label>

              <div className="input-box">
                <FiLock className="input-icon" />

                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                />

                <button
      type="button"
      className="eye-btn"
      onClick={() => setShowPassword(!showPassword)}
  >
      {showPassword ? <FiEyeOff /> : <FiEye />}
  </button>
                </div>
            </div>

            {/* Options */}

            <div className="options">

              <label className="remember">

                <input type="checkbox" />

                Remember me

              </label>

              <a href="#">Forgot Password?</a>

            </div>

            {/* Login Button */}

            <button className="login-btn">

              Sign In

              <FiArrowRight />

            </button>

          </form>

          {/* Divider */}

          <div className="divider">

            <span>OR</span>

          </div>

          {/* Social Login */}

          <div className="social-buttons">

            <button className="social-btn">
              <FcGoogle size={24} />
              <span>Google</span>
            </button>

            <button className="social-btn">
              <FaGithub size={22} color="#181717" />
              <span>GitHub</span>
            </button>

          </div>

          {/* Footer */}

          <p className="footer-text">

            Don't have an account?

            <a href="/register"> Sign Up</a>

          </p>

        </div>
      </div>
    </div>
  );
};

export default LoginPage;