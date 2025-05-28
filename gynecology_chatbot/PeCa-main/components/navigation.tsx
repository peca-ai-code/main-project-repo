"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Menu, Home, MessageCircle, Calendar, User, Info, Settings, LogOut, Bell, Sparkles, Heart } from "lucide-react"
import Link from "next/link"
import Image from "next/image"
import { usePathname } from "next/navigation"

interface NavigationProps {
  isLoggedIn?: boolean
  userName?: string
}

export function Navigation({ isLoggedIn = false, userName = "User" }: NavigationProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const pathname = usePathname()

  const navigationItems = [
    { href: "/", label: "Home", icon: Home },
    { href: "/chat", label: "AI Assistant", icon: MessageCircle },
    { href: "/doctors", label: "Find Doctors", icon: Calendar },
    { href: "/about", label: "About", icon: Info },
  ]

  const userNavigationItems = [
    { href: "/dashboard", label: "Dashboard", icon: Home },
    { href: "/chat", label: "AI Assistant", icon: MessageCircle },
    { href: "/doctors", label: "Find Doctors", icon: Calendar },
    { href: "/profile", label: "Profile", icon: User },
    { href: "/about", label: "About", icon: Info },
  ]

  const currentItems = isLoggedIn ? userNavigationItems : navigationItems

  const isActive = (href: string) => {
    if (href === "/" && pathname === "/") return true
    if (href !== "/" && pathname.startsWith(href)) return true
    return false
  }

  return (
    <header className="bg-white/80 backdrop-blur-md shadow-sm border-b sticky top-0 z-50 transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <Link href={isLoggedIn ? "/dashboard" : "/"} className="flex items-center space-x-4 group">
            <div className="relative transform group-hover:scale-105 transition-transform duration-300">
              <Image
                src="/images/peca-light.png"
                alt="PECA Logo"
                width={120}
                height={40}
                className="h-10 w-auto"
                priority
              />
            </div>
            {isLoggedIn && (
              <Badge className="bg-gradient-to-r from-pink-500 to-blue-500 text-white animate-pulse">
                <Sparkles className="w-3 h-3 mr-1" />
                Live
              </Badge>
            )}
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {currentItems.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`relative flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-all duration-300 group ${
                    isActive(item.href)
                      ? "text-pink-600 bg-pink-50"
                      : "text-gray-600 hover:text-pink-500 hover:bg-pink-50"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                  {isActive(item.href) && (
                    <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1 h-1 bg-pink-500 rounded-full animate-pulse"></div>
                  )}
                </Link>
              )
            })}
          </nav>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-4">
            {isLoggedIn ? (
              <>
                {/* Notifications */}
                <Button variant="ghost" size="sm" className="relative group">
                  <Bell className="w-5 h-5 group-hover:animate-bounce" />
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-pulse"></span>
                </Button>

                {/* User Menu */}
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" className="relative h-10 w-10 rounded-full">
                      <Avatar className="h-10 w-10">
                        <AvatarFallback className="bg-gradient-to-r from-pink-500 to-blue-500 text-white">
                          {userName[0]}
                        </AvatarFallback>
                      </Avatar>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent className="w-56" align="end" forceMount>
                    <div className="flex items-center justify-start gap-2 p-2">
                      <div className="flex flex-col space-y-1 leading-none">
                        <p className="font-medium">{userName}</p>
                        <p className="w-[200px] truncate text-sm text-muted-foreground">demo@peca.com</p>
                      </div>
                    </div>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem asChild>
                      <Link href="/profile" className="flex items-center">
                        <User className="mr-2 h-4 w-4" />
                        Profile
                      </Link>
                    </DropdownMenuItem>
                    <DropdownMenuItem asChild>
                      <Link href="/settings" className="flex items-center">
                        <Settings className="mr-2 h-4 w-4" />
                        Settings
                      </Link>
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem asChild>
                      <Link href="/login" className="flex items-center text-red-600">
                        <LogOut className="mr-2 h-4 w-4" />
                        Log out
                      </Link>
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </>
            ) : (
              <>
                <Link href="/login">
                  <Button variant="ghost" className="text-gray-600 hover:text-pink-500 font-medium">
                    Sign In
                  </Button>
                </Link>
                <Link href="/signup">
                  <Button className="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
                    Get Started
                  </Button>
                </Link>
              </>
            )}

            {/* Mobile Menu */}
            <Sheet open={isMobileMenuOpen} onOpenChange={setIsMobileMenuOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="sm" className="md:hidden">
                  <Menu className="w-6 h-6" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-80">
                <div className="flex flex-col h-full">
                  {/* Mobile Logo */}
                  <div className="flex items-center space-x-3 pb-6 border-b">
                    <Image
                      src="/images/peca-light.png"
                      alt="PECA Logo"
                      width={100}
                      height={32}
                      className="h-8 w-auto"
                    />
                    {isLoggedIn && (
                      <Badge className="bg-gradient-to-r from-pink-500 to-blue-500 text-white">
                        <Heart className="w-3 h-3 mr-1" />
                        Live
                      </Badge>
                    )}
                  </div>

                  {/* Mobile Navigation */}
                  <nav className="flex-1 py-6">
                    <div className="space-y-2">
                      {currentItems.map((item) => {
                        const Icon = item.icon
                        return (
                          <Link
                            key={item.href}
                            href={item.href}
                            onClick={() => setIsMobileMenuOpen(false)}
                            className={`flex items-center space-x-3 px-4 py-3 rounded-lg font-medium transition-all duration-300 ${
                              isActive(item.href)
                                ? "text-pink-600 bg-pink-50 border-l-4 border-pink-500"
                                : "text-gray-600 hover:text-pink-500 hover:bg-pink-50"
                            }`}
                          >
                            <Icon className="w-5 h-5" />
                            <span>{item.label}</span>
                          </Link>
                        )
                      })}
                    </div>
                  </nav>

                  {/* Mobile User Section */}
                  {isLoggedIn && (
                    <div className="border-t pt-6">
                      <div className="flex items-center space-x-3 px-4 py-3 mb-4">
                        <Avatar className="h-10 w-10">
                          <AvatarFallback className="bg-gradient-to-r from-pink-500 to-blue-500 text-white">
                            {userName[0]}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="font-medium text-gray-900">{userName}</p>
                          <p className="text-sm text-gray-500">demo@peca.com</p>
                        </div>
                      </div>
                      <div className="space-y-2">
                        <Link
                          href="/settings"
                          onClick={() => setIsMobileMenuOpen(false)}
                          className="flex items-center space-x-3 px-4 py-3 text-gray-600 hover:text-pink-500 hover:bg-pink-50 rounded-lg transition-colors"
                        >
                          <Settings className="w-5 h-5" />
                          <span>Settings</span>
                        </Link>
                        <Link
                          href="/login"
                          onClick={() => setIsMobileMenuOpen(false)}
                          className="flex items-center space-x-3 px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        >
                          <LogOut className="w-5 h-5" />
                          <span>Log out</span>
                        </Link>
                      </div>
                    </div>
                  )}
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Navigation
