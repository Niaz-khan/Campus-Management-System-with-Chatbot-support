import React, { useState } from "react";
import { 
  GraduationCap, 
  Users, 
  BookOpen, 
  Calendar, 
  BarChart3, 
  Settings, 
  Bell, 
  Search,
  LogOut,
  Menu,
  X,
  UserCheck,
  Award,
  Clock,
  TrendingUp,
  FileText,
  CreditCard,
  Home,
  ChevronRight,
  Star
} from "lucide-react";

const Dashboard: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');

  // Mock user data - replace with actual data from your API/localStorage
  const user = {
    name: "Dr. Sarah Johnson",
    role: "Administrator",
    avatar: "/api/placeholder/40/40",
    email: "sarah.johnson@edumax.edu"
  };

  // Mock statistics - replace with real data
  const stats = [
    { title: "Total Students", value: "2,847", change: "+12%", icon: Users, color: "from-blue-500 to-blue-600" },
    { title: "Active Courses", value: "156", change: "+8%", icon: BookOpen, color: "from-emerald-500 to-emerald-600" },
    { title: "Faculty Members", value: "342", change: "+5%", icon: UserCheck, color: "from-violet-500 to-violet-600" },
    { title: "Departments", value: "24", change: "+2%", icon: Award, color: "from-amber-500 to-amber-600" }
  ];

  const menuItems = [
    { id: 'overview', name: 'Overview', icon: Home },
    { id: 'students', name: 'Students', icon: Users },
    { id: 'faculty', name: 'Faculty', icon: UserCheck },
    { id: 'courses', name: 'Courses', icon: BookOpen },
    { id: 'attendance', name: 'Attendance', icon: Clock },
    { id: 'grades', name: 'Grades', icon: Award },
    { id: 'calendar', name: 'Calendar', icon: Calendar },
    { id: 'finance', name: 'Finance', icon: CreditCard },
    { id: 'reports', name: 'Reports', icon: BarChart3 },
    { id: 'settings', name: 'Settings', icon: Settings }
  ];

  const recentActivities = [
    { action: "New student enrolled", details: "John Doe - Computer Science", time: "2 mins ago", type: "success" },
    { action: "Course updated", details: "Data Structures - CS201", time: "15 mins ago", type: "info" },
    { action: "Fee payment received", details: "Alice Smith - $2,500", time: "1 hour ago", type: "success" },
    { action: "Faculty meeting scheduled", details: "Department heads - Tomorrow 2 PM", time: "3 hours ago", type: "warning" }
  ];

  const upcomingEvents = [
    { title: "Semester Exams", date: "Dec 15-22", type: "exam" },
    { title: "Faculty Meeting", date: "Dec 10, 2:00 PM", type: "meeting" },
    { title: "New Student Orientation", date: "Jan 5, 2025", type: "event" },
    { title: "Annual Sports Day", date: "Jan 15, 2025", type: "event" }
  ];

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      // Use in-memory variables instead of localStorage in artifact environment
      window.location.href = "/login";
    }
  };

  return (
    <div className="h-screen bg-slate-50 flex overflow-hidden">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden" 
          onClick={() => setSidebarOpen(false)} 
        />
      )}

      {/* Sidebar - Fixed */}
      <aside className={`
        fixed inset-y-0 left-0 z-50 w-72 bg-white/95 backdrop-blur-xl 
        shadow-2xl border-r border-slate-200/60 transform transition-transform 
        duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} 
        lg:translate-x-0 lg:static lg:inset-0
      `}>
        {/* Header */}
        <div className="flex items-center justify-between h-16 px-6 border-b border-slate-200/60 bg-white/80 backdrop-blur">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
              <GraduationCap className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
              EduMax
            </span>
          </div>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden p-2 rounded-lg text-slate-500 hover:text-slate-700 hover:bg-slate-100 transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* User Profile Section */}
        <div className="p-6 border-b border-slate-200/60 bg-gradient-to-r from-slate-50 to-slate-100/50">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-semibold text-sm shadow-lg">
              {user.name.split(' ').map(n => n[0]).join('')}
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-sm font-semibold text-slate-800 truncate">{user.name}</p>
              <p className="text-xs text-slate-600">{user.role}</p>
            </div>
          </div>
        </div>

        {/* Navigation Menu - Scrollable */}
        <nav className="flex-1 overflow-y-auto p-4 space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  setActiveTab(item.id);
                  setSidebarOpen(false);
                }}
                className={`
                  group w-full flex items-center px-4 py-3 text-left rounded-xl 
                  transition-all duration-200 relative overflow-hidden
                  ${isActive
                    ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg scale-[1.02]'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80 hover:scale-[1.01]'
                  }
                `}
              >
                <Icon 
                  size={20} 
                  className={`mr-3 transition-transform duration-200 ${
                    isActive ? 'text-white' : 'group-hover:scale-110'
                  }`} 
                />
                <span className="font-medium text-sm">{item.name}</span>
                {isActive && (
                  <div className="absolute right-2 w-2 h-2 bg-white rounded-full opacity-80" />
                )}
              </button>
            );
          })}
        </nav>

        {/* Sidebar Footer */}
        <div className="p-4 border-t border-slate-200/60 bg-slate-50/50">
          <div className="text-xs text-slate-500 text-center">
            © 2024 EduMax. All rights reserved.
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden lg:ml-0">
        {/* Header - Sticky */}
        <header className="sticky top-0 z-30 bg-white/95 backdrop-blur-xl shadow-sm border-b border-slate-200/60">
          <div className="flex items-center justify-between h-16 px-6">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden p-2 rounded-lg text-slate-500 hover:text-slate-700 hover:bg-slate-100 transition-colors"
              >
                <Menu size={20} />
              </button>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
                  Dashboard
                </h1>
                <p className="text-sm text-slate-600">Welcome back, {user.name.split(' ')[0]}!</p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* Search Bar */}
              <div className="hidden md:flex relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={18} />
                <input
                  type="text"
                  placeholder="Search anything..."
                  className="pl-10 pr-4 py-2.5 w-80 bg-slate-100/80 border border-slate-200 rounded-xl 
                           focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 focus:bg-white
                           transition-all duration-200 outline-none text-sm placeholder-slate-500"
                />
              </div>

              {/* Notifications */}
              <button className="relative p-2.5 rounded-xl text-slate-500 hover:text-slate-700 hover:bg-slate-100 transition-colors">
                <Bell size={20} />
                <span className="absolute -top-1 -right-1 h-5 w-5 bg-gradient-to-r from-red-500 to-red-600 rounded-full text-xs text-white flex items-center justify-center font-medium shadow-lg">
                  3
                </span>
              </button>

              {/* Logout Button */}
              <button
                onClick={handleLogout}
                className="flex items-center px-4 py-2.5 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white rounded-xl transition-all duration-200 shadow-lg hover:shadow-xl hover:scale-[1.02]"
              >
                <LogOut size={16} className="mr-2" />
                <span className="text-sm font-medium">Logout</span>
              </button>
            </div>
          </div>
        </header>

        {/* Scrollable Main Content */}
        <main className="flex-1 overflow-y-auto bg-gradient-to-br from-slate-50 to-slate-100/50">
          <div className="p-6 space-y-8">
            {/* Stats Cards */}
            <section>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {stats.map((stat, index) => {
                  const Icon = stat.icon;
                  return (
                    <div 
                      key={index} 
                      className="group bg-white/80 backdrop-blur rounded-2xl shadow-sm border border-slate-200/60 p-6 hover:shadow-xl hover:scale-[1.02] transition-all duration-300"
                    >
                      <div className="flex items-start justify-between">
                        <div className="space-y-2">
                          <p className="text-sm font-medium text-slate-600">{stat.title}</p>
                          <p className="text-3xl font-bold text-slate-900">{stat.value}</p>
                          <div className="flex items-center space-x-2">
                            <span className="text-sm text-emerald-600 font-semibold bg-emerald-100 px-2 py-1 rounded-lg">
                              {stat.change}
                            </span>
                            <span className="text-xs text-slate-500">vs last month</span>
                          </div>
                        </div>
                        <div className={`p-3 rounded-2xl bg-gradient-to-r ${stat.color} shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                          <Icon size={24} className="text-white" />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </section>

            {/* Main Grid */}
            <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Quick Actions */}
              <div className="lg:col-span-2 bg-white/80 backdrop-blur rounded-2xl shadow-sm border border-slate-200/60 p-8">
                <div className="flex items-center justify-between mb-8">
                  <h3 className="text-xl font-bold text-slate-800">Quick Actions</h3>
                  <div className="w-12 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full" />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {[
                    { title: "Manage Students", desc: "Add, edit, or view student records", icon: Users, color: "from-blue-500 to-blue-600" },
                    { title: "Course Management", desc: "Create and manage courses", icon: BookOpen, color: "from-emerald-500 to-emerald-600" },
                    { title: "Faculty Portal", desc: "Manage teacher profiles and assignments", icon: UserCheck, color: "from-violet-500 to-violet-600" },
                    { title: "Generate Reports", desc: "Create detailed analytics reports", icon: BarChart3, color: "from-amber-500 to-amber-600" }
                  ].map((action, index) => {
                    const Icon = action.icon;
                    return (
                      <button
                        key={index}
                        className="group flex items-start p-6 border border-slate-200/60 rounded-2xl hover:bg-slate-50/80 hover:border-indigo-300/60 hover:shadow-lg transition-all duration-300 text-left hover:scale-[1.02]"
                      >
                        <div className={`p-3 rounded-2xl bg-gradient-to-r ${action.color} mr-4 shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                          <Icon size={20} className="text-white" />
                        </div>
                        <div className="space-y-1">
                          <h4 className="font-semibold text-slate-800 text-sm">{action.title}</h4>
                          <p className="text-sm text-slate-600 leading-relaxed">{action.desc}</p>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Upcoming Events */}
              <div className="bg-white/80 backdrop-blur rounded-2xl shadow-sm border border-slate-200/60 p-8">
                <div className="flex items-center justify-between mb-8">
                  <h3 className="text-xl font-bold text-slate-800">Upcoming Events</h3>
                  <Calendar size={20} className="text-slate-400" />
                </div>
                <div className="space-y-4">
                  {upcomingEvents.map((event, index) => (
                    <div key={index} className="group flex items-center justify-between p-4 bg-slate-50/80 hover:bg-indigo-50/80 rounded-xl transition-all duration-200 hover:scale-[1.02] cursor-pointer">
                      <div className="space-y-1">
                        <p className="font-semibold text-slate-800 text-sm group-hover:text-indigo-700 transition-colors">
                          {event.title}
                        </p>
                        <p className="text-xs text-slate-600">{event.date}</p>
                      </div>
                      <ChevronRight size={16} className="text-slate-400 group-hover:text-indigo-600 transition-colors" />
                    </div>
                  ))}
                </div>
              </div>
            </section>

            {/* Recent Activities */}
            <section className="bg-white/80 backdrop-blur rounded-2xl shadow-sm border border-slate-200/60 p-8">
              <div className="flex items-center justify-between mb-8">
                <h3 className="text-xl font-bold text-slate-800">Recent Activities</h3>
                <div className="w-12 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full" />
              </div>
              <div className="space-y-1">
                {recentActivities.map((activity, index) => (
                  <div key={index} className="group flex items-start space-x-4 p-4 hover:bg-slate-50/80 rounded-xl transition-all duration-200 hover:scale-[1.01] cursor-pointer">
                    <div className={`w-3 h-3 rounded-full mt-1.5 shadow-sm ${
                      activity.type === 'success' ? 'bg-gradient-to-r from-emerald-400 to-emerald-500' : 
                      activity.type === 'warning' ? 'bg-gradient-to-r from-amber-400 to-amber-500' : 
                      'bg-gradient-to-r from-blue-400 to-blue-500'
                    }`} />
                    <div className="flex-1 space-y-1">
                      <p className="font-semibold text-slate-800 text-sm group-hover:text-indigo-700 transition-colors">
                        {activity.action}
                      </p>
                      <p className="text-sm text-slate-600">{activity.details}</p>
                      <p className="text-xs text-slate-500">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* Footer Spacer */}
            <div className="h-8" />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Dashboard;