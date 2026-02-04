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

// ---------------------------
// Helper functions: show/hide sections
// ---------------------------
function showPredictionSection() {
    loginContainer.style.display = "none";
    registerContainer.style.display = "none";
    predictionContainer.style.display = "block";
}

function showLogin() {
    loginContainer.style.display = "block";
    registerContainer.style.display = "none";
    predictionContainer.style.display = "none";
}

function showRegister() {
    loginContainer.style.display = "none";
    registerContainer.style.display = "block";
    predictionContainer.style.display = "none";
    document.getElementById("otpSection").style.display = "none"; // hide OTP input
}

// ---------------------------
// Login
// ---------------------------
window.loginUser = async function () {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const loginMsg = document.getElementById("loginMsg");

    if (!username || !password) {
        loginMsg.textContent = "Please enter username and password";
        return;
    }

    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const response = await fetch("http://localhost:8000/login", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) throw new Error("Invalid username or password");

        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        loginMsg.textContent = "✅ Login successful!";
        showPredictionSection();
    } catch (error) {
        console.error(error);
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
        const response = await fetch(`/register/send-otp?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&email=${encodeURIComponent(email)}`, {
            method: "POST"
        });

        const data = await response.json();
        if (data.message) {
            registerMsg.textContent = "✅ OTP sent to your email. Check inbox!";
            document.getElementById("otpSection").style.display = "block"; // show OTP input
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
        const response = await fetch(`/register/verify-otp?email=${encodeURIComponent(email)}&otp=${encodeURIComponent(otp)}`, {
            method: "POST"
        });

        const data = await response.json();
        if (data.success) {
            registerMsg.textContent = "✅ Registration complete! You can now login.";
            document.getElementById("otpSection").style.display = "none";
        } else {
            registerMsg.textContent = "❌ " + data.message;
        }
    } catch (error) {
        console.error(error);
        registerMsg.textContent = "❌ Could not verify OTP";
    }
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

    try {
        const response = await fetch("http://localhost:8000/predict", {
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