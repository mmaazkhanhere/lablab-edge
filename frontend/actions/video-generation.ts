import axios from "axios";

export const videoGeneration = async (memory: string) => {
  try {
    const response = await axios.post("http://localhost:8000/video", {
      memory,
    });

    if (response.status === 200) {
      return { status: 200, data: response.data };
    } else {
      return { status: 400, message: "Error in music generation" };
    }
  } catch (error) {
    console.error(error);
    return { status: 500, message: "Something went wrong" };
  }
};
