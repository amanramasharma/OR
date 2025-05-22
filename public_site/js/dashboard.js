document.getElementById("uploadForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const fileInput = document.getElementById("resumeInput");
  const file = fileInput.files[0];
  if (!file) {
    alert("Please select a resume file.");
    return;
  }

  const formData = new FormData();
  formData.append("resume", file);

  const button = this.querySelector("button");
  const originalText = button.textContent;
  button.disabled = true;
  button.textContent = "Analyzing...";

  try {
    const res = await fetch("/upload_resume", {
      method: "POST",
      body: formData,
      credentials: "include"
    });

    if (res.redirected) {
      window.location.href = res.url;
    } else {
      const text = await res.text();
      alert("Upload failed.");
      button.disabled = false;
      button.textContent = originalText;
    }
  } catch (err) {
    alert("An error occurred.");
    button.disabled = false;
    button.textContent = originalText;
  }
});

async function loadDashboardStats() {
  const nameEl = document.getElementById("welcomeUser");
  const topSkillEl = document.getElementById("topSkill");
  const totalUploadsEl = document.getElementById("totalUploads");

  try {
    const profileRes = await fetch("/profile", { credentials: "include" });
    const profile = await profileRes.json();
    if (profile.username) nameEl.textContent = `Welcome, ${profile.username}`;

    const res = await fetch("/my_uploads", { credentials: "include" });
    const html = await res.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, "text/html");

    const rows = doc.querySelectorAll("tr.upload-row");
    totalUploadsEl.textContent = rows.length;

    const skillMap = {};
    rows.forEach(row => {
      const skillCell = row.querySelector(".skills");
      if (!skillCell) return;
      const skills = skillCell.textContent.split(",").map(s => s.trim().toLowerCase());
      skills.forEach(skill => {
        if (!skill) return;
        skillMap[skill] = (skillMap[skill] || 0) + 1;
      });
    });

    const topSkill = Object.entries(skillMap)
      .sort((a, b) => b[1] - a[1])[0]?.[0] || "--";

    topSkillEl.textContent = topSkill.charAt(0).toUpperCase() + topSkill.slice(1);
  } catch (err) {
    console.error("Failed to load dashboard stats", err);
  }
}

loadDashboardStats();