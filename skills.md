# SkillForge-X Master Database

## Skills

### [Inference] Python Performance Optimization
- Level: 4.5
- Confidence: High
- Evidence:
  - Loop Invariant Code Motion (LICM) for rendering optimizations
  - EAFP pattern adoption for dict lookups and nested paths
  - Fast-path cache bypasses in `functools.lru_cache`
  - Eliminating blocking filesystem I/O via precomputation
- Usage Frequency: High
- Last Used: Recent
- Dependencies:
  - Python fundamentals
  - Profiling awareness
- Enables:
  - O(1) state updates
  - Microsecond latency reductions in hot-loops
- Status:
  - Stable
- Notes:
  - Continuous diligence required against micro-optimizations that don't yield measurable benefits

### [Inference] CustomTkinter UI Development
- Level: 4.2
- Confidence: High
- Evidence:
  - Custom list components with hover effects and animations (`DraggableList`)
  - Tooltips, cursor adjustments, keyboard accessibility overlays
  - O(1) state updates, background automation integration using `self.after`
- Usage Frequency: High
- Last Used: Recent
- Dependencies:
  - Python fundamentals
  - Tkinter
- Enables:
  - Desktop application interfaces
  - Gamified queue timers
- Status:
  - Evolving
- Notes:
  - Focus on precomputing visual tokens to minimize main thread latency

### [Inference] System Orchestration & Architecture
- Level: 4.0
- Confidence: High
- Evidence:
  - LeagueLoop background engine architecture
  - Cognitive Architect design patterns
  - Secure CLI parameter passing via lists over `shell=True`
- Usage Frequency: Medium
- Last Used: Recent
- Dependencies:
  - Python Automation
  - Software Design Patterns
- Enables:
  - Complex, resilient multi-component systems
  - Agent workflows
- Status:
  - Stable
- Notes:
  - Keep enforcing strict boundaries between UI rendering loops and asynchronous event loops

### [Inference] Desktop UI Automation & Interaction
- Level: 3.8
- Confidence: Medium
- Evidence:
  - Riot Client multi-account switching automation
  - Simulating keystrokes using the `keyboard` library
  - Background `AutomationEngine` interacting with UI threads
- Usage Frequency: Medium
- Last Used: Recent
- Dependencies:
  - OS interaction
  - Concurrency & multithreading
- Enables:
  - Clientless/headless workflow automations
- Status:
  - Stable
- Notes:
  - Needs hardening around robust cross-platform keyboard event synthesis (e.g. headless xvfb-run environments)
