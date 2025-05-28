import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import {
  Heart,
  MessageCircle,
  Calendar,
  Shield,
  Star,
  Users,
  ArrowRight,
  Sparkles,
  CheckCircle,
  Play,
} from "lucide-react"
import Link from "next/link"
import Image from "next/image"
import Navigation from "@/components/navigation"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-blue-50">
      {/* Header */}
      <Navigation />

      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-pink-200 rounded-full opacity-20 animate-pulse"></div>
          <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-blue-200 rounded-full opacity-20 animate-pulse delay-1000"></div>
        </div>

        <div className="max-w-7xl mx-auto relative">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-8 animate-fade-in">
              <div className="space-y-6">
                <Badge className="bg-gradient-to-r from-pink-500 to-blue-500 text-white px-4 py-2 text-sm font-medium">
                  <Heart className="w-4 h-4 mr-2" />
                  Trusted by 50,000+ Women
                </Badge>

                <h1 className="text-5xl lg:text-7xl font-bold text-gray-900 leading-tight">
                  Your{" "}
                  <span className="bg-gradient-to-r from-pink-500 to-blue-500 bg-clip-text text-transparent">
                    Reproductive Health
                  </span>{" "}
                  Partner
                </h1>

                <p className="text-xl lg:text-2xl text-gray-600 leading-relaxed max-w-2xl">
                  Connect with certified gynecologists, get AI-powered health insights, and take control of your
                  reproductive wellness journey with PECA.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <Link href="/login" className="group">
                  <Button
                    size="lg"
                    className="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 text-white px-8 py-6 text-lg shadow-xl hover:shadow-2xl transition-all duration-300 group-hover:scale-105"
                  >
                    <MessageCircle className="w-6 h-6 mr-3" />
                    Try Demo Login
                    <Sparkles className="w-5 h-5 ml-2 group-hover:animate-spin" />
                  </Button>
                </Link>

                <Link href="/doctors">
                  <Button
                    size="lg"
                    variant="outline"
                    className="border-2 border-blue-500 text-blue-600 hover:bg-blue-50 px-8 py-6 text-lg shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
                  >
                    <Calendar className="w-6 h-6 mr-3" />
                    Book Consultation
                  </Button>
                </Link>
              </div>

              {/* Trust Indicators */}
              <div className="flex flex-wrap items-center gap-8 pt-8">
                <div className="flex items-center space-x-3">
                  <div className="flex -space-x-2">
                    {[1, 2, 3, 4, 5].map((i) => (
                      <div
                        key={i}
                        className="w-10 h-10 bg-gradient-to-r from-pink-400 to-blue-400 rounded-full border-3 border-white shadow-lg"
                      ></div>
                    ))}
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-gray-900">50,000+ Happy Users</p>
                    <p className="text-xs text-gray-600">Join our community</p>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    {[1, 2, 3, 4, 5].map((i) => (
                      <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-gray-900">4.9/5 Rating</p>
                    <p className="text-xs text-gray-600">From 10,000+ reviews</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Hero Visual */}
            <div className="relative lg:pl-8">
              <div className="relative z-10 bg-white rounded-3xl shadow-2xl p-8 transform hover:scale-105 transition-transform duration-500">
                <div className="aspect-square bg-gradient-to-br from-pink-100 via-white to-blue-100 rounded-2xl flex items-center justify-center relative overflow-hidden">
                  {/* Demo Login Preview */}
                  <div className="absolute inset-4 bg-white rounded-xl shadow-lg p-6 flex flex-col justify-center">
                    <div className="text-center space-y-4">
                      <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-blue-500 rounded-full mx-auto flex items-center justify-center">
                        <Heart className="w-8 h-8 text-white" />
                      </div>
                      <h3 className="text-lg font-bold text-gray-900">Demo Login Ready</h3>
                      <p className="text-sm text-gray-600">Experience PECA's features instantly</p>
                      <Link href="/login">
                        <Button className="bg-gradient-to-r from-pink-500 to-blue-500 text-white">
                          <Play className="w-4 h-4 mr-2" />
                          Try Now
                        </Button>
                      </Link>
                    </div>
                  </div>
                </div>
              </div>

              {/* Floating Elements */}
              <div className="absolute -top-6 -right-6 w-24 h-24 bg-gradient-to-r from-pink-400 to-pink-500 rounded-full opacity-80 animate-bounce"></div>
              <div className="absolute -bottom-6 -left-6 w-32 h-32 bg-gradient-to-r from-blue-400 to-blue-500 rounded-full opacity-60 animate-pulse"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center space-y-6 mb-20">
            <Badge className="bg-gradient-to-r from-pink-500 to-blue-500 text-white px-4 py-2">Why Choose PECA?</Badge>
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900">
              Comprehensive Care at Your{" "}
              <span className="bg-gradient-to-r from-pink-500 to-blue-500 bg-clip-text text-transparent">
                Fingertips
              </span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              PECA combines cutting-edge AI technology with expert medical care to provide you with personalized
              reproductive health support.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: MessageCircle,
                title: "AI Health Assistant",
                description: "Get instant, personalized health insights and recommendations 24/7 with our advanced AI.",
                color: "pink",
                features: ["24/7 Availability", "Symptom Analysis", "Health Education"],
              },
              {
                icon: Users,
                title: "Expert Gynecologists",
                description: "Connect with board-certified specialists who understand your unique health needs.",
                color: "blue",
                features: ["Verified Doctors", "Video Consultations", "Secure Platform"],
              },
              {
                icon: Calendar,
                title: "Smart Booking",
                description: "Schedule appointments effortlessly with our intelligent booking system.",
                color: "green",
                features: ["Real-time Availability", "Instant Confirmation", "Reminder Alerts"],
              },
              {
                icon: Shield,
                title: "Privacy & Security",
                description: "Your health data is protected with enterprise-grade encryption and security.",
                color: "purple",
                features: ["End-to-end Encryption", "HIPAA Compliant", "Secure Storage"],
              },
              {
                icon: Heart,
                title: "Personalized Care",
                description: "Receive tailored health recommendations based on your unique profile and history.",
                color: "pink",
                features: ["Custom Plans", "Health Tracking", "Progress Monitoring"],
              },
              {
                icon: Star,
                title: "Proven Results",
                description: "Join thousands of women who have improved their health with PECA's guidance.",
                color: "yellow",
                features: ["50k+ Users", "4.9★ Rating", "Proven Outcomes"],
              },
            ].map((feature, index) => (
              <Card
                key={index}
                className="group border-0 shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-2 bg-gradient-to-br from-white to-gray-50"
              >
                <CardContent className="p-8 space-y-6">
                  <div
                    className={`w-16 h-16 rounded-2xl flex items-center justify-center ${
                      feature.color === "pink"
                        ? "bg-gradient-to-r from-pink-100 to-pink-200"
                        : feature.color === "blue"
                          ? "bg-gradient-to-r from-blue-100 to-blue-200"
                          : feature.color === "green"
                            ? "bg-gradient-to-r from-green-100 to-green-200"
                            : feature.color === "purple"
                              ? "bg-gradient-to-r from-purple-100 to-purple-200"
                              : feature.color === "yellow"
                                ? "bg-gradient-to-r from-yellow-100 to-yellow-200"
                                : "bg-gray-100"
                    } group-hover:scale-110 transition-transform duration-300`}
                  >
                    <feature.icon
                      className={`w-8 h-8 ${
                        feature.color === "pink"
                          ? "text-pink-600"
                          : feature.color === "blue"
                            ? "text-blue-600"
                            : feature.color === "green"
                              ? "text-green-600"
                              : feature.color === "purple"
                                ? "text-purple-600"
                                : feature.color === "yellow"
                                  ? "text-yellow-600"
                                  : "text-gray-600"
                      }`}
                    />
                  </div>

                  <div className="space-y-3">
                    <h3 className="text-xl font-bold text-gray-900 group-hover:text-pink-600 transition-colors">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 leading-relaxed">{feature.description}</p>
                  </div>

                  <div className="space-y-2">
                    {feature.features.map((item, idx) => (
                      <div key={idx} className="flex items-center space-x-2">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span className="text-sm text-gray-600">{item}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Demo CTA Section */}
      <section className="py-24 bg-gradient-to-r from-pink-500 via-pink-600 to-blue-600 relative overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-pink-500/20 to-blue-500/20"></div>

        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="space-y-8">
            <Badge className="bg-white/20 text-white border-white/30 px-6 py-3 text-lg">
              <Sparkles className="w-5 h-5 mr-2" />
              Demo Available Now
            </Badge>

            <h2 className="text-4xl lg:text-6xl font-bold text-white leading-tight">
              Experience PECA's Power
              <br />
              <span className="text-pink-200">Try Our Demo Login</span>
            </h2>

            <p className="text-xl lg:text-2xl text-pink-100 max-w-3xl mx-auto">
              No registration required. Explore all features instantly with our interactive demo.
            </p>

            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
              <Link href="/login">
                <Button
                  size="lg"
                  className="bg-white text-pink-600 hover:bg-gray-50 px-10 py-6 text-xl font-semibold shadow-2xl hover:shadow-3xl transition-all duration-300 hover:scale-105"
                >
                  <Play className="w-6 h-6 mr-3" />
                  Launch Demo
                  <ArrowRight className="w-6 h-6 ml-3" />
                </Button>
              </Link>

              <div className="flex items-center space-x-4 text-white">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-green-300" />
                  <span>No signup needed</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-green-300" />
                  <span>Full feature access</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="space-y-6">
              <div className="flex items-center space-x-3">
                <Image src="/images/peca-dark.png" alt="PECA Logo" width={120} height={40} className="h-8 w-auto" />
              </div>
              <p className="text-gray-400 leading-relaxed">
                Empowering women with accessible, professional reproductive health care through innovative technology.
              </p>
              <div className="flex space-x-4">
                <div className="w-10 h-10 bg-pink-600 rounded-full flex items-center justify-center hover:bg-pink-700 transition-colors cursor-pointer">
                  <span className="text-sm font-bold">f</span>
                </div>
                <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center hover:bg-blue-700 transition-colors cursor-pointer">
                  <span className="text-sm font-bold">t</span>
                </div>
                <div className="w-10 h-10 bg-pink-600 rounded-full flex items-center justify-center hover:bg-pink-700 transition-colors cursor-pointer">
                  <span className="text-sm font-bold">in</span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Services</h3>
              <ul className="space-y-3 text-gray-400">
                <li>
                  <Link href="/chat" className="hover:text-white transition-colors">
                    AI Health Assistant
                  </Link>
                </li>
                <li>
                  <Link href="/doctors" className="hover:text-white transition-colors">
                    Find Gynecologists
                  </Link>
                </li>
                <li>
                  <Link href="/appointments" className="hover:text-white transition-colors">
                    Book Appointments
                  </Link>
                </li>
                <li>
                  <Link href="/health-tracker" className="hover:text-white transition-colors">
                    Health Tracking
                  </Link>
                </li>
              </ul>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Support</h3>
              <ul className="space-y-3 text-gray-400">
                <li>
                  <Link href="/help" className="hover:text-white transition-colors">
                    Help Center
                  </Link>
                </li>
                <li>
                  <Link href="/contact" className="hover:text-white transition-colors">
                    Contact Support
                  </Link>
                </li>
                <li>
                  <Link href="/privacy" className="hover:text-white transition-colors">
                    Privacy Policy
                  </Link>
                </li>
                <li>
                  <Link href="/terms" className="hover:text-white transition-colors">
                    Terms of Service
                  </Link>
                </li>
              </ul>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Company</h3>
              <ul className="space-y-3 text-gray-400">
                <li>
                  <Link href="/about" className="hover:text-white transition-colors">
                    About PECA
                  </Link>
                </li>
                <li>
                  <Link href="/careers" className="hover:text-white transition-colors">
                    Careers
                  </Link>
                </li>
                <li>
                  <Link href="/blog" className="hover:text-white transition-colors">
                    Health Blog
                  </Link>
                </li>
                <li>
                  <Link href="/press" className="hover:text-white transition-colors">
                    Press Kit
                  </Link>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-12 pt-8">
            <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
              <p className="text-gray-400">&copy; 2024 PECA. All rights reserved.</p>
              <div className="flex items-center space-x-6 text-gray-400">
                <span>🔒 HIPAA Compliant</span>
                <span>🛡️ SOC 2 Certified</span>
                <span>⭐ 4.9/5 Rating</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
