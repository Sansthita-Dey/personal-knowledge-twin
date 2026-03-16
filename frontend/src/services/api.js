const API_URL = 'http://localhost:8000';

/**
 * Sends a query to the backend API and retrieves the AI's response.
 * @param {string} query The user's question
 * @param {string} mode student | interview | research | casual
 * @returns {Promise<{answer: string, confidence?: string}>}
 */
export const fetchChatResponse = async (query, mode = "student") => {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        mode: mode
      }),
    });

    if (!response.ok) {
      throw new Error(`API returned status: ${response.status}`);
    }

    const data = await response.json();
    return data;

  } catch (error) {
    console.error('Error fetching chat response:', error);

    return {
      answer: "⚠️ Could not connect to the backend. Make sure FastAPI is running on localhost:8000."
    };
  }
};