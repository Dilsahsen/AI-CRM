
document.addEventListener("DOMContentLoaded", () => {

  const salesCanvas = document.getElementById("salesChart");
    if (salesCanvas && window.Chart) {
        const ctx = salesCanvas.getContext("2d");
        new Chart(ctx, {
            type: "line",
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], // şimdilik dummy
                datasets: [{
                    label: "Monthly Sales ($)",
                    data: [1200, 1500, 900, 1800, 2200, 2000],
                    tension: 0.3,
                    fill: true,
                }]
            },
            options: {
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { grid: { display: false } },
                    y: { beginAtZero: true }
                }
            }
        });
    }
    
    const savedTheme = localStorage.getItem("ai_crm_theme");
    if (savedTheme === "dark") {
      document.body.classList.add("dark");
    }
  
    const flashes = document.querySelectorAll(".flash");
    flashes.forEach((flash) => {
      setTimeout(() => {
        flash.style.opacity = "0";
        flash.style.transform = "translateY(-4px)";
        setTimeout(() => flash.remove(), 400);
      }, 4000);
    });
  
    const inputs = document.querySelectorAll(".form-input");
    inputs.forEach((input) => {
      input.addEventListener("focus", () => {
        input.classList.add("input-focused");
      });
      input.addEventListener("blur", () => {
        if (!input.value.trim()) {
          input.classList.remove("input-focused");
        }
      });
    });
  
    const authForm = document.querySelector(".auth-form");
    if (authForm) {
      authForm.addEventListener("submit", (e) => {
        let hasError = false;
        const requiredInputs = authForm.querySelectorAll(".form-input");
        requiredInputs.forEach((inp) => {
          if (!inp.value.trim()) {
            inp.classList.add("input-error");
            hasError = true;
          } else {
            inp.classList.remove("input-error");
          }
        });
  
        if (hasError) {
          e.preventDefault();
        }
      });
    }
  
    const themeBtn = document.getElementById("theme-toggle");
    if (themeBtn) {
     
      const updateIcon = () => {
        if (document.body.classList.contains("dark")) {
          themeBtn.textContent = "☀️";
        } else {
          themeBtn.textContent = "🌙";
        }
      };
      updateIcon();
  
      themeBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark");
  
        if (document.body.classList.contains("dark")) {
          localStorage.setItem("ai_crm_theme", "dark");
        } else {
          localStorage.setItem("ai_crm_theme", "light");
        }
  
        updateIcon();
      });
    }
  });
  
  document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("salesChart");
    if (canvas && window.Chart && window.SALES_CHART_LABELS && window.SALES_CHART_VALUES) {
        const ctx = canvas.getContext("2d");

        new Chart(ctx, {
            type: "line",
            data: {
                labels: window.SALES_CHART_LABELS,
                datasets: [
                    {
                        label: "Sales (Last 7 Days)",
                        data: window.SALES_CHART_VALUES,
                        tension: 0.35,
                        fill: true,
                    },
                ],
            },
            options: {
                plugins: {
                    legend: {
                        display: false,
                    },
                },
                scales: {
                    x: {
                        grid: { display: false },
                    },
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        });
    }
});
