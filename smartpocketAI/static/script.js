async function getRecommendation() {

    const budget = document.getElementById("budget").value;
    const category = document.getElementById("category").value;
    const requirement = document.getElementById("requirement").value;
    const preference = document.getElementById("preference").value;

    // Basic validation
    if (!budget || Number(budget) <= 0) {
        alert("Please enter a valid budget.");
        return;
    }

    if (!requirement.trim()) {
        alert("Please enter what you need.");
        return;
    }

    // Show result section
    const resultBox = document.getElementById("result");
    const allocationBox = document.getElementById("allocation");
    const aiResultBox = document.getElementById("aiResult");

    resultBox.style.display = "block";

    allocationBox.innerHTML = "<p>Calculating your budget...</p>";
    aiResultBox.innerHTML = "";

    try {

        const response = await fetch("/recommend", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                budget: Number(budget),
                category: category,
                requirement: requirement,
                preference: preference
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Server error");
        }

        // Display budget allocation
        let allocationHTML = `
            <h3>Suggested Budget Allocation</h3>
        `;

        for (const [name, amount] of Object.entries(data.allocation)) {
            allocationHTML += `
                <div class="allocation-item">
                    <span>${name}</span>
                    <strong>₹${Number(amount).toLocaleString("en-IN")}</strong>
                </div>
            `;
        }

        allocationBox.innerHTML = allocationHTML;

        // Display AI recommendation
        aiResultBox.innerHTML = `
            <div class="ai-box">
                <h3>🤖 PocketSmart AI Recommendation</h3>
                <p>${data.ai_recommendation}</p>
            </div>
        `;

    } catch (error) {

        console.error("Error:", error);

        allocationBox.innerHTML = "";
        aiResultBox.innerHTML = `
            <div class="ai-box">
                <h3>⚠️ Error</h3>
                <p>${error.message}</p>
            </div>
        `;
    }
}