import "../styles/sign_up.css";

import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { FaGoogle, FaGithub } from "react-icons/fa";
import {
    FiUser,
    FiMail,
    FiLock,
    FiEye,
    FiEyeOff,
    FiArrowRight,
} from "react-icons/fi";

const SignupPage = () => {

    const navigate = useNavigate();

    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [loading, setLoading] = useState(false);

    const handleSignup = async (
        e: React.FormEvent<HTMLFormElement>
    ) => {

        e.preventDefault();

        if (
            username.trim() === "" ||
            email.trim() === "" ||
            password.trim() === "" ||
            confirmPassword.trim() === ""
        ) {
            alert("Please fill all fields.");
            return;
        }

        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        try {

            setLoading(true);

            const response = await fetch(
                "http://127.0.0.1:8000/auth/register",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        username,
                        email,
                        password,
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok) {
                alert(data.detail || "Registration failed.");
                return;
            }

            alert("Account created successfully.");

            navigate("/login");

        } catch (error) {

            console.error(error);

            alert("Unable to connect to server.");

        } finally {

            setLoading(false);

        }

    };

    return (

        <div className="signup-page">

            <div className="signup-left">

                <div className="brand">

                    <img
                        src="/logo.svg"
                        alt="Logo"
                        className="logo"
                    />

                    <h1>AI Assistant</h1>

                    <p>
                        Create your account and unlock
                        intelligent conversations,
                        coding assistance,
                        document analysis,
                        and AI-powered productivity.
                    </p>

                </div>

            </div>

            <div className="signup-right">

                <div className="signup-card">

                    <h2>Create Account</h2>

                    <p className="subtitle">
                        Join your AI workspace.
                    </p>

                    <form onSubmit={handleSignup}>

                        {/* Username */}

                        <div className="input-group">

                            <label>Username</label>

                            <div className="input-box">

                                <FiUser className="input-icon"/>

                                <input
                                    type="text"
                                    placeholder="Enter username"
                                    value={username}
                                    onChange={(e)=>setUsername(e.target.value)}
                                />

                            </div>

                        </div>

                        {/* Email */}

                        <div className="input-group">

                            <label>Email</label>

                            <div className="input-box">

                                <FiMail className="input-icon"/>

                                <input
                                    type="email"
                                    placeholder="Enter email"
                                    value={email}
                                    onChange={(e)=>setEmail(e.target.value)}
                                />

                            </div>

                        </div>

                        {/* Password */}

                        <div className="input-group">

                            <label>Password</label>

                            <div className="input-box">

                                <FiLock className="input-icon"/>

                                <input
                                    type={
                                        showPassword
                                            ? "text"
                                            : "password"
                                    }
                                    placeholder="Enter password"
                                    value={password}
                                    onChange={(e)=>setPassword(e.target.value)}
                                />

                                <button
                                    type="button"
                                    className="eye-btn"
                                    onClick={()=>
                                        setShowPassword(!showPassword)
                                    }
                                >

                                    {
                                        showPassword
                                            ? <FiEyeOff/>
                                            : <FiEye/>
                                    }

                                </button>

                            </div>

                        </div>

                        {/* Confirm Password */}

                        <div className="input-group">

                            <label>
                                Confirm Password
                            </label>

                            <div className="input-box">

                                <FiLock className="input-icon"/>

                                <input
                                    type={
                                        showConfirmPassword
                                            ? "text"
                                            : "password"
                                    }
                                    placeholder="Confirm password"
                                    value={confirmPassword}
                                    onChange={(e)=>
                                        setConfirmPassword(e.target.value)
                                    }
                                />

                                <button
                                    type="button"
                                    className="eye-btn"
                                    onClick={()=>
                                        setShowConfirmPassword(
                                            !showConfirmPassword
                                        )
                                    }
                                >

                                    {
                                        showConfirmPassword
                                            ? <FiEyeOff/>
                                            : <FiEye/>
                                    }

                                </button>

                            </div>

                        </div>

                        <button
                            className="signup-btn"
                            type="submit"
                            disabled={loading}
                        >

                            {
                                loading
                                    ? "Creating..."
                                    : "Create Account"
                            }

                            <FiArrowRight/>

                        </button>

                    </form>

                    <div className="divider">

                        <span>OR</span>

                    </div>

                    <div className="social-buttons">

                        <button className="social-btn">

                            <FaGoogle/>

                            Google

                        </button>

                        <button className="social-btn">

                            <FaGithub/>

                            GitHub

                        </button>

                    </div>

                    <p className="footer-text">

                        Already have an account?

                        <span
                            onClick={() => navigate("/login")}
                        >
                            Login
                        </span>

                    </p>

                </div>

            </div>

        </div>

    );

};

export default SignupPage;