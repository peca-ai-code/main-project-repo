"use strict";
"use client";
Object.defineProperty(exports, "__esModule", { value: true });
exports.BookingModal = BookingModal;
const react_1 = require("react");
const dialog_1 = require("@/components/ui/dialog");
const button_1 = require("@/components/ui/button");
const input_1 = require("@/components/ui/input");
const label_1 = require("@/components/ui/label");
const avatar_1 = require("@/components/ui/avatar");
const lucide_react_1 = require("lucide-react");
function BookingModal({ doctor, isOpen, onClose }) {
    const [currentStep, setCurrentStep] = (0, react_1.useState)("date");
    const [selectedDate, setSelectedDate] = (0, react_1.useState)("");
    const [selectedTime, setSelectedTime] = (0, react_1.useState)("");
    const [patientInfo, setPatientInfo] = (0, react_1.useState)({
        name: "",
        phone: "",
        email: "",
        age: "",
    });
    // Generate next 14 days
    const generateDates = () => {
        const dates = [];
        const today = new Date();
        for (let i = 0; i < 14; i++) {
            const date = new Date(today);
            date.setDate(today.getDate() + i);
            dates.push({
                date: date.toISOString().split("T")[0],
                display: date.toLocaleDateString("en-US", {
                    month: "short",
                    day: "numeric",
                    weekday: "short",
                }),
                isToday: i === 0,
                isTomorrow: i === 1,
            });
        }
        return dates;
    };
    const timeSlots = {
        morning: ["9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM"],
        afternoon: ["1:00 PM", "1:30 PM", "2:00 PM", "2:30 PM", "3:00 PM", "3:30 PM"],
        evening: ["4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM", "6:00 PM", "6:30 PM"],
    };
    const handleDateSelect = (date) => {
        setSelectedDate(date);
        setCurrentStep("time");
    };
    const handleTimeSelect = (time) => {
        setSelectedTime(time);
        setCurrentStep("summary");
    };
    const handleConfirmAppointment = () => {
        setCurrentStep("success");
    };
    const handleClose = () => {
        setCurrentStep("date");
        setSelectedDate("");
        setSelectedTime("");
        setPatientInfo({ name: "", phone: "", email: "", age: "" });
        onClose();
    };
    const renderDateSelection = () => (<div className="space-y-6">
      <div className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
        <avatar_1.Avatar className="w-12 h-12">
          <avatar_1.AvatarFallback className="bg-pink-100 text-pink-600">
            {doctor.name
            .split(" ")
            .map((n) => n[0])
            .join("")}
          </avatar_1.AvatarFallback>
        </avatar_1.Avatar>
        <div>
          <h3 className="font-semibold text-gray-900">{doctor.name}</h3>
          <p className="text-sm text-gray-600">{doctor.specialty}</p>
          <div className="flex items-center space-x-1 mt-1">
            <lucide_react_1.Star className="w-4 h-4 text-yellow-400 fill-current"/>
            <span className="text-sm text-gray-600">{doctor.rating}</span>
          </div>
        </div>
      </div>

      <div>
        <h4 className="font-medium text-gray-900 mb-4">Select Date</h4>
        <div className="grid grid-cols-7 gap-2">
          {generateDates().map((dateObj) => (<button key={dateObj.date} onClick={() => handleDateSelect(dateObj.date)} className="p-3 text-center border rounded-lg hover:border-pink-500 hover:bg-pink-50 transition-colors">
              <div className="text-xs text-gray-500">{dateObj.display.split(" ")[0]}</div>
              <div className="text-sm font-medium text-gray-900">{dateObj.display.split(" ")[1]}</div>
              {dateObj.isToday && <div className="text-xs text-pink-500">Today</div>}
              {dateObj.isTomorrow && <div className="text-xs text-pink-500">Tomorrow</div>}
            </button>))}
        </div>
      </div>

      <div className="flex justify-end">
        <button_1.Button variant="outline" onClick={handleClose}>
          Cancel
        </button_1.Button>
      </div>
    </div>);
    const renderTimeSelection = () => (<div className="space-y-6">
      <div className="flex items-center justify-between">
        <button_1.Button variant="ghost" onClick={() => setCurrentStep("date")}>
          <lucide_react_1.ArrowLeft className="w-4 h-4 mr-2"/>
          Back
        </button_1.Button>
        <div className="text-center">
          <p className="text-sm text-gray-600">Selected Date</p>
          <p className="font-medium text-gray-900">
            {new Date(selectedDate).toLocaleDateString("en-US", {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric",
        })}
          </p>
        </div>
        <div></div>
      </div>

      <div className="space-y-4">
        {Object.entries(timeSlots).map(([period, slots]) => (<div key={period}>
            <h4 className="font-medium text-gray-900 mb-2 capitalize">{period}</h4>
            <div className="grid grid-cols-3 gap-2">
              {slots.map((time) => (<button key={time} onClick={() => handleTimeSelect(time)} className="p-3 text-center border rounded-lg hover:border-pink-500 hover:bg-pink-50 transition-colors">
                  <div className="text-sm font-medium text-gray-900">{time}</div>
                </button>))}
            </div>
          </div>))}
      </div>
    </div>);
    const renderSummary = () => (<div className="space-y-6">
      <div className="flex items-center justify-between">
        <button_1.Button variant="ghost" onClick={() => setCurrentStep("time")}>
          <lucide_react_1.ArrowLeft className="w-4 h-4 mr-2"/>
          Back
        </button_1.Button>
        <h3 className="font-semibold text-gray-900">Appointment Summary</h3>
        <div></div>
      </div>

      <div className="bg-gray-50 rounded-lg p-4 space-y-3">
        <div className="flex items-center space-x-4">
          <avatar_1.Avatar className="w-12 h-12">
            <avatar_1.AvatarFallback className="bg-pink-100 text-pink-600">
              {doctor.name
            .split(" ")
            .map((n) => n[0])
            .join("")}
            </avatar_1.AvatarFallback>
          </avatar_1.Avatar>
          <div>
            <h4 className="font-semibold text-gray-900">{doctor.name}</h4>
            <p className="text-sm text-gray-600">{doctor.specialty}</p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Date:</span>
            <p className="font-medium text-gray-900">
              {new Date(selectedDate).toLocaleDateString("en-US", {
            weekday: "short",
            month: "short",
            day: "numeric",
        })}
            </p>
          </div>
          <div>
            <span className="text-gray-600">Time:</span>
            <p className="font-medium text-gray-900">{selectedTime}</p>
          </div>
          <div>
            <span className="text-gray-600">Consultation Fee:</span>
            <p className="font-medium text-gray-900">₹{doctor.price}</p>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h4 className="font-medium text-gray-900">Patient Information</h4>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label_1.Label htmlFor="name">Full Name *</label_1.Label>
            <input_1.Input id="name" value={patientInfo.name} onChange={(e) => setPatientInfo((prev) => (Object.assign(Object.assign({}, prev), { name: e.target.value })))} placeholder="Enter your full name"/>
          </div>
          <div>
            <label_1.Label htmlFor="phone">Phone Number *</label_1.Label>
            <input_1.Input id="phone" value={patientInfo.phone} onChange={(e) => setPatientInfo((prev) => (Object.assign(Object.assign({}, prev), { phone: e.target.value })))} placeholder="Enter your phone number"/>
          </div>
          <div>
            <label_1.Label htmlFor="email">Email Address *</label_1.Label>
            <input_1.Input id="email" type="email" value={patientInfo.email} onChange={(e) => setPatientInfo((prev) => (Object.assign(Object.assign({}, prev), { email: e.target.value })))} placeholder="Enter your email"/>
          </div>
          <div>
            <label_1.Label htmlFor="age">Age *</label_1.Label>
            <input_1.Input id="age" type="number" value={patientInfo.age} onChange={(e) => setPatientInfo((prev) => (Object.assign(Object.assign({}, prev), { age: e.target.value })))} placeholder="Enter your age"/>
          </div>
        </div>
      </div>

      <div className="flex space-x-4">
        <button_1.Button variant="outline" onClick={handleClose} className="flex-1">
          Cancel
        </button_1.Button>
        <button_1.Button onClick={handleConfirmAppointment} disabled={!patientInfo.name || !patientInfo.phone || !patientInfo.email || !patientInfo.age} className="flex-1 bg-pink-500 hover:bg-pink-600 text-white">
          Confirm Appointment
        </button_1.Button>
      </div>
    </div>);
    const renderSuccess = () => (<div className="text-center space-y-6">
      <div className="w-16 h-16 bg-green-100 rounded-full mx-auto flex items-center justify-center">
        <lucide_react_1.Check className="w-8 h-8 text-green-600"/>
      </div>

      <div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">Appointment Confirmed!</h3>
        <p className="text-gray-600">
          Your appointment with {doctor.name} is confirmed for{" "}
          {new Date(selectedDate).toLocaleDateString("en-US", {
            weekday: "long",
            month: "long",
            day: "numeric",
        })}{" "}
          at {selectedTime}.
        </p>
      </div>

      <div className="bg-gray-50 rounded-lg p-4">
        <h4 className="font-medium text-gray-900 mb-2">What's Next?</h4>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• You'll receive a confirmation email shortly</li>
          <li>• The doctor will call you at the scheduled time</li>
          <li>• You can reschedule or cancel anytime from your dashboard</li>
        </ul>
      </div>

      <div className="flex space-x-4">
        <button_1.Button variant="outline" onClick={handleClose} className="flex-1">
          Book Another
        </button_1.Button>
        <button_1.Button onClick={handleClose} className="flex-1 bg-pink-500 hover:bg-pink-600 text-white">
          Go to Dashboard
        </button_1.Button>
      </div>
    </div>);
    const getStepContent = () => {
        switch (currentStep) {
            case "date":
                return renderDateSelection();
            case "time":
                return renderTimeSelection();
            case "summary":
                return renderSummary();
            case "success":
                return renderSuccess();
            default:
                return renderDateSelection();
        }
    };
    const getTitle = () => {
        switch (currentStep) {
            case "date":
                return "Select Date";
            case "time":
                return "Select Time";
            case "summary":
                return "Confirm Appointment";
            case "success":
                return "Appointment Confirmed";
            default:
                return "Book Appointment";
        }
    };
    return (<dialog_1.Dialog open={isOpen} onOpenChange={handleClose}>
      <dialog_1.DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <dialog_1.DialogHeader>
          <dialog_1.DialogTitle className="flex items-center space-x-2">
            <lucide_react_1.Calendar className="w-5 h-5 text-pink-500"/>
            <span>{getTitle()}</span>
          </dialog_1.DialogTitle>
        </dialog_1.DialogHeader>

        <div className="mt-6">{getStepContent()}</div>
      </dialog_1.DialogContent>
    </dialog_1.Dialog>);
}
