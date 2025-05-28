"use strict";
"use client";
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = ProfilePage;
const react_1 = require("react");
const button_1 = require("@/components/ui/button");
const card_1 = require("@/components/ui/card");
const input_1 = require("@/components/ui/input");
const label_1 = require("@/components/ui/label");
const textarea_1 = require("@/components/ui/textarea");
const badge_1 = require("@/components/ui/badge");
const avatar_1 = require("@/components/ui/avatar");
const tabs_1 = require("@/components/ui/tabs");
const switch_1 = require("@/components/ui/switch");
const select_1 = require("@/components/ui/select");
const lucide_react_1 = require("lucide-react");
const navigation_1 = require("@/components/navigation");
function ProfilePage() {
    const [isEditing, setIsEditing] = (0, react_1.useState)(false);
    const [profileData, setProfileData] = (0, react_1.useState)({
        firstName: "Sarah",
        lastName: "Johnson",
        email: "demo@peca.com",
        phone: "+1 (555) 123-4567",
        dateOfBirth: "1990-05-15",
        address: "123 Health Street, Wellness City, WC 12345",
        emergencyContact: "John Johnson - +1 (555) 987-6543",
        bloodType: "O+",
        allergies: "Penicillin, Shellfish",
        medicalHistory: "No significant medical history",
    });
    const [notifications, setNotifications] = (0, react_1.useState)({
        appointments: true,
        reminders: true,
        healthTips: false,
        newsletters: true,
    });
    const [privacy, setPrivacy] = (0, react_1.useState)({
        shareData: false,
        analytics: true,
        marketing: false,
    });
    const handleSave = () => {
        setIsEditing(false);
        // Save logic here
    };
    const healthStats = [
        { label: "Consultations", value: "12", icon: lucide_react_1.User, color: "pink" },
        { label: "AI Chats", value: "28", icon: lucide_react_1.Heart, color: "blue" },
        { label: "Health Score", value: "85%", icon: lucide_react_1.Activity, color: "green" },
        { label: "Days Tracked", value: "45", icon: lucide_react_1.Calendar, color: "purple" },
    ];
    return (<div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-blue-50">
      <navigation_1.Navigation isLoggedIn={true} userName="Sarah"/>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="bg-gradient-to-r from-pink-500 to-blue-500 rounded-2xl p-8 text-white relative overflow-hidden">
            <div className="absolute inset-0 bg-black opacity-10"></div>
            <div className="relative z-10 flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-6">
              <div className="relative group">
                <avatar_1.Avatar className="w-24 h-24 border-4 border-white shadow-lg">
                  <avatar_1.AvatarFallback className="bg-white text-pink-600 text-2xl font-bold">
                    {profileData.firstName[0]}
                    {profileData.lastName[0]}
                  </avatar_1.AvatarFallback>
                </avatar_1.Avatar>
                <button_1.Button size="sm" className="absolute -bottom-2 -right-2 rounded-full w-8 h-8 p-0 bg-white text-pink-600 hover:bg-gray-50">
                  <lucide_react_1.Camera className="w-4 h-4"/>
                </button_1.Button>
              </div>
              <div className="text-center md:text-left flex-1">
                <h1 className="text-3xl font-bold mb-2">
                  {profileData.firstName} {profileData.lastName}
                </h1>
                <p className="text-pink-100 text-lg mb-4">PECA Health Member since 2024</p>
                <div className="flex flex-wrap gap-2 justify-center md:justify-start">
                  <badge_1.Badge className="bg-white/20 text-white border-white/30">
                    <lucide_react_1.Shield className="w-3 h-3 mr-1"/>
                    Verified
                  </badge_1.Badge>
                  <badge_1.Badge className="bg-white/20 text-white border-white/30">
                    <lucide_react_1.Heart className="w-3 h-3 mr-1"/>
                    Premium Member
                  </badge_1.Badge>
                </div>
              </div>
              <button_1.Button onClick={() => setIsEditing(!isEditing)} className="bg-white text-pink-600 hover:bg-gray-50">
                <lucide_react_1.Edit className="w-4 h-4 mr-2"/>
                {isEditing ? "Cancel" : "Edit Profile"}
              </button_1.Button>
            </div>
          </div>
        </div>

        {/* Health Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {healthStats.map((stat, index) => {
            const Icon = stat.icon;
            return (<card_1.Card key={index} className="text-center hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                <card_1.CardContent className="p-6">
                  <div className={`w-12 h-12 mx-auto mb-3 rounded-full flex items-center justify-center ${stat.color === "pink"
                    ? "bg-pink-100"
                    : stat.color === "blue"
                        ? "bg-blue-100"
                        : stat.color === "green"
                            ? "bg-green-100"
                            : "bg-purple-100"}`}>
                    <Icon className={`w-6 h-6 ${stat.color === "pink"
                    ? "text-pink-600"
                    : stat.color === "blue"
                        ? "text-blue-600"
                        : stat.color === "green"
                            ? "text-green-600"
                            : "text-purple-600"}`}/>
                  </div>
                  <p className="text-2xl font-bold text-gray-900 mb-1">{stat.value}</p>
                  <p className="text-sm text-gray-600">{stat.label}</p>
                </card_1.CardContent>
              </card_1.Card>);
        })}
        </div>

        {/* Profile Tabs */}
        <tabs_1.Tabs defaultValue="personal" className="space-y-6">
          <tabs_1.TabsList className="grid w-full grid-cols-4 lg:w-auto lg:grid-cols-4">
            <tabs_1.TabsTrigger value="personal" className="flex items-center space-x-2">
              <lucide_react_1.User className="w-4 h-4"/>
              <span className="hidden sm:inline">Personal</span>
            </tabs_1.TabsTrigger>
            <tabs_1.TabsTrigger value="medical" className="flex items-center space-x-2">
              <lucide_react_1.FileText className="w-4 h-4"/>
              <span className="hidden sm:inline">Medical</span>
            </tabs_1.TabsTrigger>
            <tabs_1.TabsTrigger value="notifications" className="flex items-center space-x-2">
              <lucide_react_1.Bell className="w-4 h-4"/>
              <span className="hidden sm:inline">Notifications</span>
            </tabs_1.TabsTrigger>
            <tabs_1.TabsTrigger value="privacy" className="flex items-center space-x-2">
              <lucide_react_1.Shield className="w-4 h-4"/>
              <span className="hidden sm:inline">Privacy</span>
            </tabs_1.TabsTrigger>
          </tabs_1.TabsList>

          {/* Personal Information */}
          <tabs_1.TabsContent value="personal">
            <card_1.Card className="shadow-lg border-0">
              <card_1.CardHeader>
                <card_1.CardTitle className="flex items-center space-x-2">
                  <lucide_react_1.User className="w-5 h-5 text-pink-500"/>
                  <span>Personal Information</span>
                </card_1.CardTitle>
              </card_1.CardHeader>
              <card_1.CardContent className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label_1.Label htmlFor="firstName">First Name</label_1.Label>
                    <div className="relative">
                      <lucide_react_1.User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4"/>
                      <input_1.Input id="firstName" value={profileData.firstName} onChange={(e) => setProfileData(Object.assign(Object.assign({}, profileData), { firstName: e.target.value }))} disabled={!isEditing} className="pl-10"/>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label_1.Label htmlFor="lastName">Last Name</label_1.Label>
                    <input_1.Input id="lastName" value={profileData.lastName} onChange={(e) => setProfileData(Object.assign(Object.assign({}, profileData), { lastName: e.target.value }))} disabled={!isEditing}/>
                  </div>
                  <div className="space-y-2">
                    <label_1.Label htmlFor="email">Email Address</label_1.Label>
                    <div className="relative">
                      <lucide_react_1.Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4"/>
                      <input_1.Input id="email" type="email" value={profileData.email} onChange={(e) => setProfileData(Object.assign(Object.assign({}, profileData), { email: e.target.value }))} disabled={!isEditing} className="pl-10"/>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label_1.Label htmlFor="phone">Phone Number</label_1.Label>
                    <div className="relative">
                      <lucide_react_1.Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4"/>
                      <input_1.Input id="phone" value={profileData.phone} onChange={(e) => setProfileData(Object.assign(Object.assign({}, profileData), { phone: e.target.value }))} disabled={!isEditing} className="pl-10"/>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label_1.Label htmlFor="dateOfBirth">Date of Birth</label_1.Label>
                    <div className="relative">
                      <lucide_react_1.Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4"/>
                      <input_1.Input id="dateOfBirth" type="date" value={profileData.dateOfBirth} onChange={(e) => setProfileData(Object.assign(Object.assign({}, profileData), { dateOfBirth: e.target.value }))} disabled={!isEditing} className="pl-10"/>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label_1.Label htmlFor="bloodType">Blood Type</label_1.Label>
                    <select_1.Select disabled={!isEditing}>
                      <select_1.SelectTrigger>
                        <select_1.SelectValue placeholder={profileData.bloodType}/>
                      </select_1.SelectTrigger>
                      <select_1.SelectContent>
                        <select_1.SelectItem value="A+">A+</select_1.SelectItem>
                        <select_1.SelectItem value="A-">A-</select_1.SelectItem>
                        <select_1.SelectItem value="B+">B+</select_1.SelectItem>
                        <select_1.SelectItem value="B-">B-</select_1.SelectItem>
                        <select_1.SelectItem value="AB+">AB+</select_1.SelectItem>
                        <select_1.SelectItem value="AB-">AB-</select_1.SelectItem>
                        <select_1.SelectItem value="O+">O+</select_1.SelectItem>
                        <select_1.SelectItem value="O-">O-</select_1.SelectItem>
                      </select_1.SelectContent>
                    </select_1.Select>
                  </div>
                </div>
                <div className="space-y-2">
                  <label_1.Label htmlFor="address">Address</label_1.Label>
                  <div className="relative">
                    <lucide_react_1.MapPin className="absolute left-3 top-3 text-gray-400 w-4 h-4"/>
                    <textarea_1.Textarea id="address" value={profileData.address} onChange={(e) => setProfileData(Object.assign(Object.assign({}, profileData), { address: e.target.value }))} disabled={!isEditing} className="pl-10 min-h-[80px]"/>
                  </div>
                </div>
                {isEditing && (<div className="flex space-x-4">
                    <button_1.Button onClick={handleSave} className="bg-pink-500 hover:bg-pink-600 text-white">
                      <lucide_react_1.Save className="w-4 h-4 mr-2"/>
                      Save Changes
                    </button_1.Button>
                    <button_1.Button variant="outline" onClick={() => setIsEditing(false)}>
                      Cancel
                    </button_1.Button>
                  </div>)}
              </card_1.CardContent>
            </card_1.Card>
          </tabs_1.TabsContent>

          {/* Medical Information */}
          <tabs_1.TabsContent value="medical">
            <card_1.Card className="shadow-lg border-0">
              <card_1.CardHeader>
                <card_1.CardTitle className="flex items-center space-x-2">
                  <lucide_react_1.FileText className="w-5 h-5 text-blue-500"/>
                  <span>Medical Information</span>
                </card_1.CardTitle>
              </card_1.CardHeader>
              <card_1.CardContent className="space-y-6">
                <div className="space-y-2">
                  <label_1.Label htmlFor="emergencyContact">Emergency Contact</label_1.Label>
                  <input_1.Input id="emergencyContact" value={profileData.emergencyContact} onChange={(e) => setProfileData(Object.assign(Object.assign({}, profileData), { emergencyContact: e.target.value }))} disabled={!isEditing}/>
                </div>
                <div className="space-y-2">
                  <label_1.Label htmlFor="allergies">Allergies</label_1.Label>
                  <textarea_1.Textarea id="allergies" value={profileData.allergies} onChange={(e) => setProfileData(Object.assign(Object.assign({}, profileData), { allergies: e.target.value }))} disabled={!isEditing} placeholder="List any known allergies..." className="min-h-[80px]"/>
                </div>
                <div className="space-y-2">
                  <label_1.Label htmlFor="medicalHistory">Medical History</label_1.Label>
                  <textarea_1.Textarea id="medicalHistory" value={profileData.medicalHistory} onChange={(e) => setProfileData(Object.assign(Object.assign({}, profileData), { medicalHistory: e.target.value }))} disabled={!isEditing} placeholder="Describe your medical history..." className="min-h-[120px]"/>
                </div>
                {isEditing && (<div className="flex space-x-4">
                    <button_1.Button onClick={handleSave} className="bg-blue-500 hover:bg-blue-600 text-white">
                      <lucide_react_1.Save className="w-4 h-4 mr-2"/>
                      Save Changes
                    </button_1.Button>
                    <button_1.Button variant="outline" onClick={() => setIsEditing(false)}>
                      Cancel
                    </button_1.Button>
                  </div>)}
              </card_1.CardContent>
            </card_1.Card>
          </tabs_1.TabsContent>

          {/* Notifications */}
          <tabs_1.TabsContent value="notifications">
            <card_1.Card className="shadow-lg border-0">
              <card_1.CardHeader>
                <card_1.CardTitle className="flex items-center space-x-2">
                  <lucide_react_1.Bell className="w-5 h-5 text-orange-500"/>
                  <span>Notification Preferences</span>
                </card_1.CardTitle>
              </card_1.CardHeader>
              <card_1.CardContent className="space-y-6">
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">Appointment Reminders</h4>
                      <p className="text-sm text-gray-600">Get notified about upcoming appointments</p>
                    </div>
                    <switch_1.Switch checked={notifications.appointments} onCheckedChange={(checked) => setNotifications(Object.assign(Object.assign({}, notifications), { appointments: checked }))}/>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">Health Reminders</h4>
                      <p className="text-sm text-gray-600">Medication and health check reminders</p>
                    </div>
                    <switch_1.Switch checked={notifications.reminders} onCheckedChange={(checked) => setNotifications(Object.assign(Object.assign({}, notifications), { reminders: checked }))}/>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">Health Tips</h4>
                      <p className="text-sm text-gray-600">Weekly health tips and insights</p>
                    </div>
                    <switch_1.Switch checked={notifications.healthTips} onCheckedChange={(checked) => setNotifications(Object.assign(Object.assign({}, notifications), { healthTips: checked }))}/>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">Newsletters</h4>
                      <p className="text-sm text-gray-600">Monthly PECA health newsletters</p>
                    </div>
                    <switch_1.Switch checked={notifications.newsletters} onCheckedChange={(checked) => setNotifications(Object.assign(Object.assign({}, notifications), { newsletters: checked }))}/>
                  </div>
                </div>
              </card_1.CardContent>
            </card_1.Card>
          </tabs_1.TabsContent>

          {/* Privacy */}
          <tabs_1.TabsContent value="privacy">
            <card_1.Card className="shadow-lg border-0">
              <card_1.CardHeader>
                <card_1.CardTitle className="flex items-center space-x-2">
                  <lucide_react_1.Shield className="w-5 h-5 text-green-500"/>
                  <span>Privacy & Security</span>
                </card_1.CardTitle>
              </card_1.CardHeader>
              <card_1.CardContent className="space-y-6">
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">Share Data for Research</h4>
                      <p className="text-sm text-gray-600">Help improve women's health research (anonymized)</p>
                    </div>
                    <switch_1.Switch checked={privacy.shareData} onCheckedChange={(checked) => setPrivacy(Object.assign(Object.assign({}, privacy), { shareData: checked }))}/>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">Analytics</h4>
                      <p className="text-sm text-gray-600">Help us improve the app experience</p>
                    </div>
                    <switch_1.Switch checked={privacy.analytics} onCheckedChange={(checked) => setPrivacy(Object.assign(Object.assign({}, privacy), { analytics: checked }))}/>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">Marketing Communications</h4>
                      <p className="text-sm text-gray-600">Receive promotional emails and offers</p>
                    </div>
                    <switch_1.Switch checked={privacy.marketing} onCheckedChange={(checked) => setPrivacy(Object.assign(Object.assign({}, privacy), { marketing: checked }))}/>
                  </div>
                </div>

                <div className="border-t pt-6">
                  <h4 className="font-medium text-gray-900 mb-4">Data Management</h4>
                  <div className="space-y-3">
                    <button_1.Button variant="outline" className="w-full justify-start">
                      <lucide_react_1.FileText className="w-4 h-4 mr-2"/>
                      Download My Data
                    </button_1.Button>
                    <button_1.Button variant="outline" className="w-full justify-start text-red-600 border-red-200 hover:bg-red-50">
                      <lucide_react_1.Trash2 className="w-4 h-4 mr-2"/>
                      Delete Account
                    </button_1.Button>
                  </div>
                </div>
              </card_1.CardContent>
            </card_1.Card>
          </tabs_1.TabsContent>
        </tabs_1.Tabs>
      </div>
    </div>);
}
