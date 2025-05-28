"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import {
  MessageCircle,
  Calendar,
  Clock,
  User,
  Bell,
  ArrowRight,
  Sparkles,
  TrendingUp,
  Shield,
  Activity,
} from "lucide-react"
import Link from "next/link"
import { Navigation } from "@/components/navigation"

export default function DashboardPage() {
  const [userName] = useState("Sarah")

  const upcomingAppointments = [
    {
      id: 1,
      doctor: "Dr. Priya Sharma",
      specialty: "Gynecologist",
      date: "Today",
      time: "2:30 PM",
      type: "Video Consultation",
    },
    {
      id: 2,
      doctor: "Dr. Anjali Mehta",
      specialty: "Reproductive Endocrinologist",
      date: "Tomorrow",
      time: "10:00 AM",
      type: "In-person Visit",
    },
  ]

  const recentChats = [
    {
      id: 1,
      topic: "Menstrual cycle concerns",
      date: "2 hours ago",
      severity: "low",
    },
    {
      id: 2,
      topic: "Pregnancy planning advice",
      date: "Yesterday",
      severity: "medium",
    },
  ]

  const healthReminders = [
    {
      id: 1,
      title: "Annual Pap Smear",
      dueDate: "Due in 2 weeks",
      priority: "high",
    },
    {
      id: 2,
      title: "Vitamin D Supplement",
      dueDate: "Take daily",
      priority: "medium",
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-blue-50">
      {/* Header */}
      <Navigation isLoggedIn={true} userName="Sarah" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <div className="bg-gradient-to-r from-pink-500 to-blue-500 rounded-2xl p-8 text-white relative overflow-hidden">
            <div className="absolute inset-0 bg-black opacity-10"></div>
            <div className="relative z-10">
              <h1 className="text-3xl lg:text-4xl font-bold mb-2">Welcome back, {userName}! 👋</h1>
              <p className="text-pink-100 text-lg mb-6">
                Your health journey continues. Here's what's happening today.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link href="/chat">
                  <Button className="bg-white text-pink-600 hover:bg-gray-50">
                    <MessageCircle className="w-4 h-4 mr-2" />
                    Chat with AI
                  </Button>
                </Link>
                <Link href="/doctors">
                  <Button variant="outline" className="border-white text-white hover:bg-white hover:text-pink-600">
                    <Calendar className="w-4 h-4 mr-2" />
                    Book Appointment
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-r from-pink-500 to-pink-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-pink-100 text-sm">Total Consultations</p>
                  <p className="text-2xl font-bold">12</p>
                </div>
                <User className="w-8 h-8 text-pink-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-blue-500 to-blue-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-100 text-sm">AI Chat Sessions</p>
                  <p className="text-2xl font-bold">28</p>
                </div>
                <MessageCircle className="w-8 h-8 text-blue-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-100 text-sm">Health Score</p>
                  <p className="text-2xl font-bold">85%</p>
                </div>
                <TrendingUp className="w-8 h-8 text-green-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-purple-500 to-purple-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-100 text-sm">Days Tracked</p>
                  <p className="text-2xl font-bold">45</p>
                </div>
                <Activity className="w-8 h-8 text-purple-200" />
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-8">
            {/* Upcoming Appointments */}
            <Card className="shadow-lg border-0">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center space-x-2">
                    <Calendar className="w-5 h-5 text-pink-500" />
                    <span>Upcoming Appointments</span>
                  </CardTitle>
                  <Link href="/appointments">
                    <Button variant="ghost" size="sm">
                      View All
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </Link>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {upcomingAppointments.map((appointment) => (
                  <div key={appointment.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
                    <div className="flex items-center space-x-4">
                      <Avatar>
                        <AvatarFallback className="bg-pink-100 text-pink-600">
                          {appointment.doctor
                            .split(" ")
                            .map((n) => n[0])
                            .join("")}
                        </AvatarFallback>
                      </Avatar>
                      <div>
                        <h4 className="font-semibold text-gray-900">{appointment.doctor}</h4>
                        <p className="text-sm text-gray-600">{appointment.specialty}</p>
                        <div className="flex items-center space-x-2 mt-1">
                          <Clock className="w-4 h-4 text-gray-400" />
                          <span className="text-sm text-gray-600">
                            {appointment.date} at {appointment.time}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <Badge variant="outline" className="mb-2">
                        {appointment.type}
                      </Badge>
                      <Button size="sm" className="bg-pink-500 hover:bg-pink-600 text-white">
                        Join
                      </Button>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Recent Chat History */}
            <Card className="shadow-lg border-0">
              <CardHeader className="pb-4">
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center space-x-2">
                    <MessageCircle className="w-5 h-5 text-blue-500" />
                    <span>Recent AI Conversations</span>
                  </CardTitle>
                  <Link href="/chat">
                    <Button variant="ghost" size="sm">
                      Start New Chat
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  </Link>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {recentChats.map((chat) => (
                  <div
                    key={chat.id}
                    className="flex items-center justify-between p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-colors cursor-pointer"
                  >
                    <div className="flex items-center space-x-4">
                      <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <MessageCircle className="w-5 h-5 text-blue-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-900">{chat.topic}</h4>
                        <p className="text-sm text-gray-600">{chat.date}</p>
                      </div>
                    </div>
                    <Badge
                      className={
                        chat.severity === "low"
                          ? "bg-green-100 text-green-700"
                          : chat.severity === "medium"
                            ? "bg-yellow-100 text-yellow-700"
                            : "bg-red-100 text-red-700"
                      }
                    >
                      {chat.severity}
                    </Badge>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Right Column */}
          <div className="space-y-8">
            {/* Quick Actions */}
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Sparkles className="w-5 h-5 text-purple-500" />
                  <span>Quick Actions</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Link href="/chat">
                  <Button className="w-full justify-start bg-gradient-to-r from-pink-500 to-pink-600 text-white hover:from-pink-600 hover:to-pink-700">
                    <MessageCircle className="w-4 h-4 mr-3" />
                    Ask AI Assistant
                  </Button>
                </Link>
                <Link href="/doctors">
                  <Button
                    variant="outline"
                    className="w-full justify-start border-blue-500 text-blue-600 hover:bg-blue-50"
                  >
                    <Calendar className="w-4 h-4 mr-3" />
                    Book Appointment
                  </Button>
                </Link>
                <Link href="/health-tracker">
                  <Button
                    variant="outline"
                    className="w-full justify-start border-green-500 text-green-600 hover:bg-green-50"
                  >
                    <Activity className="w-4 h-4 mr-3" />
                    Track Health
                  </Button>
                </Link>
                <Link href="/profile">
                  <Button
                    variant="outline"
                    className="w-full justify-start border-purple-500 text-purple-600 hover:bg-purple-50"
                  >
                    <User className="w-4 h-4 mr-3" />
                    Update Profile
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Health Reminders */}
            <Card className="shadow-lg border-0">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Bell className="w-5 h-5 text-orange-500" />
                  <span>Health Reminders</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {healthReminders.map((reminder) => (
                  <div key={reminder.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">{reminder.title}</h4>
                      <p className="text-sm text-gray-600">{reminder.dueDate}</p>
                    </div>
                    <Badge
                      className={
                        reminder.priority === "high"
                          ? "bg-red-100 text-red-700"
                          : reminder.priority === "medium"
                            ? "bg-yellow-100 text-yellow-700"
                            : "bg-green-100 text-green-700"
                      }
                    >
                      {reminder.priority}
                    </Badge>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Security Status */}
            <Card className="shadow-lg border-0 bg-gradient-to-r from-green-50 to-blue-50">
              <CardContent className="p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <Shield className="w-8 h-8 text-green-600" />
                  <div>
                    <h3 className="font-semibold text-gray-900">Account Secure</h3>
                    <p className="text-sm text-gray-600">Your data is protected</p>
                  </div>
                </div>
                <div className="space-y-2 text-sm text-gray-600">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span>Two-factor authentication enabled</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span>Data encrypted end-to-end</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span>HIPAA compliant</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
