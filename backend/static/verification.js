
const voterSearch = document.getElementById("voterSearch");

voterSearch.addEventListener("input", async function () {

    const searchId = voterSearch.value.trim().toUpperCase();

    if (searchId === "") {
        clearDetails();
        return;
    }

    try {

        const votersResponse = await fetch("/voters");

        const riskResponse = await fetch("/risk-report");

        const voters = await votersResponse.json();
        const riskData = await riskResponse.json();

        const voter = voters.find(
            item => item.voter_id.toUpperCase() === searchId
        );

        const risk = riskData.find(
            item => item.voter_id.toUpperCase() === searchId
        );

        if (!voter || !risk) {

            clearDetails();

            document.getElementById("reason").textContent =
                "Voter not found.";

            return;
        }

        document.getElementById("voterId").textContent =
            voter.voter_id;

        document.getElementById("voterName").textContent =
            voter.name;

        document.getElementById("dob").textContent =
            voter.date_of_birth;

        document.getElementById("gender").textContent =
            voter.gender;

        document.getElementById("address").textContent =
            voter.address;

        document.getElementById("constituency").textContent =
            voter.constituency;

        document.getElementById("efriScore").textContent =
            risk.EFRI_score;

        document.getElementById("riskLevel").textContent =
            risk.risk_level;

        document.getElementById("reason").textContent =
            risk.reason;
        document.getElementById("verifyButton").disabled = false;

        document.getElementById("verifyButton").textContent =
        "Mark Verification Complete";

        document.getElementById("verifyButton").style.background =
        "#7a1720";

        document.getElementById("verificationStatus").textContent =
        "";

    }

    catch (error) {

        console.error(error);

        document.getElementById("reason").textContent =
            "Unable to connect to Flask server.";
    }

});


function clearDetails() {

    document.getElementById("voterId").textContent = "-";
    document.getElementById("voterName").textContent = "-";
    document.getElementById("dob").textContent = "-";
    document.getElementById("gender").textContent = "-";
    document.getElementById("address").textContent = "-";
    document.getElementById("constituency").textContent = "-";
    document.getElementById("efriScore").textContent = "-";
    document.getElementById("riskLevel").textContent = "-";

    document.getElementById("reason").textContent =
        "No voter selected.";
}

function markVerificationComplete() {

    const voterId =
        document.getElementById("voterId").textContent;

    if (voterId === "-") {
        return;
    }

    const button =
        document.getElementById("verifyButton");

    const status =
        document.getElementById("verificationStatus");

    button.textContent = "✓ Verification Completed";

    button.disabled = true;

    button.style.background = "#555";

    status.textContent =
        "Verification completed successfully for " + voterId;
}