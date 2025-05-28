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
exports.default = ChatPage;
const react_1 = require("react");
const button_1 = require("@/components/ui/button");
const card_1 = require("@/components/ui/card");
const textarea_1 = require("@/components/ui/textarea");
const badge_1 = require("@/components/ui/badge");
const avatar_1 = require("@/components/ui/avatar");
const lucide_react_1 = require("lucide-react");
const link_1 = __importDefault(require("next/link"));
const navigation_1 = require("@/components/navigation");
function ChatPage() {
    const [messages, setMessages] = (0, react_1.useState)([
        {
            id: "1",
            content: "Hello! I'm your WomanCare AI assistant. I'm here to help with your gynecological health questions. How can I assist you today?",
            sender: "assistant",
            timestamp: new Date(),
            severity: "low",
            aiModel: "ChatGPT",
        },
    ]);
    const [inputValue, setInputValue] = (0, react_1.useState)("");
    const [isTyping, setIsTyping] = (0, react_1.useState)(false);
    const messagesEndRef = (0, react_1.useRef)(null);
    const scrollToBottom = () => {
        var _a;
        (_a = messagesEndRef.current) === null || _a === void 0 ? void 0 : _a.scrollIntoView({ behavior: "smooth" });
    };
    (0, react_1.useEffect)(() => {
        scrollToBottom();
    }, [messages]);
    const handleSendMessage = () => __awaiter(this, void 0, void 0, function* () {
        if (!inputValue.trim())
            return;
        const userMessage = {
            id: Date.now().toString(),
            content: inputValue,
            sender: "user",
            timestamp: new Date(),
        };
        setMessages((prev) => [...prev, userMessage]);
        setInputValue("");
        setIsTyping(true);
        // Simulate AI response
        setTimeout(() => {
            const responses = [
                {
                    content: "Based on your symptoms, this could be related to hormonal changes. I recommend tracking your cycle and noting when these symptoms occur. However, for a proper diagnosis, please consult with a gynecologist.",
                    severity: "medium",
                    aiModel: "ChatGPT",
                    showBooking: true,
                },
                {
                    content: "These symptoms are quite common and usually not serious. Here are some self-care tips that might help: stay hydrated, get adequate rest, and consider gentle exercise. If symptoms persist, please see a healthcare provider.",
                    severity: "low",
                    aiModel: "Gemini",
                    showBooking: false,
                },
                {
                    content: "I'm concerned about the symptoms you've described. This requires immediate medical attention. Please contact your healthcare provider or visit an emergency room if symptoms worsen.",
                    severity: "high",
                    aiModel: "Grok",
                    showBooking: true,
                },
            ];
            const randomResponse = responses[Math.floor(Math.random() * responses.length)];
            const assistantMessage = {
                id: (Date.now() + 1).toString(),
                content: randomResponse.content,
                sender: "assistant",
                timestamp: new Date(),
                severity: randomResponse.severity,
                aiModel: randomResponse.aiModel,
                showBooking: randomResponse.showBooking,
            };
            setMessages((prev) => [...prev, assistantMessage]);
            setIsTyping(false);
        }, 2000);
    });
    const getSeverityColor = (severity) => {
        switch (severity) {
            case "low":
                return "bg-green-100 text-green-800";
            case "medium":
                return "bg-yellow-100 text-yellow-800";
            case "high":
                return "bg-red-100 text-red-800";
            default:
                return "bg-gray-100 text-gray-800";
        }
    };
    const getSeverityIcon = (severity) => {
        switch (severity) {
            case "low":
                return <lucide_react_1.CheckCircle className="w-3 h-3"/>;
            case "medium":
                return <lucide_react_1.Info className="w-3 h-3"/>;
            case "high":
                return <lucide_react_1.AlertTriangle className="w-3 h-3"/>;
            default:
                return null;
        }
    };
    return (<div className="min-h-screen bg-gray-50">
      {/* Header */}
      <navigation_1.Navigation isLoggedIn={true} userName="User"/>

      {/* Chat Container */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <card_1.Card className="h-[calc(100vh-200px)] flex flex-col">
          {/* Messages */}
          <card_1.CardContent className="flex-1 overflow-y-auto p-6 space-y-6">
            {messages.map((message) => (<div key={message.id} className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[80%] ${message.sender === "user" ? "order-2" : "order-1"}`}>
                  <div className="flex items-center space-x-2 mb-2">
                    <avatar_1.Avatar className="w-8 h-8">
                      <avatar_1.AvatarFallback className={message.sender === "user" ? "bg-blue-100 text-blue-600" : "bg-pink-100 text-pink-600"}>
                        {message.sender === "user" ? <lucide_react_1.User className="w-4 h-4"/> : <lucide_react_1.Bot className="w-4 h-4"/>}
                      </avatar_1.AvatarFallback>
                    </avatar_1.Avatar>
                    <span className="text-sm font-medium text-gray-900">
                      {message.sender === "user" ? "You" : "AI Assistant"}
                    </span>
                    <span className="text-xs text-gray-500">
                      {message.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                    </span>
                  </div>

                  <div className={`rounded-2xl p-4 ${message.sender === "user" ? "bg-blue-500 text-white" : "bg-white border border-gray-200"}`}>
                    <p className="text-sm leading-relaxed">{message.content}</p>

                    {message.sender === "assistant" && (<div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
                        <div className="flex items-center space-x-2">
                          {message.aiModel && (<badge_1.Badge variant="secondary" className="text-xs">
                              {message.aiModel}
                            </badge_1.Badge>)}
                          {message.severity && (<badge_1.Badge className={`text-xs ${getSeverityColor(message.severity)}`}>
                              {getSeverityIcon(message.severity)}
                              <span className="ml-1 capitalize">{message.severity}</span>
                            </badge_1.Badge>)}
                        </div>

                        {message.showBooking && (<link_1.default href="/doctors">
                            <button_1.Button size="sm" className="bg-pink-500 hover:bg-pink-600 text-white">
                              Book Doctor
                            </button_1.Button>
                          </link_1.default>)}
                      </div>)}
                  </div>
                </div>
              </div>))}

            {isTyping && (<div className="flex justify-start">
                <div className="max-w-[80%]">
                  <div className="flex items-center space-x-2 mb-2">
                    <avatar_1.Avatar className="w-8 h-8">
                      <avatar_1.AvatarFallback className="bg-pink-100 text-pink-600">
                        <lucide_react_1.Bot className="w-4 h-4"/>
                      </avatar_1.AvatarFallback>
                    </avatar_1.Avatar>
                    <span className="text-sm font-medium text-gray-900">AI Assistant</span>
                  </div>

                  <div className="bg-white border border-gray-200 rounded-2xl p-4">
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                    </div>
                  </div>
                </div>
              </div>)}

            <div ref={messagesEndRef}/>
          </card_1.CardContent>

          {/* Input Section */}
          <div className="border-t border-gray-200 p-6">
            <div className="flex space-x-4">
              <div className="flex-1">
                <textarea_1.Textarea value={inputValue} onChange={(e) => setInputValue(e.target.value)} placeholder="Ask me about your gynecological health concerns..." className="min-h-[60px] resize-none border-gray-300 focus:border-pink-500 focus:ring-pink-500" maxLength={1000} onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
            }
        }}/>
                <div className="flex justify-between items-center mt-2">
                  <span className="text-xs text-gray-500">{inputValue.length}/1000 characters</span>
                  <span className="text-xs text-gray-500">Press Enter to send, Shift+Enter for new line</span>
                </div>
              </div>
              <button_1.Button onClick={handleSendMessage} disabled={!inputValue.trim() || isTyping} className="bg-pink-500 hover:bg-pink-600 text-white px-6">
                <lucide_react_1.Send className="w-4 h-4"/>
              </button_1.Button>
            </div>
          </div>
        </card_1.Card>
      </div>
    </div>);
}
