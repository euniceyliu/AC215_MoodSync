import { BASE_API_URL, uuid } from "./Common";
import { mockChats } from "./SampleData";
import axios from 'axios';

console.log("BASE_API_URL:", BASE_API_URL)

// Create an axios instance with base configuration
const api = axios.create({
    baseURL: BASE_API_URL
});

const DataService = {
  Init: function () {
    // Any application initialization logic comes here
},
  chatWithLLM: async function(message) {
    try {
      console.log("Sending message to backend:", message); // Debugging
      const response = await axios.post(`${BASE_API_URL}/chat`, message, {
        headers: {
          "Content-Type": "text", // Ensure the Content-Type matches backend expectations
        },
      });
      return response.data; // Return the API response
    } catch (error) {
      console.error("Failed to send message to LLM:", error);
      throw error; // Re-throw error to handle it in the caller
    }
  },
  chatWithLLMAgent: async function(message) {
    try {
      console.log("Sending message to backend:", message); // Debugging
      const response = await axios.post(`${BASE_API_URL}/chat_agent`, message, {
        headers: {
          "Content-Type": "text", // Ensure the Content-Type matches backend expectations
        },
      });
      return response.data; // Return the API response
    } catch (error) {
      console.error("Failed to send message to LLM agent:", error);
      throw error; // Re-throw error to handle it in the caller
    }

}
}
export default DataService;