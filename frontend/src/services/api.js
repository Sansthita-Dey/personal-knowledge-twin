const API_URL = 'http://localhost:8000';

/**
 * Sends a query to the backend API and retrieves the AI's response.
 * @param {string} query The user's question
 * @returns {Promise<{answer: string}>}
 */
export const fetchChatResponse = async (query) => {
  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      throw new Error(`API returned status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching chat response:', error);
    // Returning a fallback/simulated error message so the UI doesn't crash 
    // when the backend isn't actively running during local development testing.
    return {
      answer: "I'm sorry, I couldn't connect to the backend server. Please ensure the FastAPI server is running on localhost:8000."
    };
  }
};
