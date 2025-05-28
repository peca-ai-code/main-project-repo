"use strict";
"use client";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = LoginPage;
const react_1 = require("react");
const button_1 = require("@/components/ui/button");
const card_1 = require("@/components/ui/card");
const input_1 = require("@/components/ui/input");
const label_1 = require("@/components/ui/label");
const checkbox_1 = require("@/components/ui/checkbox");
const badge_1 = require("@/components/ui/badge");
const lucide_react_1 = require("lucide-react");
const link_1 = __importDefault(require("next/link"));
const image_1 = __importDefault(require("next/image"));
const navigation_1 = require("@/components/navigation");
function LoginPage() {
    const [showPassword, setShowPassword] = (0, react_1.useState)(false);
    const [email, setEmail] = (0, react_1.useState)("demo@peca.com");
    const [password, setPassword] = (0, react_1.useState)("demo123");
    const [rememberMe, setRememberMe] = (0, react_1.useState)(false);
    const [isLoading, setIsLoading] = (0, react_1.useState)(false);
    const handleLogin = (e) => __awaiter(this, void 0, void 0, function* () {
        e.preventDefault();
        setIsLoading(true);
        // Simulate login process
        setTimeout(() => {
            setIsLoading(false);
            // Redirect to dashboard
            window.location.href = "/dashboard";
        }, 2000);
    });
    const handleDemoLogin = () => {
        setEmail("demo@peca.com");
        setPassword("demo123");
        setRememberMe(true);
    };
    return (<div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-blue-50 flex flex-col">
      <navigation_1.Navigation />
      <div className="flex-grow flex">
        {/* Left Side - Enhanced Branding */}
        <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-pink-500 via-pink-600 to-blue-600 p-12 flex-col justify-center relative overflow-hidden">
          {/* Background Elements */}
          <div className="absolute inset-0 bg-black opacity-10"></div>
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-white rounded-full opacity-10 animate-pulse"></div>
          <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-white rounded-full opacity-5 animate-pulse delay-1000"></div>

          <div className="max-w-md relative z-10">
            <div className="flex items-center space-x-4 mb-8">
              <image_1.default src="/images/peca-dark.png" alt="PECA Logo" width={150} height={50} className="h-12 w-auto"/>
              <badge_1.Badge className="bg-white/20 text-white border-white/30">
                <lucide_react_1.Sparkles className="w-3 h-3 mr-1"/>
                Demo Ready
              </badge_1.Badge>
            </div>

            <h1 className="text-4xl lg:text-5xl font-bold text-white mb-6 leading-tight">
              Welcome Back to Your
              <span className="block text-pink-200">Health Journey</span>
            </h1>

            <p className="text-xl text-pink-100 mb-8 leading-relaxed">
              Continue your personalized reproductive health care with PECA's trusted platform.
            </p>

            <div className="space-y-6">
              <div className="flex items-center space-x-4 text-white">
                <div className="w-12 h-12 bg-white bg-opacity-20 rounded-xl flex items-center justify-center">
                  <lucide_react_1.Shield className="w-6 h-6"/>
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Secure & Private</h3>
                  <p className="text-pink-100 text-sm">Your health data is protected with enterprise-grade security</p>
                </div>
              </div>

              <div className="flex items-center space-x-4 text-white">
                <div className="w-12 h-12 bg-white bg-opacity-20 rounded-xl flex items-center justify-center">
                  <lucide_react_1.Heart className="w-6 h-6"/>
                </div>
                <div>
                  <h3 className="font-semibold text-lg">AI-Powered Insights</h3>
                  <p className="text-pink-100 text-sm">Get personalized health recommendations 24/7</p>
                </div>
              </div>

              <div className="flex items-center space-x-4 text-white">
                <div className="w-12 h-12 bg-white bg-opacity-20 rounded-xl flex items-center justify-center">
                  <lucide_react_1.Users className="w-6 h-6"/>
                </div>
                <div>
                  <h3 className="font-semibold text-lg">Expert Gynecologists</h3>
                  <p className="text-pink-100 text-sm">Connect with board-certified specialists instantly</p>
                </div>
              </div>
            </div>

            <div className="mt-8 p-6 bg-white/10 rounded-2xl backdrop-blur-sm">
              <div className="flex items-center space-x-3 mb-3">
                <lucide_react_1.Play className="w-5 h-5 text-white"/>
                <span className="text-white font-semibold">Demo Credentials</span>
              </div>
              <div className="space-y-2 text-sm text-pink-100">
                <p>
                  <strong>Email:</strong> demo@peca.com
                </p>
                <p>
                  <strong>Password:</strong> demo123
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Side - Enhanced Login Form */}
        <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
          <card_1.Card className="w-full max-w-md shadow-2xl border-0 bg-white/80 backdrop-blur-sm">
            <card_1.CardHeader className="text-center space-y-4 pb-8">
              <div className="lg:hidden flex items-center justify-center space-x-3 mb-4">
                <image_1.default src="/images/peca-light.png" alt="PECA Logo" width={120} height={40} className="h-10 w-auto"/>
              </div>

              <div className="space-y-2">
                <card_1.CardTitle className="text-3xl font-bold bg-gradient-to-r from-pink-600 to-blue-600 bg-clip-text text-transparent">
                  Welcome Back
                </card_1.CardTitle>
                <p className="text-gray-600">Sign in to continue your health journey</p>
              </div>

              {/* Demo Banner */}
              <div className="bg-gradient-to-r from-pink-50 to-blue-50 border border-pink-200 rounded-xl p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <lucide_react_1.Play className="w-5 h-5 text-pink-600"/>
                    <span className="text-sm font-semibold text-pink-700">Demo Mode Available</span>
                  </div>
                  <button_1.Button onClick={handleDemoLogin} size="sm" className="bg-gradient-to-r from-pink-500 to-blue-500 text-white hover:from-pink-600 hover:to-blue-600">
                    Use Demo
                  </button_1.Button>
                </div>
                <p className="text-xs text-gray-600 mt-2">Try all features instantly without registration</p>
              </div>
            </card_1.CardHeader>

            <card_1.CardContent className="space-y-6">
              <form onSubmit={handleLogin} className="space-y-6">
                <div className="space-y-2">
                  <label_1.Label htmlFor="email" className="text-gray-700 font-medium">
                    Email Address
                  </label_1.Label>
                  <div className="relative">
                    <lucide_react_1.Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5"/>
                    <input_1.Input id="email" type="email" placeholder="Enter your email" value={email} onChange={(e) => setEmail(e.target.value)} className="pl-10 h-12 border-gray-300 focus:border-pink-500 focus:ring-pink-500 bg-white/70" required/>
                  </div>
                </div>

                <div className="space-y-2">
                  <label_1.Label htmlFor="password" className="text-gray-700 font-medium">
                    Password
                  </label_1.Label>
                  <div className="relative">
                    <lucide_react_1.Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5"/>
                    <input_1.Input id="password" type={showPassword ? "text" : "password"} placeholder="Enter your password" value={password} onChange={(e) => setPassword(e.target.value)} className="pl-10 pr-10 h-12 border-gray-300 focus:border-pink-500 focus:ring-pink-500 bg-white/70" required/>
                    <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors">
                      {showPassword ? <lucide_react_1.EyeOff className="w-5 h-5"/> : <lucide_react_1.Eye className="w-5 h-5"/>}
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <checkbox_1.Checkbox id="remember" checked={rememberMe} onCheckedChange={setRememberMe} className="border-gray-300 data-[state=checked]:bg-pink-500 data-[state=checked]:border-pink-500"/>
                    <label_1.Label htmlFor="remember" className="text-sm text-gray-600 font-medium">
                      Remember me
                    </label_1.Label>
                  </div>
                  <link_1.default href="/forgot-password" className="text-sm text-pink-600 hover:text-pink-700 font-medium">
                    Forgot password?
                  </link_1.default>
                </div>

                <button_1.Button type="submit" disabled={isLoading} className="w-full h-12 bg-gradient-to-r from-pink-500 to-blue-500 hover:from-pink-600 hover:to-blue-600 text-white text-lg font-semibold shadow-lg hover:shadow-xl transition-all duration-300">
                  {isLoading ? (<div className="flex items-center space-x-2">
                      <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Signing In...</span>
                    </div>) : (<div className="flex items-center space-x-2">
                      <span>Sign In</span>
                      <lucide_react_1.ArrowRight className="w-5 h-5"/>
                    </div>)}
                </button_1.Button>
              </form>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t border-gray-300"/>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-4 bg-white text-gray-500 font-medium">Or continue with</span>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <button_1.Button variant="outline" className="h-12 hover:bg-gray-50 transition-colors">
                  <svg className="w-5 h-5" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                  </svg>
                </button_1.Button>
                <button_1.Button variant="outline" className="h-12 hover:bg-gray-50 transition-colors">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                  </svg>
                </button_1.Button>
                <button_1.Button variant="outline" className="h-12 hover:bg-gray-50 transition-colors">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
                  </svg>
                </button_1.Button>
              </div>

              <div className="text-center">
                <p className="text-gray-600">
                  Don't have an account?{" "}
                  <link_1.default href="/signup" className="text-pink-600 hover:text-pink-700 font-semibold">
                    Sign up for free
                  </link_1.default>
                </p>
              </div>

              {/* Trust Indicators */}
              <div className="flex items-center justify-center space-x-6 pt-4 text-xs text-gray-500">
                <div className="flex items-center space-x-1">
                  <lucide_react_1.Shield className="w-4 h-4 text-green-500"/>
                  <span>HIPAA Compliant</span>
                </div>
                <div className="flex items-center space-x-1">
                  <lucide_react_1.CheckCircle className="w-4 h-4 text-green-500"/>
                  <span>SOC 2 Certified</span>
                </div>
              </div>
            </card_1.CardContent>
          </card_1.Card>
        </div>
      </div>
    </div>);
}
