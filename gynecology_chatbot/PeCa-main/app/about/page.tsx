import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Heart, Users, Shield, Globe, Sparkles, CheckCircle, ArrowRight, MessageCircle, Calendar } from "lucide-react"
import Link from "next/link"
import { Navigation } from "@/components/navigation"

export default function AboutPage() {
  const stats = [
    { number: "50,000+", label: "Women Served", icon: Users },
    { number: "500+", label: "Certified Doctors", icon: Heart },
    { number: "1M+", label: "AI Consultations", icon: MessageCircle },
    { number: "99.9%", label: "Uptime", icon: Shield },
  ]

  const features = [
    {
      icon: MessageCircle,
      title: "AI-Powered Health Assistant",
      description:
        "Get instant, personalized health insights and recommendations 24/7 with our advanced AI technology.",
      benefits: ["24/7 Availability", "Symptom Analysis", "Health Education", "Personalized Recommendations"],
    },
    {
      icon: Users,
      title: "Expert Gynecologists",
      description: "Connect with board-certified specialists who understand your unique reproductive health needs.",
      benefits: ["Board Certified", "Video Consultations", "Secure Platform", "Expert Care"],
    },
    {
      icon: Calendar,
      title: "Smart Appointment Booking",
      description: "Schedule appointments effortlessly with our intelligent booking system and real-time availability.",
      benefits: ["Real-time Scheduling", "Instant Confirmation", "Reminder Alerts", "Easy Rescheduling"],
    },
    {
      icon: Shield,
      title: "Privacy & Security",
      description: "Your health data is protected with enterprise-grade encryption and HIPAA compliance.",
      benefits: ["End-to-end Encryption", "HIPAA Compliant", "Secure Storage", "Privacy First"],
    },
  ]

  const team = [
    {
      name: "Dr. Sarah Chen",
      role: "Chief Medical Officer",
      image: "/placeholder.svg?height=300&width=300",
      bio: "Board-certified gynecologist with 15+ years of experience in women's health.",
    },
    {
      name: "Alex Rodriguez",
      role: "CEO & Co-Founder",
      image: "/placeholder.svg?height=300&width=300",
      bio: "Former healthcare technology executive passionate about improving women's health access.",
    },
    {
      name: "Dr. Priya Patel",
      role: "Head of AI Research",
      image: "/placeholder.svg?height=300&width=300",
      bio: "AI researcher specializing in healthcare applications and machine learning.",
    },
    {
      name: "Maria Santos",
      role: "Head of Product",
      image: "/placeholder.svg?height=300&width=300",
      bio: "Product leader focused on creating intuitive healthcare experiences.",
    },
  ]

  const values = [
    {
      icon: Heart,
      title: "Empathy First",
      description:
        "We understand that women's health is personal and sensitive. Every interaction is designed with empathy and care.",
    },
    {
      icon: Shield,
      title: "Privacy & Trust",
      description:
        "Your health data is sacred. We maintain the highest standards of privacy and security in everything we do.",
    },
    {
      icon: Sparkles,
      title: "Innovation",
      description:
        "We leverage cutting-edge AI and technology to make quality healthcare more accessible and personalized.",
    },
    {
      icon: Globe,
      title: "Accessibility",
      description:
        "Healthcare should be available to everyone, everywhere. We're breaking down barriers to quality care.",
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-blue-50">
      <Navigation />

      {/* Hero Section */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-pink-200 rounded-full opacity-20 animate-pulse"></div>
          <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-blue-200 rounded-full opacity-20 animate-pulse delay-1000"></div>
        </div>

        <div className="max-w-7xl mx-auto relative">
          <div className="text-center space-y-8">
            <Badge className="bg-gradient-to-r from-pink-500 to-blue-500 text-white px-6 py-3 text-lg">
              <Heart className="w-5 h-5 mr-2" />
              About PECA
            </Badge>

            <h1 className="text-5xl lg:text-7xl font-bold text-gray-900 leading-tight">
              Revolutionizing{" "}
              <span className="bg-gradient-to-r from-pink-500 to-blue-500 bg-clip-text text-transparent">
                Women's Health
              </span>
            </h1>

            <p className="text-xl lg:text-2xl text-gray-600 leading-relaxed max-w-4xl mx-auto">
              PECA is on a mission to make quality reproductive healthcare accessible to every woman through innovative
              AI technology and expert medical care.
            </p>

            <div className="flex flex-col sm:flex-row gap-6 justify-center">
              <Link href="/signup">
                <Button
                  size="lg"
                  className="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 text-white px-8 py-6 text-lg shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105"
                >
                  Join PECA Today
                  <ArrowRight className="w-6 h-6 ml-3" />
                </Button>
              </Link>
              <Link href="/chat">
                <Button
                  size="lg"
                  variant="outline"
                  className="border-2 border-blue-500 text-blue-600 hover:bg-blue-50 px-8 py-6 text-lg shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
                >
                  Try AI Assistant
                  <Sparkles className="w-6 h-6 ml-3" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            {stats.map((stat, index) => {
              const Icon = stat.icon
              return (
                <div key={index} className="text-center group">
                  <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-blue-500 rounded-full mx-auto mb-4 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <div className="text-4xl font-bold text-gray-900 mb-2">{stat.number}</div>
                  <div className="text-gray-600 font-medium">{stat.label}</div>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 bg-gradient-to-r from-pink-500 to-blue-500 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl lg:text-5xl font-bold mb-8">Our Mission</h2>
          <p className="text-xl lg:text-2xl leading-relaxed mb-8">
            To democratize access to quality reproductive healthcare by combining the expertise of certified
            gynecologists with the power of artificial intelligence, ensuring every woman receives personalized,
            compassionate care when and where she needs it.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Badge className="bg-white/20 text-white border-white/30 px-4 py-2">
              <CheckCircle className="w-4 h-4 mr-2" />
              Accessible Healthcare
            </Badge>
            <Badge className="bg-white/20 text-white border-white/30 px-4 py-2">
              <CheckCircle className="w-4 h-4 mr-2" />
              AI-Powered Insights
            </Badge>
            <Badge className="bg-white/20 text-white border-white/30 px-4 py-2">
              <CheckCircle className="w-4 h-4 mr-2" />
              Expert Care
            </Badge>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">How PECA Works</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our platform combines cutting-edge technology with human expertise to provide comprehensive reproductive
              health support.
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <Card
                  key={index}
                  className="group border-0 shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-2"
                >
                  <CardContent className="p-8">
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 bg-gradient-to-r from-pink-500 to-blue-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                        <Icon className="w-6 h-6 text-white" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                        <p className="text-gray-600 mb-4 leading-relaxed">{feature.description}</p>
                        <div className="grid grid-cols-2 gap-2">
                          {feature.benefits.map((benefit, idx) => (
                            <div key={idx} className="flex items-center space-x-2">
                              <CheckCircle className="w-4 h-4 text-green-500" />
                              <span className="text-sm text-gray-600">{benefit}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">Our Values</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              These core values guide everything we do at PECA, from product development to patient care.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => {
              const Icon = value.icon
              return (
                <div key={index} className="text-center group">
                  <div className="w-16 h-16 bg-gradient-to-r from-pink-500 to-blue-500 rounded-2xl mx-auto mb-6 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-4">{value.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{value.description}</p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">Meet Our Team</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our diverse team of healthcare professionals, technologists, and researchers is dedicated to improving
              women's health outcomes.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {team.map((member, index) => (
              <Card key={index} className="group border-0 shadow-lg hover:shadow-xl transition-all duration-300">
                <CardContent className="p-6 text-center">
                  <div className="w-24 h-24 bg-gradient-to-r from-pink-500 to-blue-500 rounded-full mx-auto mb-4 flex items-center justify-center group-hover:scale-105 transition-transform duration-300">
                    <span className="text-white text-2xl font-bold">
                      {member.name
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold text-gray-900 mb-1">{member.name}</h3>
                  <p className="text-pink-600 font-medium mb-3">{member.role}</p>
                  <p className="text-sm text-gray-600 leading-relaxed">{member.bio}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-pink-500 to-blue-500">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <div className="space-y-8">
            <h2 className="text-4xl lg:text-5xl font-bold text-white leading-tight">
              Ready to Transform Your Health Journey?
            </h2>
            <p className="text-xl text-pink-100 max-w-3xl mx-auto">
              Join thousands of women who trust PECA for their reproductive health needs. Start your journey today.
            </p>
            <div className="flex flex-col sm:flex-row gap-6 justify-center">
              <Link href="/signup">
                <Button
                  size="lg"
                  className="bg-white text-pink-600 hover:bg-gray-50 px-10 py-6 text-xl font-semibold shadow-2xl hover:shadow-3xl transition-all duration-300 hover:scale-105"
                >
                  Get Started Free
                  <ArrowRight className="w-6 h-6 ml-3" />
                </Button>
              </Link>
              <Link href="/doctors">
                <Button
                  size="lg"
                  variant="outline"
                  className="border-2 border-white text-white hover:bg-white hover:text-pink-500 px-10 py-6 text-xl font-semibold"
                >
                  Find a Doctor
                  <Users className="w-6 h-6 ml-3" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
