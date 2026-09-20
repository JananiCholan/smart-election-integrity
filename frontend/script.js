
async function loadRiskReport() {

    try {

        const response = await fetch("http://127.0.0.1:5000/risk-report");

        const data = await response.json();

        let low = 0;
        let medium = 0;
        let high = 0;

        const table = document.getElementById("reportTable");
        const searchInput = document.getElementById("searchInput");
        let currentRiskFilter = "All";

        table.innerHTML = "";

        data.forEach(voter => {

            if (voter.risk_level === "Low Risk") {
                low++;
            }
            else if (voter.risk_level === "Medium Risk") {
                medium++;
            }
            else if (voter.risk_level === "High Risk") {
                high++;
            }

            const row = document.createElement("tr");

            let riskClass = "";

            if (voter.risk_level === "Low Risk") {
                riskClass = "low";
            }
            else if (voter.risk_level === "Medium Risk") {
                riskClass = "medium";
            }
            else {
                riskClass = "high";
            }

            row.innerHTML = `
                <td>${voter.voter_id}</td>
                <td>${voter.name}</td>
                <td>${voter.constituency}</td>
                <td>${voter.EFRI_score}</td>
                <td class="${riskClass}">
                    ${voter.risk_level}
                </td>
                <td>${voter.reason}</td>
            `;

            table.appendChild(row);
        });

        document.getElementById("totalVoters").textContent = data.length;
        document.getElementById("lowRisk").textContent = low;
        document.getElementById("mediumRisk").textContent = medium;
        document.getElementById("highRisk").textContent = high;
        searchInput.addEventListener("input", function () {

    const searchText = searchInput.value.toLowerCase();

    const rows = table.querySelectorAll("tr");

    rows.forEach(row => {

        const voterId = row.cells[0]?.textContent.toLowerCase() || "";
        const name = row.cells[1]?.textContent.toLowerCase() || "";

        if (
            voterId.includes(searchText) ||
            name.includes(searchText)
        ) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }

    });

});

    }

    catch (error) {

        console.error("Error loading risk report:", error);

        document.getElementById("reportTable").innerHTML = `
            <tr>
                <td colspan="6">
                    Unable to connect to Flask server.
                </td>
            </tr>
        `;
    }
}


loadRiskReport();
window.filterRisk = function(risk) {

    currentRiskFilter = risk;

    const table = document.getElementById("reportTable");
    const searchInput = document.getElementById("searchInput");

    const rows = table.querySelectorAll("tr");
    const searchText = searchInput.value.toLowerCase();

    rows.forEach(row => {

        const voterId =
            row.cells[0]?.textContent.toLowerCase() || "";

        const name =
            row.cells[1]?.textContent.toLowerCase() || "";

        const riskLevel =
            row.cells[4]?.textContent.trim() || "";

        const matchesSearch =
            voterId.includes(searchText) ||
            name.includes(searchText);

        const matchesRisk =
            risk === "All" ||
            riskLevel === risk;

        if (matchesSearch && matchesRisk) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
};