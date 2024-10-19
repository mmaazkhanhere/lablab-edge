"use client"

import React, {useState} from 'react'

import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Button } from './ui/button'
// import { emotionAnalyzer } from '@/actions/emotion-analyzer'
import Loader from './loader'
import { imageGeneration } from '@/actions/image-generation'
import Image from 'next/image'


const ChatInterface = () => {

  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [userMemory, setUserMemory] = useState<string>("");
  // const [aiResponse, setAIResponse] = useState<string>("");
  const [imageSrc, setImageSrc] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");

  // const handleSubmit = async() =>{
  //   setIsLoading(true)
  //   const response = await emotionAnalyzer(userMemory);

  //   if(response.status === 200){
  //     setAIResponse(response.data)
  //   }
  //   else{
  //     setErrorMessage(response?.message)
  //   }

  //   setIsLoading(false)
  // }

  const handleGenerateImage = async () => {
    setIsLoading(true);
    setErrorMessage('');
    setImageSrc('');

    const response = await imageGeneration(userMemory);

        if(response.status === 200 && response.data) {
            try {
                // Ensure data is a Blob
                if (response.data instanceof Blob) {
                    const url = URL.createObjectURL(response.data);
                    setImageSrc(url);
                } else {
                    console.error("Received data is not a Blob:", response.data);
                    setErrorMessage("Invalid image data received.");
                }
            } catch (err) {
                console.error("Error processing image blob:", err);
                setErrorMessage("Failed to process the image.");
            }
        } else {
            setErrorMessage(response.message || "Failed to generate image.");
        }

        setIsLoading(false);
  }

  return (
    <section className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <h1 className="text-3xl font-bold mb-6">Memory to Video Generator</h1>
      
      <div className='flex flex-col w-full max-w-lg gap-y-2'>
        <Label htmlFor="message">Your memory</Label>
        <Textarea
            className="p-4 border border-gray-300 rounded mb-4 min-h-52"
            placeholder="I remember one day I was..."
            value={userMemory}
            onChange={(e) => setUserMemory(e.target.value)}
        />
      </div>
      
      <Button
        className="bg-blue-500 text-white p-2 rounded w-full max-w-lg"
        disabled={isLoading}
        onClick={handleGenerateImage}
      >
        Generate Image
      </Button>

      {/* {
        isLoading ? 
          (
            <Loader />
          ) : 
          (
            <div className='flex flex-col gap-y-1 max-w-2xl w-full mt-4'>
              {
                errorMessage.length > 0 && <p className='text-sm text-red-500'>{errorMessage}</p>
              }
              {
                aiResponse.length > 0 && <p className='text-sm '>{aiResponse}</p>
              }
            </div>
          )
      } */}

      {
        isLoading ?
          (
            <Loader />
          ) :
          (
            <div className='flex flex-col gap-y-1 max-w-2xl w-full mt-4'>
              {
                errorMessage.length > 0 && <p className='text-sm text-red-500'>{errorMessage}</p>
              }
              <p>{imageSrc}</p>
              {
                imageSrc && <Image src={imageSrc} alt="Generated Image" width={500} height={500} />
              }
            </div>
            
          )
      }

      {/* {generatedVideoUrl && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-4">Generated Video</h2>
          <video src={generatedVideoUrl} controls className="w-full max-w-lg" />
        </div>
      )} */}
    </section>

  )
}

export default ChatInterface