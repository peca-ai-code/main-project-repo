"use strict";
"use client";
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = DoctorsPage;
const react_1 = require("react");
const button_1 = require("@/components/ui/button");
const card_1 = require("@/components/ui/card");
const input_1 = require("@/components/ui/input");
const select_1 = require("@/components/ui/select");
const badge_1 = require("@/components/ui/badge");
const avatar_1 = require("@/components/ui/avatar");
const lucide_react_1 = require("lucide-react");
const booking_modal_1 = require("@/components/booking-modal");
const navigation_1 = require("@/components/navigation");
const mockDoctors = [
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
];
function DoctorsPage() {
    const [searchQuery, setSearchQuery] = (0, react_1.useState)("");
    const [selectedSpecialty, setSelectedSpecialty] = (0, react_1.useState)("");
    const [selectedRating, setSelectedRating] = (0, react_1.useState)("");
    const [selectedExperience, setSelectedExperience] = (0, react_1.useState)("");
    const [selectedPriceRange, setSelectedPriceRange] = (0, react_1.useState)("");
    const [sortBy, setSortBy] = (0, react_1.useState)("rating");
    const [selectedDoctor, setSelectedDoctor] = (0, react_1.useState)(null);
    const [isBookingOpen, setIsBookingOpen] = (0, react_1.useState)(false);
    const filteredDoctors = mockDoctors.filter((doctor) => {
        const matchesSearch = doctor.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            doctor.specialty.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesSpecialty = !selectedSpecialty || doctor.specialty.includes(selectedSpecialty);
        const matchesRating = !selectedRating || doctor.rating >= Number.parseFloat(selectedRating);
        const matchesExperience = !selectedExperience || doctor.experience >= Number.parseInt(selectedExperience);
        const matchesPrice = !selectedPriceRange ||
            (selectedPriceRange === "low" && doctor.price <= 1500) ||
            (selectedPriceRange === "medium" && doctor.price > 1500 && doctor.price <= 2000) ||
            (selectedPriceRange === "high" && doctor.price > 2000);
        return matchesSearch && matchesSpecialty && matchesRating && matchesExperience && matchesPrice;
    });
    const sortedDoctors = [...filteredDoctors].sort((a, b) => {
        switch (sortBy) {
            case "rating":
                return b.rating - a.rating;
            case "experience":
                return b.experience - a.experience;
            case "price":
                return a.price - b.price;
            default:
                return 0;
        }
    });
    const handleBookNow = (doctor) => {
        setSelectedDoctor(doctor);
        setIsBookingOpen(true);
    };
    const resetFilters = () => {
        setSearchQuery("");
        setSelectedSpecialty("");
        setSelectedRating("");
        setSelectedExperience("");
        setSelectedPriceRange("");
        setSortBy("rating");
    };
    return (<div className="min-h-screen bg-gray-50">
      {/* Header */}
      <navigation_1.Navigation />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-sm border p-6 mb-8">
          <div className="space-y-6">
            {/* Search Bar */}
            <div className="relative">
              <lucide_react_1.Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5"/>
              <input_1.Input placeholder="Search by name or specialty" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pl-10 h-12 text-lg"/>
            </div>

            {/* Filters */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              <select_1.Select value={selectedSpecialty} onValueChange={setSelectedSpecialty}>
                <select_1.SelectTrigger>
                  <select_1.SelectValue placeholder="Specialty"/>
                </select_1.SelectTrigger>
                <select_1.SelectContent>
                  <select_1.SelectItem value="Gynecologist">Gynecologist</select_1.SelectItem>
                  <select_1.SelectItem value="Reproductive">Reproductive Endocrinologist</select_1.SelectItem>
                  <select_1.SelectItem value="Oncologist">Gynecologic Oncologist</select_1.SelectItem>
                  <select_1.SelectItem value="Maternal">Maternal-Fetal Medicine</select_1.SelectItem>
                </select_1.SelectContent>
              </select_1.Select>

              <select_1.Select value={selectedRating} onValueChange={setSelectedRating}>
                <select_1.SelectTrigger>
                  <select_1.SelectValue placeholder="Rating"/>
                </select_1.SelectTrigger>
                <select_1.SelectContent>
                  <select_1.SelectItem value="4.5">4.5+ Stars</select_1.SelectItem>
                  <select_1.SelectItem value="4.0">4.0+ Stars</select_1.SelectItem>
                  <select_1.SelectItem value="3.5">3.5+ Stars</select_1.SelectItem>
                </select_1.SelectContent>
              </select_1.Select>

              <select_1.Select value={selectedExperience} onValueChange={setSelectedExperience}>
                <select_1.SelectTrigger>
                  <select_1.SelectValue placeholder="Experience"/>
                </select_1.SelectTrigger>
                <select_1.SelectContent>
                  <select_1.SelectItem value="15">15+ Years</select_1.SelectItem>
                  <select_1.SelectItem value="10">10+ Years</select_1.SelectItem>
                  <select_1.SelectItem value="5">5+ Years</select_1.SelectItem>
                </select_1.SelectContent>
              </select_1.Select>

              <select_1.Select value={selectedPriceRange} onValueChange={setSelectedPriceRange}>
                <select_1.SelectTrigger>
                  <select_1.SelectValue placeholder="Price Range"/>
                </select_1.SelectTrigger>
                <select_1.SelectContent>
                  <select_1.SelectItem value="low">₹ - ₹1500</select_1.SelectItem>
                  <select_1.SelectItem value="medium">₹₹ - ₹1500-2000</select_1.SelectItem>
                  <select_1.SelectItem value="high">₹₹₹ - ₹2000+</select_1.SelectItem>
                </select_1.SelectContent>
              </select_1.Select>

              <button_1.Button variant="outline" onClick={resetFilters} className="w-full">
                <lucide_react_1.Filter className="w-4 h-4 mr-2"/>
                Reset Filters
              </button_1.Button>
            </div>

            {/* Sort */}
            <div className="flex items-center justify-between">
              <p className="text-gray-600">
                Showing {sortedDoctors.length} of {mockDoctors.length} doctors
              </p>
              <select_1.Select value={sortBy} onValueChange={setSortBy}>
                <select_1.SelectTrigger className="w-48">
                  <select_1.SelectValue placeholder="Sort by"/>
                </select_1.SelectTrigger>
                <select_1.SelectContent>
                  <select_1.SelectItem value="rating">Highest Rating</select_1.SelectItem>
                  <select_1.SelectItem value="experience">Most Experience</select_1.SelectItem>
                  <select_1.SelectItem value="price">Lowest Price</select_1.SelectItem>
                </select_1.SelectContent>
              </select_1.Select>
            </div>
          </div>
        </div>

        {/* Doctors Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sortedDoctors.map((doctor) => (<card_1.Card key={doctor.id} className="hover:shadow-lg transition-shadow duration-300">
              <card_1.CardContent className="p-6">
                <div className="space-y-4">
                  {/* Doctor Header */}
                  <div className="flex items-start space-x-4">
                    <avatar_1.Avatar className="w-16 h-16">
                      <avatar_1.AvatarImage src={doctor.image || "/placeholder.svg"}/>
                      <avatar_1.AvatarFallback className="bg-pink-100 text-pink-600 text-lg font-semibold">
                        {doctor.name
                .split(" ")
                .map((n) => n[0])
                .join("")}
                      </avatar_1.AvatarFallback>
                    </avatar_1.Avatar>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-lg font-semibold text-gray-900 truncate">{doctor.name}</h3>
                      <p className="text-sm text-gray-600">{doctor.specialty}</p>
                      <div className="flex items-center space-x-1 mt-1">
                        <lucide_react_1.Star className="w-4 h-4 text-yellow-400 fill-current"/>
                        <span className="text-sm font-medium text-gray-900">{doctor.rating}</span>
                        <span className="text-sm text-gray-500">({Math.floor(Math.random() * 500) + 100} reviews)</span>
                      </div>
                    </div>
                  </div>

                  {/* Qualifications */}
                  <div className="space-y-2">
                    <div className="flex flex-wrap gap-1">
                      {doctor.degrees.map((degree, index) => (<badge_1.Badge key={index} variant="secondary" className="text-xs">
                          {degree}
                        </badge_1.Badge>))}
                    </div>
                    <p className="text-sm text-gray-600">{doctor.institute}</p>
                  </div>

                  {/* Details */}
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <div className="flex items-center space-x-1 text-gray-600">
                        <lucide_react_1.Clock className="w-4 h-4"/>
                        <span>{doctor.experience} years exp</span>
                      </div>
                      <div className="flex items-center space-x-1 text-gray-600">
                        <lucide_react_1.MapPin className="w-4 h-4"/>
                        <span>{doctor.location}</span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-1">
                        <lucide_react_1.DollarSign className="w-4 h-4 text-green-600"/>
                        <span className="text-lg font-semibold text-gray-900">₹{doctor.price}</span>
                      </div>
                      <div className="flex space-x-1">
                        {doctor.availability.map((slot, index) => (<badge_1.Badge key={index} variant="outline" className="text-xs text-green-600 border-green-600">
                            {slot}
                          </badge_1.Badge>))}
                      </div>
                    </div>
                  </div>

                  {/* Book Button */}
                  <button_1.Button onClick={() => handleBookNow(doctor)} className="w-full bg-pink-500 hover:bg-pink-600 text-white">
                    <lucide_react_1.Calendar className="w-4 h-4 mr-2"/>
                    Book Now
                  </button_1.Button>
                </div>
              </card_1.CardContent>
            </card_1.Card>))}
        </div>

        {sortedDoctors.length === 0 && (<div className="text-center py-12">
            <div className="w-24 h-24 bg-gray-100 rounded-full mx-auto flex items-center justify-center mb-4">
              <lucide_react_1.Search className="w-12 h-12 text-gray-400"/>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No doctors found</h3>
            <p className="text-gray-600 mb-4">Try adjusting your search criteria or filters</p>
            <button_1.Button onClick={resetFilters} variant="outline">
              Reset Filters
            </button_1.Button>
          </div>)}
      </div>

      {/* Booking Modal */}
      {selectedDoctor && (<booking_modal_1.BookingModal doctor={selectedDoctor} isOpen={isBookingOpen} onClose={() => {
                setIsBookingOpen(false);
                setSelectedDoctor(null);
            }}/>)}
    </div>);
}
