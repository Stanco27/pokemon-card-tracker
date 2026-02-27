import type { SniperConfig } from "./types";

const API_BASE_URL = "http://localhost:5000";

const DEFAULT_HEADERS = {
  "Content-Type": "application/json",
};

export const botApi = {
  test: async (config: SniperConfig) => {
    try {
      const response = await fetch(`${API_BASE_URL}/bot/test`, {
        method: "POST",
        headers: DEFAULT_HEADERS,
        body: JSON.stringify(config),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error("Failed to start bot:", error);
      throw error;
    }
  }
};