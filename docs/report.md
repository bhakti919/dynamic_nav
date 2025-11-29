# One-Pager — Dynamic Obstacle Avoidance

**Objective:** Autonomous 2D navigation with dynamic obstacle avoidance and real-time replanning.

**Algorithms**
- Global planner: RRT (Rapidly-exploring Random Tree)
- Replanning: Automatic RRT re-run on path blockage by moving obstacles
- Local controller: simple point follower (pure pursuit recommended next)

**System Architecture**
- src — simulator + planners
- recordings — demo videos/screenshots
- docs — documentation

**Performance (example)**
- Avg planning time: ~0.2–1.5s (depends on RRT iterations)
- Typical path length: depends on scenario (report from run)
- Replans: shown on HUD / console

**Challenges**
- RRT parameter tuning (step size vs iterations)
- Replanning frequency vs CPU load
- Smoothing and kinematic feasibility

**Future work**
- Replace follower with Pure Pursuit / DWA
- Add obstacle motion prediction (Kalman)
- Implement RRT* for shorter paths

