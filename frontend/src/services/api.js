const API_BASE_URL = "http://localhost:8000";

export const sendMessage = async (message) => {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });
        if (!response.ok) throw new Error("Network response was not ok");
        return await response.ok ? response.json() : { reply: "Error connecting to server" };
    } catch (error) {
        console.error("API Error (sendMessage):", error);
        return { reply: "Server error occurred. Check if backend is running." };
    }
};

export const getQuiz = async (topic) => {
    try {
        const response = await fetch(`${API_BASE_URL}/quiz`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ topic }),
        });
        if (!response.ok) throw new Error("Network response was not ok");
        return await response.json();
    } catch (error) {
        console.error("API Error (getQuiz):", error);
        return { error: "Failed to generate quiz." };
    }
};

// Mock analytics for now, can be updated later with actual backend endpoint
export const getAnalytics = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/analysis/`);
        if (!response.ok) throw new Error("Network response was not ok");
        return await response.json();
    } catch (error) {
        console.error("API Error (getAnalytics):", error);
        return {
            total_attempts: 0,
            correct_answers: 0,
            incorrect_answers: 0,
            accuracy: 0.0,
        };
    }
};

