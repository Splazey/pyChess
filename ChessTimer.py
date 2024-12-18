import time

class ChessTimer:
    def __init__(self, usertime=600.0):
        # Initialize timers for both players to the specified time (default 10 minutes)
        self.user1_time = usertime  # Timer for white
        self.user2_time = usertime  # Timer for black

        # White (user 1) always starts
        self.current_user = 1
        self.start_time = time.monotonic()
        self.timer_running = True

    def switch_user(self):
        # Stop the timer for the current user and switch
        self.stop_timer()
        self.current_user = 1 if self.current_user == 2 else 2
        self.start_time = time.monotonic()

    def stop_timer(self):
        # Stop the timer for the current user
        elapsed_time = time.monotonic() - self.start_time
        if self.current_user == 1:
            self.user1_time -= elapsed_time
        else:
            self.user2_time -= elapsed_time

    def format_time(self, time_in_seconds):
        # Format the time in minutes:seconds
        minutes = int(time_in_seconds // 60)
        seconds = int(time_in_seconds % 60)
        return f"{minutes:02}:{seconds:02}"

    def get_times(self):
        # Return the remaining time for both players
        elapsed_time = time.monotonic() - self.start_time
        user1_remaining = self.user1_time - elapsed_time if self.current_user == 1 else self.user1_time
        user2_remaining = self.user2_time - elapsed_time if self.current_user == 2 else self.user2_time
        return self.format_time(user1_remaining), self.format_time(user2_remaining)

    def is_game_over(self):
        # Check if either player's time has run out
        return self.user1_time <= 0 or self.user2_time <= 0




