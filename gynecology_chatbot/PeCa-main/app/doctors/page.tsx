"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Search, Filter, Star, Calendar, MapPin, Clock, DollarSign } from "lucide-react"
import { BookingModal } from "@/components/booking-modal"
import { Navigation } from "@/components/navigation"

interface Doctor {
  id: string
  name: string
  specialty: string
  degrees: string[]
  institute: string
  rating: number
  experience: number
  price: number
  image?: string
  location: string
  availability: string[]
}

const mockDoctors: Doctor[] = [
  {
    id: "1",
    name: "Dr. Priya Sharma",
    specialty: "Gynecologist & Obstetrician",
    degrees: ["MBBS", "MD", "FRCOG"],
    institute: "AIIMS Delhi",
    rating: 4.9,
    experience: 15,
    price: 1800,
    location: "Delhi",
    availability: ["Today", "Tomorrow"],
  },
  {
    id: "2",
    name: "Dr. Anjali Mehta",
    specialty: "Reproductive Endocrinologist",
    degrees: ["MBBS", "MS", "Fellowship"],
    institute: "KEM Hospital Mumbai",
    rating: 4.8,
    experience: 12,
    price: 2200,
    location: "Mumbai",
    availability: ["Tomorrow", "Next Week"],
  },
  {
    id: "3",
    name: "Dr. Kavitha Reddy",
    specialty: "Gynecologic Oncologist",
    degrees: ["MBBS", "MD", "DM"],
    institute: "CMC Vellore",
    rating: 4.7,
    experience: 18,
    price: 2500,
    location: "Bangalore",
    availability: ["Next Week"],
  },
  {
    id: "4",
    name: "Dr. Sunita Gupta",
    specialty: "Maternal-Fetal Medicine",
    degrees: ["MBBS", "MD", "Fellowship"],
    institute: "PGIMER Chandigarh",
    rating: 4.9,
    experience: 20,
    price: 2000,
    location: "Chandigarh",
    availability: ["Today", "Tomorrow"],
  },
]

