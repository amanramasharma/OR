document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");

    form.addEventListener("submit", (event) => {
        event.preventDefault();
        form.classList.add("shake");

        setTimeout(() => {
            form.classList.remove("shake");
        }, 500);
    });
});

// Shake animation for invalid login
document.styleSheets[0].insertRule(`
    @keyframes shake {
        0% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        50% { transform: translateX(5px); }
        75% { transform: translateX(-5px); }
        100% { transform: translateX(0); }
    }
`, 0);

document.styleSheets[0].insertRule(`
    .shake {
        animation: shake 0.5s ease-in-out;
    }
`, 1);


function togglePassword(id) {
    const passwordField = document.getElementById(id);
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}
