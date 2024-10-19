"use client"

import React, {useState} from 'react'

import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Button } from './ui/button'


const ChatInterface = () => {

    const [userText, setUserText] = useState<string>("");
    const [showText, setShowText] = useState<boolean>(false)

    const handleClick = () =>{
        setShowText(!showText)
    }

  return (
    <section className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <h1 className="text-3xl font-bold mb-6">Memory to Video Generator</h1>
      
      <div className='flex flex-col w-full max-w-lg gap-y-2'>
        <Label htmlFor="message">Your memory</Label>
        <Textarea
            className="p-4 border border-gray-300 rounded mb-4"
            placeholder="I remember one day I was..."
            value={userText}
            onChange={(e) => setUserText(e.target.value)}
        />
      </div>
      
      <Button
        className="bg-blue-500 text-white p-2 rounded w-full max-w-lg"
        onClick={handleClick}
      >
        Generate Video
      </Button>


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