export default function DoctorsPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedSpecialty, setSelectedSpecialty] = useState("")
  const [selectedRating, setSelectedRating] = useState("")
  const [selectedExperience, setSelectedExperience] = useState("")
  const [selectedPriceRange, setSelectedPriceRange] = useState("")
  const [sortBy, setSortBy] = useState("rating")
  const [selectedDoctor, setSelectedDoctor] = useState<Doctor | null>(null)
  const [isBookingOpen, setIsBookingOpen] = useState(false)

  const filteredDoctors = mockDoctors.filter((doctor) => {
    const matchesSearch =
      doctor.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doctor.specialty.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesSpecialty = !selectedSpecialty || doctor.specialty.includes(selectedSpecialty)
    const matchesRating = !selectedRating || doctor.rating >= Number.parseFloat(selectedRating)
    const matchesExperience = !selectedExperience || doctor.experience >= Number.parseInt(selectedExperience)
    const matchesPrice =
      !selectedPriceRange ||
      (selectedPriceRange === "low" && doctor.price <= 1500) ||
      (selectedPriceRange === "medium" && doctor.price > 1500 && doctor.price <= 2000) ||
      (selectedPriceRange === "high" && doctor.price > 2000)

    return matchesSearch && matchesSpecialty && matchesRating && matchesExperience && matchesPrice
  })

  const sortedDoctors = [...filteredDoctors].sort((a, b) => {
    switch (sortBy) {
      case "rating":
        return b.rating - a.rating
      case "experience":
        return b.experience - a.experience
      case "price":
        return a.price - b.price
      default:
        return 0
    }
  })

  const handleBookNow = (doctor: Doctor) => {
    setSelectedDoctor(doctor)
    setIsBookingOpen(true)
  }

  const resetFilters = () => {
    setSearchQuery("")
    setSelectedSpecialty("")
    setSelectedRating("")
    setSelectedExperience("")
    setSelectedPriceRange("")
    setSortBy("rating")
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Navigation />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-sm border p-6 mb-8">
          <div className="space-y-6">
            {/* Search Bar */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <Input
                placeholder="Search by name or specialty"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 h-12 text-lg"
              />
            </div>

            {/* Filters */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              <Select value={selectedSpecialty} onValueChange={setSelectedSpecialty}>
                <SelectTrigger>
                  <SelectValue placeholder="Specialty" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Gynecologist">Gynecologist</SelectItem>
                  <SelectItem value="Reproductive">Reproductive Endocrinologist</SelectItem>
                  <SelectItem value="Oncologist">Gynecologic Oncologist</SelectItem>
                  <SelectItem value="Maternal">Maternal-Fetal Medicine</SelectItem>
                </SelectContent>
              </Select>

              <Select value={selectedRating} onValueChange={setSelectedRating}>
                <SelectTrigger>
                  <SelectValue placeholder="Rating" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="4.5">4.5+ Stars</SelectItem>
                  <SelectItem value="4.0">4.0+ Stars</SelectItem>
                  <SelectItem value="3.5">3.5+ Stars</SelectItem>
                </SelectContent>
              </Select>

              <Select value={selectedExperience} onValueChange={setSelectedExperience}>
                <SelectTrigger>
                  <SelectValue placeholder="Experience" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="15">15+ Years</SelectItem>
                  <SelectItem value="10">10+ Years</SelectItem>
                  <SelectItem value="5">5+ Years</SelectItem>
                </SelectContent>
              </Select>

              <Select value={selectedPriceRange} onValueChange={setSelectedPriceRange}>
                <SelectTrigger>
                  <SelectValue placeholder="Price Range" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="low">₹ - ₹1500</SelectItem>
                  <SelectItem value="medium">₹₹ - ₹1500-2000</SelectItem>
                  <SelectItem value="high">₹₹₹ - ₹2000+</SelectItem>
                </SelectContent>
              </Select>

              <Button variant="outline" onClick={resetFilters} className="w-full">
                <Filter className="w-4 h-4 mr-2" />
                Reset Filters
              </Button>
            </div>

            {/* Sort */}
            <div className="flex items-center justify-between">
              <p className="text-gray-600">
                Showing {sortedDoctors.length} of {mockDoctors.length} doctors
              </p>
              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Sort by" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="rating">Highest Rating</SelectItem>
                  <SelectItem value="experience">Most Experience</SelectItem>
                  <SelectItem value="price">Lowest Price</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>

        {/* Doctors Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sortedDoctors.map((doctor) => (
            <Card key={doctor.id} className="hover:shadow-lg transition-shadow duration-300">
              <CardContent className="p-6">
                <div className="space-y-4">
                  {/* Doctor Header */}
                  <div className="flex items-start space-x-4">
                    <Avatar className="w-16 h-16">
                      <AvatarImage src={doctor.image || "/placeholder.svg"} />
                      <AvatarFallback className="bg-pink-100 text-pink-600 text-lg font-semibold">
                        {doctor.name
                          .split(" ")
                          .map((n) => n[0])
                          .join("")}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg font-semibold text-gray-900 truncate">{doctor.name}</h3>
                      <p className="text-sm text-gray-600">{doctor.specialty}</p>
                      <div className="flex items-center space-x-1 mt-1">
                        <Star className="w-4 h-4 text-yellow-400 fill-current" />
                        <span className="text-sm font-medium text-gray-900">{doctor.rating}</span>
                        <span className="text-sm text-gray-500">({Math.floor(Math.random() * 500) + 100} reviews)</span>
                      </div>
                    </div>
                  </div>

                  {/* Qualifications */}
                  <div className="space-y-2">
                    <div className="flex flex-wrap gap-1">
                      {doctor.degrees.map((degree, index) => (
                        <Badge key={index} variant="secondary" className="text-xs">
                          {degree}
                        </Badge>
                      ))}
                    </div>
                    <p className="text-sm text-gray-600">{doctor.institute}</p>
                  </div>

                  {/* Details */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center space-x-1 text-gray-600">
                        <Clock className="w-4 h-4" />
                        <span>{doctor.experience} years exp</span>
                      </div>
                      <div className="flex items-center space-x-1 text-gray-600">
                        <MapPin className="w-4 h-4" />
                        <span>{doctor.location}</span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-1">
                        <DollarSign className="w-4 h-4 text-green-600" />
                        <span className="text-lg font-semibold text-gray-900">₹{doctor.price}</span>
                      </div>
                      <div className="flex space-x-1">
                        {doctor.availability.map((slot, index) => (
                          <Badge key={index} variant="outline" className="text-xs text-green-600 border-green-600">
                            {slot}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Book Button */}
                  <Button
                    onClick={() => handleBookNow(doctor)}
                    className="w-full bg-pink-500 hover:bg-pink-600 text-white"
                  >
                    <Calendar className="w-4 h-4 mr-2" />
                    Book Now
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {sortedDoctors.length === 0 && (
          <div className="text-center py-12">
            <div className="w-24 h-24 bg-gray-100 rounded-full mx-auto flex items-center justify-center mb-4">
              <Search className="w-12 h-12 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No doctors found</h3>
            <p className="text-gray-600 mb-4">Try adjusting your search criteria or filters</p>
            <Button onClick={resetFilters} variant="outline">
              Reset Filters
            </Button>
          </div>
        )}
      </div>

      {/* Booking Modal */}
      {selectedDoctor && (
        <BookingModal
          doctor={selectedDoctor}
          isOpen={isBookingOpen}
          onClose={() => {
            setIsBookingOpen(false)
            setSelectedDoctor(null)
          }}
        />
      )}
    </div>
  )
}
