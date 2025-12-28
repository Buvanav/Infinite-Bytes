const API_BASE = "http://127.0.0.1:8001";

function initWorkerInsights() {
  const errorDiv    = document.getElementById("wi-error");
  const kycCard     = document.getElementById("wi-kyc-card");
  const kycText     = document.getElementById("wi-kyc-text");
  const summaryText = document.getElementById("wi-summary-text");
  const txnCard     = document.getElementById("wi-txn-card");
  const txnBody     = document.querySelector("#wi-txn-table tbody");
  const predictCard = document.getElementById("wi-predict-card");
  const predictText = document.getElementById("wi-predict-text");

  window.wiLoadProfile = async function () {
    const workerId = document.getElementById("wi-worker_id").value.trim();
    errorDiv.textContent = "";
    kycCard.style.display = "none";
    txnCard.style.display = "none";

    if (!workerId) {
      errorDiv.textContent = "Please enter a worker ID (e.g., W001).";
      return;
    }

    try {
      const resp = await fetch(`${API_BASE}/worker/${encodeURIComponent(workerId)}`);
      if (!resp.ok) {
        errorDiv.textContent = "Worker not found.";
        return;
      }
      const data = await resp.json();

      const k   = data.kyc;
      const inc = data.income || [];
      const lastIncome = inc.length > 0 ? inc[inc.length - 1] : null;

      kycText.textContent =
        `${k.name} (${k.worker_id || workerId}), age ${k.age}, ` +
        `PAN ${k.pan}, city ${k.city || ""}`.trim();

      if (lastIncome) {
        summaryText.textContent =
          `Recent average monthly income: ₹${lastIncome.avg_monthly_income || lastIncome.amount || "NA"}, ` +
          `months on platform (approx): ${data.income.length}`;
      } else {
        summaryText.textContent = "No income history available.";
      }
      kycCard.style.display = "block";

      txnBody.innerHTML = "";
      (data.transactions || []).forEach(txn => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${txn.date}</td>
          <td>₹${txn.amount}</td>
          <td>${txn.type}</td>
          <td>${txn.source || ""}</td>
        `;
        txnBody.appendChild(tr);
      });
      if ((data.transactions || []).length > 0) {
        txnCard.style.display = "block";
      }
    } catch (e) {
      console.error(e);
      errorDiv.textContent = "Error contacting backend 2.0.";
    }
  };

  window.wiPredictScore = async function () {
    const workerId = document.getElementById("wi-worker_id").value.trim();
    errorDiv.textContent = "";
    predictCard.style.display = "none";

    if (!workerId) {
      errorDiv.textContent = "Enter a worker ID first.";
      return;
    }

    const payload = {
      worker_id: workerId,
      age: 28,
      hours_worked: 40,
      avg_monthly_income: 25000
    };

    try {
      const resp = await fetch(`${API_BASE}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) {
        const t = await resp.text();
        throw new Error(t);
      }
      const data = await resp.json();
      predictText.textContent =
        `Worker: ${data.worker_id} | Score: ${data.credit_score} | ` +
        `Status: ${data.status} | Amount: ₹${data.loan_amount}`;
      predictCard.style.display = "block";
    } catch (e) {
      console.error(e);
      errorDiv.textContent = "Error during prediction.";
    }
  };
}

document.addEventListener("DOMContentLoaded", initWorkerInsights);
