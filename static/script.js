//const API_BASE = "https://air-quality-api-251707603195.asia-south1.run.app";
const API_BASE = "http://127.0.0.1:8000"; 
console.log("JS loaded ✅");

// ---------------------------
// DOM Elements
// ---------------------------
const input = document.getElementById("imageInput");
const previewDiv = document.getElementById("preview");
const resultsDiv = document.getElementById("results");
const loginContainer = document.getElementById("loginContainer");
const registerContainer = document.getElementById("registerContainer");
const predictionContainer = document.getElementById("predictionContainer");
const registerMsg = document.getElementById("registerMsg");
const forgotContainer = document.getElementById("forgotContainer");
const forgotMsg = document.getElementById("forgotMsg");
const locationMsg = document.getElementById("locationMsg");
let userLocation = null;

// ---------------------------
// Helper functions: show/hide sections
// ---------------------------
function showPredictionSection() {
    loginContainer.style.display = "none";
    registerContainer.style.display = "none";
    predictionContainer.style.display = "block";
    requestLocation();
}

function showRegister() {
    loginContainer.style.display = "none";
    registerContainer.style.display = "block";
    predictionContainer.style.display = "none";
    document.getElementById("otpSection").style.display = "none"; // hide OTP input
}

function showForgotPassword() {
    loginContainer.style.display = "none";
    registerContainer.style.display = "none";
    predictionContainer.style.display = "none";
    forgotContainer.style.display = "block";
}

function showLogin() {
    loginContainer.style.display = "block";
    registerContainer.style.display = "none";
    predictionContainer.style.display = "none";
    forgotContainer.style.display = "none";
}

// ---------------------------
// Login
// ---------------------------
window.loginUser = async function () {
    const identifier = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const loginMsg = document.getElementById("loginMsg");

    if (!identifier || !password) {
        loginMsg.textContent = "Please enter email/username and password";
        return;
    }

    const formData = new URLSearchParams();
    formData.append("username", identifier);  // MUST be username
    formData.append("password", password);

    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        if (!response.ok) throw new Error("Invalid credentials");

        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        loginMsg.textContent = "✅ Login successful!";
        showPredictionSection();
    } catch (error) {
        loginMsg.textContent = "❌ " + error.message;
    }
};


// ---------------------------
// Registration with OTP
// ---------------------------

// Step 1: Send OTP
window.sendOtp = async function () {
    const username = document.getElementById("regUsername").value.trim();
    const password = document.getElementById("regPassword").value.trim();
    const email = document.getElementById("regEmail").value.trim();

    if (!username || !password || !email) {
        registerMsg.textContent = "Please fill in all fields";
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/register/send-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password, email })
        });

        const data = await response.json();
        if (data.message) {
            registerMsg.textContent = "✅ OTP sent to your email. Check inbox!";
            document.getElementById("otpSection").style.display = "block";
        }
    } catch (error) {
        console.error(error);
        registerMsg.textContent = "❌ Could not send OTP. Is backend running?";
    }
};

// Step 2: Verify OTP
window.verifyOtp = async function () {
    const email = document.getElementById("regEmail").value.trim();
    const otp = document.getElementById("regOtp").value.trim();

    if (!otp) {
        registerMsg.textContent = "Please enter OTP";
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/register/verify-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, otp })
        });

        const data = await response.json();
        if (data.success) {
            registerMsg.textContent = "✅ Registration complete! You can now login.";
            document.getElementById("otpSection").style.display = "none";
            document.getElementById("regOtp").value = "";
        } else {
            registerMsg.textContent = "❌ " + (data.message || "OTP verification failed");
        }
    } catch (error) {
        console.error(error);
        registerMsg.textContent = "❌ Could not verify OTP";
    }
};

window.sendResetOtp = async function () {
    const email = document.getElementById("forgotEmail").value.trim();

    if (!email) {
        forgotMsg.textContent = "Please enter your email";
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/forgot-password/send-otp`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (data.success) {
            forgotMsg.textContent = "✅ OTP sent to your email.";
            document.getElementById("resetOtpSection").style.display = "block";
        } else {
            forgotMsg.textContent = "❌ " + (data.message || "Error sending OTP");
        }
    } catch (error) {
        console.error(error);
        forgotMsg.textContent = "❌ Could not send OTP.";
    }
};

window.verifyResetOtp = async function () {
    const email = document.getElementById("forgotEmail").value.trim();
    const otp = document.getElementById("resetOtp").value.trim();
    const new_password = document.getElementById("newPassword").value.trim();

    if (!otp || !new_password) {
        forgotMsg.textContent = "Please enter OTP and new password";
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/forgot-password/reset`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, otp, new_password })
        });

        const data = await response.json();

        if (data.success) {
            forgotMsg.textContent = "✅ Password reset successful. You can now login.";
            document.getElementById("resetOtpSection").style.display = "none";
        } else {
            forgotMsg.textContent = "❌ " + (data.message || "Reset failed");
        }
    } catch (error) {
        console.error(error);
        forgotMsg.textContent = "❌ Could not reset password.";
    }
};

window.requestLocation = async function () {
    if (!navigator.geolocation) {
        locationMsg.textContent = "Geolocation not supported.";
        return;
    }

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            userLocation = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude
            };

            locationMsg.textContent = "✅ Location access granted.";
            localStorage.setItem("user_location", JSON.stringify(userLocation));

            // 🔹 Send to backend
            await fetch(`${API_BASE}/forgot-password/send-otp`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(userLocation)
            });
        },
        (error) => {
            locationMsg.textContent = "❌ Location permission denied.";
        }
    );
};


// ---------------------------
// Image picker & preview
// ---------------------------
window.selectImage = function () {
    input.click();
};

input.addEventListener("change", function () {
    const file = input.files[0];
    if (!file) return;

    previewDiv.style.display = "block";
    resultsDiv.style.display = "none";

    previewDiv.innerHTML = `<img src="${URL.createObjectURL(file)}" style="max-width:300px; margin-top:10px;">`;
});

// ---------------------------
// Upload image for prediction
// ---------------------------
window.uploadImage = async function () {
    const file = input.files[0];
    if (!file) {
        alert("Please upload an image first.");
        return;
    }

    const token = localStorage.getItem("token");
    if (!token) {
        alert("You must login first.");
        showLogin();
        return;
    }

    resultsDiv.style.display = "block";
    resultsDiv.innerHTML = "⏳ Predicting... Please wait.";

    const formData = new FormData();
    formData.append("file", file);
    const storedLocation = JSON.parse(localStorage.getItem("user_location"));
    if (storedLocation) {
        formData.append("latitude", storedLocation.latitude);
        formData.append("longitude", storedLocation.longitude);
    }
    try {
        const response = await fetch(`${API_BASE}/predict`, {
            method: "POST",
            body: formData,
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error("Server error");

        const data = await response.json();
        console.log("Prediction response:", data);

        let output = "<h3>Prediction Results:</h3><ul>";
        for (const [key, valStr] of Object.entries(data.predictions)) {
            output += `<li><strong>${key}</strong>: ${valStr.trim()}</li>`;
        }
        output += "</ul>";

        resultsDiv.innerHTML = output;

        input.value = ""; // reset file input
    } catch (error) {
        console.error(error);
        resultsDiv.innerHTML = "❌ Could not get prediction. Is the backend running?";
    }
};