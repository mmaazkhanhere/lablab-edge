import axios from 'axios'

export const imageGeneration = async (memory: string) => {
    try {
        const response = await axios.post('http://localhost:8000/image', { memory }, {
            responseType: 'json'  // Expect JSON response
        });

        if (response.status === 200 && response.data.image_urls) {
            return { status: 200, data: response.data.image_urls }
        } else {
            return { status: 400, message: "Error in image generation" }
        }
    } catch (error) {
        console.error(error)
        return { status: 500, message: "Something went wrong" }
    }
}
