import "../styles/sign_in.css";

import { FaGoogle, FaGithub } from "react-icons/fa";
import { FiMail, FiArrowRight } from "react-icons/fi";

import { useNavigate } from "react-router-dom";

const SignInPage = () => {

    const navigate = useNavigate();

    return (

        <div className="signin-page">

            <div className="signin-card">

                {/* Logo */}

                <img
                    src="/logo.svg"
                    alt="Logo"
                    className="signin-logo"
                />

                {/* Heading */}

                <h1>AI Assistant</h1>

                <p className="subtitle">
                    Your intelligent workspace for coding, chatting,
                    document analysis and automation.
                </p>

                {/* Illustration */}

                <div className="hero">

                    <img
                        src="/ai-illustration.svg"
                        alt="AI"
                    />

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

                    <button className="social-btn">

                        <FaGoogle />

                        Continue with Google

                    </button>

                    <button className="social-btn">

                        <FaGithub />

                        Continue with GitHub

                    </button>

                    <p className="signup-text">

                        Don't have an account?

                        <span
                            onClick={() => navigate("/signup")}
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