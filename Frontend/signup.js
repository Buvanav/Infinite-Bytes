import { createUserWithEmailAndPassword } 
from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

import { doc, setDoc, serverTimestamp } 
from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

import { auth, db } from "./firebase.js";

console.log(" signup.js loaded");

const form = document.getElementById("signupForm");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;
  const confirm = document.getElementById("confirm").value;

  if (password !== confirm) {
    alert("Passwords do not match ❌");
    return;
  }

  try {
    // 1️⃣ Create Auth user
    const userCredential =
      await createUserWithEmailAndPassword(auth, email, password);

    const user = userCredential.user;
    console.log("✅ Auth user created:", user.uid);

    // 2️⃣ Save profile to Firestore
    await setDoc(doc(db, "users", user.uid), {
      fullName: name,
      email: user.email,
      uid: user.uid,
      createdAt: serverTimestamp()
    });

    console.log("✅ Firestore saved");
    window.location.href = "dashboard.html";

  } catch (err) {
    console.error("❌ Signup error:", err);
    alert(err.message);
  }
});
