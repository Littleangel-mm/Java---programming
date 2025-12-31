import { GoogleGenAI, Type } from "@google/genai";

export const generateAttributes = async (entityName: string): Promise<string[]> => {
  if (!process.env.API_KEY) {
    console.warn("API Key not found, returning mock data");
    return ["ID", "Name", "Created At", "Updated At"];
  }

  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: `Generate a list of 6 to 10 common database attributes for an entity named "${entityName}". 
      For example, if the entity is 'User', return attributes like 'user_id', 'username', 'email', 'avatar', etc.
      Keep attribute names concise (1-3 words max). Return a plain JSON array of strings.`,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.ARRAY,
          items: {
            type: Type.STRING
          }
        }
      }
    });

    const text = response.text;
    if (!text) return [];
    
    const parsed = JSON.parse(text);
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    console.error("Gemini API Error:", error);
    return [];
  }
};