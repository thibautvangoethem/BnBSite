<script>
    import { onMount } from "svelte";
    import { writable } from "svelte/store";

    // Writable store to manage the bearer token (optional, if you want global state)
    export const bearerToken = writable(null);

    let username = "";
    let password = "";
    let errorMessage = "";
    const backendUrl = import.meta.env.VITE_BACKEND_URL;

    const handleSubmit = async (e) => {
        e.preventDefault();
        errorMessage = ""; // Reset error message

        try {
            // Create form-encoded data
            const formData = new URLSearchParams();
            formData.append("grant_type", "password");
            formData.append("username", username);
            formData.append("password", password);
            formData.append("scope", "");

            const response = await fetch(backendUrl + "/token", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded", // Correct Content-Type for form encoding
                },
                body: formData.toString(), // Send form-encoded data as body
            });

            if (!response.ok) {
                throw new Error("Login failed. Please check your credentials.");
            }

            const data = await response.json();

            if (data.access_token) {
                localStorage.setItem("bearerToken", data.access_token); // Save token in localStorage
                bearerToken.set(data.access_token); // Update the writable store (optional)
                console.log("Login successful. Token saved:", data.access_token);
            } else {
                throw new Error("No token received from server.");
            }
        } catch (err) {
            console.error(err);
            errorMessage = err.message;
        }
    };
</script>

<main>
    <form on:submit={handleSubmit}>
        <h1>Login</h1>

        {#if errorMessage}
            <p class="error">{errorMessage}</p>
        {/if}

        <label for="username">Username</label>
        <input
            type="text"
            id="username"
            bind:value={username}
            placeholder="Enter your username"
            required
        />

        <label for="password">Password</label>
        <input
            type="password"
            id="password"
            bind:value={password}
            placeholder="Enter your password"
            required
        />

        <button type="submit">Login</button>
    </form>
</main>

<style>
    form {
        max-width: 400px;
        margin: auto;
        padding: 1rem;
        border: 1px solid #ccc;
        border-radius: 8px;
        background-color: #f9f9f9;
    }
    label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    input {
        width: 100%;
        padding: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    button {
        width: 100%;
        padding: 0.75rem;
        background-color: #007bff;
        color: #fff;
        border: none;
        border-radius: 4px;
        font-size: 1rem;
        cursor: pointer;
    }
    button:hover {
        background-color: #0056b3;
    }
    .error {
        color: red;
        margin-bottom: 1rem;
    }
</style>
