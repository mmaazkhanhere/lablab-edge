"use client"

import React, {useState} from 'react'
// import Image from 'next/image'

import Loader from './loader'

import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Button } from '@/components/ui/button'

import { emotionalTherapy } from '@/actions/emotional-therapy'
// import { imageGeneration } from '@/actions/image-generation'

const ChatInterface = () => {

  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [userMemory, setUserMemory] = useState<string>("");
  const [aiResponse, setAIResponse] = useState<string>("");
  // const [imageSrcs, setImageSrcs] = useState([])
  const [errorMessage, setErrorMessage] = useState<string>("");


  const handleEmotionalTherapy = async() =>{
    setIsLoading(true)
    const response = await emotionalTherapy(userMemory);

    if(response.status === 200){
      setAIResponse(response.data)
    }
    else{
      setErrorMessage(response?.message)
    }

    setIsLoading(false)
  }

  // const handleGenerateImage = async () => {
  //   setIsLoading(true)
  //   setErrorMessage('')
  //   setImageSrcs([])

  //   const response = await imageGeneration(userMemory)

  //   if (response.status === 200 && response.data) {
  //       try {
  //           // response.data is a list of image URLs
  //           setImageSrcs(response.data)
  //       } catch (err) {
  //           console.error("Error processing image URLs:", err)
  //           setErrorMessage("Failed to process the images.")
  //       }
  //   } else {
  //       setErrorMessage(response.message || "Failed to generate images.")
  //   }

  //   setIsLoading(false)
  // }


  return (
    <section className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <div className='flex flex-col items-center gap-y-1 mb-8'>
        <h1 className="text-3xl font-bold uppercase">Revisit</h1>
        <p >Because Every Memory Deserves Healing</p>
      </div>
      
      
      <div className='flex flex-col w-full max-w-lg gap-y-2'>
        <Label htmlFor="message">Your memory</Label>
        <Textarea
            className="p-4 border border-gray-300 rounded mb-4 min-h-52"
            placeholder="I remember one day I was..."
            value={userMemory}
            onChange={(e) => setUserMemory(e.target.value)}
        />
      </div>
      
      <div className='flex items-center max-w-lg w-full gap-x-2'>
      
        <Button
          className="bg-blue-500 text-white p-2 rounded w-full max-w-lg"
          disabled={isLoading}
          onClick={handleEmotionalTherapy}
        >
          Heal Me
        </Button>
      </div>
      

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
              {
                aiResponse.length > 0 && <p className='text-sm '>{aiResponse}</p>
              }
            </div>
          )
      }

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
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {
                  imageSrcs.map((src, index) => (
                    <Image
                      key={index}
                      src={`http://localhost:8000${src}`}  // Adjust the base URL as needed
                      alt={`Generated Image ${index + 1}`}
                      width={500}
                      height={500}
                      className="object-cover rounded"
                    />
                  ))
                }
              </div>
            </div>
            
          )
      } */}

    </section>

  )
}

export default ChatInterface