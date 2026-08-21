import "../styles/sign_in.css";

import { FaGoogle, FaGithub, FaRobot } from "react-icons/fa";
import { FiMail, FiArrowRight } from "react-icons/fi";

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const getIndianGreeting = () => {
    const hour = Number(new Intl.DateTimeFormat("en-IN", {
        hour: "numeric",
        hour12: false,
        timeZone: "Asia/Kolkata",
    }).format(new Date()));

    if (hour < 12) return "Good morning";
    if (hour < 17) return "Good afternoon";
    if (hour < 21) return "Good evening";
    return "Good night";
};

const SignInPage = () => {

    const navigate = useNavigate();
    const [greeting, setGreeting] = useState(getIndianGreeting);
    const apiUrl = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

    useEffect(() => {
        const timer = window.setInterval(() => setGreeting(getIndianGreeting()), 60_000);
        return () => window.clearInterval(timer);
    }, []);

    return (

        <div className="signin-page">

            <div className="ambient-orb orb-one" />
            <div className="ambient-orb orb-two" />
            <div className="stars" />

            <div className="signin-card">

                <div className="auth-status">
                    <span /> {greeting} · India
                </div>

                {/* Logo */}

                <div className="signin-logo" aria-label="AI Assistant logo">
                    <FaRobot />
                </div>

                {/* Heading */}

                <h1>AI Assistant<span>.</span></h1>

                <p className="subtitle">
                    Your intelligent workspace for coding, chatting,
                    document analysis and automation.
                </p>

                {/* Illustration */}

                <div className="hero">

                    <div className="hero-avatar" aria-label="AI assistant">
                        <FaRobot />
                    </div>

                </div>

                {/* Features */}

                <div className="features">

                    <div className="feature-card">
                        🤖 AI Chat
                    </div>

                    <div className="feature-card">
                        💻 Coding Assistant
                    </div>

                    <div className="feature-card">
                        📄 Document Analysis
                    </div>

                    <div className="feature-card">
                        🎤 Voice Assistant
                    </div>

                </div>

                {/* Bottom Buttons */}

                <div className="bottom-buttons">

                    <button
                        className="primary-btn"
                        onClick={() => navigate("/login")}
                    >

                        <FiMail />

                        Continue with Email

                        <FiArrowRight />

                    </button>

                    <a className="social-btn" href={`${apiUrl}/auth/google`}>

                        <FaGoogle className="google-logo" />

                        Continue with Google

                    </a>

                    <a className="social-btn" href={`${apiUrl}/auth/github`}>

                        <FaGithub className="github-logo" />

                        Continue with GitHub

                    </a>

                    <p className="signup-text">

                        Don't have an account?

                        <span
                            onClick={() => navigate("/sign_up")}
                        >
                            Create Account
                        </span>

                    </p>

                </div>

            </div>

        </div>

    );

};

export default SignInPage;