<style data-purpose="base-styling">
body {
  font-family:
    'Roboto',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Roboto,
    Helvetica,
    Arial,
    sans-serif;
  -webkit-font-smoothing: antialiased;
  color: #3c4043;
}
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #dadce0;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #bdc1c6;
}
</style>
<style data-purpose="event-card-styles">
/* Hour row height is 52px */
.hour-slot {
  height: 52px;
}
.grid-line {
  border-bottom: 1px solid #dadce0;
  height: 52px;
  box-sizing: border-box;
}
</style>

<template>
  <div class="h-full flex flex-col overflow-hidden text-sm">
    <!-- BEGIN: MainHeader -->
    <header
      class="flex items-center justify-between px-3 py-2 border-b border-[#dadce0] bg-white select-none z-20 shrink-0 h-16"
    >
      <!-- Left Section: Menu Toggle, Logo, Date Navigation -->
      <div class="flex items-center space-x-3">
        <!-- Hamburger Menu -->
        <button
          aria-label="Main menu"
          class="p-2.5 rounded-full hover:bg-gray-100 text-[#5f6368] transition-colors"
        >
          <svg class="w-6 h-6" fill="currentColor" viewbox="0 0 24 24">
            <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"></path>
          </svg>
        </button>
        <!-- Calendar Logo & Title -->
        <div class="flex items-center space-x-2 mr-3 cursor-pointer">
          <div class="w-10 h-10 relative flex items-center justify-center">
            <svg class="w-10 h-10" viewbox="0 0 40 40">
              <rect fill="#ffffff" height="40" rx="8" width="40"></rect>
              <path
                d="M30 7H10C8.34 7 7 8.34 7 10v20c0 1.66 1.34 3 3 3h20c1.66 0 3-1.34 3-3V10c0-1.66-1.34-3-3-3z"
                fill="#4285F4"
              ></path>
              <path
                d="M30 11H10v19c0 1.66 1.34 3 3 3h17c1.66 0 3-1.34 3-3V11z"
                fill="#ffffff"
              ></path>
              <path d="M10 11h20v4H10z" fill="#EA4335"></path>
              <path d="M7 11h3v22H7z" fill="#FBBC05"></path>
              <path d="M30 11h3v22h-3z" fill="#34A853"></path>
              <text
                fill="#4285F4"
                font-family="'Roboto', sans-serif"
                font-size="16"
                font-weight="700"
                text-anchor="middle"
                x="20"
                y="27"
              >
                7
              </text>
            </svg>
          </div>
          <span class="text-[22px] tracking-tight font-normal text-[#3c4043]">Calendar</span>
        </div>
        <!-- Today Button -->
        <button
          class="border border-[#dadce0] rounded-md px-5 py-2 font-medium text-sm text-[#3c4043] hover:bg-gray-50 active:bg-gray-100 ml-4 transition-colors"
        >
          Today
        </button>
        <!-- Month Navigation Arrows -->
        <div class="flex items-center space-x-1 pl-2">
          <button
            aria-label="Previous week"
            class="p-2 rounded-full hover:bg-gray-100 text-[#5f6368]"
          >
            <svg class="w-5 h-5" fill="currentColor" viewbox="0 0 24 24">
              <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"></path>
            </svg>
          </button>
          <button aria-label="Next week" class="p-2 rounded-full hover:bg-gray-100 text-[#5f6368]">
            <svg class="w-5 h-5" fill="currentColor" viewbox="0 0 24 24">
              <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"></path>
            </svg>
          </button>
        </div>
        <!-- Month & Year Label -->
        <h1 class="text-[22px] font-normal text-[#3c4043] ml-3">May 2025</h1>
      </div>
      <!-- Right Section: Search & Top Controls -->
      <div class="flex items-center space-x-1">
        <button class="p-2.5 rounded-full hover:bg-gray-100 text-[#5f6368]" title="Search">
          <svg class="w-5 h-5" fill="currentColor" viewbox="0 0 24 24">
            <path
              d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
            ></path>
          </svg>
        </button>
        <button class="p-2.5 rounded-full hover:bg-gray-100 text-[#5f6368]" title="Support">
          <svg class="w-5 h-5" fill="currentColor" viewbox="0 0 24 24">
            <path
              d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"
            ></path>
          </svg>
        </button>
        <button class="p-2.5 rounded-full hover:bg-gray-100 text-[#5f6368]" title="Settings menu">
          <svg class="w-5 h-5" fill="currentColor" viewbox="0 0 24 24">
            <path
              d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z"
            ></path>
          </svg>
        </button>
        <!-- View Selector (Week) -->
        <button
          class="flex items-center space-x-1 border border-[#dadce0] rounded-md px-3 py-2 font-medium text-xs text-[#3c4043] hover:bg-gray-50 ml-2"
        >
          <span>Week</span>
          <svg class="w-4 h-4 text-[#5f6368]" fill="currentColor" viewbox="0 0 20 20">
            <path
              d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
            ></path>
          </svg>
        </button>
      </div>
    </header>
    <!-- END: MainHeader -->
    <!-- BEGIN: MainBodyWrapper -->
    <div class="flex flex-1 overflow-hidden relative">
      <!-- BEGIN: LeftSidebar -->
      <aside
        class="w-64 flex-shrink-0 flex flex-col border-r border-[#dadce0] px-3 pt-3 overflow-y-auto custom-scrollbar select-none bg-white"
      >
        <!-- Create Button -->
        <div class="mb-4">
          <button
            class="flex items-center justify-between bg-white hover:shadow-md transition-shadow border border-gray-200 shadow-sm rounded-full py-2.5 px-4 pr-3 min-w-[140px] text-gray-700"
          >
            <div class="flex items-center space-x-3">
              <svg class="w-8 h-8" viewbox="0 0 36 36">
                <path d="M16 16v14h4V16h14v-4H20V-2h-4v14H2v4h14z" fill="#4285F4"></path>
                <path d="M30 16H20l-4-4h14v4z" fill="#34A853"></path>
                <path d="M16 30h4v-14h-4v14z" fill="#FBBC05"></path>
                <path d="M20 16V2h-4v14h4z" fill="#EA4335"></path>
              </svg>
              <span class="font-medium text-sm text-[#3c4043]">Create</span>
            </div>
            <svg class="w-4 h-4 ml-2 text-gray-500" fill="currentColor" viewbox="0 0 20 20">
              <path
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
              ></path>
            </svg>
          </button>
        </div>
        <!-- Mini Calendar -->
        <div class="mb-5 select-none pr-2">
          <div class="flex items-center justify-between mb-2 px-2">
            <span class="text-sm font-medium text-[#3c4043]">May 2025</span>
            <div class="flex items-center space-x-2 text-[#5f6368]">
              <button class="hover:bg-gray-100 p-1 rounded-full">
                <svg class="w-4 h-4" fill="currentColor" viewbox="0 0 24 24">
                  <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"></path>
                </svg>
              </button>
              <button class="hover:bg-gray-100 p-1 rounded-full">
                <svg class="w-4 h-4" fill="currentColor" viewbox="0 0 24 24">
                  <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"></path>
                </svg>
              </button>
            </div>
          </div>
          <!-- Days of Week Headers -->
          <div class="grid grid-cols-7 text-center text-[10px] text-gray-500 font-medium mb-1">
            <span>S</span><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span
            ><span>S</span>
          </div>
          <!-- Date Matrix -->
          <div class="grid grid-cols-7 text-center text-xs text-[#3c4043] gap-y-1">
            <span class="text-gray-400 py-1">27</span>
            <span class="text-gray-400 py-1">28</span>
            <span class="text-gray-400 py-1">29</span>
            <span class="text-gray-400 py-1">30</span>
            <span class="py-1">1</span>
            <span class="py-1">2</span>
            <span class="py-1">3</span>
            <span class="py-1">4</span>
            <span class="py-1">5</span>
            <span class="py-1">6</span>
            <span
              class="py-1 font-semibold text-white bg-[#1a73e8] rounded-full mx-auto w-6 h-6 flex items-center justify-center"
              >7</span
            >
            <span class="py-1">8</span>
            <span class="py-1">9</span>
            <span class="py-1">10</span>
            <span class="py-1">11</span>
            <span class="py-1">12</span>
            <span class="py-1">13</span>
            <span class="py-1">14</span>
            <span class="py-1">15</span>
            <span class="py-1">16</span>
            <span class="py-1">17</span>
            <span class="py-1">18</span>
            <span class="py-1">19</span>
            <span class="py-1">20</span>
            <span class="py-1">21</span>
            <span class="py-1">22</span>
            <span class="py-1">23</span>
            <span class="py-1">24</span>
            <span class="py-1">25</span>
            <span class="py-1">26</span>
            <span class="py-1">27</span>
            <span class="py-1">28</span>
            <span class="py-1">29</span>
            <span class="py-1">30</span>
            <span class="py-1">31</span>
            <span class="text-gray-400 py-1">1</span>
            <span class="text-gray-400 py-1">2</span>
            <span class="text-gray-400 py-1">3</span>
            <span class="text-gray-400 py-1">4</span>
            <span class="text-gray-400 py-1">5</span>
            <span class="text-gray-400 py-1">6</span>
            <span class="text-gray-400 py-1">7</span>
          </div>
        </div>
        <!-- Search for people -->
        <div class="mb-4">
          <div
            class="flex items-center bg-[#f1f3f4] rounded-md px-3 py-2 text-gray-600 focus-within:bg-white focus-within:ring-1 focus-within:ring-blue-500"
          >
            <svg
              class="w-4 h-4 text-gray-500 mr-2 flex-shrink-0"
              fill="currentColor"
              viewbox="0 0 20 20"
            >
              <path
                d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"
              ></path>
            </svg>
            <input
              class="w-full bg-transparent border-0 p-0 text-xs text-[#3c4043] focus:ring-0 placeholder-gray-500"
              placeholder="Search for people"
              type="text"
            />
          </div>
        </div>
        <!-- My Calendars Section -->
        <div class="mb-4">
          <div
            class="flex items-center justify-between text-xs font-medium text-[#3c4043] py-1 cursor-pointer"
          >
            <span class="font-medium">My calendars</span>
            <svg class="w-4 h-4 text-gray-600" fill="currentColor" viewbox="0 0 20 20">
              <path
                clip-rule="evenodd"
                d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z"
                fill-rule="evenodd"
              ></path>
            </svg>
          </div>
          <div class="space-y-1.5 mt-2">
            <label class="flex items-center space-x-3 text-xs cursor-pointer group">
              <input
                checked=""
                class="w-4 h-4 rounded text-[#1a73e8] border-gray-400 focus:ring-0"
                type="checkbox"
              />
              <span class="text-[#3c4043] group-hover:text-black">First Name</span>
            </label>
            <label class="flex items-center space-x-3 text-xs cursor-pointer group">
              <input
                class="w-4 h-4 rounded text-[#0b8043] border-gray-400 focus:ring-0"
                type="checkbox"
              />
              <span class="text-[#3c4043] group-hover:text-black">Birthdays</span>
            </label>
            <label class="flex items-center space-x-3 text-xs cursor-pointer group">
              <input
                class="w-4 h-4 rounded text-[#1a73e8] border-gray-400 focus:ring-0"
                type="checkbox"
              />
              <span class="text-[#3c4043] group-hover:text-black">Tasks</span>
            </label>
          </div>
        </div>
        <!-- Other Calendars Section with Context Popup -->
        <div class="relative mb-6">
          <div
            class="flex items-center justify-between text-xs font-medium text-[#3c4043] py-1 cursor-pointer"
          >
            <span class="font-medium">Other calendars</span>
            <button
              class="p-1 rounded-full hover:bg-gray-100 text-gray-600"
              title="Add other calendars"
            >
              <svg class="w-4 h-4" fill="currentColor" viewbox="0 0 20 20">
                <path
                  clip-rule="evenodd"
                  d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                  fill-rule="evenodd"
                ></path>
              </svg>
            </button>
          </div>
          <div class="space-y-1.5 mt-2">
            <label class="flex items-center space-x-3 text-xs cursor-pointer group">
              <input
                class="w-4 h-4 rounded text-[#a52714] border-gray-400 focus:ring-0"
                type="checkbox"
              />
              <span class="text-[#3c4043] group-hover:text-black">Calendar</span>
            </label>
            <label class="flex items-center space-x-3 text-xs cursor-pointer group">
              <input
                class="w-4 h-4 rounded text-[#0b8043] border-gray-400 focus:ring-0"
                type="checkbox"
              />
              <span class="text-[#3c4043] group-hover:text-black truncate"
                >Holidays in United...</span
              >
            </label>
          </div>
          <!-- Popover Context Menu: "Create new calendar" -->
          <div
            class="absolute left-6 top-8 w-56 bg-white rounded-md shadow-2xl border border-gray-200 py-1.5 z-50 text-[13px] text-[#3c4043]"
            data-purpose="other-calendars-context-menu"
          >
            <div class="px-4 py-2 hover:bg-gray-100 cursor-pointer">Subscribe to calendar</div>
            <!-- Highlighted/Circled Option -->
            <div class="relative px-4 py-2 hover:bg-gray-100 cursor-pointer text-[#202124]">
              <span>Create new calendar</span>
              <!-- Orange highlight oval ring matching screenshot callout -->
              <div
                class="absolute inset-0 mx-[-6px] my-[-2px] border-[3px] border-[#ea580c] rounded-full pointer-events-none opacity-90"
              ></div>
            </div>
            <div class="px-4 py-2 hover:bg-gray-100 cursor-pointer">
              Browse calendars of interest
            </div>
            <div class="px-4 py-2 hover:bg-gray-100 cursor-pointer">From URL</div>
            <div class="px-4 py-2 hover:bg-gray-100 cursor-pointer">Import</div>
          </div>
        </div>
      </aside>
      <!-- END: LeftSidebar -->
      <!-- BEGIN: MainCalendarGrid -->
      <main class="flex-1 flex flex-col h-full bg-white overflow-hidden">
        <!-- Day Columns Header Bar -->
        <div class="flex border-b border-[#dadce0] pl-16 pr-3 bg-white select-none">
          <!-- Sunday 4 -->
          <div class="flex-1 text-center py-2 border-r border-[#dadce0]">
            <span class="block text-[11px] font-medium text-[#70757a] tracking-wider uppercase"
              >SUN</span
            >
            <span class="inline-block text-[24px] font-normal text-[#3c4043] leading-none mt-1"
              >4</span
            >
          </div>
          <!-- Monday 5 -->
          <div class="flex-1 text-center py-2 border-r border-[#dadce0]">
            <span class="block text-[11px] font-medium text-[#70757a] tracking-wider uppercase"
              >MON</span
            >
            <span class="inline-block text-[24px] font-normal text-[#3c4043] leading-none mt-1"
              >5</span
            >
          </div>
          <!-- Tuesday 6 -->
          <div class="flex-1 text-center py-2 border-r border-[#dadce0]">
            <span class="block text-[11px] font-medium text-[#70757a] tracking-wider uppercase"
              >TUE</span
            >
            <span class="inline-block text-[24px] font-normal text-[#3c4043] leading-none mt-1"
              >6</span
            >
          </div>
          <!-- Wednesday 7 (Current Day Highlighted) -->
          <div class="flex-1 text-center py-2 border-r border-[#dadce0]">
            <span class="block text-[11px] font-semibold text-[#1a73e8] tracking-wider uppercase"
              >WED</span
            >
            <span
              class="inline-flex items-center justify-center w-10 h-10 rounded-full bg-[#1a73e8] text-white text-[22px] font-medium leading-none mt-0.5 shadow-sm"
              >7</span
            >
          </div>
        </div>
        <!-- Timezone / All-day row mini bar -->
        <div class="flex border-b border-[#dadce0] h-6 pl-2 items-center text-[10px] text-gray-500">
          <span class="w-14">GMT-04</span>
        </div>
        <!-- Scrollable Grid with Time Labels & Day Columns -->
        <div
          class="flex-1 overflow-y-auto custom-scrollbar relative flex"
          id="calendar-scroll-area"
        >
          <!-- Hourly Y-Axis Time Labels -->
          <div
            class="w-16 flex-shrink-0 flex flex-col text-right pr-2 select-none text-[10px] text-[#70757a] font-medium pt-1"
          >
            <div class="hour-slot leading-none">7 AM</div>
            <div class="hour-slot leading-none">8 AM</div>
            <div class="hour-slot leading-none">9 AM</div>
            <div class="hour-slot leading-none">10 AM</div>
            <div class="hour-slot leading-none">11 AM</div>
            <div class="hour-slot leading-none">12 PM</div>
            <div class="hour-slot leading-none">1 PM</div>
            <div class="hour-slot leading-none">2 PM</div>
            <div class="hour-slot leading-none">3 PM</div>
            <div class="hour-slot leading-none">4 PM</div>
            <div class="hour-slot leading-none">5 PM</div>
            <div class="hour-slot leading-none">6 PM</div>
            <div class="hour-slot leading-none">7 PM</div>
            <div class="hour-slot leading-none">8 PM</div>
            <div class="hour-slot leading-none">9 PM</div>
            <div class="hour-slot leading-none">10 PM</div>
          </div>
          <!-- Columns Area (SUN 4, MON 5, TUE 6, WED 7) -->
          <div class="flex-1 grid grid-cols-4 relative">
            <!-- Horizontal Background Grid Lines across all 4 columns -->
            <div class="absolute inset-0 pointer-events-none z-0">
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
              <div class="grid-line"></div>
            </div>
            <!-- COLUMN 1: Sunday, May 4 -->
            <div class="relative border-r border-[#dadce0] h-[832px] px-1">
              <!-- Gym & Exercise (7:00 - 8:00 AM) -> top: 0px, height: 52px -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#8e24aa] text-white p-1.5 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 0px; height: 50px"
              >
                <p class="font-medium text-[11px] leading-tight truncate">Gym &amp; Exercise</p>
                <p class="text-[10px] text-purple-100">7 – 8am</p>
              </div>
              <!-- Client Project Work (8:30 - 10:30 AM) -> top: 78px, height: 104px -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#0288d1] text-white p-2 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 78px; height: 102px"
              >
                <div class="flex items-start justify-between">
                  <div>
                    <p class="font-medium text-[11px] leading-tight">Client Project Work</p>
                    <p class="text-[10px] text-sky-100">8:30 – 10:30am</p>
                  </div>
                </div>
              </div>
              <!-- Video meeting small badge icon attached to left border -->
              <div
                class="absolute left-[-6px] top-[148px] z-20 bg-white rounded-full p-0.5 shadow-sm border border-gray-200"
              >
                <svg class="w-3.5 h-3.5 text-[#0288d1]" fill="currentColor" viewbox="0 0 24 24">
                  <path
                    d="M19 4H5a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm-2 9.5-3.5-2.28v-1.44L17 7.5v6zm-5-1H6v-2h6v2z"
                  ></path>
                </svg>
              </div>
              <!-- Plan Tomorrow's schedule and close out loose ends (4:45 - 6:15 PM) -> top: 507px, height: 78px -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#0288d1] text-white p-1.5 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 507px; height: 76px"
              >
                <p class="font-medium text-[11px] leading-tight truncate">
                  Plan Tomorrow's schedule and close out loose ends
                </p>
                <p class="text-[10px] text-sky-100">4:45 – 6:15pm</p>
              </div>
            </div>
            <!-- COLUMN 2: Monday, May 5 -->
            <div class="relative border-r border-[#dadce0] h-[832px] px-1">
              <!-- Gym & Exercise (7:00 - 8:00 AM) -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#8e24aa] text-white p-1.5 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 0px; height: 50px"
              >
                <p class="font-medium text-[11px] leading-tight truncate">Gym &amp; Exercise</p>
                <p class="text-[10px] text-purple-100">7 – 8am</p>
              </div>
              <!-- Client Project Work (8:30 - 10:30 AM) -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#0288d1] text-white p-2 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 78px; height: 102px"
              >
                <p class="font-medium text-[11px] leading-tight">Client Project Work</p>
                <p class="text-[10px] text-sky-100">8:30 – 10:30am</p>
              </div>
              <!-- Client Calls & Zoom Meetings (11:00 AM - 12:30 PM) -> top: 208px, height: 78px -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#0288d1] text-white p-2 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 208px; height: 76px"
              >
                <p class="font-medium text-[11px] leading-tight truncate">
                  Client Calls &amp; Zoom Meetings
                </p>
                <p class="text-[10px] text-sky-100">11am – 12:30pm</p>
              </div>
              <!-- Lunch Break (12:30 - 1:00 PM) -> top: 286px, height: 26px -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#8e24aa] text-white px-2 py-0.5 shadow-xs overflow-hidden select-none cursor-pointer z-10 flex items-center justify-between"
                style="top: 286px; height: 25px"
              >
                <p class="font-medium text-[11px] truncate">Lunch Break, 12:30pm</p>
              </div>
              <!-- Sales follow up & networking (3:00 - 4:30 PM) -> top: 416px, height: 78px -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#e64a19] text-white p-2 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 416px; height: 76px"
              >
                <p class="font-medium text-[11px] leading-tight">
                  Sales follow up &amp; networking
                </p>
                <p class="text-[10px] text-orange-100">3 – 4:30pm</p>
              </div>
              <!-- Plan Tomorrow's schedule and close out loose ends (4:45 - 6:15 PM) -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#0288d1] text-white p-1.5 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 507px; height: 76px"
              >
                <p class="font-medium text-[11px] leading-tight truncate">
                  Plan Tomorrow's schedule and close out loose ends
                </p>
                <p class="text-[10px] text-sky-100">4:45 – 6:15pm</p>
              </div>
            </div>
            <!-- COLUMN 3: Tuesday, May 6 -->
            <div class="relative border-r border-[#dadce0] h-[832px] px-1">
              <!-- Client Work (Top banner) -->
              <div
                class="absolute left-1 right-2 rounded-t-[4px] bg-[#f9a825] text-white px-2 py-0.5 shadow-xs overflow-hidden select-none cursor-pointer z-20 text-[11px] font-medium"
                style="top: -24px; height: 22px"
              >
                Client Work
              </div>
              <!-- Gym & Exercise (7:00 - 8:00 AM) -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#8e24aa] text-white p-1.5 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 0px; height: 50px"
              >
                <p class="font-medium text-[11px] leading-tight truncate">Gym &amp; Exercise</p>
                <p class="text-[10px] text-purple-100">7 – 8am</p>
              </div>
              <!-- Client Project Work (8:30 - 10:30 AM) -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#0288d1] text-white p-2 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 78px; height: 102px"
              >
                <p class="font-medium text-[11px] leading-tight">Client Project Work</p>
                <p class="text-[10px] text-sky-100">8:30 – 10:30am</p>
              </div>
              <!-- Video meeting small badge icon attached to left border -->
              <div
                class="absolute left-[-6px] top-[148px] z-20 bg-white rounded-full p-0.5 shadow-sm border border-gray-200"
              >
                <svg class="w-3.5 h-3.5 text-[#0288d1]" fill="currentColor" viewbox="0 0 24 24">
                  <path
                    d="M19 4H5a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm-2 9.5-3.5-2.28v-1.44L17 7.5v6zm-5-1H6v-2h6v2z"
                  ></path>
                </svg>
              </div>
              <!-- Lunch Break (12:30 - 1:00 PM) -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#8e24aa] text-white px-2 py-0.5 shadow-xs overflow-hidden select-none cursor-pointer z-10 flex items-center justify-between"
                style="top: 286px; height: 25px"
              >
                <p class="font-medium text-[11px] truncate">Lunch Break, 12:30pm</p>
              </div>
              <!-- Personal Business Marketing (1:00 - 3:00 PM) -> top: 312px, height: 104px -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#2e7d32] text-white p-2 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 312px; height: 102px"
              >
                <p class="font-medium text-[11px] leading-tight">Personal Business Marketing</p>
                <p class="text-[10px] text-green-100">1 – 3pm</p>
              </div>
              <!-- Plan Tomorrow's schedule and close out loose ends (4:45 - 6:15 PM) -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#0288d1] text-white p-1.5 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 507px; height: 76px"
              >
                <p class="font-medium text-[11px] leading-tight truncate">
                  Plan Tomorrow's schedule and close out loose ends
                </p>
                <p class="text-[10px] text-sky-100">4:45 – 6:15pm</p>
              </div>
            </div>
            <!-- COLUMN 4: Wednesday, May 7 (Current Day) -->
            <div class="relative border-r border-[#dadce0] h-[832px] px-1 bg-red-50/10">
              <!-- Red Current Time Indicator at ~7:45 AM (approx 39px from top) -->
              <div
                class="absolute -left-2 right-0 z-30 flex items-center pointer-events-none"
                style="top: 39px"
              >
                <div class="w-3 h-3 bg-[#ea4335] rounded-full -ml-1.5 shadow-xs"></div>
                <div class="flex-1 h-[2px] bg-[#ea4335]"></div>
              </div>
              <!-- Gym & Exercise (7:00 - 8:00 AM) -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#8e24aa] text-white p-1.5 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 0px; height: 50px"
              >
                <p class="font-medium text-[11px] leading-tight truncate">Gym &amp; Exercise</p>
                <p class="text-[10px] text-purple-100">7 – 8am</p>
              </div>
              <!-- Client Project Work (8:30 - 10:30 AM) -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#0288d1] text-white p-2 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 78px; height: 102px"
              >
                <p class="font-medium text-[11px] leading-tight">Client Project Work</p>
                <p class="text-[10px] text-sky-100">8:30 – 10:30am</p>
              </div>
              <!-- Video meeting small badge icon attached to left border -->
              <div
                class="absolute left-[-6px] top-[148px] z-20 bg-white rounded-full p-0.5 shadow-sm border border-gray-200"
              >
                <svg class="w-3.5 h-3.5 text-[#0288d1]" fill="currentColor" viewbox="0 0 24 24">
                  <path
                    d="M19 4H5a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm-2 9.5-3.5-2.28v-1.44L17 7.5v6zm-5-1H6v-2h6v2z"
                  ></path>
                </svg>
              </div>
              <!-- Client Calls & Zoom Meetings (11:00 AM - 12:30 PM) -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#0288d1] text-white p-2 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 208px; height: 76px"
              >
                <p class="font-medium text-[11px] leading-tight truncate">
                  Client Calls &amp; Zoom Meetings
                </p>
                <p class="text-[10px] text-sky-100">11am – 12:30pm</p>
              </div>
              <!-- Lunch Break (12:30 - 1:00 PM) -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#8e24aa] text-white px-2 py-0.5 shadow-xs overflow-hidden select-none cursor-pointer z-10 flex items-center justify-between"
                style="top: 286px; height: 25px"
              >
                <p class="font-medium text-[11px] truncate">Lunch Break, 12:30pm</p>
              </div>
              <!-- Weekly Check in (3:15 PM) -> top: 429px, height: 26px -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#0288d1] text-white px-2 py-0.5 shadow-xs overflow-hidden select-none cursor-pointer z-10 flex items-center justify-between"
                style="top: 429px; height: 25px"
              >
                <p class="font-medium text-[11px] truncate">Weekly Check in, 3:15pm</p>
              </div>
              <!-- Plan Tomorrow's schedule and close out loose ends (4:45 - 6:15 PM) -->
              <div
                class="absolute left-1 right-2 rounded-[4px] bg-[#0288d1] text-white p-1.5 shadow-xs overflow-hidden select-none cursor-pointer z-10"
                style="top: 507px; height: 76px"
              >
                <p class="font-medium text-[11px] leading-tight truncate">
                  Plan Tomorrow's schedule and close out loose ends
                </p>
                <p class="text-[10px] text-sky-100">4:45 – 6:15pm</p>
              </div>
            </div>
          </div>
        </div>
      </main>
      <!-- END: MainCalendarGrid -->
    </div>
    <!-- END: MainBodyWrapper -->
  </div>
</template>
