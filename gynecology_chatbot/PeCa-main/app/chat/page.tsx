"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Send, Bot, User, AlertTriangle, Info, CheckCircle } from "lucide-react"
import Link from "next/link"
import { Navigation } from "@/components/navigation"

interface Message {
  id: string
  content: string
  sender: "user" | "assistant"
  timestamp: Date
  severity?: "low" | "medium" | "high"
  aiModel?: "ChatGPT" | "Gemini" | "Grok"
  showBooking?: boolean
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content:
        "Hello! I'm your WomanCare AI assistant. I'm here to help with your gynecological health questions. How can I assist you today?",
      sender: "assistant",
      timestamp: new Date(),
      severity: "low",
      aiModel: "ChatGPT",
    },
  ])
  const [inputValue, setInputValue] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue("")
    setIsTyping(true)

    // Simulate AI response
    setTimeout(() => {
      const responses = [
        {
          content:
            "Based on your symptoms, this could be related to hormonal changes. I recommend tracking your cycle and noting when these symptoms occur. However, for a proper diagnosis, please consult with a gynecologist.",
          severity: "medium" as const,
          aiModel: "ChatGPT" as const,
          showBooking: true,
        },
        {
          content:
            "These symptoms are quite common and usually not serious. Here are some self-care tips that might help: stay hydrated, get adequate rest, and consider gentle exercise. If symptoms persist, please see a healthcare provider.",
          severity: "low" as const,
          aiModel: "Gemini" as const,
          showBooking: false,
        },
        {
          content:
            "I'm concerned about the symptoms you've described. This requires immediate medical attention. Please contact your healthcare provider or visit an emergency room if symptoms worsen.",
          severity: "high" as const,
          aiModel: "Grok" as const,
          showBooking: true,
        },
      ]

      const randomResponse = responses[Math.floor(Math.random() * responses.length)]

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: randomResponse.content,
        sender: "assistant",
        timestamp: new Date(),
        severity: randomResponse.severity,
        aiModel: randomResponse.aiModel,
        showBooking: randomResponse.showBooking,
      }

      setMessages((prev) => [...prev, assistantMessage])
      setIsTyping(false)
    }, 2000)
  }

  const getSeverityColor = (severity?: string) => {
    switch (severity) {
      case "low":
        return "bg-green-100 text-green-800"
      case "medium":
        return "bg-yellow-100 text-yellow-800"
      case "high":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  const getSeverityIcon = (severity?: string) => {
    switch (severity) {
      case "low":
        return <CheckCircle className="w-3 h-3" />
      case "medium":
        return <Info className="w-3 h-3" />
      case "high":
        return <AlertTriangle className="w-3 h-3" />
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Navigation isLoggedIn={true} userName="User" />

      {/* Chat Container */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card className="h-[calc(100vh-200px)] flex flex-col">
          {/* Messages */}
          <CardContent className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.map((message) => (
              <div key={message.id} className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[80%] ${message.sender === "user" ? "order-2" : "order-1"}`}>
                  <div className="flex items-center space-x-2 mb-2">
                    <Avatar className="w-8 h-8">
                      <AvatarFallback
                        className={
                          message.sender === "user" ? "bg-blue-100 text-blue-600" : "bg-pink-100 text-pink-600"
                        }
                      >
                        {message.sender === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                      </AvatarFallback>
                    </Avatar>
                    <span className="text-sm font-medium text-gray-900">
                      {message.sender === "user" ? "You" : "AI Assistant"}
                    </span>
                    <span className="text-xs text-gray-500">
                      {message.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                    </span>
                  </div>

                  <div
                    className={`rounded-2xl p-4 ${
                      message.sender === "user" ? "bg-blue-500 text-white" : "bg-white border border-gray-200"
                    }`}
                  >
                    <p className="text-sm leading-relaxed">{message.content}</p>

                    {message.sender === "assistant" && (
                      <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
                        <div className="flex items-center space-x-2">
                          {message.aiModel && (
                            <Badge variant="secondary" className="text-xs">
                              {message.aiModel}
                            </Badge>
                          )}
                          {message.severity && (
                            <Badge className={`text-xs ${getSeverityColor(message.severity)}`}>
                              {getSeverityIcon(message.severity)}
                              <span className="ml-1 capitalize">{message.severity}</span>
                            </Badge>
                          )}
                        </div>

                        {message.showBooking && (
                          <Link href="/doctors">
                            <Button size="sm" className="bg-pink-500 hover:bg-pink-600 text-white">
                              Book Doctor
                            </Button>
                          </Link>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="flex justify-start">
                <div className="max-w-[80%]">
                  <div className="flex items-center space-x-2 mb-2">
                    <Avatar className="w-8 h-8">
                      <AvatarFallback className="bg-pink-100 text-pink-600">
                        <Bot className="w-4 h-4" />
                      </AvatarFallback>
                    </Avatar>
                    <span className="text-sm font-medium text-gray-900">AI Assistant</span>
                  </div>

                  <div className="bg-white border border-gray-200 rounded-2xl p-4">
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: "0.1s" }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </CardContent>

          {/* Input Section */}
          <div className="border-t border-gray-200 p-6">
            <div className="flex space-x-4">
              <div className="flex-1">
                <Textarea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Ask me about your gynecological health concerns..."
                  className="min-h-[60px] resize-none border-gray-300 focus:border-pink-500 focus:ring-pink-500"
                  maxLength={1000}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault()
                      handleSendMessage()
                    }
                  }}
                />
                <div className="flex justify-between items-center mt-2">
                  <span className="text-xs text-gray-500">{inputValue.length}/1000 characters</span>
                  <span className="text-xs text-gray-500">Press Enter to send, Shift+Enter for new line</span>
                </div>
              </div>
              <Button
                onClick={handleSendMessage}
                disabled={!inputValue.trim() || isTyping}
                className="bg-pink-500 hover:bg-pink-600 text-white px-6"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}
