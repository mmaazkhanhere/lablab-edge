import axios from 'axios'

export const imageGeneration = async(memory: string) => {
    try {
        const response = await axios.post('http://localhost:8000/image', {memory}, {
            responseType: 'blob'
        });

        if(response.status === 200) {
            return {status: 200, data: response.data}
        }
        else{
            return {status:400, message: "Error in image generation"}
        }
    } catch (error) {
        console.log(error)
        return {status:500, message: "Something went wrong"}
    }
}
