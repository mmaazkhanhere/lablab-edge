"use client";

import React, { useState } from "react";
import Image from "next/image";

import Loader from "./loader";

import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

import { emotionalTherapy } from "@/actions/emotional-therapy";
import { imageGeneration } from "@/actions/image-generation";
import { musicGeneration } from "@/actions/music-generation";
import { videoGeneration } from "@/actions/video-generation";

const ChatInterface = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [userMemory, setUserMemory] = useState<string>("");
  const [aiResponse, setAIResponse] = useState<string>("");
  const [musicUrl, setMusicUrl] = useState("");
  const [imageSrcs, setImageSrcs] = useState([]);
  const [videoUrl, setVideoUrl] = useState("");
  const [errorMessage, setErrorMessage] = useState<string>("");

  /*emotional therapy function */
  const handleEmotionalTherapy = async () => {
    setIsLoading(true);
    setErrorMessage("");
    setImageSrcs([]);
    setMusicUrl("");
    setVideoUrl("");
    setAIResponse("");
    const response = await emotionalTherapy(userMemory);
    if (response.status === 200) {
      setAIResponse(response.data);
    } else {
      setErrorMessage(response?.message || "Failed to generate response");
    }
    setIsLoading(false);
  };

  const handleImageTherapy = async () => {
    setIsLoading(true);
    setErrorMessage("");
    setImageSrcs([]);
    setMusicUrl("");
    setAIResponse("");
    setVideoUrl("");
    try {
      const imageResponse = await imageGeneration(userMemory);
      const musicResponse = await musicGeneration(userMemory);
      if (imageResponse.status === 200) {
        const updatedImageSrcs = imageResponse.data.map((src: string) => {
          const timestamp = new Date().getTime();
          return `${src}?t=${timestamp}`;
        });
        setImageSrcs(updatedImageSrcs);
      } else {
        setErrorMessage(imageResponse.message || "Failed to generate images.");
      }
      if (musicResponse.status === 200 && musicResponse.data) {
        setMusicUrl(musicResponse.data.audio_url);
      } else {
        setErrorMessage(musicResponse.message || "Failed to generate music.");
      }
    } catch (error) {
      console.log("Error generating images or music:", error);
      setErrorMessage("An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleVideoTherapy = async () => {
    setIsLoading(true);
    setErrorMessage("");
    setImageSrcs([]);
    setMusicUrl("");
    setAIResponse("");
    setVideoUrl("");

    try {
      const videoResponse = await videoGeneration(userMemory);
      if (videoResponse.status === 200) {
        setVideoUrl(videoResponse.data.video_url);
      } else {
        setErrorMessage(videoResponse.message || "Failed to generate video.");
      }
    } catch (error) {
      console.log("Error generating video:", error);
      setErrorMessage("An unexpected error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <div className="flex flex-col items-center gap-y-1 mb-8">
        <h1 className="text-3xl font-bold uppercase">Revisit</h1>
        <p>Because Every Memory Deserves Healing</p>
      </div>

      <div className="flex flex-col w-full max-w-lg gap-y-2">
        <Label htmlFor="message">Your memory</Label>
        <Textarea
          className="p-4 border border-gray-300 rounded mb-4 min-h-52"
          placeholder="I remember one day I was..."
          value={userMemory}
          onChange={(e) => setUserMemory(e.target.value)}
        />
      </div>

      <div className="flex flex-col max-w-lg w-full gap-y-2">
        <Button
          className="bg-blue-500 text-white p-2 rounded w-full max-w-lg"
          disabled={isLoading}
          onClick={handleEmotionalTherapy}
        >
          Text Emotional Therapy
        </Button>

        <Button
          className="bg-blue-500 text-white p-2 rounded w-full max-w-lg"
          disabled={isLoading}
          onClick={handleImageTherapy}
        >
          Visual Emotional Therapy
        </Button>

        <Button
          className="bg-blue-500 text-white p-2 rounded w-full max-w-lg"
          disabled={isLoading}
          onClick={handleVideoTherapy}
        >
          Visual Video Therapy
        </Button>
      </div>

      {isLoading ? (
        <Loader />
      ) : (
        <div className="flex flex-col gap-y-1 max-w-2xl w-full mt-4">
          {errorMessage.length > 0 && (
            <p className="text-sm text-red-500">{errorMessage}</p>
          )}
          {aiResponse.length > 0 && <p className="text-sm ">{aiResponse}</p>}
          {
            <Carousel>
              <CarouselContent>
                {imageSrcs.map((src, index) => (
                  <CarouselItem key={index} className="md:basis-1/2">
                    <div className="p-1">
                      <Image
                        key={index}
                        src={`http://localhost:8000${src}`} // Adjust the base URL as needed
                        alt={`Generated Image ${index + 1}`}
                        width={500}
                        height={500}
                        className="object-cover rounded"
                      />
                    </div>
                  </CarouselItem>
                ))}
              </CarouselContent>
              <CarouselPrevious />
              <CarouselNext />
            </Carousel>
          }
          {musicUrl && (
            <div className="mt-6">
              <h2 className="text-xl font-semibold mb-4">Generated Music</h2>
              <audio src={musicUrl} controls className="w-full max-w-lg" />
            </div>
          )}

          {videoUrl && (
            <div className="mt-6">
              <h2 className="text-xl font-semibold mb-4">Generated Video</h2>
              <video
                src={videoUrl}
                controls
                className="w-full max-w-lg"
                autoPlay
              />
            </div>
          )}
        </div>
      )}
    </section>
  );
};

export default ChatInterface;
