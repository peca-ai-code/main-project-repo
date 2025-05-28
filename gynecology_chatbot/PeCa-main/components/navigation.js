"use strict";
"use client";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Navigation = Navigation;
const react_1 = require("react");
const button_1 = require("@/components/ui/button");
const badge_1 = require("@/components/ui/badge");
const avatar_1 = require("@/components/ui/avatar");
const sheet_1 = require("@/components/ui/sheet");
const dropdown_menu_1 = require("@/components/ui/dropdown-menu");
const lucide_react_1 = require("lucide-react");
const link_1 = __importDefault(require("next/link"));
const image_1 = __importDefault(require("next/image"));
const navigation_1 = require("next/navigation");
function Navigation({ isLoggedIn = false, userName = "User" }) {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = (0, react_1.useState)(false);
    const pathname = (0, navigation_1.usePathname)();
    const navigationItems = [
        { href: "/", label: "Home", icon: lucide_react_1.Home },
        { href: "/chat", label: "AI Assistant", icon: lucide_react_1.MessageCircle },
        { href: "/doctors", label: "Find Doctors", icon: lucide_react_1.Calendar },
        { href: "/about", label: "About", icon: lucide_react_1.Info },
    ];
    const userNavigationItems = [
        { href: "/dashboard", label: "Dashboard", icon: lucide_react_1.Home },
        { href: "/chat", label: "AI Assistant", icon: lucide_react_1.MessageCircle },
        { href: "/doctors", label: "Find Doctors", icon: lucide_react_1.Calendar },
        { href: "/profile", label: "Profile", icon: lucide_react_1.User },
        { href: "/about", label: "About", icon: lucide_react_1.Info },
    ];
    const currentItems = isLoggedIn ? userNavigationItems : navigationItems;
    const isActive = (href) => {
        if (href === "/" && pathname === "/")
            return true;
        if (href !== "/" && pathname.startsWith(href))
            return true;
        return false;
    };
    return (<header className="bg-white/80 backdrop-blur-md shadow-sm border-b sticky top-0 z-50 transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <link_1.default href={isLoggedIn ? "/dashboard" : "/"} className="flex items-center space-x-4 group">
            <div className="relative transform group-hover:scale-105 transition-transform duration-300">
              <image_1.default src="/images/peca-light.png" alt="PECA Logo" width={120} height={40} className="h-10 w-auto" priority/>
            </div>
            {isLoggedIn && (<badge_1.Badge className="bg-gradient-to-r from-pink-500 to-blue-500 text-white animate-pulse">
                <lucide_react_1.Sparkles className="w-3 h-3 mr-1"/>
                Live
              </badge_1.Badge>)}
          </link_1.default>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {currentItems.map((item) => {
            const Icon = item.icon;
            return (<link_1.default key={item.href} href={item.href} className={`relative flex items-center space-x-2 px-3 py-2 rounded-lg font-medium transition-all duration-300 group ${isActive(item.href)
                    ? "text-pink-600 bg-pink-50"
                    : "text-gray-600 hover:text-pink-500 hover:bg-pink-50"}`}>
                  <Icon className="w-4 h-4"/>
                  <span>{item.label}</span>
                  {isActive(item.href) && (<div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1 h-1 bg-pink-500 rounded-full animate-pulse"></div>)}
                </link_1.default>);
        })}
          </nav>

          {/* Right Side Actions */}
          <div className="flex items-center space-x-4">
            {isLoggedIn ? (<>
                {/* Notifications */}
                <button_1.Button variant="ghost" size="sm" className="relative group">
                  <lucide_react_1.Bell className="w-5 h-5 group-hover:animate-bounce"/>
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-pulse"></span>
                </button_1.Button>

                {/* User Menu */}
                <dropdown_menu_1.DropdownMenu>
                  <dropdown_menu_1.DropdownMenuTrigger asChild>
                    <button_1.Button variant="ghost" className="relative h-10 w-10 rounded-full">
                      <avatar_1.Avatar className="h-10 w-10">
                        <avatar_1.AvatarFallback className="bg-gradient-to-r from-pink-500 to-blue-500 text-white">
                          {userName[0]}
                        </avatar_1.AvatarFallback>
                      </avatar_1.Avatar>
                    </button_1.Button>
                  </dropdown_menu_1.DropdownMenuTrigger>
                  <dropdown_menu_1.DropdownMenuContent className="w-56" align="end" forceMount>
                    <div className="flex items-center justify-start gap-2 p-2">
                      <div className="flex flex-col space-y-1 leading-none">
                        <p className="font-medium">{userName}</p>
                        <p className="w-[200px] truncate text-sm text-muted-foreground">demo@peca.com</p>
                      </div>
                    </div>
                    <dropdown_menu_1.DropdownMenuSeparator />
                    <dropdown_menu_1.DropdownMenuItem asChild>
                      <link_1.default href="/profile" className="flex items-center">
                        <lucide_react_1.User className="mr-2 h-4 w-4"/>
                        Profile
                      </link_1.default>
                    </dropdown_menu_1.DropdownMenuItem>
                    <dropdown_menu_1.DropdownMenuItem asChild>
                      <link_1.default href="/settings" className="flex items-center">
                        <lucide_react_1.Settings className="mr-2 h-4 w-4"/>
                        Settings
                      </link_1.default>
                    </dropdown_menu_1.DropdownMenuItem>
                    <dropdown_menu_1.DropdownMenuSeparator />
                    <dropdown_menu_1.DropdownMenuItem asChild>
                      <link_1.default href="/login" className="flex items-center text-red-600">
                        <lucide_react_1.LogOut className="mr-2 h-4 w-4"/>
                        Log out
                      </link_1.default>
                    </dropdown_menu_1.DropdownMenuItem>
                  </dropdown_menu_1.DropdownMenuContent>
                </dropdown_menu_1.DropdownMenu>
              </>) : (<>
                <link_1.default href="/login">
                  <button_1.Button variant="ghost" className="text-gray-600 hover:text-pink-500 font-medium">
                    Sign In
                  </button_1.Button>
                </link_1.default>
                <link_1.default href="/signup">
                  <button_1.Button className="bg-gradient-to-r from-pink-500 to-pink-600 hover:from-pink-600 hover:to-pink-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105">
                    Get Started
                  </button_1.Button>
                </link_1.default>
              </>)}

            {/* Mobile Menu */}
            <sheet_1.Sheet open={isMobileMenuOpen} onOpenChange={setIsMobileMenuOpen}>
              <sheet_1.SheetTrigger asChild>
                <button_1.Button variant="ghost" size="sm" className="md:hidden">
                  <lucide_react_1.Menu className="w-6 h-6"/>
                </button_1.Button>
              </sheet_1.SheetTrigger>
              <sheet_1.SheetContent side="right" className="w-80">
                <div className="flex flex-col h-full">
                  {/* Mobile Logo */}
                  <div className="flex items-center space-x-3 pb-6 border-b">
                    <image_1.default src="/images/peca-light.png" alt="PECA Logo" width={100} height={32} className="h-8 w-auto"/>
                    {isLoggedIn && (<badge_1.Badge className="bg-gradient-to-r from-pink-500 to-blue-500 text-white">
                        <lucide_react_1.Heart className="w-3 h-3 mr-1"/>
                        Live
                      </badge_1.Badge>)}
                  </div>

                  {/* Mobile Navigation */}
                  <nav className="flex-1 py-6">
                    <div className="space-y-2">
                      {currentItems.map((item) => {
            const Icon = item.icon;
            return (<link_1.default key={item.href} href={item.href} onClick={() => setIsMobileMenuOpen(false)} className={`flex items-center space-x-3 px-4 py-3 rounded-lg font-medium transition-all duration-300 ${isActive(item.href)
                    ? "text-pink-600 bg-pink-50 border-l-4 border-pink-500"
                    : "text-gray-600 hover:text-pink-500 hover:bg-pink-50"}`}>
                            <Icon className="w-5 h-5"/>
                            <span>{item.label}</span>
                          </link_1.default>);
        })}
                    </div>
                  </nav>

                  {/* Mobile User Section */}
                  {isLoggedIn && (<div className="border-t pt-6">
                      <div className="flex items-center space-x-3 px-4 py-3 mb-4">
                        <avatar_1.Avatar className="h-10 w-10">
                          <avatar_1.AvatarFallback className="bg-gradient-to-r from-pink-500 to-blue-500 text-white">
                            {userName[0]}
                          </avatar_1.AvatarFallback>
                        </avatar_1.Avatar>
                        <div>
                          <p className="font-medium text-gray-900">{userName}</p>
                          <p className="text-sm text-gray-500">demo@peca.com</p>
                        </div>
                      </div>
                      <div className="space-y-2">
                        <link_1.default href="/settings" onClick={() => setIsMobileMenuOpen(false)} className="flex items-center space-x-3 px-4 py-3 text-gray-600 hover:text-pink-500 hover:bg-pink-50 rounded-lg transition-colors">
                          <lucide_react_1.Settings className="w-5 h-5"/>
                          <span>Settings</span>
                        </link_1.default>
                        <link_1.default href="/login" onClick={() => setIsMobileMenuOpen(false)} className="flex items-center space-x-3 px-4 py-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                          <lucide_react_1.LogOut className="w-5 h-5"/>
                          <span>Log out</span>
                        </link_1.default>
                      </div>
                    </div>)}
                </div>
              </sheet_1.SheetContent>
            </sheet_1.Sheet>
          </div>
        </div>
      </div>
    </header>);
}
exports.default = Navigation;
