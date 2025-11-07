class FootfallCounter:
    
    # Handles counting logic for people entering and exiting through a defined ROI line.
    # Supports both horizontal and vertical counting modes.

    def __init__(self, line_pos: int, orientation: str = "horizontal"):
        
        # Initialize counters and tracking memory.
        
        self.line_pos = line_pos
        self.orientation = orientation
        self.in_count = 0
        self.out_count = 0
        self.track_history = {}
        self.crossed_ids = set()

    def update_horizontal(self, track_id: int, cx: int, cy: int):
        
        # Update count based on vertical movement (Up/Down) across a horizontal line.
        
        if track_id in self.track_history:
            prev_cx, prev_cy = self.track_history[track_id]

            if prev_cy < self.line_pos <= cy and track_id not in self.crossed_ids:
                self.in_count += 1
                self.crossed_ids.add(track_id)

            elif prev_cy > self.line_pos >= cy and track_id not in self.crossed_ids:
                self.out_count += 1
                self.crossed_ids.add(track_id)

        self.track_history[track_id] = (cx, cy)

    def update_vertical(self, track_id: int, cx: int, cy: int):
        
        # Update count based on horizontal movement (Left/Right) across a vertical line.
        
        if track_id in self.track_history:
            prev_cx, prev_cy = self.track_history[track_id]

            if prev_cx < self.line_pos <= cx and track_id not in self.crossed_ids:
                self.in_count += 1
                self.crossed_ids.add(track_id)

            elif prev_cx > self.line_pos >= cx and track_id not in self.crossed_ids:
                self.out_count += 1
                self.crossed_ids.add(track_id)

        self.track_history[track_id] = (cx, cy)

    def get_counts(self):
        
        # Returns the current counts of people entering and exiting.
        
        return self.in_count, self.out_count
